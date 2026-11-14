import pytest
from jsonschema import Draft202012Validator, FormatChecker, ValidationError
from ruamel.yaml import YAML


SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Questions Academy question",
    "type": "object",
    "properties": {
        "ID": {
            "type": "string",
            "format": "uuid",
            "description": "A unique identifier for the question.",
        },
        "Question": {
            "type": "string",
            "description": "The question stem.",
        },
        "Answers": {
            "type": "object",
            "minProperties": 1,
            "propertyNames": {
                "pattern": "^[1-9][0-9]*$",
            },
            "additionalProperties": {
                "type": "string",
            },
            "description": "Answer text keyed by a positive integer index.",
        },
        "Correct": {
            "type": "integer",
            "minimum": 1,
            "description": "The index of the correct answer.",
        },
        "Explanation": {
            "type": "string",
            "description": "An optional explanation of the answer.",
        },
        "Active": {
            "type": "boolean",
            "description": "Whether the question is active on the website.",
        },
        "Notes": {
            "type": "string",
            "description": "Notes about the question, not displayed on the website.",
        },
        "SchemaVersion": {
            "type": "integer",
            "const": 1,
            "description": "The question schema version.",
        },
    },
    "required": [
        "ID",
        "Question",
        "Answers",
        "Correct",
        "Active",
        "Notes",
        "SchemaVersion",
    ],
    "additionalProperties": False,
}


def test_schema(category_paths):
    Draft202012Validator.check_schema(SCHEMA)
    validator = Draft202012Validator(SCHEMA, format_checker=FormatChecker())

    for category_path in category_paths:
        with category_path.open(encoding="utf-8") as category_file:
            questions = YAML(typ="safe").load_all(category_file)
            for document_number, question in enumerate(questions, start=1):
                instance = question
                if isinstance(question, dict) and isinstance(question.get("Answers"), dict):
                    # JSON object member names are strings; YAML allows numeric keys. Since we're using JSONSchema to
                    # validate YAML, we have to convert the integer keys to strings:
                    instance = {
                        **question,
                        "Answers": {
                            str(index): answer
                            for index, answer in question["Answers"].items()
                        },
                    }

                try:
                    validator.validate(instance)
                except ValidationError as error:
                    if isinstance(question, dict):
                        question_id = question.get("ID", "<missing ID>")
                    else:
                        question_id = "<not a mapping>"
                    pytest.fail(
                        f"{category_path}, document {document_number}, question {question_id}: "
                        f"{error.message}",
                        pytrace=False,
                    )
