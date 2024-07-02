# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import os
import sys
import shutil

import time

from datetime import datetime

from argparse import ArgumentParser

# This one is hardcoded yea. At least you can change is relatively easily.
# Still better than manually typing it out all the time...
RECORDINGS_ORIGIN_DIR: str = os.getenv(
    "RECORDINGS_ORIGIN_DIR", "/home/hutao/Videos/Recordings/"
)

# Also serves as the target directories pivot. It's SCRIPT_DIR followed by the
# corresponding month.
SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))

# If no month argument is specified - do all of them.
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


def make_month_dir(month_dir: str):
    print(f"Making: {month_dir}")
    try:
        os.makedirs(month_dir)
        print("DONE!")
    except FileExistsError:
        print(f"Dicrectory: '{month_dir}' already exists. Skipping...")


def move_recordings(month_pos: int, year: int, year_dir: str, current_month: str):
    str_month_pos: str
    if month_pos < 10:
        str_month_pos = "0" + str(month_pos)
    else:
        str_month_pos = str(month_pos)
    # Example: '2024-07' (OBS saves recordings in that format)
    target_month_str = str(year) + "-" + str_month_pos
    print(f"TARGET sequence: {target_month_str}")
    # SCRIPT_DIR/2024/July
    month_dir = os.path.join(year_dir, current_month)

    for recording_filename in os.listdir(RECORDINGS_ORIGIN_DIR):
        if target_month_str not in recording_filename:
            continue

        full_recording_path = os.path.join(RECORDINGS_ORIGIN_DIR, recording_filename)
        target_path = os.path.join(month_dir, recording_filename)
        print(f"Moving {full_recording_path} to {target_path}")
        shutil.move(full_recording_path, target_path)


def main(year: int, month: int | None):
    if year > datetime.now().year:
        return

    print("Starting...")
    start = time.perf_counter()

    year_dir = os.path.join(SCRIPT_DIR, str(year))
    os.makedirs(year_dir, exist_ok=True)

    if month is not None and month in range(1, 13):
        month_dir = os.path.join(year_dir, MONTHS[month - 1])
        make_month_dir(month_dir=month_dir)
        move_recordings(
            month_pos=month,
            year=year,
            year_dir=year_dir,
            # I hate off by one errors.
            current_month=MONTHS[month - 1],
        )
        print(f"All videos from {MONTHS[month - 1]} are moved over!")
    else:
        for month_idx, current_month in enumerate(MONTHS):
            month_dir = os.path.join(year_dir, current_month)

            make_month_dir(month_dir=month_dir)

            move_recordings(
                month_pos=month_idx + 1,
                year=year,
                year_dir=year_dir,
                current_month=current_month,
            )
            print(f"All videos from {current_month} are moved over!")
        print("All videos from all months are moved over!")

    elapsed = time.perf_counter() - start
    print(f"Finished in: {elapsed:.2f} seconds")

    print("Exiting!...")

    return


if __name__ == "__main__":
    if not os.path.exists(RECORDINGS_ORIGIN_DIR):
        print(
            f"The recordings directory: '{RECORDINGS_ORIGIN_DIR}' DOESN'T"
            + "exist. Make sure to hardcode it properly or use a correct"
            + "RECORDINGS_ORIGIN_DIR environment variable."
        )
        sys.exit(1)

    parser = ArgumentParser(
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

    args = parser.parse_args()

    try:
        main(year=args.year, month=args.month)
    except KeyboardInterrupt:
        sys.exit(1)
    except EOFError:
        sys.exit(1)
