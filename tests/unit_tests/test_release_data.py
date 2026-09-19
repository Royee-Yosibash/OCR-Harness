import re
import tomllib
import unittest
from datetime import datetime
from pathlib import Path

from consts import APP_ROOT

PYPROJECT_PATH = APP_ROOT / "pyproject.toml"
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+(?:(?:rc|alpha|beta)\d+)?$")
ISO_DATE_FORMAT = "%Y-%m-%d"


class TestReleaseData(unittest.TestCase):
    """Tests for pyproject.toml release metadata validity."""

    def setUp(self):
        with open(PYPROJECT_PATH, "rb") as _f:
            self.pyproject = tomllib.load(_f)

    def test_required_keys_exist(self):
        """Verifies that all release metadata is declared in pyproject.toml."""
        self.assertIn("version", self.pyproject["project"])
        self.assertGreater(len(self.pyproject["project"].get("authors", [])), 0)
        self.assertIn("release-date", self.pyproject["tool"]["ocr-toolkit"])

    def test_version_is_valid_semver(self):
        """Verifies that the version string matches the MAJOR.MINOR.PATCH format."""
        version = self.pyproject["project"]["version"]
        self.assertRegex(version, SEMVER_PATTERN, f"Invalid semver format: {version}")

    def test_version_segments_are_non_negative(self):
        """Verifies that each semver segment is a non-negative integer."""
        parts = self.pyproject["project"]["version"].split(".")
        for part in parts:
            value = int(part)
            self.assertGreaterEqual(value, 0, f"Negative version segment: {value}")

    def test_release_date_is_valid_iso8601(self):
        """Verifies that the release date is a valid ISO 8601 date (YYYY-MM-DD)."""
        date_str = self.pyproject["tool"]["ocr-toolkit"]["release-date"]
        try:
            datetime.strptime(date_str, ISO_DATE_FORMAT)
        except ValueError:
            self.fail(f"Invalid ISO 8601 date format: {date_str}. Expected YYYY-MM-DD.")