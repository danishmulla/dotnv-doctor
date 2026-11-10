# Contributing

Thanks for helping! Small PRs are very welcome.

## Setup

```bash
git clone https://github.com/<you>/dotenv-doctor
cd dotenv-doctor
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Before you open a PR

```bash
ruff check .
pytest
```

- Add or update a test for every behaviour change.
- Keep the package dependency-free (standard library only).
- One focused change per PR; describe the *why* in the description.

Look for issues labelled **good first issue**, or pick something from the
roadmap in the README.
