"""
Inspiration for test cases drawn from,

 * https://en.wikipedia.org/wiki/Help:Wikitext#Links_and_URLs
"""
from mwtext import Wikitext2Structured
from .wikilink_fixtures import WIKILINK_TEST_FIXTURES


def test_wikilinks_only():
    for test_name, test_data in WIKILINK_TEST_FIXTURES.items():
        transformer = Wikitext2Structured(
            forbidden_wikilink_prefixes={"file", "image", "category"})
        structured = transformer.transform(test_data["wikitext"])

        actual = {
            "paragraphs": structured["paragraphs"],
            "categories": structured["categories"],
        }
        expected = {
            "paragraphs": [
                {
                    "section_idx": 0,
                    "section_name": "Introduction",
                    "plaintext": test_data["plaintext"],
                    "wikilinks": test_data["wikilinks"]
                },
            ],
            "categories": test_data["categories"],
        }
        assert actual == expected
