import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


class ADFGVX:
    def __init__(self):
        self.adfgvx = "ADFGVX"
        self.alphabet = "ABCČDEFGHIJKLMNOPRSŠTUVZŽ0123456789X"
        self.substitution_key = None  # key phrase
        self.transposition_key = None  # column key

    def set_substitution_key(self, substitution_key):
        if self.create_polybius_square(substitution_key):
            self.substitution_key = substitution_key

    def set_transposition_key(self, transposition_key):
        self.transposition_key = transposition_key

    def create_polybius_square(self, key):
        # Remove duplicate characters from the keyword and convert it to uppercase
        key = "".join(sorted(set(key.upper()), key=key.upper().index))

        # Create the remaining characters for the polybius square
        remaining_chars = [char for char in self.alphabet if char not in key]
        remaining_chars = "".join(remaining_chars)

        # Combine the keyword and remaining characters to create the polybius square
        self.polybius_square = key + remaining_chars

        # print("Polybius square:")
        # for i in range(6):
        #     print(self.polybius_square[i * 6 : (i + 1) * 6])

        return True

    def encrypt(self, text):
        encrypted_text = ""
        # print(f"text: {text}")

        # Perform the substitution step (Polybius square)
        for char in text:
            if char.upper() in self.polybius_square:
                index = self.polybius_square.index(char.upper())
                row = self.adfgvx[index // 6]
                column = self.adfgvx[index % 6]
                encrypted_text += row + column

        # print(f"Encrypted text: {encrypted_text}")

        # Perform the transposition step using the user-provided key
        transposed_text = [""] * len(self.transposition_key)
        for i in range(len(encrypted_text)):
            transposed_text[i % len(self.transposition_key)] += encrypted_text[i]

        # Reorder the columns based on the transposition key
        transposed_text = [
            x
            for _, x in sorted(
                zip(self.transposition_key, transposed_text), key=lambda pair: pair[0]
            )
        ]

        return "".join(transposed_text)

    def decrypt(self, encrypted_text):
        # Calculate the number of full columns
        full_columns = len(encrypted_text) % len(self.transposition_key)

        # Calculate the number of characters per column
        chars_per_column = len(encrypted_text) // len(self.transposition_key)

        # Create a list to hold the columns
        columns = [""] * len(self.transposition_key)

        # Distribute the characters back to their original positions
        i = 0
        for key in sorted(self.transposition_key):
            length = (
                chars_per_column + 1
                if self.transposition_key.index(key) < full_columns
                else chars_per_column
            )
            columns[self.transposition_key.index(key)] = encrypted_text[i : i + length]
            i += length

        # Combine the columns to get the original encrypted text (before the transposition step)
        decrypted_text = ""
        max_len = max(len(column) for column in columns)
        for i in range(max_len):
            for column in columns:
                if i < len(column):
                    decrypted_text += column[i]

        # Reverse the substitution step (Polybius square)
        i = 0
        while i < len(decrypted_text):
            row = decrypted_text[i]
            column = decrypted_text[i + 1]
            index = self.adfgvx.index(row) * 6 + self.adfgvx.index(column)
            if index < len(self.polybius_square):
                decrypted_text = (
                    decrypted_text[:i]
                    + self.polybius_square[index]
                    + decrypted_text[i + 2 :]
                )
            i += 1

        return decrypted_text


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ADFGVX Cipher")
        self.cipher = ADFGVX()

        # region input frame
        self.input_frame = tk.Frame(root)
        self.input_frame.grid(row=0, column=0, padx=20)

        self.text_label = tk.Label(self.input_frame, text="Input:")
        self.text_label.grid(row=0, column=0)
        self.input_box = tk.Text(self.input_frame, width=100, height=15)
        self.input_box.grid(row=1, column=0)

        self.key_phrase_label = tk.Label(self.input_frame, text="Substitution key:")
        self.key_phrase_label.grid(row=2, column=0)
        self.substitution_key_entry = tk.Entry(self.input_frame, width=77)
        self.substitution_key_entry.grid(row=3, column=0)
        validate_command = self.root.register(self.validate_substitution_key)
        self.substitution_key_entry.config(
            validate="key", validatecommand=(validate_command, "%P")
        )

        self.column_key_label = tk.Label(self.input_frame, text="Transposition key:")
        self.column_key_label.grid(row=4, column=0)
        self.transposition_key_entry = tk.Entry(self.input_frame, width=77)
        self.transposition_key_entry.grid(row=5, column=0)

        self.output_label = tk.Label(self.input_frame, text="Output:")
        self.output_label.grid(row=6, column=0)
        self.output_box = tk.Text(self.input_frame, width=100, height=15)
        self.output_box.grid(row=7, column=0)
        self.save_output_button = tk.Button(
            self.input_frame, text="Save as..", command=self.save_output, width=5
        )
        self.save_output_button.grid(row=7, column=1)
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

        self.switch_button = tk.Button(
            self.button_frame,
            text="Switch I/O",
            command=lambda: self.switch_text(),
            width=10,
        )
        self.switch_button.grid(row=1, column=1)

        self.encrypt_button = tk.Button(
            self.button_frame, text="Encrypt", command=self.encrypt_text, width=10
        )
        self.encrypt_button.grid(row=1, column=2)

        self.decrypt_button = tk.Button(
            self.button_frame, text="Decrypt", command=self.decrypt_text, width=10
        )
        self.decrypt_button.grid(row=1, column=3)

        self.input_text = ""

    def validate_substitution_key(self, new_value):
        return new_value == "" or new_value.isalpha()

    def switch_text(self):
        self.input_text = self.input_box.get("1.0", tk.END).strip()
        self.input_box.delete("1.0", tk.END)
        self.input_box.insert(tk.END, self.output_box.get("1.0", tk.END).strip())
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, self.input_text)
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
        substitution_key = self.substitution_key_entry.get().strip()
        self.cipher.set_substitution_key(substitution_key)
        transposition_key = self.transposition_key_entry.get().strip()
        self.cipher.set_transposition_key(transposition_key)
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
        substitution_key = self.substitution_key_entry.get().strip()
        self.cipher.set_substitution_key(substitution_key)
        transposition_key = self.transposition_key_entry.get().strip()
        self.cipher.set_transposition_key(transposition_key)
        decrypted_text = self.cipher.decrypt(text)
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, decrypted_text.strip())
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

    # endregion


if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
