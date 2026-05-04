"""Sphinx extension for rendering external Gherkin ``.feature`` files.

The extension intentionally exposes only the plain ``gherkinfile`` directive::

    .. gherkinfile:: path/to/example.feature
"""

from __future__ import annotations

from collections.abc import Iterable
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.errors import SphinxError

package_dir = Path(__file__).parent.resolve()
_package_name = "sphinx-gherkinfile"

try:
    __version__ = str(version(_package_name))
except PackageNotFoundError:
    __version__ = "0.1.0"

KEYWORD_OBJTYPE = {
    "feature": "feature",
    "rule": "rule",
    "background": "background",
    "scenario": "scenario",
    "example": "scenario",
    "scenario outline": "scenario",
    "scenario template": "scenario",
    "outline": "scenario",
    "template": "scenario",
    "examples": "examples",
    "scenarios": "examples",
    "step": "step",
    "given": "step",
    "and": "step",
    "but": "step",
    "*": "step",
    "when": "step",
    "then": "step",
}


class SphinxGherkinFileError(SphinxError):
    category = "Sphinx-GherkinFile error"


class NotFound(SphinxGherkinFileError):
    pass


class MultipleFound(SphinxGherkinFileError):
    pass


def keyword_to_objtype(keyword: str) -> str:
    return KEYWORD_OBJTYPE[keyword.strip().strip(":").lower()]


def setup(app: Sphinx) -> dict[str, object]:
    app.require_sphinx("3.0")
    app.add_config_value("gherkinfile_dirs", ["."], "env", [list, tuple, str])

    from sphinx_gherkinfile.directive import GherkinFileDirective

    app.add_directive("gherkinfile", GherkinFileDirective)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


def get_config_gherkinfile_dirs(env: BuildEnvironment) -> list[Path]:
    configured = env.config.gherkinfile_dirs

    if isinstance(configured, str):
        configured_paths: Iterable[Any] = [configured]
    elif isinstance(configured, Iterable):
        configured_paths = configured
    else:
        raise SphinxGherkinFileError("Invalid 'gherkinfile_dirs' configuration. Use a string or a list of paths.")

    dirs: list[Path] = []
    for configured_path in configured_paths:
        path = Path(str(configured_path))
        if not path.is_absolute():
            path = Path(env.srcdir, path)
        dirs.append(path.resolve())

    if not dirs:
        raise SphinxGherkinFileError("No Gherkin search path configured. Set 'gherkinfile_dirs' in conf.py.")

    return dirs
