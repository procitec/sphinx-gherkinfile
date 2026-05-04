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

`gherkinfile_dirs` is a list of directories that are searched for files passed to `.. gherkinfile::`.
Relative paths are resolved from the Sphinx source directory, the same style used by common Sphinx configuration values such as `html_static_path`.

Absolute directive arguments are used directly. Relative directive arguments are looked up in every configured search directory and then, as a final fallback, in the Sphinx source directory.

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

## Styling

The generated HTML exposes CSS classes for Gherkin elements and rendered step keywords.
This makes it possible to style features, scenarios, examples, steps and tags from a custom Sphinx stylesheet.

For example, add a stylesheet to your documentation, such as `_static/gherkinfile.css`:

```css
dl.gherkin.examples dd table tbody tr td,
dl.gherkin-examples dd table tbody tr td {
    padding: var(--zero_margin);
}

dl.gherkin.scenario dd > p,
dl.gherkin-scenario dd > p {
    font-style: italic;
    padding-top: 0.7em;
    padding-bottom: 0.7em;
}

dl.gherkin.step:not(:first-of-type) dt.when,
dl.gherkin-step:not(:first-of-type) dt.when {
    padding-top: 0.7em;
}

dl.gherkin.step:not(:first-of-type) dt.and,
dl.gherkin-step:not(:first-of-type) dt.and {
    padding-left: 0.5em;
}

dl.gherkin dd {
    margin-left: 20px;
}

dl.gherkin .tag_tbc {
    background-color: #b3e0ff;
}

dl.gherkin .tag_skip {
    background-color: #ff9980;
}
```

Then include it in `conf.py`:

```python
html_static_path = ["_static"]
html_css_files = ["gherkinfile.css"]
```

The rendered step keyword is added as a class to the step signature. For example:

```html
<dt class="sig sig-object given">Given a precondition</dt>
<dt class="sig sig-object when">When an action happens</dt>
<dt class="sig sig-object then">Then an outcome is expected</dt>
<dt class="sig sig-object and">And another condition applies</dt>
```

Tags are rendered as classes on the surrounding Gherkin block and as inline tag elements.
A tag such as `@tbc` can therefore be styled with `.tag_tbc`, and `@skip` with `.tag_skip`.

## Scope

This package deliberately does not include the broader `sphinx-gherkin` feature set.
It has no `gherkin` domain, no `gherkin:autofeature` directive, no manual Gherkin directives, no cross-reference roles, no viewcode pages and no command line generator.

