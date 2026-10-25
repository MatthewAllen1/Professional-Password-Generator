# Local Secure Password Generator

[![Python tests](https://github.com/MatthewAllen1/Professional-Password-Generator/actions/workflows/python-tests.yml/badge.svg)](https://github.com/MatthewAllen1/Professional-Password-Generator/actions/workflows/python-tests.yml)

A [CI-verified](https://github.com/MatthewAllen1/Professional-Password-Generator/actions) personal Python security engineering exercise. See [security policy](./SECURITY.md) and [license](./LICENSE).

A small, standalone Python desktop application that generates random passwords locally using the standard-library `secrets` module. Intended as a learning/demo project rather than a replacement for a vetted password manager.

## Security properties

- Uses cryptographically secure randomness via `secrets.choice` and `secrets.randbelow`, not `random`.
- Guarantees at least one character from each selected category.
- Requires a length from 12 to 128 characters and at least one category.
- Makes no network requests and writes no generated passwords to disk.
- No third-party dependencies; desktop GUI uses `tkinter`.
- Clipboard copies may remain readable by other applications. Clear your clipboard after use.

## Run

Requires Python 3.10+ and Tk support. From the repository root:

```bash
python PasswordGenerator.py
```

On some Linux distributions, install the OS-provided `python3-tk` package.

## Test

```bash
python -m unittest discover -s tests -v
```

## Limitations and threat model

This tool assumes the local operating system is trusted. It does **not** protect against malware, clipboard monitors, screen captures, compromised desktops, or password reuse. Passwords are visible in the GUI. A password manager remains the preferred way to create and store account credentials.

## What changed in the security refresh

Replaced predictable pseudo-random generation, ensured requested category coverage, added input validation, removed the `pyperclip` dependency, moved GUI initialization behind `main()` for testability, and documented realistic security limitations.
