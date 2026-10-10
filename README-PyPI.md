# OCR-Harness

OCR-Harness is a Python library for integrating OCR engines, applying image preprocessing, and evaluating recognition
results against labeled data. Install the core library from PyPI, then add the OCR engines you need.

## Features

- An extensible OCR interface for implementing and registering OCR engines.
- Evaluation metrics for character accuracy, word accuracy, word recall, word precision, and word count ratio, with
  per-image results, aggregate statistics, confidence intervals, and plotting utilities.
- Image preprocessing for grid splitting, contour-based segmentation, and adaptive or Otsu binarization. The OCR interface
  maps detections from processed image regions back to the original image coordinates.
- OCR result and configuration serialization, including configurable preprocessing steps and detection validators.
- Optional wrappers for EasyOCR, PaddleOCR, and pytesseract.


## Installation

Requires Python 3.12 or newer.

Install the core library:

```bash
pip install ocr-harness
```

Install with the optional OCR engines:

```bash
pip install "ocr-harness[ocrs]"
```

Pytesseract also requires the system Tesseract executable.

## Run OCR from a config file

Save an engine configuration as `config.json`:

```json
{
    "model_name": "EasyOCRModule",
    "model_params": {"languages": ["en"], "gpu": false},
    "preprocess_methods": [
        {"name": "grid_split_image", "kwargs": {"grid": [2, 2]}}
    ]
}
```

Load the configuration and run OCR on an RGB NumPy image:

```python
from PIL import Image
import numpy as np

from ocr_harness.ocr_backbone import OCRAbstract
from ocr_harness.ocr_backbone.ocr_config import load_config
from ocr_harness.ocr_modules import import_all_modules

image = np.array(Image.open("image.png").convert("RGB"))

import_all_modules()
config = load_config("config.json")
ocr = OCRAbstract.from_config(config)
result = ocr.get_text_detections(image)
```

Install the `ocrs` extra to use the optional engine wrappers. Engine-specific system requirements still apply.

## Add an OCR engine

Subclass `OCRAbstract` and implement `_run_single` to return an `OCRResult`:

```python
import numpy as np

from ocr_harness.ocr_backbone import OCRAbstract, OCRConfig, OCRResult


class MyOCRModule(OCRAbstract):
    def __init__(self, config: OCRConfig | dict) -> None:
        super().__init__(config)
        # Initialize the OCR engine.

    def _run_single(self, image: np.ndarray, single_run_model_params: dict) -> OCRResult:
        # Return detections produced by the engine.
        ...
```

Subclasses register by class name and can be created with `OCRAbstract.from_config`.

## License

MIT. See [LICENSE](LICENSE).
