# D2R Holy Grail CLI - Plan

## Summary

A simple read-only Python CLI to track holy grail progress, using `rich` for output.
Run from PowerShell via `uv run grail.py [command]`.

---

## Commands

| Command          | Description                                  |
| ---------------- | -------------------------------------------- |
| `uv run grail.py m`  | Show missing items, grouped by category  |
| `uv run grail.py f`  | Show full list with found/missing styling |

Both commands show a progress header at the top: `471 / 502 — 93.8%`

---

## Data source

- Reads `HolyGrail_Invisibles.json` from the same folder as the script
- Read-only (no write-back for now)
- No separate database or state file

---

## `dia m` — Missing view

Groups missing items by the JSON hierarchy:

```
[Progress bar] 471/502 — 93.8%

UNIQUES — Armor
  chest (elite)
    - Templar's Might
    - Tyrael's Might
  helm (elite)
    - Giant Skull
  ...

UNIQUES — Weapons
  ...

UNIQUES — Other
  ...

SETS
  Arctic Gear
    - Arctic Furs
  ...
```

---

## `dia f` — Full list view

Same grouping as above, but shows all items:
- Found items: dimmed green (or just dim)
- Missing items: bold white (stand out clearly)
- Section headers in Rich `Panel` or styled `rule`

---

## File structure

```
sandbox/d2r/
  grail.py                    ← single script, all logic here
  HolyGrail_Invisibles.json   ← data source
  new-items.md                ← for future expansion items
  holy-grail-plan.md          ← this file
```

---

## Script structure

```python
# /// script
# dependencies = ["rich"]
# ///

# 1. Load JSON
# 2. Parse args (m / f)
# 3. Flatten items into a list of (name, category, tier, found) tuples
# 4. Render with Rich
```

Using `uv` inline script metadata so no `pyproject.toml` needed.

---

## Out of scope (for now)

- `dia find` command (write-back)
- Expansion/Warlock items
- Search/fuzzy match
