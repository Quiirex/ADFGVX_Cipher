import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


class PlayfairCipher:
    def __init__(self):
        self.alphabet = "ABCČDEFGHIJKLMNOPRSŠTUVZŽX"
        self.key = None

    def set_key(self, key):
        self.key = key.upper()

    def generate_key_matrix(self):
        if not self.key:
            raise ValueError("Please set a key before generating the key matrix.")

        filtered_key = "".join(char for char in self.key if char in self.alphabet)

        # Add 'X' to the key matrix if it's not already included
        if "X" not in filtered_key:
            filtered_key += "X"

        key_matrix = filtered_key

        for char in self.alphabet:
            if char not in key_matrix:
                key_matrix += char

        return key_matrix

    def prepare_text(self, text):
        text = text.upper()
        filtered_text = "".join(char for char in text if char in self.alphabet)
        filtered_text = filtered_text.replace("J", "I")

        pairs = []
        i = 0
        while i < len(filtered_text):
            if i + 1 < len(filtered_text) and filtered_text[i] == filtered_text[i + 1]:
                pairs.append(filtered_text[i] + "X")
                i += 1
            else:
                pairs.append(filtered_text[i : i + 2])
                i += 2

        # Check if the length of all pairs is odd
        if len(pairs[-1]) == 1:
            pairs[-1] += "X"

        print(f"Valid pairs: {pairs}")
        return pairs

    def encrypt(self, text):
        key_matrix = self.generate_key_matrix()
        # Generate the key matrix.
        text = self.prepare_text(text)
        print(f"Text: {text}")
        # Prepare the text for encryption.
        encrypted_text = ""
        # Initialize an empty string to store the encrypted text.
        for pair in text:
            print(f"pair: {pair}")
            print(
                f"divmod(key_matrix.index(pair[0]), 5): {divmod(key_matrix.index(pair[0]), 5)}"
            )
            print(
                f"divmod(key_matrix.index(pair[1]), 5): {divmod(key_matrix.index(pair[1]), 5)}"
            )
            print(f"keymatrix.index(pair[0]): {key_matrix.index(pair[0])}")
            print(f"keymatrix.index(pair[1]): {key_matrix.index(pair[1])}")
            print(f"pair[0]: {pair[0]}")
            print(f"pair[1]: {pair[1]}")
            x1, y1 = divmod(key_matrix.index(pair[0]), 5)
            x2, y2 = divmod(key_matrix.index(pair[1]), 5)
            # Calculate the row and column positions of the characters in the key matrix.

            if x1 == x2:
                encrypted_text += (
                    key_matrix[x1 * 5 + (y1 + 1) % 5]
                    + key_matrix[x2 * 5 + (y2 + 1) % 5]
                )
                # If the characters are in the same row, shift them to the right.
            elif y1 == y2:
                encrypted_text += (
                    key_matrix[(x1 + 1) % 5 * 5 + y1]
                    + key_matrix[(x2 + 1) % 5 * 5 + y2]
                )
                # If the characters are in the same column, shift them down.
            else:
                encrypted_text += key_matrix[x1 * 5 + y2] + key_matrix[x2 * 5 + y1]
                # Otherwise, form a rectangle and swap the characters.
        return encrypted_text
        # Return the encrypted text.

    def decrypt(self, text):
        key_matrix = self.generate_key_matrix()
        # Generate the key matrix.
        text = self.prepare_text(text)
        # Prepare the text for decryption.
        decrypted_text = ""
        # Initialize an empty string to store the decrypted text.
        for pair in text:
            x1, y1 = divmod(key_matrix.index(pair[0]), 5)
            x2, y2 = divmod(key_matrix.index(pair[1]), 5)
            # Calculate the row and column positions of the characters in the key matrix.
            if x1 == x2:
                decrypted_text += (
                    key_matrix[x1 * 5 + (y1 - 1) % 5]
                    + key_matrix[x2 * 5 + (y2 - 1) % 5]
                )
                # If the characters are in the same row, shift them to the left.
            elif y1 == y2:
                decrypted_text += (
                    key_matrix[(x1 - 1) % 5 * 5 + y1]
                    + key_matrix[(x2 - 1) % 5 * 5 + y2]
                )
                # If the characters are in the same column, shift them up.
            else:
                decrypted_text += key_matrix[x1 * 5 + y2] + key_matrix[x2 * 5 + y1]
                # Otherwise, form a rectangle and swap the characters.
        return decrypted_text
        # Return the decrypted text.


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Playfair Cipher")
        self.cipher = PlayfairCipher()

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
        key = self.key_entry.get("1.0", tk.END).strip()
        self.cipher.set_key(key)
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
        self.cipher.set_key(key)
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
