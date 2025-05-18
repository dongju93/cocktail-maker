from os import chdir
from pathlib import Path

# change directory to app directory
chdir(Path(__file__).parent.parent / "app")

from main import cocktail_maker  # noqa: E402 # type: ignore[import]

api_service = cocktail_maker
