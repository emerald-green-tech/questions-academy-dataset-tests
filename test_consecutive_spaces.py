from ruamel.yaml import YAML


def test_consecutive_spaces(category_paths) -> None:
    """
    Consecutive spaces aren't necessarily problematic, but removing them makes for cleaner data.
    """
    for category_path in category_paths:
        category = YAML(typ="safe").load_all(category_path)
        for question in category:
            assert "  " not in question["Question"]
