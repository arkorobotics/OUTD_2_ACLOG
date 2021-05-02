# OUTD-2-ACLOG

Converts OutD ADIF log files to ACLOG (N3FJP) ADIF parseable log files

## Build Dependencies

OUTD-2-ACLOG is typically used on Windows machines since ACLOG is a Windows-only program, but it can run on any machine which supports Python.

1.  [Python](https://www.python.org/downloads/) 
2. [Pip](https://pip.pypa.io/en/stable/installing/)
3. Tkinter
```
pip install tk
```
4. (OPTIONAL) To build an exe for Windows, you will need [Pyinstaller](https://www.pyinstaller.org/downloads.html)

## Run
```
> python outd2aclog.py
```

## Build Window EXE

```
pyinstaller --onefile --noconsole --icon outd2aclogicon.ico outd2aclog.py
```