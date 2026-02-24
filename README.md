# D2R Holy Grail CLI

A simple CLI to track your Diablo 2 Resurrected holy grail progress.

## Requirements

- [uv](https://github.com/astral-sh/uv)

## Usage

```
uv run grail.py m    # missing items only
uv run grail.py f    # full list
```

## Data

Place your `HolyGrail_Invisibles.json` (from [zeddicus-pl/d2rHolyGrail](https://github.com/zeddicus-pl/d2rHolyGrail)) in the same folder as the script.

The missing view shows each item's base type so you can identify drops on the fly:

```
UNIQUES — Weapons
  Gull [Dagger]
  Ghostflame [Legend Spike]

SETS
  Arctic Furs [Quilted Armor]
```
