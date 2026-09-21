"""Diagnostics helpers for comparing ``OCRResult`` instances in tests."""

from ocr_backbone.ocr_result import OCRResult


def ocr_result_mismatch_summary(
    actual: OCRResult,
    expected: OCRResult,
    confidence_tolerance: float = 1e-3,
    max_mismatches: int | None = None,
) -> list[str]:
    """Describe the differences between two ``OCRResult`` instances.

    Intended for test failure diagnostics where printing the full ``repr`` of
    both results would be too large for CI logs. Mirrors the comparison rules
    of ``OCRResult.is_close`` per detection: coordinates and text must match
    exactly, while confidence values may differ by up to
    ``confidence_tolerance``.

    Args:
        actual: The actual result produced by an OCR module.
        expected: The expected result.
        confidence_tolerance: Maximum allowed difference in confidence.
        max_mismatches: Maximum number of issues to include, or ``None`` to
            include all.

    Returns:
        A list of human-readable issue strings describing the differences.
        Empty if the results match within the tolerance.
    """
    if actual.is_close(expected, confidence_tolerance=confidence_tolerance):
        return []

    if len(actual.detections) != len(expected.detections):
        return [
            f"Detection count mismatch: expected {len(expected.detections)}, "
            f"got {len(actual.detections)}."
        ]

    issues = []
    for i, (a, e) in enumerate(zip(actual.detections, expected.detections, strict=True)):
        if a.coordinates != e.coordinates:
            issues.append(f"detection {i}: coordinates {a.coordinates} != {e.coordinates}")
        elif a.text != e.text:
            issues.append(f"detection {i}: text {a.text!r} != {e.text!r}")
        elif abs(a.confidence - e.confidence) > confidence_tolerance:
            issues.append(
                f"detection {i}: confidence {a.confidence:.6f} vs "
                f"{e.confidence:.6f} (tolerance {confidence_tolerance:g})"
            )

    return issues[:max_mismatches] if max_mismatches is not None else issues
