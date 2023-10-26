import random
import string
import tkinter as tk
from tkinter import messagebox
import pyperclip

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

def generate_password_and_display():
    try:
        password_length = int(length_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Password length must be an integer.")
        return

    use_uppercase = uppercase_var.get()
    use_lowercase = lowercase_var.get()
    use_digits = digits_var.get()
    use_special_chars = special_chars_var.get()

    try:
        generated_password = generate_password(password_length, use_uppercase, use_lowercase, use_digits, use_special_chars)
        password_label.config(text=f"Generated Password: {generated_password}")
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def copy_to_clipboard():
    generated_password = password_label.cget("text")[18:]  # Extract the generated password from the label
    pyperclip.copy(generated_password)
    messagebox.showinfo("Copied to Clipboard", "Password copied to clipboard.")

app = tk.Tk()
app.title("Professional Password Generator")
app.geometry("400x400")

font = ('Helvetica', 12)

# Label and entry for password length
length_label = tk.Label(app, text="Password Length:", font=font)
length_label.pack()
length_entry = tk.Entry(app, font=font)
length_entry.pack()

# Checkboxes for character types
uppercase_var = tk.BooleanVar()
lowercase_var = tk.BooleanVar()
digits_var = tk.BooleanVar()
special_chars_var = tk.BooleanVar()

uppercase_check = tk.Checkbutton(app, text="Uppercase", variable=uppercase_var, font=font)
lowercase_check = tk.Checkbutton(app, text="Lowercase", variable=lowercase_var, font=font)
digits_check = tk.Checkbutton(app, text="Digits", variable=digits_var, font=font)
special_chars_check = tk.Checkbutton(app, text="Special Characters", variable=special_chars_var, font=font)

uppercase_check.pack()
lowercase_check.pack()
digits_check.pack()
special_chars_check.pack()

# Generate Password button
generate_button = tk.Button(app, text="Generate Password", command=generate_password_and_display, font=font)
generate_button.pack()

# Password display label
password_label = tk.Label(app, text="", font=('Helvetica', 14, 'bold'))
password_label.pack()

# Copy to Clipboard button
copy_button = tk.Button(app, text="Copy to Clipboard", command=copy_to_clipboard, font=font)
copy_button.pack()

app.mainloop()
