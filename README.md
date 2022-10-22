# appsel

**appsel** (APP SELector) is a file types manager for Linux desktops.

I wrote this tool because the default applications selectors in Linux aren't as powerful as what I've seen on Windows. Specifically, many of them only allow setting a few apps (web browser, terminal, mail reader) and not the full palette of programs (text editor, media player, etc.).

## Features

- Set default application for a MIME type
- Add / remove custom associations for MIME types
- Enable / disable associations for MIME types
- Set / unset defaults by application

## Install

This app requires Python 3, PyQt5, and python-xdg. On Debian/Ubuntu, this is `apt-get install python3-pyqt5 python3-xdg`.

After installing these dependencies, just clone the repo and run `main.py`.

## License

GPLv3
