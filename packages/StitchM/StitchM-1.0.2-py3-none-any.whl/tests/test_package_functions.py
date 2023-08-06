import sys
import unittest
from unittest.mock import patch, MagicMock, ANY

from stitch_m import stitch_and_save


class TestPackageFunctions(unittest.TestCase):
    def test_module_stitch_and_save_method(self):
        with patch('stitch_m.run.main_run', MagicMock()) as stitch_m_run:
            args = ["path_to/mosaic.txt", None]
            stitch_and_save(args[0])
            stitch_m_run.assert_called_once_with(ANY, *args)

    def test_module_stitch_and_save_method_with_marker_file(self):
        with patch('stitch_m.run.main_run', MagicMock()) as stitch_m_run:
            args = ["path_to/mosaic.txt", "path_to/markers.txt"]
            stitch_and_save(*args)
            stitch_m_run.assert_called_once_with(ANY, *args)
