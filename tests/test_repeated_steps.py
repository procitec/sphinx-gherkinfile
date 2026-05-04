from __future__ import annotations

import html as html_module
import re

import pytest


def html_text(content: str) -> str:
    text = re.sub(r"<[^>]+>", " ", content)
    text = html_module.unescape(text)
    return re.sub(r"\s+", " ", text)


@pytest.mark.sphinx(testroot="repeated-steps")
def test_gherkinfile_directive_renders_feature_file(app, outdir):
    app.builder.build_all()
    html = (outdir / "index.html").read_text(encoding="utf-8")
    text = html_text(html)

    assert "a second precondition" in text
    assert "a third precondition" in text
    assert "starts a chat" in text
    assert "enters" in text
    assert "the systems adds a new prompt" in text


@pytest.mark.sphinx(testroot="repeated-steps")
def test_step_keywords_are_rendered_without_colon_and_wildcard_as_and(app, outdir):
    app.builder.build_all()

    html = (outdir / "index.html").read_text(encoding="utf-8")
    text = html_text(html)

    assert "Given a first precondition" in text
    assert "And a second precondition" in text
    assert "And a third precondition" in text
    assert "When the user does login to the system" in text
    assert "Then the system repeats the text in the chat" in text

    assert not re.search(r"\b(Given|When|Then|And)\s*:\s", text)
