# OUTD-2-ACLOG

Converts OutD and HAMRS ADIF log files to ACLOG (N3FJP) or qrz.com ADI parsable log files.

![OUTD-2-ACLOG Workflow](outd2aclog/static/OUTD2ACLOG_Workflow.png)

## How it works

![OUTD-2-ACLOG Mac Screenshot](outd2aclog/static/outd2aclog_mac_screenshot.png)

<h3>Steps:</h3>

1. Click "Browse Files" and select the OutD ADIF log file
2. Enter your 4 digit gridsquare in the "My 4-Digit Gridsquare" field
3. The "Comment" field works in three different ways <br>
    * If you write anything in this field, outd2aclog will overwrite all COMMENT fields in the ADI with the value entered. <br>
    * If you enabled OutD QSPMSG, leaving this field blank will convert all QSPMSG fields to COMMENT fields in the ADI. <br>
    * If you disabled OutD QSPMSG, leaving this field blank will auto-generate a comment with the following format: <br>
        * SOTA Activator log entry: "SOTA \[my summit reference\]" <br>
        * SOTA Chaser log entry "SOTA CHASE \[other summit reference\]" <br>
        * SOTA S2S log entry: "SOTA \[summit reference\] - S2S - \[other summit reference\]" <br>
4. Click the "Convert" button to create the converted log file! Note: Outd2aclog will generate a new ADI log file which follows the naming convention of the original OutD filename (i.e. - "OutdLog-YYYYMMDD.adif" will generate "ACLOG-YYYYMMDD.adi")

## Build Dependencies

OUTD-2-ACLOG is typically used on Windows machines since ACLOG is a Windows-only program, but it can run on any machine
which supports Python.

1. [Python](https://www.python.org/downloads/)
2. [Pip](https://pip.pypa.io/en/stable/installing/)
3. Tkinter
4. Tkmacosx

```shell
pip install -r requirements.txt
```

4. (OPTIONAL) To build an executable you will need [Pyinstaller](https://www.pyinstaller.org/downloads.html)

```shell
pip install -r requirements-build.txt
```

## Run

As a Script:

```shell
python launch.py
```

As a Python Module:

```shell
python -m outd2aclog
```

## Build Executable (Mac, Windows, Linux)

Easy mode:

```shell
python setup.py build
```

Manual build:

```shell
pyinstaller --name outd2aclog --onefile --noconsole --add-data outd2aclog\static\*;outd2aclog\static\ --icon outd2aclog\static\outd2aclogicon.ico launch.py
```
