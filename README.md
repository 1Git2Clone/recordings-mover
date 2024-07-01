# Recordings mover

[![GH_Build Icon]][GH_Build Status]&emsp;[![License Icon]][LICENSE]

[GH_Build Icon]: https://img.shields.io/github/actions/workflow/status/1git2clone/recordings-mover/pylint.yml?branch=main
[GH_Build Status]: https://github.com/1git2clone/recordings-mover/actions?query=branch%3Amaster
[License Icon]: https://img.shields.io/badge/license-MIT-blue.svg
[LICENSE]: LICENSE

> [!IMPORTANT]
> This script was mainly done for OBS-styled recordings but it can be used on
> any type of recordings which have files saved in the following format:
> `YYYY-MM`.

It gets the specified year (default: current year) and makes a directory with
it in this directory and makes directories for all months in it (or for a
single specified month if you use the `--month` flag).

This is an example of how the file structure is laid out after finishing the
usage of the script:

```txt
REPO
├── .git
├── 2023
│   ├── April
│   ├── August
│   ├── December
│   ├── February
│   ├── January
│   ├── July
│   ├── June
│   ├── March
│   ├── May
│   ├── November
│   ├── October
│   └── September
├── 2024
│   ├── April
│   ├── August
│   ├── December
│   ├── February
│   ├── January
│   ├── July
│   ├── June
│   ├── March
│   ├── May
│   ├── November
│   ├── October
│   └── September
├── .gitignore
├── README.md
└── move_recordings.py
```

## Setting up

First of all, you need to configure the `RECORDINGS_ORIGIN_DIR` environment
variable. You can set it as a shell environment variable or change the
hard-coded one from the top of [the source file](move_recordings.py).

After you set the RECORDINGS_ORIGIN_DIR, you need to run the script with the
year and month as optional flags.

> [!NOTE]
> Despite the month and year flags **not** being mandatory, having your files
> following the `YYYY-MM` naming convention IS required in order for the script
> to work properly! Any months with digits less than 2 have to have a trialing
> zero behind them too. If you're using OBS then this is the default recording
> output naming convention anyway.

## Usage

```sh
py move_recordings.py
```

Optional but you can specify a specific year and/or month as numbers for it as well:

```sh
py move_recordings.py -y=2023 -m=1 # January
```

The defaults are:

- Year: current year

- Month: All months from the current year
