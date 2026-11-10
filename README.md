# dotenv-doctor

Check that your `.env` matches your `.env.example`, so a missing variable
fails in CI instead of in production. Pure standard library, Python 3.9+.

## Install

```bash
pip install git+https://github.com/<you>/dotenv-doctor
```

## Usage

```bash
dotenv-doctor                          # compares .env with .env.example
dotenv-doctor --env .env.production --example .env.example
dotenv-doctor --strict                 # extra / empty / duplicate keys fail too
dotenv-doctor --allow-empty DEBUG      # DEBUG may be blank
dotenv-doctor --format json            # machine-readable output
```

Example output:

```
[ERROR] missing from .env (2): DATABASE_URL, SECRET_KEY
[WARN] not in .env.example (1): OLD_FLAG
[WARN] empty values (1): API_KEY
```

Exit codes: `0` ok, `1` problems found, `2` file not found.

## What it checks

| Finding | Meaning | Fails by default? |
| --- | --- | --- |
| missing | key in `.env.example` but not in `.env` | yes |
| extra | key in `.env` but not in `.env.example` | with `--strict` |
| empty | key present but value is empty | with `--strict` |
| duplicate | key defined more than once | with `--strict` |

## pre-commit

```yaml
repos:
  - repo: https://github.com/<you>/dotenv-doctor
    rev: v0.1.0
    hooks:
      - id: dotenv-doctor
```

## Roadmap (good first issues)

- [ ] `--fix` flag that appends missing keys to `.env`
- [ ] Support multi-line quoted values
- [ ] Variable interpolation awareness (`${OTHER_VAR}`)
- [ ] Config via `pyproject.toml` (`[tool.dotenv-doctor]`)
- [ ] Check several env files in one run
- [ ] Publish to PyPI

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). MIT licensed.
