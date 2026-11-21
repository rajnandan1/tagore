#!/usr/bin/env python3
"""UserPromptSubmit hook: print the straight-talk reminder line when that output style is on.

Reads the hook input from stdin. Prints nothing and exits 0 on any error, so it never blocks a message.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

STYLE = "tagore:straight-talk"
REMINDER = (
    "straight-talk is on: answer first, keep numbers and conditions exact, "
    "define each new term, and finish with one next action."
)


def active_style(project: Path, user_config: Path) -> str | None:
    settings_files = (
        project / ".claude" / "settings.local.json",
        project / ".claude" / "settings.json",
        user_config / "settings.json",
    )
    for path in settings_files:
        if not path.is_file():
            continue
        settings = json.loads(path.read_text(encoding="utf-8"))
        if "outputStyle" in settings:
            return settings["outputStyle"]
    return None


def main() -> int:
    try:
        hook_input = json.loads(sys.stdin.read())
        project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or hook_input["cwd"])
        user_config = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")
        if active_style(project, user_config) == STYLE:
            print(REMINDER)
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
