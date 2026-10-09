import unittest

from vesper.sites import SITES, _gitlab, normalize_username


class SiteTests(unittest.TestCase):
    def test_username(self):
        self.assertEqual(normalize_username(" Gabriel "), "Gabriel")
        with self.assertRaises(ValueError):
            normalize_username("../etc")
        with self.assertRaises(ValueError):
            normalize_username("a b")
        with self.assertRaises(ValueError):
            normalize_username("javascript:alert(1)")
        with self.assertRaises(ValueError):
            normalize_username("ada.")
        with self.assertRaises(ValueError):
            normalize_username("-ada")

    def test_gitlab_body(self):
        self.assertEqual(_gitlab(200, "[]"), "missing")
        self.assertEqual(_gitlab(200, '[{"id": 1}]'), "found")
        self.assertEqual(_gitlab(500, ""), "unknown")

    def test_urls_stay_on_known_hosts(self):
        sample = "ada"
        for site in SITES:
            self.assertTrue(site.probe(sample).startswith("https://"))
            self.assertNotIn(sample + "@", site.probe(sample).split("/", 3)[-1][:0])
            host = site.probe(sample).split("/")[2]
            self.assertIn(
                host,
                {
                    "api.github.com",
                    "gitlab.com",
                    "codeberg.org",
                    "huggingface.co",
                    "registry.npmjs.org",
                    "dev.to",
                },
            )


if __name__ == "__main__":
    unittest.main()
