import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from conversion import DEFAULT_RATE, format_amount, load_rate, parse_rate, save_rate


class ConversionTests(unittest.TestCase):
    def test_presets_at_default_and_changed_rate(self):
        self.assertEqual([format_amount(Decimal(n) * DEFAULT_RATE) for n in (5, 10, 20, 50, 100, 200)],
                         ["440", "880", "1,760", "4,400", "8,800", "17,600"])
        self.assertEqual(format_amount(Decimal(200) * parse_rate("86")), "17,200")

    def test_fractional_rate_and_validation(self):
        self.assertEqual(format_amount(Decimal(5) * parse_rate("86,25")), "431.25")
        for invalid in ("", "0", "-5", "NaN", "Infinity", "abc"):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                parse_rate(invalid)

    def test_persistence_and_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            self.assertEqual(load_rate(path), DEFAULT_RATE)
            save_rate(Decimal("86.5"), path)
            self.assertEqual(load_rate(path), Decimal("86.5"))
            path.write_text('{"rate": "bad"}')
            self.assertEqual(load_rate(path), DEFAULT_RATE)


if __name__ == "__main__":
    unittest.main()
