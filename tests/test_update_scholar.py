import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location("update_scholar", Path(__file__).resolve().parents[1] / "scripts/update_scholar.py")
scholar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scholar)


def profile(citations="501", h_index="9", i10_index="9"):
    return '<table id="gsc_rsb_st"><tr><th></th><th>All</th><th>Since 2021</th></tr>' + "".join(
        '<tr><td><a>{}</a></td><td class="gsc_rsb_std">{}</td><td>1</td></tr>'.format(label, value)
        for label, value in [("Citations", citations), ("h-index", h_index), ("i10-index", i10_index)]
    ) + "</table>"


ROBOTS = """User-agent: *
Disallow: /citations?
Allow: /citations?user=
Disallow: /citations?*cstart=
User-agent: PetalBot
Disallow: /
"""
URL = "https://scholar.google.com/citations?user=y5FkC7cAAAAJ&hl=en"


class ScholarTests(unittest.TestCase):
    def test_all_time_not_recent(self):
        self.assertEqual(scholar.parse_metrics(profile()), {"citations": 501, "h_index": 9, "i10_index": 9})

    def test_formatted_numbers(self):
        self.assertEqual(scholar.parse_metrics(profile("1,234"))["citations"], 1234)
        self.assertEqual(scholar.parse_metrics(profile("1&nbsp;234"))["citations"], 1234)

    def test_missing_and_blocked_html(self):
        for html in ["<html>CAPTCHA</html>", "<table></table>", profile().replace("i10-index", "Changed")]:
            with self.subTest(html=html), self.assertRaises(ValueError):
                scholar.parse_metrics(html)

    def test_bad_values(self):
        for value in ["-1", "NaN", "Rate limit", "1.5"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                scholar.parse_metrics(profile(value))

    def test_inconsistent_metrics(self):
        with self.assertRaises(ValueError):
            scholar.parse_metrics(profile("20", "9"))

    def test_robots_longest_match(self):
        self.assertTrue(scholar.robots_allows_profile(ROBOTS, URL))
        self.assertFalse(scholar.robots_allows_profile(ROBOTS, URL + "&cstart=20"))
        self.assertFalse(scholar.robots_allows_profile("User-agent: *\nDisallow: /", URL))

    def test_successful_update(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "scholar.json"
            with patch.object(scholar, "read_url", side_effect=[ROBOTS, profile()]):
                data = scholar.update("y5FkC7cAAAAJ", output)
            self.assertEqual(data, json.loads(output.read_text()))
            self.assertEqual(data["source"], URL)
            self.assertEqual(data["schema_version"], 1)
            self.assertTrue(data["updated_at"].endswith("Z"))

    def test_failed_fetch_preserves_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "scholar.json"
            output.write_text("previous snapshot")
            with patch.object(scholar, "read_url", side_effect=[ROBOTS, "CAPTCHA"]), self.assertRaises(ValueError):
                scholar.update("y5FkC7cAAAAJ", output)
            self.assertEqual(output.read_text(), "previous snapshot")

    def test_disallowed_profile_is_not_requested(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(scholar, "read_url", return_value="User-agent: *\nDisallow: /") as read:
                with self.assertRaises(ValueError):
                    scholar.update("y5FkC7cAAAAJ", Path(directory) / "scholar.json")
                read.assert_called_once_with("https://scholar.google.com/robots.txt")

    def test_invalid_author_id(self):
        with self.assertRaises(ValueError):
            scholar.update("id&cstart=20", "/tmp/unused-scholar.json")


if __name__ == "__main__":
    unittest.main()
