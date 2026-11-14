from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def yaml_dir() -> Path:
    """
    This package is configued as a Git submodule of other packages that contain datasets of questions. Discovering the
    directory that contains the YAML files assumes that:

    1.  the tests package is cloned in a directory at the root of the dataset repository, and
    2.  the YAML files are in subdirectory `data/yaml` of the dataset repository.

    These conditions are met automatically, the user doesn't have to set these up manually.
    """
    _yaml_dir = Path(__file__).resolve().parent.parent / "data" / "yaml"
    if _yaml_dir.is_dir():
        return _yaml_dir

    raise RuntimeError("Could not find data/yaml in the dataset repository.")


@pytest.fixture(scope="session")
def category_paths(yaml_dir: Path) -> list[Path]:
    return list(yaml_dir.glob("*.yaml"))
