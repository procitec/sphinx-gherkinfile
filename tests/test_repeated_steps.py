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

