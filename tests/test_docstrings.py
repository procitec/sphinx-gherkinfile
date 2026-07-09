from __future__ import annotations

import html as html_module
import re

import pytest

from sphinx_gherkinfile.gherkin import DefinitionBuildah, Step


def html_text(content: str) -> str:
    text = re.sub(r"<[^>]+>", " ", content)
    text = html_module.unescape(text)
    return re.sub(r"\s+", " ", text)


def parse_first_step(raw_code: str) -> Step:
    document = DefinitionBuildah("docstrings.feature", raw_code).parse()
    return document.find_first(Step)


def test_docstring_without_media_type_can_be_parsed():
    step = parse_first_step(
        "Feature: Doc strings\n"
        "  Scenario: Without media type\n"
        "    Given a doc string without media type\n"
        '      """\n'
        "      plain doc string content\n"
        '      """\n'
    )

    assert step.docstring is not None
    assert step.docstring.content.strip() == "plain doc string content"
    assert step.docstring.mediatype in ("", None)
    assert step.docstring.delimiter == '"""'


def test_docstring_with_media_type_can_be_parsed():
    step = parse_first_step(
        "Feature: Doc strings\n"
        "  Scenario: With media type\n"
        "    Given a doc string with media type\n"
        '      """text/plain\n'
        "      typed doc string content\n"
        '      """\n'
    )

    assert step.docstring is not None
    assert step.docstring.content.strip() == "typed doc string content"
    assert step.docstring.mediatype == "text/plain"
    assert step.docstring.delimiter == '"""'


@pytest.mark.sphinx(testroot="docstrings")
def test_gherkinfile_directive_renders_docstrings_with_and_without_media_type(
    app,
    outdir,
):
    app.builder.build_all()

    html = (outdir / "index.html").read_text(encoding="utf-8")
    text = html_text(html)

    assert "Feature" in text
    assert "Doc strings are rendered" in text
    assert "Scenario" in text
    assert "Doc string without media type" in text
    assert "doc string without media type" in text
    assert "plain doc string content" in text
    assert "Doc string with media type" in text
    assert "doc string with media type" in text
    assert "typed doc string content" in text
