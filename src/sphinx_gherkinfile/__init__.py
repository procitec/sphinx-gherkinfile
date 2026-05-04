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
    "funktionalität": "feature",
    "funktion": "feature",
    "eigenschaft": "feature",
    "rule": "rule",
    "regel": "rule",
    "background": "background",
    "grundlage": "background",
    "hintergrund": "background",
    "voraussetzungen": "background",
    "vorbedingungen": "background",
    "scenario": "scenario",
    "example": "scenario",
    "beispiel": "scenario",
    "szenario": "scenario",
    "scenario outline": "scenario",
    "scenario template": "scenario",
    "outline": "scenario",
    "template": "scenario",
    "szenariogrundriss": "scenario",
    "szenarien": "scenario",
    "examples": "examples",
    "scenarios": "examples",
    "beispiele": "examples",
    "step": "step",
    "given": "step",
    "angenommen": "step",
    "gegeben sei": "step",
    "gegeben seien": "step",
    "and": "step",
    "und": "step",
    "but": "step",
    "aber": "step",
    "*": "step",
    "when": "step",
    "wenn": "step",
    "then": "step",
    "dann": "step",
}


KEYWORD_CSS_CLASS = {
    "feature": "feature",
    "funktionalität": "feature",
    "funktion": "feature",
    "eigenschaft": "feature",
    "rule": "rule",
    "regel": "rule",
    "background": "background",
    "grundlage": "background",
    "hintergrund": "background",
    "voraussetzungen": "background",
    "vorbedingungen": "background",
    "scenario": "scenario",
    "example": "scenario",
    "beispiel": "scenario",
    "szenario": "scenario",
    "scenario outline": "scenario",
    "scenario template": "scenario",
    "outline": "scenario",
    "template": "scenario",
    "szenariogrundriss": "scenario",
    "szenarien": "scenario",
    "examples": "examples",
    "scenarios": "examples",
    "beispiele": "examples",
    "step": "step",
    "given": "given",
    "angenommen": "given",
    "gegeben sei": "given",
    "gegeben seien": "given",
    "and": "and",
    "und": "and",
    "but": "but",
    "aber": "but",
    "*": "and",
    "when": "when",
    "wenn": "when",
    "then": "then",
    "dann": "then",
}


class SphinxGherkinFileError(SphinxError):
    category = "Sphinx-GherkinFile error"


class NotFound(SphinxGherkinFileError):
    pass


class MultipleFound(SphinxGherkinFileError):
    pass


def normalize_keyword(keyword: str) -> str:
    return " ".join(keyword.strip().strip(":").lower().split())


def keyword_to_objtype(keyword: str) -> str:
    return KEYWORD_OBJTYPE[normalize_keyword(keyword)]


def keyword_to_css_class(keyword: str) -> str:
    return KEYWORD_CSS_CLASS.get(normalize_keyword(keyword), keyword_to_objtype(keyword))


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
