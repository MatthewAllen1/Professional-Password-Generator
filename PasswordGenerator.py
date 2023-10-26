import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
import random
import string

def generate_password(length, use_uppercase, use_lowercase, use_digits, use_special_chars):
    characters = ''
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_special_chars:
        characters += string.punctuation

    if not characters:
        raise ValueError("Select at least one character type.")

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def password_strength(password):
    strength = 0
    if any(char.islower() for char in password):
        strength += 1
    if any(char.isupper() for char in password):
        strength += 1
    if any(char.isdigit() for char in password):
        strength += 1
    if any(char in string.punctuation for char in password):
        strength += 1
    return strength

def generate_password_and_display():
    try:
        length = int(length_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Password length must be an integer.")
        return

    use_uppercase = uppercase_var.get()
    use_lowercase = lowercase_var.get()
    use_digits = digits_var.get()
    use_special_chars = special_chars_var.get()

    try:
        generated_password = generate_password(length, use_uppercase, use_lowercase, use_digits, use_special_chars)
        password_label.config(text=f"Generated Password: {generated_password}")
        strength = password_strength(generated_password)
        strength_label.config(text=f"Password Strength: {strength}/4")
        strength_progress.set(strength * 25)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def copy_to_clipboard():
    generated_password = password_label.cget("text")[18:]  # Extract the generated password from the label
    pyperclip.copy(generated_password)
    messagebox.showinfo("Copy Successful", "Password copied to clipboard")

app = tk.Tk()
app.title("Professional Password Generator")
app.geometry("400x500")

# Center the application on the screen
app.eval('tk::PlaceWindow . center')

style = ttk.Style()
style.configure("TButton", font=('Helvetica', 12))
style.configure("TCheckbutton", font=('Helvetica', 12))
style.configure("TLabel", font=('Helvetica', 12))
style.configure("Password.TLabel", font=('Helvetica', 14, 'bold'))

# Title label
title_label = ttk.Label(app, text="Password Generator", style="TLabel")
title_label.pack(pady=10)

# Frame for input elements
input_frame = ttk.Frame(app)
input_frame.pack(pady=10)

# Label and entry for password length
length_label = ttk.Label(input_frame, text="Password Length:")
length_label.grid(row=0, column=0, padx=5, pady=5)
length_entry = ttk.Entry(input_frame)
length_entry.grid(row=0, column=1, padx=5, pady=5)

# Checkboxes for character types with labels
uppercase_var = tk.BooleanVar()
lowercase_var = tk.BooleanVar()
digits_var = tk.BooleanVar()
special_chars_var = tk.BooleanVar()

uppercase_check = ttk.Checkbutton(input_frame, text="Uppercase", variable=uppercase_var, style="TCheckbutton")
lowercase_check = ttk.Checkbutton(input_frame, text="Lowercase", variable=lowercase_var, style="TCheckbutton")
digits_check = ttk.Checkbutton(input_frame, text="Include Digits", variable=digits_var, style="TCheckbutton")
special_chars_check = ttk.Checkbutton(input_frame, text="Special Characters", variable=special_chars_var, style="TCheckbutton")

uppercase_check.grid(row=1, column=0, padx=5, pady=5, sticky="w")
lowercase_check.grid(row=2, column=0, padx=5, pady=5, sticky="w")
digits_check.grid(row=3, column=0, padx=5, pady=5, sticky="w")
special_chars_check.grid(row=4, column=0, padx=5, pady=5, sticky="w")

# Generate Password button
generate_button = ttk.Button(app, text="Generate Password", command=generate_password_and_display, style="TButton")
generate_button.pack(pady=10)

# Password display label
password_label = ttk.Label(app, text="", style="Password.TLabel")
password_label.pack()

# Password strength label
strength_label = ttk.Label(app, text="", style="TLabel")
strength_label.pack()

# Progress bar to show password strength
strength_progress = tk.IntVar()
strength_bar = ttk.Progressbar(app, variable=strength_progress, maximum=100, length=200)
strength_bar.pack(pady=10)

# Copy to Clipboard button
copy_button = ttk.Button(app, text="Copy to Clipboard", command=copy_to_clipboard, style="TButton")
copy_button.pack()

app.mainloop()
