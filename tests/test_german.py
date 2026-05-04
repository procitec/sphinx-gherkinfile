from __future__ import annotations

import html as html_module
import re

import pytest


def html_text(content: str) -> str:
    text = re.sub(r"<[^>]+>", " ", content)
    text = html_module.unescape(text)
    return re.sub(r"\s+", " ", text)


def assert_signature_class(html: str, class_name: str, keyword: str) -> None:
    assert re.search(
        rf'<dt\b[^>]*class="[^"]*\b{re.escape(class_name)}\b[^"]*"[^>]*>.*?{re.escape(keyword)}',
        html,
        re.DOTALL,
    )


@pytest.mark.sphinx(testroot="german")
def test_gherkinfile_directive_renders_german_feature_file(app, outdir):
    app.builder.build_all()

    html = (outdir / "index.html").read_text(encoding="utf-8")
    text = html_text(html)

    assert "Test für Verwendung Deutscher Keywords" in text
    assert "die App ist gestartet" in text
    assert "der lokale Rechner ist läuft" in text
    assert "Editieren der Dateien" in text
    assert 'die Datei "<Datei>" ist selektiert' in text
    assert 'die Datei "<Datei>" per Drag und Drop auf "<Position>" gezogen wird' in text
    assert "ist die Datei an Position <Position>" in text
    assert "test_versch_2" in text
    assert "(30,30)" in text
    assert "Datei hilfe selektieren" in text
    assert 'die Datei "hilfe" selektiert wird' in text
    assert 'ist der Status der App "Datei hilfe"' in text
    assert "Auswahl mehrerer Dateien" in text
    assert "die Datei hilfe2 wird selektiert" in text
    assert 'die Datei "hilfe2" selektiert wird' in text
    assert 'ist der Status der App "Datei hilfe2"' in text


@pytest.mark.sphinx(testroot="german")
def test_german_step_keywords_are_rendered_without_colon_and_with_canonical_css_classes(app, outdir):
    app.builder.build_all()

    html = (outdir / "index.html").read_text(encoding="utf-8")
    text = html_text(html)

    assert "Angenommen die App ist gestartet" in text
    assert "Und der lokale Rechner ist läuft" in text
    assert 'Wenn die Datei "hilfe" selektiert wird' in text
    assert 'Dann ist der Status der App "Datei hilfe"' in text
    assert 'Und ist der Status der App "Datei hilfe"'

    assert not re.search(r"\b(Angenommen|Wenn|Dann|Und|Aber)\s*:\s", text)

    assert_signature_class(html, "given", "Angenommen")
    assert_signature_class(html, "and", "Und")
    assert_signature_class(html, "when", "Wenn")
    assert_signature_class(html, "then", "Dann")


@pytest.mark.sphinx(testroot="german")
def test_german_keywords_are_mapped_to_gherkin_object_types(app, outdir):
    app.builder.build_all()

    html = (outdir / "index.html").read_text(encoding="utf-8")

    assert re.search(r'<dl\b[^>]*class="[^"]*\bgherkin-feature\b', html)
    assert re.search(r'<dl\b[^>]*class="[^"]*\bgherkin-background\b', html)
    assert re.search(r'<dl\b[^>]*class="[^"]*\bgherkin-scenario\b', html)
    assert re.search(r'<dl\b[^>]*class="[^"]*\bgherkin-rule\b', html)
    assert re.search(r'<dl\b[^>]*class="[^"]*\bgherkin-examples\b', html)
