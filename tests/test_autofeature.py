from __future__ import annotations

import html as html_module
import re
from pathlib import Path

import pytest
from sphinx.errors import ExtensionError


def html_text(content: str) -> str:
    text = re.sub(r"<[^>]+>", " ", content)
    text = html_module.unescape(text)
    return re.sub(r"\s+", " ", text)


@pytest.mark.sphinx(testroot="autofeature")
def test_gherkinfile_directive_renders_feature_file(app, outdir):
    app.builder.build_all()
    html = (outdir / "index.html").read_text(encoding="utf-8")
    text = html_text(html)

    assert "Feature" in text
    assert "Parameter module changed" in text
    assert "Scenario" in text
    assert "Changing a known parameter" in text
    assert "Given" in text
    assert "a module parameter file" in text
    assert "module_name" in text
    assert "RX" in text
    assert "The documentation includes a feature file that already exists on disk"
    assert re.search(r"<table", html)


@pytest.mark.sphinx(testroot="autofeature")
def test_tags_are_rendered_inline_and_as_css_classes(app, outdir):
    app.builder.build_all()
    html = (outdir / "index.html").read_text(encoding="utf-8")
    assert "wip" in html

    assert '<p class="gherkin-tags">' not in html
    assert '<span class="gherkin-tags">' in html
    assert 'class="gherkin gherkin-feature tag_requirements"' in html
    assert 'class="gherkin gherkin-scenario tag_wip"' in html
    assert 'class="gherkin-tag tag_wip"' in html
    assert re.search(r"Scenario.*Changing.*parameter.*gherkin-tag tag_wip", html, re.DOTALL)


@pytest.mark.sphinx(testroot="autofeature")
def test_extension_uses_plain_directive_without_gherkin_domain(app, outdir):
    app.builder.build_all()

    with pytest.raises(ExtensionError):
        app.env.get_domain("gherkin")


@pytest.mark.sphinx(testroot="autofeature")
def test_feature_file_is_registered_as_dependency(app, outdir):
    app.builder.build_all()
    dependencies = {Path(path) for path in app.env.dependencies["index"]}

    assert any(path.name == "parameter_module_changed.feature" for path in dependencies)


@pytest.mark.sphinx(testroot="search-paths")
def test_gherkinfile_dirs_are_used_as_search_paths(app, outdir):
    app.builder.build_all()
    html = (outdir / "index.html").read_text(encoding="utf-8")
    text = html_text(html)

    dependencies = {Path(path) for path in app.env.dependencies["index"]}

    assert "Parameter module changed" in text
    assert any(
        path.name == "parameter_module_changed.feature"
        and path.parent.name == "features"
        for path in dependencies
    )
