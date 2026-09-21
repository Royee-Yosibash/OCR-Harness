import unittest

from ocr_backbone.bounding_box import BoundingBox
from ocr_backbone.ocr_result import OCRResult
from tests.ocr_result_comparison import ocr_result_mismatch_summary


class TestOcrResultMismatchSummary(unittest.TestCase):
    """Tests for the ``ocr_result_mismatch_summary`` diagnostics helper."""

    def test_empty_when_close(self):
        a = OCRResult(
            detections=[
                BoundingBox(coordinates=((0, 0), (10, 10)), text="hi", confidence=0.9),
            ]
        )
        b = OCRResult(
            detections=[
                BoundingBox(coordinates=((0, 0), (10, 10)), text="hi", confidence=0.9005),
            ]
        )
        self.assertEqual(ocr_result_mismatch_summary(a, b), [])

    def test_count(self):
        a = OCRResult(detections=[BoundingBox(coordinates=((0, 0), (10, 10)), text="hi")])
        b = OCRResult(detections=[])
        self.assertEqual(
            ocr_result_mismatch_summary(a, b),
            ["Detection count mismatch: expected 0, got 1."],
        )

    def test_coordinates(self):
        a = OCRResult(detections=[BoundingBox(coordinates=((0, 0), (10, 10)), text="hi")])
        b = OCRResult(detections=[BoundingBox(coordinates=((0, 0), (11, 10)), text="hi")])
        self.assertIn("detection 0: coordinates", ocr_result_mismatch_summary(a, b)[0])

    def test_text(self):
        a = OCRResult(detections=[BoundingBox(coordinates=((0, 0), (10, 10)), text="hi")])
        b = OCRResult(detections=[BoundingBox(coordinates=((0, 0), (10, 10)), text="bye")])
        self.assertEqual(
            ocr_result_mismatch_summary(a, b),
            ["detection 0: text 'hi' != 'bye'"],
        )

    def test_confidence(self):
        a = OCRResult(detections=[BoundingBox(coordinates=((0, 0), (10, 10)), text="hi", confidence=0.9)])
        b = OCRResult(detections=[BoundingBox(coordinates=((0, 0), (10, 10)), text="hi", confidence=0.5)])
        issues = ocr_result_mismatch_summary(a, b)
        self.assertIn("detection 0: confidence", issues[0])
        self.assertIn("tolerance", issues[0])

    def test_limits(self):
        dets = [BoundingBox(coordinates=((i, 0), (i + 10, 10)), text=f"t{i}", confidence=0.9) for i in range(10)]
        wrong = [BoundingBox(coordinates=((i, 0), (i + 9, 10)), text=f"t{i}", confidence=0.9) for i in range(10)]
        a = OCRResult(detections=dets)
        b = OCRResult(detections=wrong)
        self.assertEqual(len(ocr_result_mismatch_summary(a, b, max_mismatches=3)), 3)

    def test_all_mismatches_by_default(self):
        dets = [BoundingBox(coordinates=((i, 0), (i + 10, 10)), text=f"t{i}") for i in range(3)]
        wrong = [BoundingBox(coordinates=((i, 0), (i + 9, 10)), text=f"t{i}") for i in range(3)]
        a = OCRResult(detections=dets)
        b = OCRResult(detections=wrong)
        self.assertEqual(len(ocr_result_mismatch_summary(a, b)), 3)
