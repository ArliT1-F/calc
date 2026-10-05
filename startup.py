"""Install or remove an XDG desktop launcher and login autostart entry."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

APP_ID = "euro-lek-board.desktop"


def desktop_quote(path: Path) -> str:
    # Desktop Entry Specification Exec quoting (including reserved characters).
    value = str(path)
    for char in ("\\", '"', "$", "`"):
        value = value.replace(char, "\\" + char)
    return '"' + value + '"'


def entry(app_path: Path) -> str:
    return ("[Desktop Entry]\n"
            "Type=Application\n"
            "Name=Euro to Lek Board\n"
            "Comment=Fixed euro to Albanian lek conversion board\n"
            f"Exec=python3 {desktop_quote(app_path)}\n"
            "Icon=accessories-calculator\n"
            "Terminal=false\n"
            "Categories=Utility;Calculator;\n"
            "StartupNotify=true\n")


def locations() -> tuple[Path, Path]:
    home = Path.home()
    config = Path(os.environ.get("XDG_CONFIG_HOME") or home / ".config")
    data = Path(os.environ.get("XDG_DATA_HOME") or home / ".local/share")
    return config / "autostart" / APP_ID, data / "applications" / APP_ID


def main() -> None:
    parser = argparse.ArgumentParser(description="Set up Euro to Lek Board for desktop login")
    parser.add_argument("--uninstall", action="store_true", help="remove startup and app menu entries")
    args = parser.parse_args()
    autostart, menu = locations()
    if args.uninstall:
        for path in (autostart, menu):
            path.unlink(missing_ok=True)
        print("Removed login startup and app menu entries. Saved exchange rate was not deleted.")
    else:
        content = entry(Path(__file__).resolve().parent / "app.py")
        for path in (autostart, menu):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            print(f"Installed {path}")
        print("The board will open automatically at your next graphical login.")


if __name__ == "__main__":
    main()
