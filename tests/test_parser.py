import unittest

from cache_header_audit.parser import parse_cache_control


class ParserTests(unittest.TestCase):
    def test_parse_cache_control_handles_tokens_and_values(self):
        self.assertEqual(
            parse_cache_control('public, max-age=3600, immutable, stale-while-revalidate="60"'),
            {
                "public": True,
                "max-age": "3600",
                "immutable": True,
                "stale-while-revalidate": "60",
            },
        )

    def test_parse_cache_control_ignores_empty_parts(self):
        self.assertEqual(
            parse_cache_control("public,, max-age=120"),
            {
                "public": True,
                "max-age": "120",
            },
        )


if __name__ == "__main__":
    unittest.main()
