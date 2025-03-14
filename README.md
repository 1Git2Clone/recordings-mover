# Recordings mover

[![GH_Build Icon]][GH_Build Status]&emsp;[![License Icon]][LICENSE]

[GH_Build Icon]: https://img.shields.io/github/actions/workflow/status/1git2clone/recordings-mover/pylint.yml?branch=main
[GH_Build Status]: https://github.com/1git2clone/recordings-mover/actions?query=branch%3Amaster
[License Icon]: https://img.shields.io/badge/license-MIT-blue.svg
[LICENSE]: LICENSE

<!-- markdownlint-disable MD033 -->
<p>
  <img
    height="50px"
    src="https://codeberg.org/1Kill2Steal/skill-icons/raw/branch/main/icons/Python-Dark.svg"
    alt="Python"
  />
</p>
<!-- markdownlint-enable MD033 -->

<!-- markdownlint-disable MD028 -->

> [!IMPORTANT]
> This script was mainly done for OBS-styled recordings but it can be used on
> any type of recordings which have files saved in the following format:
> `YYYY-MM`.

> [!NOTE]
> The `YYYY-MM` part can be **anywhere** in the file name, it doesn't
> particularly restrain the file from not having anything before and/or after
> the year and month. Think of it as running:

```sh
mv origin_dir/*YYYY-MM* repo_dir/year/month/
```

<!-- markdownlint-enable MD028 -->

It gets the specified year (default: current year) and makes a directory with
it in this directory and makes directories for all months in it (or for a
single specified month if you use the `--month` flag).

This is an example of how the file structure is laid out after finishing the
usage of the script:

```txt
REPO
├── 2025
│   ├── 01-January
│   ├── 02-February
│   ├── 03-March
│   ├── 04-April
│   ├── 05-May
│   ├── 06-June
│   ├── 07-July
│   ├── 08-August
│   ├── 09-September
│   ├── 10-October
│   ├── 11-November
│   └── 12-December
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
RECORDINGS_ORIGIN_DIR="/your/recordings/source/path" python3 move_recordings.py
```

Optional: you can specify a specific year and/or month as numbers for it as well:

```sh
RECORDINGS_ORIGIN_DIR="/your/recordings/source/path" \
python3 move_recordings.py -y=2023 -m=1 # January
```

^ The Recordings paths work with Windows directories as well. Here's a
PowerShell example:

```powershell
$env:RECORDINGS_ORIGIN_DIR="D:\Your\Recordings\Source\Path"
python3 move_recordings.py
```

> [!NOTE]
> If you're tired of setting that environment variable each time you can either
> use it in your `.profile` file or change the hard-coded alternative in the
> source code (At the top of the [move_recordings.py](./move_recordings.py)
> file).

The defaults are:

- Year: current year

- Month: All months
