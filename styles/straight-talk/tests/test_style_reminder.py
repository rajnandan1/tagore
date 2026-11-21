"""scripts/style_reminder.py: the reminder line prints only while the straight-talk output style is on.

Temporary folders stand in for the project and the home folder.

    python3 -m pytest styles/straight-talk/tests/test_style_reminder.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "style_reminder.py"
STYLE = "tagore:straight-talk"
REMINDER = (
    "straight-talk is on: answer first, keep numbers and conditions exact, "
    "define each new term, and finish with one next action.\n"
)


def run_hook(tmp_path: Path, local=None, project=None, user=None, config_dir=None) -> subprocess.CompletedProcess:
    project_dir = tmp_path / "project"
    home_dir = tmp_path / "home"
    contents = {
        project_dir / ".claude" / "settings.local.json": local,
        project_dir / ".claude" / "settings.json": project,
        home_dir / ".claude" / "settings.json": user,
        tmp_path / "config" / "settings.json": config_dir,
    }
    project_dir.mkdir()
    home_dir.mkdir()
    for path, content in contents.items():
        if content is not None:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content if isinstance(content, str) else json.dumps(content), encoding="utf-8")
    env = {k: v for k, v in os.environ.items() if k not in ("CLAUDE_PROJECT_DIR", "CLAUDE_CONFIG_DIR")}
    env["HOME"] = str(home_dir)
    if config_dir is not None:
        env["CLAUDE_CONFIG_DIR"] = str(tmp_path / "config")
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=json.dumps({"cwd": str(project_dir)}),
        capture_output=True,
        text=True,
        env=env,
    )


def test_local_file_turns_the_reminder_on(tmp_path):
    result = run_hook(tmp_path, local={"outputStyle": STYLE})
    assert result.stdout == REMINDER


def test_local_file_wins_over_user_file(tmp_path):
    result = run_hook(tmp_path, local={"outputStyle": "default"}, user={"outputStyle": STYLE})
    assert result.stdout == ""


def test_user_file_alone_turns_the_reminder_on(tmp_path):
    result = run_hook(tmp_path, user={"outputStyle": STYLE})
    assert result.stdout == REMINDER


def test_another_style_in_the_project_file_prints_nothing(tmp_path):
    result = run_hook(tmp_path, project={"outputStyle": "Concise"})
    assert result.stdout == ""


def test_no_settings_file_prints_nothing(tmp_path):
    result = run_hook(tmp_path)
    assert result.stdout == ""


def test_invalid_json_prints_nothing_and_exits_zero(tmp_path):
    result = run_hook(tmp_path, local="{not json", user={"outputStyle": STYLE})
    assert result.stdout == ""
    assert result.returncode == 0


def test_config_dir_replaces_the_home_settings_file(tmp_path):
    result = run_hook(tmp_path, user={"outputStyle": "default"}, config_dir={"outputStyle": STYLE})
    assert result.stdout == REMINDER


def test_config_dir_with_another_style_prints_nothing(tmp_path):
    result = run_hook(tmp_path, user={"outputStyle": STYLE}, config_dir={"outputStyle": "default"})
    assert result.stdout == ""
