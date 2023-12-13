#!/usr/bin/env python3

import os
import re
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> str:
    return subprocess.run(cmd, capture_output=True).stdout.decode("utf-8")


def is_rebasing() -> bool:
    stdout = run(["git", "branch"])
    return "rebasing" in stdout


def is_dotfiles_repo() -> bool:
    stdout = run(["git", "remote", "-v"])
    return "dotfiles" in stdout


def read_codegpt_commit_title() -> str | None:
    path = Path(".git/CODEGPT_COMMIT_EDITMSG")
    if not path.exists():
        return None

    with open(path) as f:
        msg = f.read()
    os.remove(path)

    return msg


def read_prev_commit_msg() -> str:
    return run(["git", "log", "-1", "--pretty=%B"])


def replace_title(codegpt_commit_title: str, prev_commit_msg: str) -> str:
    pattern = r"\s-\s.*"
    replace = f" - {codegpt_commit_title}"
    return re.sub(pattern, replace, prev_commit_msg, count=1)


def prepare_commit_msg() -> None:
    codegpt_commit_tile = read_codegpt_commit_title()
    if codegpt_commit_tile is None:
        msg = read_prev_commit_msg()
    else:
        msg = replace_title(codegpt_commit_tile, read_prev_commit_msg())

    commit_msg_file = sys.argv[1]
    with open(commit_msg_file, "w") as f:
        f.write(msg)


if __name__ == "__main__":
    if not is_rebasing():
        prepare_commit_msg()
