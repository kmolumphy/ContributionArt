#!/usr/bin/env python3
"""
GitHub Contribution Graph Art

USAGE:
  python generate_commits.py "HELLO THERE"          # draw text in current year
  python generate_commits.py "HI" --year=2025       # draw in a specific year
  python generate_commits.py --reset                 # wipe art, start fresh
  python generate_commits.py --reset "NEW TEXT"      # reset then draw new text

After running, push with:
  git push origin main --force
"""

import subprocess, os, sys
from datetime import date, timedelta

FONT = {
    'A': [[0,1,0],[1,0,1],[1,0,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1]],
    'B': [[1,1,0],[1,0,1],[1,0,1],[1,1,0],[1,0,1],[1,0,1],[1,1,0]],
    'C': [[0,1,1],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[0,1,1]],
    'D': [[1,1,0],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,0]],
    'E': [[1,1,1],[1,0,0],[1,0,0],[1,1,0],[1,0,0],[1,0,0],[1,1,1]],
    'F': [[1,1,1],[1,0,0],[1,0,0],[1,1,0],[1,0,0],[1,0,0],[1,0,0]],
    'G': [[0,1,1],[1,0,0],[1,0,0],[1,0,1],[1,0,1],[1,0,1],[0,1,1]],
    'H': [[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1]],
    'I': [[1,1,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[1,1,1]],
    'J': [[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[1,0,1],[0,1,0]],
    'K': [[1,0,1],[1,0,1],[1,1,0],[1,0,0],[1,1,0],[1,0,1],[1,0,1]],
    'L': [[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,1,1]],
    'M': [[1,0,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1]],
    'N': [[1,0,1],[1,1,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1]],
    'O': [[0,1,0],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[0,1,0]],
    'P': [[1,1,0],[1,0,1],[1,0,1],[1,1,0],[1,0,0],[1,0,0],[1,0,0]],
    'Q': [[0,1,0],[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,0,1],[0,1,1]],
    'R': [[1,1,0],[1,0,1],[1,0,1],[1,1,0],[1,1,0],[1,0,1],[1,0,1]],
    'S': [[0,1,1],[1,0,0],[1,0,0],[0,1,0],[0,0,1],[0,0,1],[1,1,0]],
    'T': [[1,1,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0]],
    'U': [[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[0,1,0]],
    'V': [[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[0,1,0]],
    'W': [[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,1,1],[1,0,1]],
    'X': [[1,0,1],[1,0,1],[0,1,0],[0,1,0],[0,1,0],[1,0,1],[1,0,1]],
    'Y': [[1,0,1],[1,0,1],[1,0,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0]],
    'Z': [[1,1,1],[0,0,1],[0,1,0],[0,1,0],[0,1,0],[1,0,0],[1,1,1]],
    ' ': [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],
}

COMMITS_PER_PIXEL = 4
BASE_COMMIT_FILE = ".art_base"


def text_to_columns(text):
    cols = []
    for i, ch in enumerate(text.upper()):
        glyph = FONT.get(ch, FONT[' '])
        width = len(glyph[0])
        for c in range(width):
            cols.append([bool(glyph[r][c]) for r in range(7)])
        if i < len(text) - 1:
            cols.append([False] * 7)
    return cols


def last_sunday(d):
    return d - timedelta(days=(d.weekday() + 1) % 7)


def commit_date(start_sunday, col_index, row_index):
    return start_sunday + timedelta(weeks=col_index, days=row_index)


def get_head():
    r = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def make_commit(d, msg="art"):
    iso = d.strftime("%Y-%m-%dT12:00:00")
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = iso
    env["GIT_COMMITTER_DATE"] = iso
    with open("art.txt", "a") as f:
        f.write(f"{d}\n")
    subprocess.run(["git", "add", "art.txt"], check=True, env=env)
    subprocess.run(["git", "commit", "-m", msg, "--allow-empty"],
                   check=True, env=env, capture_output=True)


def reset_art():
    if not os.path.exists(BASE_COMMIT_FILE):
        print("No saved base commit found — nothing to reset.")
        return False
    with open(BASE_COMMIT_FILE) as f:
        base = f.read().strip()
    print(f"Resetting to base commit {base[:8]}...")
    subprocess.run(["git", "reset", "--hard", base], check=True, capture_output=True)
    for path in ("art.txt", BASE_COMMIT_FILE):
        if os.path.exists(path):
            os.remove(path)
    print("Reset complete.")
    return True


def main():
    args = sys.argv[1:]
    do_reset = "--reset" in args
    year_arg = next((a for a in args if a.startswith("--year=")), None)
    start_year = int(year_arg.split("=")[1]) if year_arg else None
    text_args = [a for a in args if a != "--reset" and not a.startswith("--year=")]
    text = text_args[0] if text_args else "HELLO THERE"

    if do_reset:
        reset_art()
        if not text_args:
            print("Done. Run again with your new text, or push to apply changes.")
            return

    if not os.path.exists(BASE_COMMIT_FILE):
        head = get_head()
        with open(BASE_COMMIT_FILE, "w") as f:
            f.write(head if head else "empty")
        subprocess.run(["git", "add", BASE_COMMIT_FILE], check=True)
        subprocess.run(["git", "commit", "-m", "save base for art reset"],
                       check=True, capture_output=True)

    today = date.today()
    year = start_year if start_year else today.year
    year_start = date(year, 1, 1)
    start_sunday = last_sunday(year_start) + timedelta(weeks=2)

    cols = text_to_columns(text)
    total = sum(COMMITS_PER_PIXEL for col in cols for on in col if on)
    print(f'Generating {total} commits for "{text.upper()}"...')
    print(f"Graph starts: {start_sunday}  ({len(cols)} columns wide)\n")

    count = 0
    for ci, col in enumerate(cols):
        for ri, on in enumerate(col):
            if on:
                d = commit_date(start_sunday, ci, ri)
                for _ in range(COMMITS_PER_PIXEL):
                    make_commit(d)
                    count += 1
                    if count % 20 == 0:
                        print(f"  {count}/{total} commits done...")

    print(f"\nDone! {count} commits created.")
    print("Now run:  git push origin main --force")


if __name__ == "__main__":
    main()
