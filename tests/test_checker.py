from dotenv_doctor.core import compare, parse_env


def run(example, env, **kwargs):
    return compare(parse_env(example), parse_env(env), **kwargs)


def test_clean():
    assert not run("A=\nB=", "A=1\nB=2").failed(strict=True)


def test_missing_keys_keep_example_order():
    report = run("A=\nB=\nC=", "B=1")
    assert report.missing == ["A", "C"]
    assert report.failed()


def test_extra_keys():
    report = run("A=", "A=1\nZ=9")
    assert report.extra == ["Z"]
    assert not report.failed()
    assert report.failed(strict=True)


def test_empty_and_allow_empty():
    assert run("A=\nB=", "A=\nB=2").empty == ["A"]
    assert run("A=\nB=", "A=\nB=2", allow_empty=["A"]).empty == []


def test_duplicate_key_last_value_wins():
    report = run("A=", "A=\nA=filled")
    assert report.duplicates == ["A"]
    assert report.empty == []
