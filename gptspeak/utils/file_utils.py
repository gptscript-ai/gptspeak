from pathlib import Path
from ..exceptions import FileValidationError


def validate_input_file(file_path: str) -> Path:
    path = Path(file_path)
    if not path.exists():
        raise FileValidationError(f"Input file does not exist: {file_path}")
    if not path.is_file():
        raise FileValidationError(f"Input path is not a file: {file_path}")
    return path


def validate_output_file(file_path: str) -> Path:
    path = Path(file_path)
    if path.exists() and not path.is_file():
        raise FileValidationError(f"Output path exists but is not a file: {file_path}")
    return path
