import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from startup import desktop_quote, entry


class StartupTests(unittest.TestCase):
    def test_entry_escapes_path(self):
        self.assertIn('Exec=python3 "/tmp/with space/app.py"', entry(Path('/tmp/with space/app.py')))
        self.assertEqual(desktop_quote(Path('/tmp/a$"b')), '"/tmp/a\\$\\"b"')

    def test_install_and_remove(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            env = {**os.environ, 'XDG_CONFIG_HOME': str(root / 'config'),
                   'XDG_DATA_HOME': str(root / 'data')}
            script = Path(__file__).resolve().parents[1] / 'startup.py'
            subprocess.run([sys.executable, str(script)], env=env, check=True, capture_output=True)
            autostart = root / 'config/autostart/euro-lek-board.desktop'
            menu = root / 'data/applications/euro-lek-board.desktop'
            self.assertTrue(autostart.exists())
            self.assertEqual(autostart.read_text(), menu.read_text())
            subprocess.run([sys.executable, str(script), '--uninstall'], env=env,
                           check=True, capture_output=True)
            self.assertFalse(autostart.exists())
            self.assertFalse(menu.exists())
