import os
import sys
import unittest
from pathlib import Path
from io import StringIO
from unittest.mock import patch, MagicMock, ANY
from subprocess import Popen, PIPE, STDOUT
from time import sleep

from stitch_m.__init__ import __version__ as version

from stitch_m.scripts import commandline

class TestEntryPointCommandline(unittest.TestCase):
# Before these running tests, the module must be installed in development mode using:
# `pip install --editable . --user` (from the project folder)
# it can be uninstalled at the end using:
# `pip uninstall StitchM`
# IF TESTING ON WINDOWS: make sure the correct python installation is set as the default in PATH

    @classmethod
    def setUpClass(cls):
        # Set maximum difference string length to None (infinite)
        cls.maxDiff = None
        # Add local intall to path for testing with development install
        if os.name == "posix":
            os.environ["PATH"] += os.pathsep + os.path.join(os.path.expanduser("~"), ".local", "bin")
    
    @patch('argparse.ArgumentParser.print_help')
    def test_commandline_function(self, mocked_printhelp):
        sys.argv = ["StitchM"]
        commandline.main()

        mocked_printhelp.assert_called_once()

    @patch('argparse.ArgumentParser.print_help')
    def test_commandline_function_setup_subpaser(self, mocked_printhelp):
        sys.argv = ["StitchM", "setup"]
        commandline.main()

        mocked_printhelp.assert_called_once()

    @patch('stitch_m.file_handler.create_user_config')
    def test_commandline_function_setup_config(self, mocked_config_creator):
        local_config_file = Path(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "stitch_m", "config.cfg"))

        sys.argv = ["StitchM", "setup", "--config"]
        commandline.main()

        mocked_config_creator.assert_called_once()


    @patch('stitch_m.file_handler.create_Windows_shortcut')
    def test_commandline_function_setup_windows_shortcut(self, mocked_shortcut_creator):
        local_config_file = Path(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "stitch_m", "config.cfg"))

        sys.argv = ["StitchM", "setup", "-w"]
        commandline.main()

        mocked_shortcut_creator.assert_called_once()

    @patch('stitch_m.run.main_run')
    def test_commandline_function_with_args(self, main_run):
        main_run.return_value = None
        mosaic_arg = "mosaic_path"
        marker_arg = "marker_path"
        sys.argv =["StitchM", "--mosaic", mosaic_arg, "--markers", marker_arg]
        commandline.main()

        main_run.assert_called_once_with(ANY, mosaic_arg, marker_arg)

    def test_commandline_method(self):
        args = ["path_to/mosaic"]
        run_args = ["StitchM", "--mosaic", args[0]]
        with Popen(run_args, universal_newlines=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT) as p:
            sleep(2)
            stdout, _ = p.communicate("pressed key", timeout=5)
        stdout = stdout.strip("\r\n").strip("\n")
        self.assertIn(f"Invalid arguments: {args[0]}, None", stdout, msg=f"Actual stdout: {stdout}")

    def test_commandline_method_invalid_path(self):
        args = ["path_to/mosaic.txt"]
        run_args = ["StitchM", "--mosaic", args[0]]
        with Popen(run_args, universal_newlines=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT) as p:
            sleep(2)
            stdout, _ = p.communicate("pressed key", timeout=5)
        stdout = stdout.strip("\r\n").strip("\n")
        self.assertIn(f"Mosaic file path cannot be resolved", stdout, msg=f"Actual stdout: {stdout}")

    def test_commandline_method_with_marker_file(self):
        args = ["path_to/mosaic", "path_to/markers"]
        run_args = ["StitchM", "--mosaic", args[0], "--markers", args[1]]
        with Popen(run_args, universal_newlines=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT) as p:
            sleep(2)
            stdout, _ = p.communicate("pressed key", timeout=5)
        stdout = stdout.strip("\r\n").strip("\n")
        self.assertIn(f"Invalid arguments: {args[0]}, {args[1]}", stdout, msg=f"Actual stdout: {stdout}")

    def test_commandline_method_version_number(self):
        run_args = ["StitchM", "--version"]
        with Popen(run_args, universal_newlines=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT) as p:
            sleep(2)
            stdout, _ = p.communicate("pressed key", timeout=5)
        stdout = stdout.strip("\r\n").strip("\n")
        self.assertEqual(f"StitchM {version}", stdout, msg=f"Actual stdout: {stdout}")

    def test_commandline_method_setup_subparser(self):
        run_args = ["StitchM", "setup"]
        with Popen(run_args, universal_newlines=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT) as p:
            sleep(2)
            stdout, _ = p.communicate("pressed key", timeout=5)
        stdout = stdout.strip("\r\n").strip("\n")
        self.assertIn(f"StitchM setup [-w] [-c] [-h]", stdout, msg=f"Actual stdout: {stdout}")
