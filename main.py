import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import math
import pyperclip  # For clipboard functionality

class FortiPass:
    def __init__(self, root):
        self.root = root
        self.root.title("FortiPass - Secure Password Generator")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        # Theme Toggle
        self.dark_mode = True
        self.style = ttk.Style()

        # Title Label
        ttk.Label(root, text="FortiPass - Secure Password Generator", font=("Arial", 14, "bold")).pack(pady=10)

        # Password Length
        ttk.Label(root, text="Password Length:", font=("Arial", 12)).pack(pady=5)
        self.length_var = tk.IntVar(value=12)
        ttk.Entry(root, textvariable=self.length_var, width=5).pack()

        # Checkboxes for password rules
        self.include_upper = tk.BooleanVar(value=True)
        self.include_digits = tk.BooleanVar(value=True)
        self.include_special = tk.BooleanVar(value=True)

        ttk.Checkbutton(root, text="Include Uppercase Letters", variable=self.include_upper).pack(anchor="w", padx=50)
        ttk.Checkbutton(root, text="Include Digits (0-9)", variable=self.include_digits).pack(anchor="w", padx=50)
        ttk.Checkbutton(root, text="Include Special Characters (!@#$...)", variable=self.include_special).pack(anchor="w", padx=50)

        # Generate Button
        ttk.Button(root, text="Generate Password", command=self.generate_password).pack(pady=10)

        # Display Password
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(root, textvariable=self.password_var, font=("Arial", 14), justify="center", width=30, state="readonly")
        self.password_entry.pack(pady=5)

        # Copy Button
        ttk.Button(root, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(pady=5)

        # Password Strength
        self.strength_label = ttk.Label(root, text="Password Strength: -", font=("Arial", 12, "bold"))
        self.strength_label.pack(pady=5)

        # Theme Toggle Button
        ttk.Button(root, text="Toggle Theme", command=self.toggle_theme).pack(pady=10)

        # Apply Theme
        self.apply_theme()

    def generate_password(self):
        """Generates a secure password based on user preferences."""
        length = self.length_var.get()
        if length < 6:
            messagebox.showerror("Error", "Password length must be at least 6 characters!")
            return

        char_set = string.ascii_lowercase
        if self.include_upper.get():
            char_set += string.ascii_uppercase
        if self.include_digits.get():
            char_set += string.digits
        if self.include_special.get():
            char_set += string.punctuation

        password = ''.join(random.choice(char_set) for _ in range(length))
        self.password_var.set(password)

        self.analyze_strength(password)

    def analyze_strength(self, password):
        """Calculates the password strength based on entropy."""
        char_set_size = len(set(password))
        entropy = len(password) * math.log2(char_set_size)

        if entropy < 40:
            strength = "Weak 🔴"
            color = "red"
        elif entropy < 60:
            strength = "Medium 🟡"
            color = "orange"
        else:
            strength = "Strong 🟢"
            color = "green"

        self.strength_label.config(text=f"Password Strength: {strength}", foreground=color)

    def copy_to_clipboard(self):
        """Copies the generated password to clipboard."""
        pyperclip.copy(self.password_var.get())
        messagebox.showinfo("Copied", "Password copied to clipboard!")

    def apply_theme(self):
        """Applies the selected theme (Dark/Light)."""
        if self.dark_mode:
            bg_color = "#2b2b2b"
            fg_color = "#ffffff"
            entry_bg = "#1c1c1c"
            entry_fg = "#ffffff"
        else:
            bg_color = "#ffffff"
            fg_color = "#000000"
            entry_bg = "#f5f5f5"
            entry_fg = "#000000"

        # Apply window background
        self.root.config(bg=bg_color)

        # Apply style to ttk.Entry widget
        self.style.configure("TEntry", fieldbackground=entry_bg, foreground=entry_fg)

    def toggle_theme(self):
        """Toggles between Dark and Light mode."""
        self.dark_mode = not self.dark_mode
        self.apply_theme()

# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    FortiPass(root)
    root.mainloop()
