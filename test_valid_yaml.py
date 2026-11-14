from typing import Generator

from ruamel.yaml import YAML


def test_valid_yaml(category_paths):
    """
    Test parsing the category files as YAML.
    """
    for category_path in category_paths:
        category = YAML(typ="safe").load_all(category_path)
        assert isinstance(category, Generator)
        assert all([isinstance(question, dict) for question in category])
