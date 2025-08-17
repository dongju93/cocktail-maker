import re
import unicodedata

from fastapi import HTTPException, UploadFile, status
from pydantic import field_validator

# 모듈 레벨에서 미리 컴파일된 정규식 사용 (재사용 및 성능)
KOREAN_NAME_RE: re.Pattern[str] = re.compile(r"^[가-힣\s]+$")

MAX_FILE_SIZE: int = 2 * 1024 * 1024
# // TODO: Form 필드에서 media_type 로 컨텐츠 타입 제한이 가능하다면 내부 검증 로직에서 제외
ALLOWED_CONTENT_TYPES: set[str] = {
    "image/jpeg",
    "image/png",
    "image/jpg",
    "image/webp",
    "image/bmp",
    "image/gif",
    "image/tiff",
}


class ImageValidation:
    def is_allowed_content_type(self, file: UploadFile | None) -> bool:
        if file is not None and file.content_type not in ALLOWED_CONTENT_TYPES:  # noqa
            return False
        return True

    def is_less_than_max_size(self, read_file: bytes | None) -> bool:
        return bool(read_file is not None and len(read_file) <= MAX_FILE_SIZE)

    async def read_image(self, file: UploadFile | None) -> bytes | None:
        return await file.read() if file is not None else None

    @classmethod
    async def files(
        cls,
        main_image: UploadFile,
        sub_images: list[UploadFile | None],
    ) -> tuple[bytes, list[bytes | None]]:
        """
        이미지 파일을 검증하고 바이트로 변환하여 반환합니다.

        Args:
            main_image: 주 이미지 파일
            sub_images: 보조 이미지 파일 목록

        Returns:
            Tuple[bytes, List[bytes, None]]: 주 이미지 바이트 스트림, , 보조 이미지의 바이트 스트림 목록

        Raises:
            HTTPException: 이미지 검증 실패 시 발생
        """
        self_cls = cls()

        # 이미지 파일 타입 검사
        all_images = [main_image] + [img for img in sub_images if img is not None]
        for image in all_images:
            if not self_cls.is_allowed_content_type(image):
                raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid file extension"
                )

        # 이미지 읽기
        main_image_bytes = await main_image.read()
        sub_images_bytes = []
        for sub_image in sub_images:
            sub_image_bytes = await self_cls.read_image(sub_image)
            sub_images_bytes.append(sub_image_bytes)

        # 이미지 크기 검사
        all_image_bytes = [main_image_bytes] + [
            img for img in sub_images_bytes if img is not None
        ]
        for image_byte in all_image_bytes:
            if not self_cls.is_less_than_max_size(image_byte):
                raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    "File size is too large, maximum 2MB",
                )

        return main_image_bytes, sub_images_bytes


class HangulValidationMixIn:
    @field_validator("name", "kind", check_fields=False)
    @classmethod
    def validate_hangul_only(cls, v: str) -> str:
        # 전처리: 양쪽 공백 제거, 유니코드 정규화
        v = v.strip()
        v = unicodedata.normalize("NFKC", v)
        # 한글 및 공백만 허용하는 정규식 검사
        if not KOREAN_NAME_RE.match(v):
            raise ValueError("name must contain only Korean characters and spaces")
        return v
