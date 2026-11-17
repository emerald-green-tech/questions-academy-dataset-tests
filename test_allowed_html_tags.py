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
    "<blockquote>",
    "</blockquote>",
    "<ul>",
    "</ul>",
    "<li>",
    "</li>",
}


def test_allowed_html_tags(category_paths):
    """
    Question stems are treated as Markdown. We only allow a few HTML tags in the rendered Markdown.
    """
    logging.info("Testing allowed HTML tags...")
    for category_path in category_paths:
        logging.debug(f"Testing category {category_path}...")
        category = YAML(typ="safe").load_all(category_path)
        for question in category:
            question_html_stem = markdown.markdown(question["Question"])
            question_html_tags = set(re.findall(r'<[^>]+>', question_html_stem))
            assert question_html_tags.issubset(ALLOWED_HTML_TAGS), (
                "\n"
                f"Question {question["ID"]} HTML tags {question_html_tags - ALLOWED_HTML_TAGS} are not allowed.\n"
                f"  HTML stem: {question_html_stem}\n"
            )
