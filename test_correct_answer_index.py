from ruamel.yaml import YAML


def test_correct_answer_index(category_paths) -> None:
    for category_path in category_paths:
        category = YAML(typ="safe").load_all(category_path)
        for question in category:
            assert question["Correct"] in question["Answers"].keys()
