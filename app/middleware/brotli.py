import logging
from functools import lru_cache
from typing import Any

import brotli
from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

logger = logging.getLogger("brotli_middleware")


class BrotliCompressionError(Exception):
    """Brotli 압축 과정에서 발생하는 예외"""

    pass


class BrotliResponder:
    """
    Brotli 압축을 수행하는 응답 처리기.

    ASGI 애플리케이션의 응답을 가로채서 Brotli 압축을 적용하고,
    스트리밍 방식으로 압축된 데이터를 클라이언트에 전송합니다.

    주요 기능:
    - 응답 헤더 분석 및 압축 가능 여부 판단
    - 스트리밍 방식의 Brotli 압축
    - 최소 크기 임계값 기반 압축 결정
    - 오류 발생 시 원본 데이터로 fallback
    """

    def __init__(
        self,
        app: ASGIApp,
        send: Send,
        quality: int,
        mode: int,
        lgwin: int,
        lgblock: int,
        exclude_media_types: set[str],
        minimum_size: int,
        chunk_buffer_size: int,
        max_buffer_size: int = 1024 * 1024,  # 1MB 최대 버퍼 크기
    ):
        """
        BrotliResponder 초기화.

        Args:
            app: ASGI 애플리케이션
            send: ASGI Send 인터페이스
            quality: Brotli 압축 품질 (0-11)
            mode: Brotli 압축 모드
            lgwin: Brotli 윈도우 크기
            lgblock: Brotli 블록 크기
            exclude_media_types: 압축에서 제외할 미디어 타입들
            minimum_size: 압축을 시작할 최소 크기
            chunk_buffer_size: 청크 버퍼 크기
            max_buffer_size: 최대 버퍼 크기 (메모리 보호)
        """
        self.app = app
        self.send = send
        self.quality = quality
        self.mode = mode
        self.lgwin = lgwin
        self.lgblock = lgblock
        self.exclude_media_types = exclude_media_types
        self.minimum_size = minimum_size
        self.chunk_buffer_size = chunk_buffer_size
        self.max_buffer_size = max_buffer_size

        # 상태 관리
        self.compressor: Any = None
        self.headers_sent = False
        self.should_compress = False
        self.buffer = bytearray()
        self.total_size = 0
        self.compression_started = False
        self.original_headers: MutableHeaders | None = None

    async def __call__(self, scope: Scope, receive: Receive) -> None:
        """ASGI 인터페이스 구현"""
        await self.app(scope, receive, self.send_with_brotli)

    async def send_with_brotli(self, message: Message) -> None:
        """
        Brotli 압축이 적용된 응답 전송 처리.

        메시지 타입에 따라 적절한 처리를 수행합니다:
        - http.response.start: 헤더 분석 및 압축 설정
        - http.response.body: 본문 압축 및 전송
        """
        message_type = message["type"]

        try:
            if message_type == "http.response.start":
                await self._handle_response_start(message)
            elif message_type == "http.response.body":
                await self._handle_response_body(message)
            else:
                await self.send(message)
        except Exception as e:
            logger.error(f"Brotli response handling error: {e}", exc_info=True)
            await self._handle_error_fallback(message)

    async def _handle_response_start(self, message: Message) -> None:
        """
        응답 시작 메시지 처리.

        응답 헤더를 분석하여 압축 가능 여부를 판단하고,
        압축이 가능한 경우 헤더를 수정합니다.
        """
        if self.headers_sent:
            raise RuntimeError("Response headers already sent.")

        # 원본 헤더 백업 (오류 시 복원용)
        headers = MutableHeaders(raw=message.get("headers", []))
        self.original_headers = MutableHeaders(raw=list(headers.raw))

        content_type = self._parse_content_type(headers.get("content-type", ""))
        content_encoding = headers.get("content-encoding")
        content_length = headers.get("content-length")

        # 압축 여부 결정
        self.should_compress = self._should_compress_response(
            content_encoding, content_type, content_length
        )

        if self.should_compress:
            logger.debug(
                f"Enabling Brotli compression for content-type: {content_type}"
            )
            self._modify_headers_for_compression(headers)
            message["headers"] = headers.raw

        await self.send(message)
        self.headers_sent = True

    async def _handle_response_body(self, message: Message) -> None:
        """
        응답 본문 메시지 처리.

        압축이 활성화된 경우 본문 데이터를 버퍼에 축적하고,
        적절한 시점에 압축하여 전송합니다.
        """
        if not self.headers_sent:
            raise RuntimeError("Cannot send body without headers.")

        body = message.get("body", b"")
        more_body = message.get("more_body", False)

        if not self.should_compress:
            await self.send(message)
            return

        # 메모리 보호를 위한 버퍼 크기 체크
        if len(self.buffer) + len(body) > self.max_buffer_size:
            logger.warning(f"Buffer size limit exceeded, processing chunk")
            await self._process_compressed_chunk(False)

        self.total_size += len(body)
        self.buffer.extend(body)

        # 버퍼가 충분히 크거나 마지막 청크인 경우 압축 처리
        if len(self.buffer) >= self.chunk_buffer_size or not more_body:
            await self._process_compressed_chunk(not more_body)

        # 스트림 종료
        if not more_body:
            await self._finalize_compression()

    async def _process_compressed_chunk(self, is_final: bool) -> None:
        """
        압축된 청크 처리.

        버퍼의 데이터를 압축하고 전송합니다.
        첫 번째 청크에서 최소 크기 조건을 확인합니다.
        """
        if not self.buffer:
            return

        # minimum_size 체크 (첫 번째 청크에서만)
        if not self.compression_started:
            if is_final and self.total_size < self.minimum_size:
                logger.debug(
                    f"Skipping compression: size {self.total_size} < {self.minimum_size}"
                )
                await self._send_uncompressed_response()
                return

            self._initialize_compressor()

        if self.compressor:
            try:
                compressed_data = self.compressor.process(bytes(self.buffer))
                if compressed_data:
                    await self.send(
                        {
                            "type": "http.response.body",
                            "body": compressed_data,
                            "more_body": True,
                        }
                    )
                logger.debug(
                    f"Compressed chunk: {len(self.buffer)} -> {len(compressed_data)} bytes"
                )
            except Exception as e:
                logger.error(f"Brotli compression error: {e}", exc_info=True)
                raise BrotliCompressionError(f"Compression failed: {e}") from e

        self.buffer.clear()

    async def _finalize_compression(self) -> None:
        """
        압축 종료 처리.

        압축기의 최종 데이터를 처리하고 응답을 완료합니다.
        """
        if self.compressor:
            try:
                final_data = self.compressor.finish()
                await self.send(
                    {
                        "type": "http.response.body",
                        "body": final_data,
                        "more_body": False,
                    }
                )
                logger.debug(
                    f"Compression finalized with {len(final_data)} final bytes"
                )
            except Exception as e:
                logger.error(f"Brotli finalization error: {e}", exc_info=True)
                await self.send(
                    {"type": "http.response.body", "body": b"", "more_body": False}
                )
        else:
            # 압축하지 않은 경우
            await self.send(
                {"type": "http.response.body", "body": b"", "more_body": False}
            )

    def _initialize_compressor(self) -> None:
        """Brotli 압축기 초기화"""
        try:
            self.compressor = brotli.Compressor(
                quality=self.quality,
                mode=self.mode,
                lgwin=self.lgwin,
                lgblock=self.lgblock,
            )
            self.compression_started = True
            logger.debug("Brotli compressor initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Brotli compressor: {e}")
            raise BrotliCompressionError(
                f"Compressor initialization failed: {e}"
            ) from e

    async def _send_uncompressed_response(self) -> None:
        """압축하지 않은 응답 전송"""
        await self.send(
            {
                "type": "http.response.body",
                "body": bytes(self.buffer),
                "more_body": False,
            }
        )
        self.buffer.clear()

    async def _handle_error_fallback(self, message: Message) -> None:
        """오류 발생 시 fallback 처리"""
        if not self.headers_sent and self.original_headers:
            # 원본 헤더로 복원하여 전송
            await self.send(
                {
                    "type": "http.response.start",
                    "status": message.get("status", 500),
                    "headers": self.original_headers.raw,
                }
            )
            self.headers_sent = True

        # 버퍼에 있는 원본 데이터 전송
        if self.buffer:
            await self.send(
                {
                    "type": "http.response.body",
                    "body": bytes(self.buffer),
                    "more_body": False,
                }
            )

    @lru_cache(maxsize=256)
    def _parse_content_type(self, content_type: str) -> str:
        """Content-Type 헤더 파싱 (캐시됨)"""
        return content_type.split(";")[0].strip().lower()

    def _should_compress_response(
        self,
        content_encoding: str | None,
        content_type: str,
        content_length: str | None,
    ) -> bool:
        """
        응답 압축 여부 결정.

        다음 조건들을 확인합니다:
        - 이미 압축되지 않았는지
        - 제외 미디어 타입이 아닌지
        - 최소 크기 조건을 만족하는지
        """
        # 이미 압축되었거나 제외 타입인 경우
        if content_encoding or content_type in self.exclude_media_types:
            return False

        # Content-Length가 있고 minimum_size보다 작은 경우
        if content_length:
            try:
                if int(content_length) < self.minimum_size:
                    return False
            except (ValueError, TypeError):
                logger.debug(f"Invalid content-length: {content_length}")

        return True

    def _modify_headers_for_compression(self, headers: MutableHeaders) -> None:
        """압축을 위한 헤더 수정"""
        # Content-Length 제거 (스트리밍 압축)
        if "content-length" in headers:
            del headers["content-length"]

        headers["content-encoding"] = "br"
        self._update_vary_header(headers)

    def _update_vary_header(self, headers: MutableHeaders) -> None:
        """Vary 헤더 업데이트"""
        vary_values = []
        existing_vary = headers.get("vary", "")

        if existing_vary:
            vary_values = [v.strip() for v in existing_vary.split(",") if v.strip()]

        if "accept-encoding" not in [v.lower() for v in vary_values]:
            vary_values.append("Accept-Encoding")

        headers["vary"] = ", ".join(vary_values)


class BrotliMiddleware:
    """
    FastAPI용 Brotli 압축 미들웨어.

    HTTP 응답을 Brotli 알고리즘으로 압축하여 네트워크 대역폭을 절약하고
    응답 시간을 개선합니다. 클라이언트가 Brotli를 지원하는 경우에만 압축을 수행합니다.

    특징:
    - 스트리밍 압축 지원
    - 설정 가능한 압축 품질 및 옵션
    - 미디어 타입별 압축 제외 설정
    - 최소 크기 임계값 설정
    - 포괄적인 오류 처리

    사용법:
        app = FastAPI()
        app.add_middleware(BrotliMiddleware, quality=6, minimum_size=1024)
    """

    def __init__(
        self,
        app: ASGIApp,
        quality: int = 4,
        mode: int = brotli.MODE_GENERIC,
        lgwin: int = 22,
        lgblock: int = 0,
        minimum_size: int = 1024,  # 1KB
        chunk_buffer_size: int = 8192,  # 8KB
        max_buffer_size: int = 1024 * 1024,  # 1MB
        exclude_media_types: tuple[str, ...] = (
            "image/png",
            "image/jpeg",
            "image/gif",
            "image/webp",
            "image/svg+xml",
            "application/pdf",
            "application/zip",
            "application/gzip",
            "application/brotli",
            "video/mp4",
            "video/webm",
            "audio/mpeg",
            "audio/ogg",
            "font/woff",
            "font/woff2",
        ),
    ):
        """
        BrotliMiddleware 초기화.

        Args:
            app: ASGI 애플리케이션
            quality: 압축 품질 (0-11, 높을수록 더 나은 압축률)
            mode: 압축 모드 (GENERIC, TEXT, FONT)
            lgwin: 윈도우 크기 (10-24, 클수록 더 나은 압축률)
            lgblock: 블록 크기 (0=자동, 16-24)
            minimum_size: 압축을 시작할 최소 바이트 크기
            chunk_buffer_size: 청크 단위 처리 크기
            max_buffer_size: 메모리 보호를 위한 최대 버퍼 크기
            exclude_media_types: 압축에서 제외할 미디어 타입들

        Raises:
            ValueError: 잘못된 매개변수 값
        """
        self._validate_parameters(
            quality, lgwin, lgblock, minimum_size, chunk_buffer_size, max_buffer_size
        )

        self.app = app
        self.quality = quality
        self.mode = mode
        self.lgwin = lgwin
        self.lgblock = lgblock
        self.minimum_size = minimum_size
        self.chunk_buffer_size = chunk_buffer_size
        self.max_buffer_size = max_buffer_size
        self.exclude_media_types = self._normalize_media_types(exclude_media_types)

        logger.info(
            f"BrotliMiddleware initialized: quality={quality}, "
            f"minimum_size={minimum_size}, chunk_size={chunk_buffer_size}"
        )

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """ASGI 미들웨어 진입점"""
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # 클라이언트 요청 분석
        if not self._should_enable_compression(scope):
            await self.app(scope, receive, send)
            return

        # Brotli 응답 처리기 생성 및 실행
        responder = BrotliResponder(
            app=self.app,
            send=send,
            quality=self.quality,
            mode=self.mode,
            lgwin=self.lgwin,
            lgblock=self.lgblock,
            exclude_media_types=self.exclude_media_types,
            minimum_size=self.minimum_size,
            chunk_buffer_size=self.chunk_buffer_size,
            max_buffer_size=self.max_buffer_size,
        )

        try:
            await responder(scope, receive)
        except Exception as e:
            logger.error(f"BrotliMiddleware error: {e}", exc_info=True)
            await self._handle_middleware_error(e, scope, responder, send)

    def _should_enable_compression(self, scope: Scope) -> bool:
        """압축 활성화 여부 결정"""
        headers = dict(scope.get("headers", []))
        accept_encoding = headers.get(b"accept-encoding", b"").decode("latin1")
        method = scope.get("method", "GET")

        # Brotli 지원 확인 및 HEAD 요청 처리
        if "br" not in accept_encoding or method == "HEAD":
            logger.debug(
                f"Compression skipped: method={method}, "
                f"accept_encoding={accept_encoding}"
            )
            return False

        return True

    async def _handle_middleware_error(
        self, error: Exception, scope: Scope, responder: BrotliResponder, send: Send
    ) -> None:
        """미들웨어 레벨 오류 처리"""
        if not responder.headers_sent:
            await send(
                {
                    "type": "http.response.start",
                    "status": 500,
                    "headers": [(b"content-type", b"text/plain")],
                }
            )
            await send(
                {
                    "type": "http.response.body",
                    "body": b"Internal Server Error",
                    "more_body": False,
                }
            )
        raise

    def _validate_parameters(
        self,
        quality: int,
        lgwin: int,
        lgblock: int,
        minimum_size: int,
        chunk_buffer_size: int,
        max_buffer_size: int,
    ) -> None:
        """매개변수 유효성 검증"""
        if not (0 <= quality <= 11):
            raise ValueError(f"Quality must be between 0 and 11, got {quality}")

        if not (10 <= lgwin <= 24):
            raise ValueError(f"lgwin must be between 10 and 24, got {lgwin}")

        if lgblock != 0 and not (16 <= lgblock <= 24):
            raise ValueError(f"lgblock must be 0 or between 16 and 24, got {lgblock}")

        if minimum_size < 0:
            raise ValueError(f"minimum_size must be non-negative, got {minimum_size}")

        if chunk_buffer_size <= 0:
            raise ValueError(
                f"chunk_buffer_size must be positive, got {chunk_buffer_size}"
            )

        if max_buffer_size < chunk_buffer_size:
            raise ValueError("max_buffer_size must be >= chunk_buffer_size")

    def _normalize_media_types(self, media_types: tuple[str, ...]) -> set[str]:
        """미디어 타입 정규화"""
        return {mt.lower().strip() for mt in media_types}
