import logging
import re

import markdown
from ruamel.yaml import YAML

ALLOWED_HTML_TAGS = {
    "<p>",
    "</p>",
    "<em>",
    "</em>",
    "<strong>",
    "</strong>",
    "<br />",
}


def test_allowed_html_tags(category_paths):
    """
    Question stems are treated as Markdown. We only allow a few HTML tags in the rendered Markdown.
    """
    logging.debug("Testing allowed HTML tags...")
    found_tags = set()
    for category_path in category_paths:
        category = YAML(typ="safe").load_all(category_path)
        for question in category:
            found_tags.update(
                re.findall(r'<[^>]+>', markdown.markdown(question["Question"]))
            )

    assert found_tags.issubset(ALLOWED_HTML_TAGS)
