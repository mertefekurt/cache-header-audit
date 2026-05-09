import unittest

from cache_header_audit import audit_headers


class AuditorTests(unittest.TestCase):
    def test_audit_scores_cacheable_response_highly(self):
        result = audit_headers(
            "https://example.test/app.js",
            200,
            {
                "Cache-Control": "public, max-age=3600, immutable, stale-while-revalidate=60",
                "ETag": '"abc"',
                "Vary": "Accept-Encoding",
            },
        )

        self.assertEqual(result.grade, "A")
        self.assertGreaterEqual(result.score, 90)

    def test_audit_flags_uncacheable_response(self):
        result = audit_headers(
            "https://example.test/account",
            200,
            {
                "Cache-Control": "private, no-store, max-age=0",
                "Vary": "*",
            },
        )

        self.assertEqual(result.grade, "F")
        self.assertTrue(any(finding.severity == "error" for finding in result.findings))

    def test_audit_warns_when_cache_control_missing(self):
        result = audit_headers("https://example.test", 200, {"ETag": '"abc"'})

        self.assertIn(result.grade, {"D", "F"})
        self.assertTrue(any("Cache-Control" in finding.message for finding in result.findings))


if __name__ == "__main__":
    unittest.main()
