"""Safe storage for files received in transfer chunks."""

import os
import tempfile
from collections.abc import Iterable
from pathlib import Path

from contracts.models import TransferChunk
from utils.logger import get_logger


logger = get_logger(__name__)


def get_destination_path(destination_directory: str | Path, filename: str) -> Path:
    """Return a safe destination path under an existing directory."""
    directory = Path(destination_directory)

    try:
        resolved_directory = directory.resolve(strict=True)
    except OSError:
        logger.exception("Unable to access destination directory: %s", directory)
        raise

    if not resolved_directory.is_dir():
        error = NotADirectoryError(f"Destination is not a directory: {directory}")
        logger.error("%s", error)
        raise error

    safe_filename = filename.replace("\\", "/").rsplit("/", maxsplit=1)[-1]
    if (
        not safe_filename
        or safe_filename in {".", ".."}
        or "\x00" in safe_filename
        or ":" in safe_filename
    ):
        error = ValueError(f"Invalid destination filename: {filename!r}")
        logger.error("%s", error)
        raise error

    destination = resolved_directory / safe_filename
    try:
        if destination.resolve(strict=False).parent != resolved_directory:
            error = ValueError(f"Destination escapes its directory: {filename!r}")
            logger.error("%s", error)
            raise error
    except OSError:
        logger.exception("Unable to resolve destination path: %s", destination)
        raise

    return destination


def save_file(
    destination_directory: str | Path,
    filename: str,
    chunks: Iterable[bytes | TransferChunk],
) -> Path:
    """Stream byte chunks to a file and return its final path.

    The destination file is replaced only after every chunk has been written.
    """
    destination = get_destination_path(destination_directory, filename)
    temporary_path: Path | None = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=destination.parent,
            prefix=".bilkod-",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            for chunk in chunks:
                data = chunk.data if isinstance(chunk, TransferChunk) else chunk
                if not isinstance(data, bytes):
                    raise TypeError("Each chunk must contain bytes")
                if isinstance(chunk, TransferChunk) and chunk.chunk_size_bytes != len(data):
                    raise ValueError("TransferChunk size does not match its data")
                temporary_file.write(data)

        os.replace(temporary_path, destination)
        return destination
    except (OSError, TypeError, ValueError):
        logger.exception("Unable to save file to: %s", destination)
        raise
    finally:
        if temporary_path is not None and temporary_path.exists():
            try:
                temporary_path.unlink()
            except OSError:
                logger.exception("Unable to remove temporary file: %s", temporary_path)
