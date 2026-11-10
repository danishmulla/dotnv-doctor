from dotenv_doctor.core import parse_env


def test_basic_pairs():
    assert parse_env("A=1\nB=two\n") == [("A", "1"), ("B", "two")]


def test_comments_and_blank_lines_ignored():
    assert parse_env("# note\n\nA=1\n   # indented\n") == [("A", "1")]


def test_export_prefix():
    assert parse_env("export TOKEN=abc") == [("TOKEN", "abc")]


def test_quoted_values_keep_hash_and_spaces():
    pairs = dict(parse_env('A="x # y"\nB=\'  spaced  \'\n'))
    assert pairs == {"A": "x # y", "B": "  spaced  "}


def test_inline_comment_on_unquoted_value():
    assert parse_env("A=value # trailing") == [("A", "value")]


def test_empty_values():
    assert parse_env("A=\nB=''") == [("A", ""), ("B", "")])


def test_malformed_lines_skipped():
    assert parse_env("just text\n1BAD=x\nGOOD=y") == [("GOOD", "y")]


def test_value_can_contain_equals():
    url = "postgres://u:p@h/db?x=1"
    assert parse_env(f"URL={url}") == [("URL", url)]
