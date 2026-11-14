import logging
import re
from pathlib import Path

import pytest
from hunspell import Hunspell
from ruamel.yaml import YAML


@pytest.mark.skip
def test_spelling(category_paths):
    """
    Checking for spelling in such large and diverse datasets as those used in Questions Academy is complicated. We're
    skipping this test for the moment.
    """
    logging.info("Running spell checker...")
    spell_checker = Hunspell("en_US")

    # add custom words to the spell_checker:
    lines = (
        Path(__file__)
        .resolve()
        .with_name("complementary-dictionary.txt")
        .read_text(encoding="utf-8")
        .splitlines()
    )
    words = [word.split("#")[0].strip() for word in lines if word.strip()]
    logging.info(f"Adding {len(words)} word to the spelling dictionary...")
    for word in words:
        logging.debug(f"Adding word '{word}' to the spelling dictionary...")
        spell_checker.add(word)

    for category_path in category_paths:
        logging.debug(f"Spell checking {category_path}...")
        category = YAML(typ="safe").load_all(category_path)
        for question in category:
            tokens = re.findall(r"\b\w+\b", question["Question"])
            for token in tokens:
                logging.debug(f"spell checking token: {token}")
                assert spell_checker.spell(token), (
                    "\n",
                    f"Token '{token}' failed spell checking. Suggestions: {spell_checker.suggest(token)}.\n"
                    f"  Category: {category_path}\n"
                    f"  Question: {question['Question']}\n"
                )
