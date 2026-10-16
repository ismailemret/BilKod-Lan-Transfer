from contracts.models import TransferOffer, TransferProgress

MOCK_OFFER = TransferOffer(
    transfer_id="tx-1001",
    sender_id="dev-01",
    filename="sample_bilkod.pdf",
    file_size_bytes=4194304,
    expected_sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
)

def get_mock_progress(transferred_bytes: int) -> TransferProgress:
    total = MOCK_OFFER.file_size_bytes
    pct = (transferred_bytes / total) * 100.0 if total > 0 else 0.0
    return TransferProgress(
        transfer_id=MOCK_OFFER.transfer_id,
        transferred_bytes=transferred_bytes,
        total_bytes=total,
        speed_bps=524288.0,
        percentage=round(pct, 2),
    )
