# /// script
# dependencies = ["rich"]
# ///

import json
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich import box
from rich.text import Text
from rich.rule import Rule
from rich.panel import Panel

DATA_FILE = Path(__file__).parent / "HolyGrail_Invisibles.json"
BASES_FILE = Path(__file__).parent / "bases.json"

console = Console()


def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)


def load_bases():
    with open(BASES_FILE) as f:
        return json.load(f)


def count_items(d):
    found = not_found = 0
    for v in d.values():
        if isinstance(v, dict):
            if "wasFound" in v or v == {}:
                if v.get("wasFound"):
                    found += 1
                else:
                    not_found += 1
            else:
                f, nf = count_items(v)
                found += f
                not_found += nf
    return found, not_found


def print_progress(data):
    found, missing = count_items(data)
    total = found + missing
    pct = found / total * 100
    bar_width = 40
    filled = int(bar_width * found / total)
    bar = "█" * filled + "░" * (bar_width - filled)
    console.print()
    console.print(f"  [bold cyan]{bar}[/bold cyan]  [bold]{found}[/bold]/[bold]{total}[/bold] — [bold green]{pct:.1f}%[/bold green]")
    console.print()


def iter_items(d, path=None):
    """Yield (name, path_list, found) for every leaf item."""
    if path is None:
        path = []
    for k, v in d.items():
        if isinstance(v, dict):
            if "wasFound" in v or v == {}:
                yield k, path, v.get("wasFound", False)
            else:
                yield from iter_items(v, path + [k])


def cmd_missing(data, bases):
    sections = [
        ("UNIQUES — Armor", data["uniques"]["armor"], "gold1"),
        ("UNIQUES — Weapons", data["uniques"]["weapons"], "gold1"),
        ("UNIQUES — Other", data["uniques"]["other"], "gold1"),
        ("SETS", data["sets"], "green"),
    ]

    for section_title, section_data, color in sections:
        missing = [(name, path) for name, path, found in iter_items(section_data) if not found]
        if not missing:
            continue

        console.print(f"[bold {color}]{section_title}[/bold {color}]")

        for item, path in missing:
            base = bases.get(item, "")
            suffix = f" [cyan][{base}][/cyan]" if base else ""
            console.print(f"  [bold white]{item}[/bold white]{suffix}")

        console.print()


def cmd_full(data):
    print_progress(data)
    console.print(Rule("[bold cyan]FULL GRAIL LIST[/bold cyan]"))
    console.print()

    sections = [
        ("UNIQUES — Armor", data["uniques"]["armor"]),
        ("UNIQUES — Weapons", data["uniques"]["weapons"]),
        ("UNIQUES — Other", data["uniques"]["other"]),
        ("SETS", data["sets"]),
    ]

    for section_title, section_data in sections:
        found_count = sum(1 for _, _, f in iter_items(section_data) if f)
        total_count = sum(1 for _ in iter_items(section_data))
        console.print(f"[bold magenta]{section_title}[/bold magenta]  [dim]{found_count}/{total_count}[/dim]")

        grouped = {}
        for name, path, found in iter_items(section_data):
            key = " > ".join(path) if path else "—"
            grouped.setdefault(key, []).append((name, found))

        for group, items in grouped.items():
            console.print(f"  [dim]{group}[/dim]")
            for name, found in items:
                if found:
                    console.print(f"    [dim green]✓ {name}[/dim green]")
                else:
                    console.print(f"    [bold white]✗ {name}[/bold white]")

        console.print()


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("m", "f"):
        console.print("[bold red]Usage:[/bold red] grail.py [bold]m[/bold] (missing) | [bold]f[/bold] (full list)")
        sys.exit(1)

    data = load_data()
    bases = load_bases()
    cmd = sys.argv[1]

    if cmd == "m":
        cmd_missing(data, bases)
    elif cmd == "f":
        cmd_full(data)


if __name__ == "__main__":
    main()
