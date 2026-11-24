"""Monday, Reviewed in One Line — make.fun entry.

Writes the single one-line review of Monday to entry.txt in the output
directory ($MAKEFUN_OUTPUT_DIR, default /output). Python stdlib only,
deterministic, no network, no clock, no randomness.

Gate (from the competition rules): /output/entry.txt must be UTF-8 text
of 1 to 200 characters, not only white space. The entry is written with
no trailing newline so the file holds exactly the judged line.

Usage:
    python3 main.py --self-test   # validate + byte-identical round-trip
    python3 main.py --check       # validate ENTRY only, write nothing
    python3 main.py               # validate and write entry.txt
"""

import argparse
import os
import sys
import tempfile

ENTRY = (
    "Monday: one star. Woke up tired, worked tired, went to bed tired. "
    "Would not recommend \u2014 unfortunately, I am a regular."
)

MAX_CHARS = 200


def validate(text: str) -> list:
    """Return a list of gate failures for `text` (empty means valid)."""
    problems = []
    if not 1 <= len(text) <= MAX_CHARS:
        problems.append("length %d chars, must be 1-%d" % (len(text), MAX_CHARS))
    if not text.strip():
        problems.append("entry is only white space")
    if text != text.strip():
        problems.append("entry has leading or trailing whitespace")
    if "  " in text:
        problems.append("entry contains double spaces")
    if "\n" in text or "\r" in text:
        problems.append("entry must be a single line")
    return problems


def write_entry(directory: str) -> str:
    """Write ENTRY to entry.txt in `directory`, no trailing newline."""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    return path


def read_back(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Write the Monday review.")
    parser.add_argument("--check", action="store_true",
                        help="validate ENTRY only, write nothing")
    parser.add_argument("--self-test", action="store_true",
                        help="validate + byte-identical round-trip in a temp dir")
    args = parser.parse_args(argv)

    problems = validate(ENTRY)
    if problems:
        for problem in problems:
            print("invalid: " + problem, file=sys.stderr)
        return 1

    if args.check:
        print("valid: %d chars" % len(ENTRY))
        return 0

    if args.self_test:
        with tempfile.TemporaryDirectory() as tmp:
            path = write_entry(tmp)
            if read_back(path) != ENTRY:
                print("self-test FAILED: round-trip mismatch", file=sys.stderr)
                return 1
        print("self-test OK: %d chars, byte-identical round-trip" % len(ENTRY))
        return 0

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = write_entry(out_dir)
    if read_back(path) != ENTRY:
        print("FAILED: entry.txt does not match ENTRY", file=sys.stderr)
        return 1
    print("wrote %s (%d chars)" % (path, len(ENTRY)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
