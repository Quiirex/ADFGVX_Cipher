import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


class ADFGVX:
    def __init__(self):
        self.adfgvx = "ADFGVX"
        self.alphabet = "ABCČDEFGHIJKLMNOPRSŠTUVZŽ"
        self.keyword = None
        self.polybius_square = None

    def create_polybius_square(self, keyword):
        # Remove duplicate characters from the keyword and convert it to uppercase
        keyword = "".join(sorted(set(keyword.upper()), key=keyword.upper().index))

        # Create the remaining characters for the polybius square
        remaining_chars = [char for char in self.alphabet if char not in keyword]
        remaining_chars = "".join(remaining_chars)

        # Combine the keyword and remaining characters to create the polybius square
        self.polybius_square = keyword + remaining_chars

        return True

    def set_keyword(self, keyword):
        if self.create_polybius_square(keyword):
            self.keyword = keyword

    def encrypt(self, text):
        encrypted_text = ""
        for char in text:
            if char.upper() in self.polybius_square:
                index = self.polybius_square.index(char.upper())
                row = self.adfgvx[index // 6]
                column = self.adfgvx[index % 6]
                encrypted_text += row + column
        return encrypted_text

    def decrypt(self, encrypted_text):
        decrypted_text = ""
        i = 0
        while i < len(encrypted_text):
            row = encrypted_text[i]
            column = encrypted_text[i + 1]
            index = self.adfgvx.index(row) * 6 + self.adfgvx.index(column)
            decrypted_text += self.polybius_square[index]
            i += 2
        return decrypted_text


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ADFGVX Cipher")
        self.cipher = ADFGVX()

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

        self.key_label = tk.Label(self.input_frame, text="Key:")
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
        keyword = self.key_entry.get("1.0", tk.END).strip()
        self.cipher.set_keyword(keyword)
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
        keyword = self.key_entry.get("1.0", tk.END).strip()
        self.cipher.set_keyword(keyword)
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
