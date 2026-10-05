"""Exchange-rate validation, formatting and persistence."""

import json
import os
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

DEFAULT_RATE = Decimal("88")

def config_path() -> Path:
    base = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    return base / "euro-lek-board" / "settings.json"


def parse_rate(value: str | int | float | Decimal) -> Decimal:
    try:
        rate = Decimal(str(value).strip().replace(",", "."))
    except (InvalidOperation, ValueError):
        raise ValueError("Enter a valid number, such as 86 or 86.5.") from None
    if not rate.is_finite() or rate <= 0:
        raise ValueError("The rate must be greater than zero.")
    return rate


def load_rate(path: Path | None = None) -> Decimal:
    try:
        data = json.loads((path or config_path()).read_text(encoding="utf-8"))
        return parse_rate(data["rate"])
    except (OSError, ValueError, KeyError, TypeError):
        return DEFAULT_RATE


def save_rate(rate: Decimal, path: Path | None = None) -> None:
    target = path or config_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_name(target.name + ".tmp")
    try:
        temp.write_text(json.dumps({"rate": str(rate)}, indent=2) + "\n", encoding="utf-8")
        temp.replace(target)
    finally:
        temp.unlink(missing_ok=True)


def format_amount(value: Decimal) -> str:
    rounded = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"{rounded:,.2f}".rstrip("0").rstrip(".")

