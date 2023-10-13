import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


class ADFGVXCipher:
    def __init__(self):
        self.adfgvx = "ADFGVX"
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZČŠŽ"

    def encrypt(self, text, key):
        encrypted_text = ""
        for char in text:
            if char.upper() in self.alphabet:
                index = self.alphabet.index(char.upper())
                row = self.adfgvx[index // 6]
                column = self.adfgvx[index % 6]
                encrypted_text += row + column
        return encrypted_text

    def decrypt(self, encrypted_text, key):
        decrypted_text = ""
        i = 0
        while i < len(encrypted_text):
            row = encrypted_text[i]
            column = encrypted_text[i + 1]
            index = self.adfgvx.index(row) * 6 + self.adfgvx.index(column)
            decrypted_text += self.alphabet[index]
            i += 2
        return decrypted_text


class CipherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ADFGVX Cipher")
        self.cipher = ADFGVXCipher()

        self.text_label = tk.Label(root, text="Enter Text:")
        self.text_label.pack()
        self.text_entry = tk.Entry(root, width=30)
        self.text_entry.pack()

        self.key_label = tk.Label(root, text="Enter Key:")
        self.key_label.pack()
        self.key_entry = tk.Entry(root, show="*", width=30)
        self.key_entry.pack()

        self.load_file_button = tk.Button(
            root, text="Load Text from File", command=self.load_text_from_file
        )
        self.load_file_button.pack()

        self.encrypt_button = tk.Button(root, text="Encrypt", command=self.encrypt_text)
        self.encrypt_button.pack()

        self.decrypt_button = tk.Button(root, text="Decrypt", command=self.decrypt_text)
        self.decrypt_button.pack()

        self.save_button = tk.Button(root, text="Save Result", command=self.save_result)
        self.save_button.pack()

        self.input_text = ""

    def load_text_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                self.input_text = file.read()
                self.text_entry.delete(0, tk.END)  # Clear any existing text
                self.text_entry.insert(0, self.input_text)
        else:
            messagebox.showerror("Error", "No file selected!")

    def encrypt_text(self):
        text = self.text_entry.get() if not self.input_text else self.input_text
        key = self.key_entry.get()
        encrypted_text = self.cipher.encrypt(text, key)
        messagebox.showinfo("Encrypted Text", f"Encrypted Text: {encrypted_text}")

    def decrypt_text(self):
        text = self.text_entry.get() if not self.input_text else self.input_text
        key = self.key_entry.get()
        decrypted_text = self.cipher.decrypt(text, key)
        messagebox.showinfo("Decrypted Text", f"Decrypted Text: {decrypted_text}")

    def save_result(self):
        text = self.text_entry.get() if not self.input_text else self.input_text
        key = self.key_entry.get()
        encrypted_text = self.cipher.encrypt(text, key)
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text Files", "*.txt")]
        )
        with open(file_path, "w") as file:
            file.write(encrypted_text)
        messagebox.showinfo("Saved", "Result saved successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = CipherGUI(root)
    root.mainloop()
