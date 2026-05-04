from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from pathlib import Path

from docutils import nodes
from sphinx import addnodes
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import make_id

from sphinx_gherkinfile import (
    SphinxGherkinFileError,
    get_config_gherkinfile_dirs,
    keyword_to_css_class,
    keyword_to_objtype,
)
from sphinx_gherkinfile.gherkin import (
    Background,
    BehaviorScope,
    DataTable,
    DefinitionBuildah,
    Document,
    Examples,
    Feature,
    Rule,
    Scenario,
    Step,
)

KeywordNode = Feature | Rule | Background | Scenario | Examples | Step


class GherkinFileDirective(SphinxDirective):
    """Render a Gherkin feature from an existing ``.feature`` file."""

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self) -> list[nodes.Node]:
        feature_path = self._resolve_feature_file(self.arguments[0])
        self._note_dependency(feature_path)

        document = DefinitionBuildah.from_path(feature_path).parse()
        return [self._render_keyword(document.feature, document)]

    def _resolve_feature_file(self, argument: str) -> Path:
        requested = Path(argument)
        candidates: list[Path] = []

        if requested.is_absolute():
            candidates.append(requested)
        else:
            for source_root in get_config_gherkinfile_dirs(self.env):
                candidates.append(source_root / requested)
            candidates.append(Path(self.env.srcdir, requested))

        for candidate in candidates:
            if candidate.is_file():
                return candidate.resolve()

        searched = ", ".join(str(candidate) for candidate in candidates)
        raise SphinxGherkinFileError(f"Could not find Gherkin feature file '{argument}'. Searched: {searched}")

    def _note_dependency(self, feature_path: Path) -> None:
        try:
            self.env.note_dependency(str(feature_path))
        except AttributeError:
            self.state.document.settings.record_dependencies.add(str(feature_path))

    def _render_keyword(self, keyword: KeywordNode, document: Document) -> addnodes.desc:
        objtype = keyword_to_objtype(keyword.keyword)
        desc = addnodes.desc()
        desc["domain"] = "gherkinfile"
        desc["objtype"] = objtype
        desc["classes"].extend(["gherkin", f"gherkin-{objtype}"])
        # enable if it should be backward compatible with old implementation
        desc["classes"].extend(["gherkin", objtype, f"gherkin-{objtype}"])
        if isinstance(keyword, BehaviorScope):
            desc["classes"].extend(self._tag_classes(keyword))

        signature = self._make_signature(keyword, objtype, document)
        content = addnodes.desc_content()
        content.extend(self._make_content(keyword, document))

        desc += signature
        desc += content
        return desc

    def _repeated_step_keyword(self, document: Document) -> str:
        if document.feature.language.lower() == "de":
            return "Und"

        return "And"

    def _display_keyword(self, keyword: KeywordNode, document: Document) -> str:
        display_keyword = keyword.keyword.strip()
        if isinstance(keyword, Step) and display_keyword == "*":
            return self._repeated_step_keyword(document)

        return display_keyword

    def _keyword_class(self, keyword: KeywordNode) -> str:
        return keyword_to_css_class(keyword.keyword)

    def _make_signature(self, keyword: KeywordNode, objtype: str, document: Document) -> addnodes.desc_signature:
        summary = keyword.summary
        signature = addnodes.desc_signature(summary, "")
        signature["ids"].append(self._make_node_id(keyword, objtype, document))
        signature["classes"].append(self._keyword_class(keyword))

        display_keyword = self._display_keyword(keyword, document)
        signature += addnodes.desc_annotation(display_keyword, "", nodes.Text(display_keyword))

        if not isinstance(keyword, Step):
            signature += addnodes.desc_sig_punctuation("", ":")

        if summary:
            signature += addnodes.desc_sig_space()
            signature += addnodes.desc_name(summary, summary)
        if isinstance(keyword, BehaviorScope):
            tag_nodes = self._render_inline_tags(keyword)
            if tag_nodes:
                signature += addnodes.desc_sig_space()
                signature.extend(tag_nodes)
        self.state.document.note_explicit_target(signature)
        return signature

    def _make_node_id(self, keyword: KeywordNode, objtype: str, document: Document) -> str:
        raw_id = f"gherkin-{document.name}-{objtype}-{keyword.location.start.line}-{keyword.summary}"
        return make_id(self.env, self.state.document, "", raw_id)

    def _make_content(self, keyword: KeywordNode, document: Document) -> list[nodes.Node]:
        content: list[nodes.Node] = []

        if isinstance(keyword, BehaviorScope):
            # content.extend(self._render_tags(keyword))
            content.extend(self._render_description(keyword.description))

        if isinstance(keyword, (Feature, Rule)):
            content.extend(self._render_children(keyword.children, document))
        elif isinstance(keyword, Background):
            content.extend(self._render_children(keyword.steps, document))
        elif isinstance(keyword, Scenario):
            content.extend(self._render_children(keyword.steps, document))
            content.extend(self._render_children(keyword.examples, document))
        elif isinstance(keyword, Step):
            if keyword.docstring:
                literal = nodes.literal_block(keyword.docstring.content, keyword.docstring.content)
                if keyword.docstring.mediatype:
                    literal["language"] = keyword.docstring.mediatype
                content.append(literal)
            if keyword.datatable:
                content.append(self._render_datatable(keyword.datatable))
        elif isinstance(keyword, Examples):
            content.append(self._render_datatable(keyword.datatable))

        return content

    def _render_children(self, children: Iterable[KeywordNode], document: Document) -> list[nodes.Node]:
        return [self._render_keyword(child, document) for child in children]

    def _render_inline_tags(self, keyword: BehaviorScope) -> list[nodes.Node]:
        if not keyword.tags:
            return []

        tag_list = nodes.inline(classes=["gherkin-tags"])
        for index, tag in enumerate(keyword.tags):
            if index:
                tag_list += nodes.Text(" ")
            tag_node = nodes.inline(tag.name, tag.name)
            tag_node["classes"].extend(["gherkin-tag", self._tag_class(tag.name)])
            tag_list += tag_node
        return [tag_list]

    def _tag_classes(self, keyword: BehaviorScope) -> list[str]:
        return [self._tag_class(tag.name) for tag in keyword.tags]

    def _tag_class(self, tag_name: str) -> str:
        tag = tag_name.strip().removeprefix("@").lower()
        sanitized = re.sub(r"[^a-z0-9]+", "_", tag).strip("_")
        return f"tag_{sanitized}" if sanitized else "tag"

    def _render_description(self, description: str) -> list[nodes.Node]:
        paragraphs: list[nodes.Node] = []
        for raw_line in description.splitlines():
            line = raw_line.strip()
            if line:
                paragraphs.append(nodes.paragraph(text=line))
        return paragraphs

    def _render_datatable(self, datatable: DataTable) -> nodes.table:
        rows: Sequence[Sequence[str]] = datatable.values
        column_count = max((len(row) for row in rows), default=0)
        table = nodes.table()
        tgroup = nodes.tgroup(cols=column_count)
        table += tgroup

        for _ in range(column_count):
            tgroup += nodes.colspec(colwidth=1)

        thead = nodes.thead()
        tbody = nodes.tbody()
        tgroup += thead
        tgroup += tbody

        for index, row_values in enumerate(rows):
            row = nodes.row()
            for cell_value in row_values:
                entry = nodes.entry()
                entry += nodes.paragraph(text=cell_value)
                row += entry
            if index == 0:
                thead += row
            else:
                tbody += row

        return table
