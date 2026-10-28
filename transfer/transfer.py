"""File transfer metadata and hashing functionality."""

import hashlib
import uuid
from collections.abc import Iterator
from pathlib import Path

from contracts.models import TransferOffer
from utils.logger import get_logger


DEFAULT_HASH_CHUNK_SIZE = 1024 * 1024
TRANSFER_CHUNK_SIZE_BYTES = 64 * 1024
logger = get_logger(__name__)


def iter_file_chunks(file_path: str | Path) -> Iterator[bytes]:
    """Yield file contents in chunks no larger than 64 KB."""
    path = Path(file_path)

    try:
        with path.open("rb") as file:
            while chunk := file.read(TRANSFER_CHUNK_SIZE_BYTES):
                yield chunk
    except OSError:
        logger.exception("Unable to read file in transfer chunks: %s", path)
        raise


def calculate_file_sha256(
    file_path: str | Path,
    chunk_size: int = DEFAULT_HASH_CHUNK_SIZE,
) -> tuple[str, int]:
    """Return a file's SHA-256 digest and byte count using bounded memory."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    path = Path(file_path)
    digest = hashlib.sha256()
    file_size_bytes = 0

    try:
        with path.open("rb") as file:
            while chunk := file.read(chunk_size):
                digest.update(chunk)
                file_size_bytes += len(chunk)
    except OSError:
        logger.exception("Unable to read file for SHA-256 calculation: %s", path)
        raise

    return digest.hexdigest(), file_size_bytes


def create_transfer_offer(
    file_path: str | Path,
    sender_id: str,
    transfer_id: str | None = None,
    chunk_size: int = DEFAULT_HASH_CHUNK_SIZE,
) -> TransferOffer:
    """Build transfer metadata without loading or sending the file contents."""
    if not sender_id:
        raise ValueError("sender_id must not be empty")
    if transfer_id is not None and not transfer_id:
        raise ValueError("transfer_id must not be empty")

    path = Path(file_path)
    expected_sha256, file_size_bytes = calculate_file_sha256(path, chunk_size)

    return TransferOffer(
        transfer_id=transfer_id if transfer_id is not None else uuid.uuid4().hex,
        sender_id=sender_id,
        filename=path.name,
        file_size_bytes=file_size_bytes,
        expected_sha256=expected_sha256,
    )
