import re
from collections import Counter
from dataclasses import dataclass, field

KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.-]*$")


@dataclass
class Report:
    missing: list[str] = field(default_factory=list)
    extra: list[str] = field(default_factory=list)
    empty: list[str] = field(default_factory=list)
    duplicates: list[str] = field(default_factory=list)

    def failed(self, strict=False):
        # a missing key is always a failure, the rest only count in strict mode
        if self.missing:
            return True
        return strict and bool(self.extra or self.empty or self.duplicates)


def parse_value(raw):
    raw = raw.strip()
    if not raw:
        return ""

    if raw[0] in "\"'":
        quote = raw[0]
        i = 1
        while i < len(raw):
            if quote == '"' and raw[i] == "\\":
                i += 2  # skip the escaped character
                continue
            if raw[i] == quote:
                return raw[1:i]
            i += 1
        return raw[1:]  # quote never closed, just take the rest

    # only " #" starts a comment, so something like a#b is left alone
    return raw.split(" #", 1)[0].strip()


def parse_env(text):
    """Return a list of (key, value) pairs in the order they appear."""
    pairs = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].lstrip()

        key, sep, value = line.partition("=")
        key = key.strip()
        if not sep or not KEY_RE.match(key):
            continue  # not an assignment, ignore it
        pairs.append((key, parse_value(value)))
    return pairs


def compare(example, env, allow_empty=()):
    example_keys = list(dict.fromkeys(k for k, _ in example))
    env_keys = list(dict.fromkeys(k for k, _ in env))
    example_set = set(example_keys)
    allowed = set(allow_empty)
    counts = Counter(k for k, _ in env)
    values = dict(env)  # if a key repeats, the last one wins (like most loaders)

    return Report(
        missing=[k for k in example_keys if k not in values],
        extra=[k for k in env_keys if k not in example_set],
        empty=[
            k
            for k in env_keys
            if k in example_set and k not in allowed and values[k] == ""
        ],
        duplicates=[k for k, n in counts.items() if n > 1],
    )
