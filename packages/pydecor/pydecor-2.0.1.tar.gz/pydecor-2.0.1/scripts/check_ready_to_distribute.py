#!/usr/bin/env python
"""Prepare to distribute the package."""

from subprocess import Popen, PIPE
from sys import argv

import pydecor as pkg


def check_version(version: str) -> None:
    """Ensure the version matches the package."""
    assert version == pkg.__version__, "Failed version check."


def check_branch() -> None:
    """Ensure we are on the master branch."""
    proc = Popen(
        ("git", "rev-parse", "--abbrev-ref", "HEAD"), stdout=PIPE, stderr=PIPE
    )
    out, err = proc.communicate()
    assert proc.returncode == 0, err.decode()
    assert out.decode().strip() == "master", "Not on master!"


def check_diff() -> None:
    """Ensure there is no git diff output with origin/master."""
    proc = Popen(("git", "diff", "origin/master"), stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    assert proc.returncode == 0, err.decode()
    assert out.decode().strip() == "", "There is a diff with origin/master!"


def main() -> None:
    """Check version, git tag, etc."""
    version = argv[1]
    check_version(version)
    check_branch()
    check_diff()


if __name__ == "__main__":
    main()
