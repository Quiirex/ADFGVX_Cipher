import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np


class HillCipher:
    def __init__(self):
        self.key = None

    def set_key(self, key):
        self.key = key

    def encrypt(self, text):
        if self.key is not None:
            text = text.upper().replace(" ", "")
            text_length = len(text)
            key_size = len(self.key)

            if text_length % key_size != 0:
                raise ValueError("Text length must be a multiple of the key size.")

            encrypted_text = ""
            for i in range(0, text_length, key_size):
                plaintext_block = np.array(
                    [ord(char) - ord("A") for char in text[i : i + key_size]]
                )
                ciphertext_block = np.dot(self.key, plaintext_block) % 26
                encrypted_text += "".join([chr(c + ord("A")) for c in ciphertext_block])
            return encrypted_text
        else:
            raise ValueError("Please set a key before encrypting.")

    def decrypt(self, encrypted_text):
        if self.key is not None:
            encrypted_text = encrypted_text.upper().replace(" ", "")
            encrypted_text_length = len(encrypted_text)
            key_size = len(self.key)
            if encrypted_text_length % key_size != 0:
                raise ValueError("Text length must be a multiple of the key size.")

            decrypted_text = ""
            inverse_key = np.linalg.inv(self.key)
            for i in range(0, encrypted_text_length, key_size):
                ciphertext_block = np.array(
                    [ord(char) - ord("A") for char in encrypted_text[i : i + key_size]]
                )
                plaintext_block = np.dot(inverse_key, ciphertext_block) % 26
                decrypted_text += "".join(
                    [chr(int(c) + ord("A")) for c in plaintext_block]
                )
            return decrypted_text
        else:
            raise ValueError("Please set a key before decrypting.")


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hill Cipher")
        self.cipher = HillCipher()

        # region input frame
        self.input_frame = tk.Frame(root)
        self.input_frame.grid(row=0, column=0, padx=20)

        self.text_label = tk.Label(self.input_frame, text="Text:")
        self.text_label.grid(row=0, column=0)
        self.input_box = tk.Text(self.input_frame, width=100, height=12)
        self.input_box.grid(row=1, column=0)
        self.save_text_button = tk.Button(
            self.input_frame, text="Save as..", command=self.save_input, width=5
        )
        self.save_text_button.grid(row=1, column=1)

        self.key_label = tk.Label(self.input_frame, text="Key (NxN matrix):")
        self.key_label.grid(row=2, column=0)
        self.key_entry = tk.Text(self.input_frame, width=100, height=12)
        self.key_entry.grid(row=3, column=0)

        self.output_label = tk.Label(self.input_frame, text="Output:")
        self.output_label.grid(row=4, column=0)
        self.output_box = tk.Text(self.input_frame, width=100, height=12)
        self.output_box.grid(row=5, column=0)
        self.save_output_button = tk.Button(
            self.input_frame, text="Save as..", command=self.save_output, width=5
        )
        self.save_output_button.grid(row=5, column=1)
        # endregion

        # region button frame
        self.button_frame = tk.Frame(root)
        self.button_frame.grid(row=4, column=0, padx=20, pady=20)

        self.load_file_button = tk.Button(
            self.button_frame,
            text="Open text file",
            command=self.load_text_from_file,
            width=10,
        )
        self.load_file_button.grid(row=1, column=0)

        self.encrypt_button = tk.Button(
            self.button_frame, text="Encrypt", command=self.encrypt_text, width=10
        )
        self.encrypt_button.grid(row=1, column=1)

        self.decrypt_button = tk.Button(
            self.button_frame, text="Decrypt", command=self.decrypt_text, width=10
        )
        self.decrypt_button.grid(row=1, column=2)
        # endregion

        self.input_text = ""

    def load_text_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                self.input_text = file.read()
                self.input_box.delete("1.0", tk.END)
                self.input_box.insert(tk.END, self.input_text.strip())
                self.input_text = ""
        else:
            messagebox.showerror("Error", "No file selected!")

    def encrypt_text(self):
        text = (
            self.input_box.get("1.0", tk.END)
            if not self.input_text
            else self.input_text
        ).strip()
        key = self.key_entry.get("1.0", tk.END).strip()

        # Parse the key matrix from the input
        key = key.split("\n")
        key = [list(map(int, row.split())) for row in key]
        key_matrix = np.array(key)

        self.cipher.set_key(key_matrix)
        encrypted_text = self.cipher.encrypt(text)
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, encrypted_text.strip())
        self.input_text = ""

    def decrypt_text(self):
        text = (
            self.input_box.get("1.0", tk.END)
            if not self.input_text
            else self.input_text
        ).strip()
        key = self.key_entry.get("1.0", tk.END).strip()

        # Parse the key matrix from the input
        key = key.split("\n")
        key = [list(map(int, row.split())) for row in key]
        key_matrix = np.array(key)

        self.cipher.set_key(key_matrix)
        decrypted_text = self.cipher.decrypt(text)
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, decrypted_text.strip())
        self.input_text = ""

    def save_input(self):
        text = (
            self.input_box.get("1.0", tk.END)
            if not self.input_text
            else self.input_text
        ).strip()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text Files", "*.txt")]
        )
        with open(file_path, "w") as file:
            file.write(text)
        messagebox.showinfo("Saved", "Input saved successfully!")
        self.input_text = ""

    def save_output(self):
        text = (
            self.output_box.get("1.0", tk.END)
            if not self.input_text
            else self.input_text
        ).strip()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text Files", "*.txt")]
        )
        with open(file_path, "w") as file:
            file.write(text)
        messagebox.showinfo("Saved", "Output saved successfully!")
        self.input_text = ""


if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
