import json

from dotenv_doctor.cli import main


def write(tmp_path, example, env):
    (tmp_path / ".env.example").write_text(example)
    (tmp_path / ".env").write_text(env)
    env, example = tmp_path / ".env", tmp_path / ".env.example"
    return ["--env", str(env), "--example", str(example)]


def test_ok(tmp_path, capsys):
    args = write(tmp_path, "A=\n", "A=1\n")
    assert main(args) == 0
    assert capsys.readouterr().out.startswith("OK")


def test_missing_fails(tmp_path, capsys):
    args = write(tmp_path, "A=\nB=\n", "A=1\n")
    assert main(args) == 1
    assert "missing" in capsys.readouterr().out


def test_extra_only_fails_in_strict(tmp_path):
    args = write(tmp_path, "A=\n", "A=1\nB=2\n")
    assert main(args) == 0
    assert main(args + ["--strict"]) == 1


def test_file_not_found(tmp_path, capsys):
    assert main(["--env", str(tmp_path / "nope")]) == 2
    assert "not found" in capsys.readouterr().err


def test_json_output(tmp_path, capsys):
    args = write(tmp_path, "A=\nB=\n", "A=1\n")
    assert main(args + ["--format", "json"]) == 1
    data = json.loads(capsys.readouterr().out)
    assert data["missing"] == ["B"] and data["ok"] is False
