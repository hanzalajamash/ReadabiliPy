"""Test readability.py on sample articles"""
from pytest import mark
from .checks import check_exact_html_output, check_extract_article, check_extract_paragraphs_as_plain_text

# Test end-to-end article extraction
def test_extract_article_full_page():
    check_extract_article(
        "addictinginfo.com-1_full_page.html",
        "addictinginfo.com-1_simple_article_from_full_page.json"
    )


def test_extract_article_full_article():
    check_extract_article(
        "addictinginfo.com-1_full_article.html",
        "addictinginfo.com-1_simple_article_from_full_article.json"
    )


def test_extract_article_non_article():
    check_extract_article(
        "non_article_full_page.html",
        "non_article_full_page.json"
    )


def test_extract_article_unicode_normalisation():
    check_extract_article(
        "conservativehq.com-1_full_page.html",
        "conservativehq.com-1_simple_article_from_full_page.json"
    )


def test_extract_article_list_items():
    check_extract_article(
        "list_items_full_page.html",
        "list_items_simple_article_from_full_page.json"
    )


def test_extract_article_headers_and_non_paragraph_blockquote_text():
    check_extract_article(
        "davidwolfe.com-1_full_page.html",
        "davidwolfe.com-1_simple_article_from_full_page.json"
    )


def test_extract_article_list_items_content_digests():
    check_extract_article(
        "list_items_full_page.html",
        "list_items_simple_article_from_full_page_content_digests.json",
        content_digests=True
    )


def test_extract_article_list_items_node_indexes():
    check_extract_article(
        "list_items_full_page.html",
        "list_items_simple_article_from_full_page_node_indexes.json",
        node_indexes=True
    )


def test_extract_article_full_page_content_digest():
    check_extract_article(
        "addictinginfo.com-1_full_page.html",
        "addictinginfo.com-1_simple_article_from_full_page_content_digest.json",
        content_digests=True
    )


def test_extract_article_full_page_node_indexes():
    check_extract_article(
        "addictinginfo.com-1_full_page.html",
        "addictinginfo.com-1_simple_article_from_full_page_node_indexes.json",
        node_indexes=True
    )


def test_extract_article_full_page_content_digest_node_indexes():
    check_extract_article(
        "addictinginfo.com-1_full_page.html",
        "addictinginfo.com-1_simple_article_from_full_page_content_digest_node_indexes.json",
        content_digests=True,
        node_indexes=True
    )


# Test plain text extraction
def test_extract_paragraphs_as_plain_text():
    check_extract_paragraphs_as_plain_text(
        "addictinginfo.com-1_simple_article_from_full_article.json",
        "addictinginfo.com-1_plain_text_paragraphs_from_simple_article.json"
    )


def test_extract_paragraphs_as_plain_text_node_indexes():
    check_extract_paragraphs_as_plain_text(
        "list_items_simple_article_from_full_page_node_indexes.json",
        "list_items_plain_text_paragraph_node_indexes.json"
    )


# Test correct wrapping
def test_ensure_correct_div_wrapping():
    """Do not wrap in a <div> if this is already a <div>."""
    check_exact_html_output("""
        <div>
            <p>
                Some example text here.
            </p>
        </div>""",
    """<div><p>Some example text here.</p></div>""")


# Test whitespace around tags
@mark.parametrize('punctuation', ['.', ',', '!', ':', ';', '?'])
def test_ensure_correct_punctuation_joining(punctuation):
    """Do not join with ' ' if the following character is a punctuation mark."""
    check_exact_html_output("""
        <div>
            <p>
                Some text <a href="example.com">like this</a>{0} with punctuation.
            </p>
        </div>""".format(punctuation),
    """<div><p>Some text like this{0} with punctuation.</p></div>""".format(punctuation))


# Test comments inside tags
def test_comments_inside_tags():
    """Ensure that comments inside tags are removed."""
    check_exact_html_output("""
        <p>Some <!-- --> text <!-- with a comment --> here <!--or here-->.<!----></p>
        """,
    """<div><p>Some text here.</p></div>""")

