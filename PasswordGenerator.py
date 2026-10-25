"""Local password generator using cryptographically secure randomness.

No network calls, disk writes, or password telemetry.
Clipboard contents can be accessed by other local applications.
"""
import math
import secrets
import string
import tkinter as tk
from tkinter import messagebox, ttk

MIN_LENGTH = 12
MAX_LENGTH = 128

CHARACTER_GROUPS = (
    ("Uppercase", string.ascii_uppercase),
    ("Lowercase", string.ascii_lowercase),
    ("Digits", string.digits),
    ("Symbols", string.punctuation),
)


def generate_password(length: int, use_uppercase: bool, use_lowercase: bool,
                      use_digits: bool, use_special_chars: bool) -> str:
    """Generate a password containing at least one of each enabled category."""
    if isinstance(length, bool) or not isinstance(length, int):
        raise ValueError("Length must be an integer.")
    if not MIN_LENGTH <= length <= MAX_LENGTH:
        raise ValueError(f"Length must be between {MIN_LENGTH} and {MAX_LENGTH}.")

    enabled = (use_uppercase, use_lowercase, use_digits, use_special_chars)
    groups = [chars for selected, (_, chars) in zip(enabled, CHARACTER_GROUPS) if selected]
    if not groups:
        raise ValueError("Select at least one character category.")

    alphabet = "".join(groups)
    characters = [secrets.choice(group) for group in groups]
    characters.extend(secrets.choice(alphabet) for _ in range(length - len(characters)))

    # Fisher-Yates shuffle with rejection-sampled secure random indices.
    for i in range(len(characters) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        characters[i], characters[j] = characters[j], characters[i]
    return "".join(characters)


def entropy_lower_bound(length: int, enabled: tuple[bool, bool, bool, bool]) -> float:
    """Conservative informational estimate; not a password strength guarantee."""
    groups = [chars for selected, (_, chars) in zip(enabled, CHARACTER_GROUPS) if selected]
    if not groups:
        return 0.0
    # Guaranteed category selections make this a rough estimate, not exact entropy.
    return max(0.0, (length - len(groups)) * math.log2(len("".join(groups))))


def main() -> None:
    app = tk.Tk()
    app.title("Local Secure Password Generator")
    app.geometry("600x390")
    app.resizable(True, False)

    frame = ttk.Frame(app, padding=18)
    frame.pack(fill="both", expand=True)
    ttk.Label(frame, text="Local Password Generator", font=("Arial", 17, "bold")).pack(anchor="w")
    ttk.Label(frame, text="Generated locally using Python's secrets module.").pack(anchor="w", pady=(3, 12))

    controls = ttk.Frame(frame)
    controls.pack(fill="x")
    ttk.Label(controls, text="Length (12–128):").pack(side="left")
    length_var = tk.StringVar(value="20")
    ttk.Entry(controls, textvariable=length_var, width=7).pack(side="left", padx=8)

    vars_ = [tk.BooleanVar(value=True) for _ in CHARACTER_GROUPS]
    for (label, _), selected in zip(CHARACTER_GROUPS, vars_):
        ttk.Checkbutton(frame, text=label, variable=selected).pack(anchor="w")

    generated_var = tk.StringVar()
    status_var = tk.StringVar(value="Password has not been generated.")
    ttk.Entry(frame, textvariable=generated_var, state="readonly", width=70).pack(fill="x", pady=(12, 4))
    ttk.Label(frame, textvariable=status_var, wraplength=560).pack(anchor="w")

    def generate() -> None:
        try:
            length = int(length_var.get())
            selections = tuple(v.get() for v in vars_)
            password = generate_password(length, *selections)
        except ValueError as exc:
            messagebox.showerror("Invalid options", str(exc))
            return
        generated_var.set(password)
        status_var.set(
            f"Generated {len(password)} characters. "
            "Keep passwords private; clipboard copies may remain accessible to other apps."
        )

    def copy_password() -> None:
        if not generated_var.get():
            messagebox.showwarning("Nothing to copy", "Generate a password first.")
            return
        app.clipboard_clear()
        app.clipboard_append(generated_var.get())
        app.update()
        status_var.set("Copied to clipboard. Clear clipboard after using your password.")

    buttons = ttk.Frame(frame)
    buttons.pack(anchor="w", pady=12)
    ttk.Button(buttons, text="Generate", command=generate).pack(side="left")
    ttk.Button(buttons, text="Copy", command=copy_password).pack(side="left", padx=8)
    ttk.Label(frame, text="Never reuse passwords. Use a reputable password manager for storage.").pack(anchor="w")
    app.mainloop()


if __name__ == "__main__":
    main()
