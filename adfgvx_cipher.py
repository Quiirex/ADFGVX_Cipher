import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


class ADFGVX:
    def __init__(self):
        self.adfgvx = "ADFGVX"
        self.alphabet = "ABCČDEFGHIJKLMNOPRSŠTUVZŽ"

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


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ADFGVX Cipher")
        self.cipher = ADFGVX()

        # input frame
        self.input_frame = tk.Frame(root)
        self.input_frame.grid(row=0, column=0, padx=20)

        self.text_label = tk.Label(self.input_frame, text="Enter Text:")
        self.text_label.grid(row=0, column=0)
        self.text_entry = tk.Text(self.input_frame, width=50, height=10)
        self.text_entry.grid(row=1, column=0)

        self.key_label = tk.Label(self.input_frame, text="Enter Key:")
        self.key_label.grid(row=2, column=0)
        self.key_entry = tk.Text(self.input_frame, width=50, height=10)
        self.key_entry.grid(row=3, column=0)

        # button frame
        self.button_frame = tk.Frame(root)
        self.button_frame.grid(row=4, column=0, padx=20, pady=20)

        self.encrypt_button = tk.Button(
            self.button_frame, text="Encrypt", command=self.encrypt_text, width=10
        )
        self.encrypt_button.grid(row=1, column=0)

        self.decrypt_button = tk.Button(
            self.button_frame, text="Decrypt", command=self.decrypt_text, width=10
        )
        self.decrypt_button.grid(row=1, column=1)

        self.load_file_button = tk.Button(
            self.button_frame,
            text="Open file",
            command=self.load_text_from_file,
            width=10,
        )
        self.load_file_button.grid(row=2, column=0)

        self.save_button = tk.Button(
            self.button_frame, text="Save result", command=self.save_result, width=10
        )
        self.save_button.grid(row=2, column=1)

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
    app = GUI(root)
    root.mainloop()
