# sphinx-gherkinfile

`sphinx-gherkinfile` is a minimal Sphinx extension for rendering an existing
Gherkin `.feature` file in Sphinx documentation.

It intentionally exposes only this plain directive:

```rst
.. gherkinfile:: parameter_module_changed.feature
```

The directive reads the referenced file from the configured search paths, parses
the feature and renders features, rules, backgrounds, scenarios, steps, doc
strings and data tables into the Sphinx document.

This is based on the Sphinx extension [sphinx-gherkin](https://github.com/cblegare/sphinx-gherkin),
but reduced to the

```rst
.. gherkin:autofeature::
```

directive with additional parsing of tags and comments.


## Installation

```bash
uv pip install sphinx-gherkinfile
```

For local development:

```bash
uv sync --dev
uv run pytest
uv build
```

## Sphinx configuration

```python
extensions = ["sphinx_gherkinfile"]
gherkinfile_dirs = ["."]
```

`gherkinfile_dirs` is a list of directories that are searched for files passed
to `.. gherkinfile::`. Relative paths are resolved from the Sphinx source
directory, the same style used by common Sphinx configuration values such as
`html_static_path`.

Absolute directive arguments are used directly. Relative directive arguments are
looked up in every configured search directory and then, as a final fallback, in
the Sphinx source directory.

## Example

```rst
Feature documentation
=====================

.. gherkinfile:: parameter_module_changed.feature
```

With feature files stored outside the documentation root:

```python
extensions = ["sphinx_gherkinfile"]
gherkinfile_dirs = ["../features", "../acceptance-tests/features"]
```

```rst
.. gherkinfile:: parameter_module_changed.feature
```

## Scope

This package deliberately does not include the broader `sphinx-gherkin` feature
set. It has no `gherkin` domain, no `gherkin:autofeature` directive, no manual
Gherkin directives, no cross-reference roles, no viewcode pages and no command
line generator.
