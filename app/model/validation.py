from fastapi import HTTPException, UploadFile, status

from database.query import ReadSpiritsMetadata
from model.spirits import SpiritsMetadataCategory
from utils.etc import single_word_list_to_many_word_list

MAX_FILE_SIZE: int = 2 * 1024 * 1024
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
    async def is_allowed_content_type(self, file: UploadFile | None) -> bool:
        if file is not None and file.content_type not in ALLOWED_CONTENT_TYPES:  # noqa
            return False
        return True

    async def is_less_than_max_size(self, read_file: bytes | None) -> bool:
        if read_file is not None and len(read_file) > MAX_FILE_SIZE:  # noqa
            return False
        return True

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
            if not await self_cls.is_allowed_content_type(image):
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
            if not await self_cls.is_less_than_max_size(image_byte):
                raise HTTPException(
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    "File size is too large, maximum 2MB",
                )

        return main_image_bytes, sub_images_bytes


class MetadataValidation:
    async def is_validated_category(
        self, category: SpiritsMetadataCategory, user_input_metadata: list[str]
    ) -> bool:
        valid_metadata_list: list[dict[str, int | str]] = (
            ReadSpiritsMetadata.based_on_category(category)
        )
        # // TODO: TypedDict 을 적용하여 mypy 에러 해결해야함
        valid_names: list[str] = [
            str(metadata["name"]) for metadata in valid_metadata_list
        ]

        return all(user_input in valid_names for user_input in user_input_metadata)

    @classmethod
    async def data(
        cls,
        aroma: list[str],
        taste: list[str],
        finish: list[str],
    ) -> tuple[list[str], list[str], list[str]]:
        """
        메타데이터 값을 검증합니다.

        Args:
            aroma: 향 메타데이터 값 목록
            taste: 맛 메타데이터 값 목록
            finish: 끝맛 메타데이터 값 목록

        Returns:
            Tuple[List[str], List[str], List[str]]: 변환된 메타데이터 값 목록

        Raises:
            HTTPException: 메타데이터 검증 실패 시 발생
        """

        self_cls = cls()

        # 메타데이터 변환
        listed_aroma = single_word_list_to_many_word_list(aroma)
        listed_taste = single_word_list_to_many_word_list(taste)
        listed_finish = single_word_list_to_many_word_list(finish)

        # 메타데이터 값 검사
        for category, values in [
            (SpiritsMetadataCategory.AROMA, listed_aroma),
            (SpiritsMetadataCategory.TASTE, listed_taste),
            (SpiritsMetadataCategory.FINISH, listed_finish),
        ]:
            if not await self_cls.is_validated_category(category, values):
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, "Invalid metadata values provided"
                )

        return listed_aroma, listed_taste, listed_finish
