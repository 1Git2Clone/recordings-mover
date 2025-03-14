# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import os
import sys
import shutil

import time

from datetime import datetime

from argparse import ArgumentParser, Namespace

from pathlib import Path

TEXT_WIDTH: int = 80
TEXT_FILL: str = "*"

RECORDINGS_ORIGIN_DIR: Path = Path(
    os.environ.get("RECORDINGS_ORIGIN_DIR") or Path.cwd()
)

SCRIPT_DIR: Path = Path(__file__).absolute().parent

MONTHS: list[str] = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def make_month_dir(month_dir: Path) -> None:
    print(
        " MAKING ".center(TEXT_WIDTH, TEXT_FILL),
        f"{month_dir}",
        sep="\n",
    )
    print(TEXT_FILL * TEXT_WIDTH)
    try:
        month_dir.mkdir(parents=True)
        print("DONE".center(TEXT_WIDTH))
    except FileExistsError:
        print(
            "Dicrectory:",
            f"  -  `{month_dir}`",
            "already exists. Skipping...",
            sep="\n",
        )
    print(TEXT_FILL * TEXT_WIDTH)


def move_recordings(
    month_pos: int, year: int, year_dir: Path, current_month: str
) -> None:
    month_formatted_idx: str = f"{(month_pos - 1):02}"
    target_month_str: str = str(year) + "-" + month_formatted_idx
    print(f"Current month: {month_formatted_idx}-{current_month}")
    month_dir: Path = Path(year_dir) / current_month

    for recording_filename in RECORDINGS_ORIGIN_DIR.iterdir():
        if target_month_str not in str(recording_filename):
            continue

        full_recording_path: Path = Path(RECORDINGS_ORIGIN_DIR) / recording_filename
        target_path: Path = Path(month_dir) / recording_filename
        print(
            "MOVING".center(TEXT_WIDTH, "-"),
            f"{full_recording_path}",
            "to",
            f"{target_path}",
            sep="\n",
        )
        shutil.move(full_recording_path, target_path)


def main(year: int, month: int | None) -> None:
    if year > datetime.now().year:
        return None

    print("Starting...")
    start: float = time.perf_counter()

    year_dir: Path = RECORDINGS_ORIGIN_DIR / str(year)
    os.makedirs(year_dir, exist_ok=True)

    if month is not None and month in range(1, 13):
        month_idx = month - 1
        month_dir = Path(year_dir) / f"{month:02}-{MONTHS[month_idx]}"
        make_month_dir(month_dir=month_dir)
        move_recordings(
            month_pos=month,
            year=year,
            year_dir=year_dir,
            current_month=MONTHS[month_idx],
        )
        print(f"All videos from {MONTHS[month_idx]} {year} are moved over!")
    else:
        for month_idx, current_month in enumerate(MONTHS, 1):
            month_dir = Path(year_dir) / f"{month_idx:02}-{current_month}"

            make_month_dir(month_dir=month_dir)

            move_recordings(
                month_pos=month_idx + 1,
                year=year,
                year_dir=year_dir,
                current_month=current_month,
            )
            print(f"All videos from {current_month} {year} are moved over!")
        print(f"All videos from all months of {year} are moved over!")

    elapsed: float = time.perf_counter() - start
    print(f"Finished in: {elapsed:.2f} seconds")

    print("Exiting!...")


if __name__ == "__main__":
    if not RECORDINGS_ORIGIN_DIR.exists:
        print(
            f"The recordings directory: '{RECORDINGS_ORIGIN_DIR}' DOESN'T"
            + "exist. Make sure to hardcode it properly or use a correct"
            + "RECORDINGS_ORIGIN_DIR environment variable."
        )
        sys.exit(1)

    parser: ArgumentParser = ArgumentParser(
        prog="move_recordings.py",
        description="Moves the OBS recordings from a specific month over from"
        + " one hardcoded directory to the script directory.",
    )
    parser.add_argument(
        "--year",
        "-y",
        type=int,
        default=datetime.now().year,
        required=False,
        help=("Enter the year as a number directly."),
    )
    parser.add_argument(
        "--month",
        "-m",
        type=int,
        default=None,
        required=False,
        help=("Enter the month as a number directly. Does every month by default!"),
    )

    args: Namespace = parser.parse_args()

    try:
        main(year=args.year, month=args.month)
    except KeyboardInterrupt:
        sys.exit(1)
    except EOFError:
        sys.exit(1)
