# Carbon-Share

Carbon-Share is a local-network file sharing tool built with:

- `Flask` for the HTTP server and browser UI
- `GTK 3` for the desktop QR window
- `pam` for local user authentication
- `xclip`, `gio trash`, and `notify-send` for desktop integration

The app starts a local web server, detects the machine's LAN IP, and shows a QR code that points other devices to the share URL.

## Project Layout

- `Code/Share.py`: main entry point
- `Code/server.py`: Flask routes and file operations
- `Code/directShare.py`: GTK QR-code window
- `Code/data.py`: shared configuration and helper functions
- `Code/bridge.py`: exposes the shared `data` module without circular imports
- `Code/Templates/`: HTML templates used by Flask
- `Code/static/`: CSS, icons, fonts, and background assets

## How It Works

1. `Code/Share.py` creates the desktop app wrapper.
2. A background thread runs the Flask server on port `5000`.
3. Another background thread checks the current LAN IP every 2 seconds.
4. When the IP changes, the GTK window updates the button label and QR code.
5. A browser client opens the shared URL, authenticates with the machine user's PAM credentials, and then browses, downloads, uploads, deletes, or opens files.

## Main Features

- QR code for quick access from another device
- Browser-based file browsing
- File download and upload
- Send files inline through `/media/...`
- Delete files through the desktop trash
- Copy text to the host clipboard
- Session gate on most Flask routes

## Runtime Requirements

The code assumes a Linux desktop with these tools available:

- `python3`
- `Flask`
- `PyGObject` / `gi`
- `qrcode`
- `python-pam`
- `xclip`
- `gio`
- `notify-send`

GTK 3 is required because `directShare.py` explicitly loads `Gtk 3.0`.

## Running The App

Run the main script:

```bash
python3 Code/Share.py
```

Expected behavior:

- the Flask server starts on port `5000`
- the terminal logs the active URL
- a small GTK window appears
- the window shows the current share URL and a QR code

## Authentication

Login is handled in `Code/server.py` by `login_route()` and validated through `data.verifyPass()`.

- `username`: local system username
- `key`: local system password

The code uses PAM, so this is not an app-specific account system.

## Important Routes

- `GET /`: login page or main file browser
- `POST /login`: authenticate and create session
- `GET /logout`: clear session
- `GET /files/<path>`: list directory contents
- `GET /media/<path>`: open a file directly
- `GET /download/<path>`: download a file
- `POST /upload`: upload files into a destination path
- `GET /delete/<path>`: move a file to trash
- `POST /clipboard/copy`: copy base64 text into the host clipboard
- `GET /back/<path>`: move to parent directory listing
- `GET /url/<path>`: return metadata for a file path
- `GET /about`: return device name
- `GET /action/<command>`: run a basic host action, currently `lock` or `off`

## Data Files

The app may create `share.json` in the project directory. It stores:

- `session`: saved session value returned by `data.getPass()`
- `PAIRS`: reserved list for pairing support

The pairing logic exists only as partial or disabled code right now.

## Current Code Notes

- `server.py` runs host actions through `/action/<command>` and currently supports `lock` and `off`
- `data.savePass()` references `session` without importing Flask session state, so that path is incomplete
- `data.addPAIR()` returns immediately, so pairing is effectively disabled.
- hidden files are skipped in directory listings
- uploads are saved directly to the provided destination path

## Documentation

Detailed logic notes are in `notes.txt`. That file explains the flow of control, globals, class members, and each function in the Python modules.
