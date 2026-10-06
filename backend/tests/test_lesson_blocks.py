"""The figure-marker syntax: `{{figure:<key>}}` on a line of its own, and how a lesson body splits around it."""
import pytest

from app.services.content.lesson_blocks import (
    FigureBlock, TextBlock, empty_anchors, figure_keys, has_figures, is_valid_key, malformed_markers, split_lesson,
)

BODY = """# LoRA

LoRA decomposes the trainable update into two low-rank matrices.

{{figure:lora-low-rank-adaptation}}

The original weights stay frozen while the small matrices are trained.

{{figure:parameter-savings}}

That is why far fewer parameters are trained.
"""


def test_a_body_splits_into_ordered_text_and_figure_blocks():
    blocks = split_lesson(BODY)
    assert [type(b).__name__ for b in blocks] == ["TextBlock", "FigureBlock", "TextBlock", "FigureBlock", "TextBlock"]
    assert blocks[0].content == "# LoRA\n\nLoRA decomposes the trainable update into two low-rank matrices."
    assert blocks[1] == FigureBlock("lora-low-rank-adaptation")
    assert blocks[2].content == "The original weights stay frozen while the small matrices are trained."
    assert blocks[3] == FigureBlock("parameter-savings")
    assert blocks[4].content == "That is why far fewer parameters are trained."


def test_figure_order_is_preserved_and_repeats_are_kept():
    text = "a\n\n{{figure:one}}\n\nb\n\n{{figure:two}}\n\n{{figure:one}}\n\nc"
    assert figure_keys(text) == ["one", "two", "one"]


def test_the_surrounding_markdown_is_kept_exactly():
    text = "intro\n\n```python\nprint('x')\n```\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\n{{figure:k}}\n\n> callout\n"
    before, figure, after = split_lesson(text)
    assert before.content == "intro\n\n```python\nprint('x')\n```\n\n| a | b |\n|---|---|\n| 1 | 2 |"
    assert figure == FigureBlock("k")
    assert after.content == "> callout"


def test_a_body_without_figures_is_a_single_unchanged_block():
    text = "# Title\n\nJust prose.\n\n- a\n- b\n"
    assert split_lesson(text) == [TextBlock(text.strip("\n"))]
    assert not has_figures(text)
    assert split_lesson("") == [] and split_lesson("   \n\n") == []


@pytest.mark.parametrize("fence", ["```", "~~~", "````"])
def test_a_marker_inside_a_code_fence_is_code_not_a_figure(fence):
    text = f"How to place one:\n\n{fence}text\n{{{{figure:example}}}}\n{fence}\n\nDone."
    assert not has_figures(text)
    assert malformed_markers(text) == []
    assert split_lesson(text) == [TextBlock(text.strip("\n"))]


def test_a_shorter_inner_fence_does_not_close_a_longer_one():
    text = "````md\n```\n{{figure:inside}}\n```\n````\n\n{{figure:outside}}\n"
    assert figure_keys(text) == ["outside"]


def test_indentation_and_trailing_spaces_around_a_marker_are_ignored():
    assert figure_keys("a\n\n   {{figure:spaced}}   \n\nb") == ["spaced"]
    assert figure_keys("a\n\n{{figure:crlf}}\r\n\r\nb") == ["crlf"]


def test_adjacent_markers_produce_no_empty_text_block_between_them():
    assert split_lesson("{{figure:a}}\n{{figure:b}}\n") == [FigureBlock("a"), FigureBlock("b")]


@pytest.mark.parametrize("line", [
    "As shown in {{figure:inline}} the model",
    "{{figure:Upper-Case}}",
    "{{figure:under_score}}",
    "{{ figure : spaced }}",
    "{{figure:missing-brace}",
    "{{figure:}}",
])
def test_anything_that_looks_like_a_marker_but_is_not_valid_is_reported(line):
    assert malformed_markers(f"text\n\n{line}\n\nmore") != []
    assert not has_figures(f"text\n\n{line}\n\nmore")


def test_a_valid_marker_is_not_reported_as_malformed():
    assert malformed_markers(BODY) == []


@pytest.mark.parametrize("anchor", [
    '<a id="dispersion"></a>',
    "<a id='dispersion'></a>",
    '<a id="dispersion" ></a>',
    '<a  id="dispersion"></a>',
    '<a id="dispersion">\n</a>',
    '<a name="dispersion"></a>',
    '<A ID="dispersion"></A>',
    '&lt;a id="dispersion"&gt;&lt;/a&gt;',
])
def test_an_empty_extraction_anchor_is_reported_with_its_line(anchor):
    found = empty_anchors(f"# Title\n\n{anchor}\n## Dispersion\n\nText.")
    assert [line for line, _ in found] == [3]


@pytest.mark.parametrize("text", [
    '<a href="https://example.com">Documentation</a>',
    '<a href="#dispersion">Jump to Dispersion</a>',
    '<a id="dispersion">Dispersion</a>',
    '<h2 id="dispersion">Dispersion</h2>',
    '<div id="example"></div>',
    '`<a id="dispersion"></a>` is how the old export marked a section.',
    '```html\n<a id="dispersion"></a>\n```',
    '~~~\n<a id="dispersion"></a>\n~~~',
])
def test_links_other_ids_and_anchors_shown_as_code_are_not_reported(text):
    assert empty_anchors(f"Intro\n\n{text}\n\nMore") == []


def test_several_anchors_report_each_line_in_order():
    body = '<a id="a"></a>\n## A\n\ntext\n\n<a id="b"></a>\n## B\n'
    assert [(n, tag) for n, tag in empty_anchors(body)] == [(1, '<a id="a"></a>'), (6, '<a id="b"></a>')]


@pytest.mark.parametrize("key,ok", [
    ("lora-low-rank-adaptation", True), ("fig-1", True), ("a", True), ("x" * 120, True), ("x" * 121, False),
    ("", False), ("-a", False), ("a-", False), ("a--b", False), ("A", False), ("a_b", False), ("a/b", False),
    ("..", False), ("a b", False),
])
def test_asset_keys_are_lowercase_words_joined_by_hyphens(key, ok):
    assert is_valid_key(key) is ok
