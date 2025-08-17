"""Metadata management module for SQLite database operations."""

from fastapi import HTTPException, status
from sqlmodel import and_, select
from structlog import BoundLogger

from database import MetadataTable, sqlite_conn_orm
from model import COCKTAIL_DATA_KIND, MetadataCategory, MetadataRegister
from utils import Logger

logger: BoundLogger = Logger().setup()


class Metadata:
    """Handle metadata operations for cocktail data categories."""

    @staticmethod
    def create(
        category: MetadataCategory,
        items: MetadataRegister,
        kind: COCKTAIL_DATA_KIND,
    ) -> None:
        """Create new metadata entries in SQLite database.

        Args:
            category: The metadata category (e.g., AROMA, TASTE, FINISH)
            items: The metadata items to register
            kind: The type of cocktail data (spirits, liqueur, etc.)

        Raises:
            Exception: If database insertion fails
        """
        try:
            with sqlite_conn_orm() as session:
                for name in items.names:
                    metadata = MetadataTable(
                        category=category.value, name=name, kind=kind
                    )  # type: ignore
                    session.add(metadata)
                session.commit()
        except Exception as e:
            logger.error("Insert Spirits metadata to sqlite has an error", error=str(e))
            raise e

    @staticmethod
    def read(
        category: MetadataCategory,
        kind: COCKTAIL_DATA_KIND,
    ) -> list[dict[str, int | str]]:
        """Read metadata entries from SQLite database.

        Args:
            category: The metadata category to read
            kind: The type of cocktail data

        Returns:
            List of metadata entries with index and name

        Raises:
            Exception: If database query fails
        """
        try:
            with sqlite_conn_orm() as session:
                statement = (
                    select(MetadataTable.id, MetadataTable.name)
                    .where(
                        and_(
                            MetadataTable.category == category.value,
                            MetadataTable.kind == kind,
                        )
                    )
                    .order_by(MetadataTable.name)
                )

                return [
                    {"index": id, "name": name} for id, name in session.exec(statement)
                ]

        except Exception as e:
            logger.error("Get Spirits metadata from sqlite has an error", error=str(e))
            raise e

    @staticmethod
    def delete(metadata_id: int) -> None:
        """Delete a metadata entry from SQLite database.

        Args:
            metadata_id: The ID of the metadata entry to delete

        Raises:
            HTTPException: If metadata not found (404)
            Exception: If database deletion fails
        """
        try:
            with sqlite_conn_orm() as session:
                metadata: MetadataTable | None = session.get(MetadataTable, metadata_id)
                if metadata is None:
                    raise HTTPException(404, "Metadata not found")

                session.delete(metadata)
                session.commit()
        except Exception as e:
            logger.error("Delete Spirits metadata has an error", error=str(e))
            raise e


class MetadataValidation:
    """Validate metadata values against database records."""

    kind: COCKTAIL_DATA_KIND

    def __init__(
        self,
        kind: COCKTAIL_DATA_KIND,
        taste: list[str],
        aroma: list[str] | None = None,
        finish: list[str] | None = None,
    ) -> None:
        self.kind = kind
        self.taste = taste
        self.aroma = aroma
        self.finish = finish

    def _is_validated_category(
        self,
        category: MetadataCategory,
        user_input_metadata: list[str],
    ) -> bool:
        """Check if user input metadata values are valid."""
        valid_metadata_list: list[dict[str, int | str]] = Metadata.read(
            category, self.kind
        )
        valid_names: list[str] = [
            str(metadata["name"]) for metadata in valid_metadata_list
        ]

        return all(user_input in valid_names for user_input in user_input_metadata)

    def __call__(
        self,
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
        listed_taste: list[str] = []
        listed_aroma: list[str] = []
        listed_finish: list[str] = []

        # 메타데이터 변환
        listed_taste = self.taste
        if self.aroma is not None:
            listed_aroma = self.aroma
        if self.finish is not None:
            listed_finish = self.finish

        # 메타데이터 값 검사
        for category, values in [
            (MetadataCategory.AROMA, listed_aroma),
            (MetadataCategory.TASTE, listed_taste),
            (MetadataCategory.FINISH, listed_finish),
        ]:
            if not self._is_validated_category(category, values):
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, "Invalid metadata values provided"
                )

        return listed_taste, listed_aroma, listed_finish
