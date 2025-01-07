import os
from pathlib import Path


def file_writer(dir_path: Path, file_name: str, content: str) -> bool:
    try:
        root_dir_path: Path = Path("..") / dir_path
        file_path: Path = root_dir_path / file_name

        # 경로가 없으면 생성
        os.makedirs(root_dir_path, exist_ok=True)

        with open(file_path, "w") as file:
            file.write(content)
    except Exception as e:
        print(str(e))
        return False

    return True
