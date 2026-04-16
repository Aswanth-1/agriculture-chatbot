import unittest

from utils import supports_unicode_output, to_console_text


class DummyStream:
    def __init__(self, encoding):
        self.encoding = encoding


class UtilsTests(unittest.TestCase):
    def test_supports_unicode_output_for_utf8_streams(self):
        self.assertTrue(supports_unicode_output(DummyStream("utf-8")))

    def test_to_console_text_preserves_unicode_for_utf8_streams(self):
        text = to_console_text("Farm update 🌾", DummyStream("utf-8"))

        self.assertEqual(text, "Farm update 🌾")

    def test_to_console_text_strips_emoji_for_non_unicode_streams(self):
        text = to_console_text("Farm update 🌾 with pH 6.5–7", DummyStream("cp1252"))

        self.assertNotIn("🌾", text)
        self.assertIn("6.5-7", text)


if __name__ == "__main__":
    unittest.main()
