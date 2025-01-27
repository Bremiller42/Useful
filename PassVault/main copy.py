import os
import tkinter as tk
import sqlite3
import random
import string
from cryptography.fernet import Fernet
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
import hashlib

# Font definitions
FONT = ("Arial", 16)

# Variables for password generator
uppers = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
specials = "<>?/:;[]}{()/*-+!@#$%^&_="

# Dictionary for uppers, digits, specials Boolean values
variables = {"uppers": False,
             "digits": False,
             "specials": False}

# Directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Creating master key location
MASTER_KEY_FILE = os.path.join(SCRIPT_DIR, "master.key")

# Creating database location
DATABASE_FILE = os.path.join(SCRIPT_DIR, "passwords_vault.db")

# Hash the master password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Verify the master password
def verify_password(stored_hash, password):
    return stored_hash == hashlib.sha256(password.encode()).hexdigest()

# Generate a master key
def generate_master_key(password):
    key = Fernet.generate_key()
    hashed_password = hash_password(password)
    with open(MASTER_KEY_FILE, "wb") as key_file:
        key_file.write(key + b"\n" + hashed_password.encode())

# Load the master key and hashed password
def load_master_key():
    try:
        with open(MASTER_KEY_FILE, "rb") as key_file:
            lines = key_file.readlines()
            master_key = lines[0].strip()
            stored_hash = lines[1].strip()
            return master_key, stored_hash
    except FileNotFoundError:
        messagebox.showerror("Error", "Master key not found. Please add a password first.")
        return None, None

# Encrypt data using master key
def encrypt_with_master_key(data, master_key):
    f = Fernet(master_key)
    return f.encrypt(data)

# Decrypt data using master key
def decrypt_with_master_key(encrypted_data, master_key):
    f = Fernet(master_key)
    return f.decrypt(encrypted_data)

# Generate a key using the provided password
def generate_key_from_password(password):
    return Fernet.generate_key()

# Encrypt data using the provided key
def encrypt_with_key(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode())

# Decrypt data using the provided key
def decrypt_with_key(encrypted_data, key):
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()

# Function to set which types of characters to include:
def set_inclusion(uppers_included, digits_included, specials_included):
    variables["uppers"] = uppers_included
    variables["digits"] = digits_included
    variables["specials"] = specials_included

# Function for generating passwords if needed
def generate_password(length):
    options = "abcdefghijklmnopqrstuvwxyz"
    password_list = []
    if variables["uppers"]:
        options += uppers
    if variables["digits"]:
        options += digits
    if variables["specials"]:
        options += specials
    for _ in range(length):
        choice = random.choice(options)
        password_list.append(choice)
    return str(''.join(password_list))

# Create or connect to database
conn = sqlite3.connect(DATABASE_FILE)

# Create a cursor
c = conn.cursor()

# Create a table
c.execute('''CREATE TABLE IF NOT EXISTS passwords(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          website TEXT NOT NULL,
          username TEXT NOT NULL,
          password TEXT NOT NULL,
          key TEXT NOT NULL)''')

# Commit changes
conn.commit()

# Close the connection
conn.close()

class PassVault(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PassVault")
        self.geometry("400x250")
        self.resizable(False, False)

        if not os.path.exists(MASTER_KEY_FILE):
            self.prompt_master_password()
        else:
            self.main_menu_frame = MainMenuFrame(self)
            self.main_menu_frame.pack(fill="both", expand=True)

    def prompt_master_password(self):
        password = askstring("Master Password", "Set your master password:", show="*")
        if password:
            confirm_password = askstring("Confirm Master Password", "Confirm your master password:", show="*")
            if password == confirm_password:
                generate_master_key(password)
                messagebox.showinfo("Success", "Master password set successfully!")
                self.main_menu_frame = MainMenuFrame(self)
                self.main_menu_frame.pack(fill="both", expand=True)
            else:
                messagebox.showerror("Error", "Passwords do not match. Please restart the application.")
                self.quit()
        else:
            messagebox.showerror("Error", "Master password not set. Please restart the application.")
            self.quit()


class MainMenuFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master.geometry("400x250")
        self.master.resizable(False, False)
        self.master = master
        self.create_widgets()


    def create_widgets(self):

        self.label = tk.Label(self, 
                              text="PassVault Password Manager", 
                              font=FONT)
        self.label.pack(pady=20)

        self.add_password_button = tk.Button(self,
                                             text="Add Password",
                                             command=self.add_password)
        self.add_password_button.pack(pady=10)

        self.view_passwords_button = tk.Button(self,
                                               text="View Passwords",
                                               command=self.view_passwords)
        self.view_passwords_button.pack(pady=10)

        self.quit_button = tk.Button(self,
                                     text="Exit",
                                     command=self.master.quit)
        self.quit_button.pack(pady=10)


    def add_password(self):
        AddPasswordFrame(self.master).pack(fill="both", expand=True)
        self.pack_forget()

    def view_passwords(self):
        ViewPasswordsFrame(self.master).pack(fill="both", expand=True)
        self.pack_forget()


class AddPasswordFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master.geometry("475x250")
        self.master.resizable(False, False)
        self.master = master
        self.create_widgets()
        
        self.master.bind("<Return>", self.on_enter)



    def create_widgets(self):


        self.label = tk.Label(self,
                              text="Add Password",
                              font=FONT)
        self.label.grid(row=0, column=0, columnspan=2, pady=20)

        self.website_label = tk.Label(self,
                                      text="Website: ")
        self.website_label.grid(row=1, column=0, padx=10, pady=5)
        self.website_entry = tk.Entry(self)
        self.website_entry.grid(row=1, column=1, pady=5)

        self.user_label = tk.Label(self,
                                   text="Username: ")
        self.user_label.grid(row=2, column=0, padx=10, pady=5)
        self.user_entry = tk.Entry(self)
        self.user_entry.grid(row=2, column=1, pady=5)

        self.password_label = tk.Label(self,
                                       text="Password: ")
        self.password_label.grid(row=3, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=3, column=1, pady=5)

        self.generate_password_button = tk.Button(self,
                                                  text="Generate Password",
                                                  command=self.generate_password)
        self.generate_password_button.grid(row=6, column=2, pady=5)

        self.save_button = tk.Button(self,
                                     text="Save Password",
                                     command=self.save_password)
        self.save_button.grid(row=5, column=1, pady=5)

        self.back_button = tk.Button(self,
                                     text="Back",
                                     command=self.back_to_menu)
        self.back_button.grid(row=5, column=0, pady=5)

        self.upper_var = tk.IntVar()
        self.digit_var = tk.IntVar()
        self.special_var = tk.IntVar()

        self.variables_label = tk.Label(self,
                                        text="Generation Inclusion: ",
                                        font=FONT)
        self.variables_label.grid(row=0, column=2, pady=5)

        self.upper_check = tk.Checkbutton(self,
                                          text="Include Uppercase",
                                          variable=self.upper_var)
        self.upper_check.grid(row=1, column=2, pady=5, padx=10, sticky="w")

        self.digit_check = tk.Checkbutton(self,
                                          text="Include Digits",
                                          variable=self.digit_var)
        self.digit_check.grid(row=2, column=2, pady=5, padx=10, sticky="w")

        self.special_check = tk.Checkbutton(self,
                                            text="Include Specials",
                                            variable=self.special_var)
        self.special_check.grid(row=3, column=2, pady=5, padx=10, sticky="w")

        self.length_label = tk.Label(self,
                                     text="Password Length: ")
        self.length_label.grid(row=4, column=2)

        self.length_entry = tk.Entry(self)
        self.length_entry.insert(0, "12")
        self.length_entry.grid(row=5, column=2)


    def generate_password(self):
        length = self.length_entry.get()
        if length.isdigit() and int(length) > 0:
            set_inclusion(bool(self.upper_var.get()),
                          bool(self.digit_var.get()),
                          bool(self.special_var.get()))
            generated_password = generate_password(int(length))
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, generated_password)
        else:
            messagebox.showwarning("Input Error", "Please enter a valid length for the password.")

    def save_password(self):
        website = self.website_entry.get().lower()
        username = self.user_entry.get()
        password = self.password_entry.get()

        if website and username and password:
            master_password = askstring("Master Password", "Enter your master password:", show="*")
            if master_password:
                master_key, stored_hash = load_master_key()
                if master_key and verify_password(stored_hash.decode(), master_password):
                    key = generate_key_from_password(master_password)
                    encrypted_password = encrypt_with_key(password, key)
                    encrypted_key = encrypt_with_master_key(key, master_key)

                    conn = sqlite3.connect(DATABASE_FILE)
                    c = conn.cursor()
                    c.execute("INSERT INTO passwords (website, username, password, key) VALUES (?, ?, ?, ?)",
                              (website, username, encrypted_password, encrypted_key))
                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Success", "Password saved successfully!")
                    self.back_to_menu()
                else:
                    messagebox.showerror("Error", "Incorrect master password!")
            else:
                messagebox.showwarning("Cancelled", "Master password entry cancelled.")
        else:
            messagebox.showwarning("Input Error", "All fields are required!")
    
    
    def on_enter(self, event):
        self.save_password()


    def back_to_menu(self):
        self.destroy()
        self.master.main_menu_frame.pack(fill="both", expand=True)
        self.master.geometry("400x250")


class ViewPasswordsFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master.geometry("525x400")
        self.master.resizable(False, True)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self,
                              text="View Passwords",
                              font=FONT)
        self.label.grid(row=1, column=1, pady=10, sticky="we")

        self.tree = ttk.Treeview(self)
        self.tree["columns"] = ("ID", "Website", "Username", "Password")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", anchor=tk.CENTER, width=50)
        self.tree.column("Website", anchor=tk.W, width=150)
        self.tree.column("Username", anchor=tk.W, width=150)
        self.tree.column("Password", anchor=tk.W, width=150)

        self.tree.heading("#0", text="", anchor=tk.CENTER)
        self.tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.tree.heading("Website", text="Website", anchor=tk.W)
        self.tree.heading("Username", text="Username", anchor=tk.W)
        self.tree.heading("Password", text="Password", anchor=tk.W)

        self.tree.bind("<Double-1>", self.on_double_click)

        self.tree.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.back_button = tk.Button(self,
                                     text="Back",
                                     command=self.back_to_menu)
        self.back_button.grid(row=1, column=0, padx=10, pady=10, sticky='e')

        self.delete_password_button = tk.Button(self,
                                                text="Delete Password",
                                                command=self.delete_password)
        self.delete_password_button.grid(row=1, column=2, padx=10, pady=10, sticky='w')

        self.load_passwords()


    def delete_password(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No Password Selected")
            return

        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this password?")
        if confirm:
            master_password = askstring("Master Password", "Enter your master password", show="*")
            _, stored_hash = load_master_key()

            if not verify_password(stored_hash.decode(), master_password):
                messagebox.showerror("Error", "Incorrect master password!")
                return
            
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        for item in selected_item:
            item_id = self.tree.item(item, 'values')[0]
            c.execute("DELETE FROM passwords WHERE id=?", (item_id,))
        conn.commit()
        conn.close()

        self.reconfigure_ids()
        self.load_passwords()
        messagebox.showinfo("Delete Successful", "The password has been successfully deleted")



    def reconfigure_ids(self):
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()

        # Fetch all remaining records, ordered by the current ID
        c.execute("SELECT id, website, username, password, key FROM passwords ORDER BY id")
        records = c.fetchall()

        # Reassign new IDS
        new_id = 1
        for record in records:
            old_id = record[0]
            c.execute("UPDATE passwords SET id = ? WHERE id = ?", (new_id, old_id))
            new_id += 1

        conn.commit()
        conn.close()


    def load_passwords(self):
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        c.execute("SELECT id, website, username FROM passwords")
        records = c.fetchall()
        conn.close()

        self.tree.delete(*self.tree.get_children())

        for record in records:
            self.tree.insert("", tk.END, values=(record[0], record[1], record[2], ""))

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        record_id = self.tree.item(item, "values")[0]
        self.show_password(item, record_id)

    def show_password(self, item, record_id):
        master_password = askstring("Master Password", "Enter your master password:", show="*")
        if master_password:
            master_key, stored_hash = load_master_key()
            if master_key and verify_password(stored_hash.decode(), master_password):
                conn = sqlite3.connect(DATABASE_FILE)
                c = conn.cursor()
                c.execute("SELECT password, key FROM passwords WHERE id=?", (record_id,))
                record = c.fetchone()
                conn.close()

                encrypted_password, encrypted_key = record
                decrypted_password = self.decrypt_password(encrypted_password, encrypted_key)

                self.tree.item(item, values=(record_id, self.tree.item(item, "values")[1],
                                              self.tree.item(item, "values")[2], decrypted_password))
            else:
                messagebox.showerror("Error", "Incorrect master password!")

    def decrypt_password(self, encrypted_password, encrypted_key):
        master_key, stored_hash = load_master_key()
        key = decrypt_with_master_key(encrypted_key, master_key)
        return decrypt_with_key(encrypted_password, key)

    def back_to_menu(self):
        self.destroy()
        self.master.main_menu_frame.pack(fill="both", expand=True)
        self.master.geometry("400x250")


if __name__ == "__main__":
    app = PassVault()
    app.mainloop()
