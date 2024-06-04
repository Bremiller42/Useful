"""A simple password generator with options for what types of characters to include.
Created by Brennon Miller. 
To use:
-Enter the number of characters to generate.
-Choose character inclusion settings.
-Press Generate! button."""

import tkinter as tk
import random
from tkinter.font import Font

# Variables
uppers = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
specials = "<>?/:;[]}{()/*-+!@#$%^&_="

char_numbers = 0

# Dictionary for uppers, digits, specials
variables = {"uppers": False,
             "digits": False,
             "specials": False}


# Functions
def uppers_true():
    if upper_var.get():
        variables["uppers"] = True
    else:
        variables["uppers"] = False


def digits_true():
    if digit_var.get():
        variables["digits"] = True
    else:
        variables["digits"] = False


def specials_true():
    if special_var.get():
        variables["specials"] = True
    else:
        variables["specials"] = False


def numbers_check():
    global char_numbers
    try:
        int(number_of_chars.get())
    except ValueError:
        password_output.delete(0, tk.END)
        password_output.insert(0, "Must Be an Integer")
    char_numbers = int(number_of_chars.get())
        

def generate_password():
    global char_numbers
    numbers_check()
    options = "abcdefghijklmnopqrstuvwxyz"
    password = []
    if variables["uppers"] == True:
        options = options + uppers
    if variables["digits"] == True:
        options = options + digits
    if variables["specials"] == True:
        options = options + specials
    password_list = []
    for i in range(char_numbers):
        choice = random.choice(options)
        password_list.append(choice)
    password = ''.join(password_list)
    password_output.delete(0, tk.END)
    password_output.insert(0, password)


# Main window information
root = tk.Tk()
root.title("Password Generator")
root.geometry("700x150")
root.resizable(False, False)

# Set the default font type
FONT = Font(family="Times New Roman",
        size=16)

# Password output
pass_label = tk.Label(root, 
                      text="Generated Password:",
                      font=FONT)
pass_label.grid(row=5, 
                column=1)

password_output = tk.Entry(root, 
                           font=FONT,
                           width=32, 
                           state=tk.NORMAL)
password_output.grid(row=5, 
                     column=2)

# Blank space to seperate radios and output
blank = tk.Label(root, 
                 text="")
blank.grid(row=4, 
           column=1, 
           sticky="ew")

# Button to generate password
generate = tk.Button(root, 
                     text="Generate!", 
                     font=FONT,
                     command=generate_password)
generate.grid(row=3, 
              column=2)

# Setting up checkbutton variable types
upper_var = tk.IntVar()
digit_var = tk.IntVar()
special_var = tk.IntVar()


# Entry for number of characters
chars_label = tk.Label(text="Numbers of characters to generate: ",
                       font=FONT,)
chars_label.grid(row=1,
                 column=1,
                 sticky='w')

number_of_chars = tk.Entry(root,
                           font=FONT,
                           width=4)
number_of_chars.grid(row=1,
                     column=2,
                     sticky="w")


# Buttons for uppers, digits, and specials inclusion
upper_radio = tk.Checkbutton(root,
                             text="Include Uppercase", 
                             font=FONT,
                             justify="left", 
                             variable=upper_var,
                             command=uppers_true)
upper_radio.grid(row=2, 
                 column=1, 
                 sticky='w')

digit_radio = tk.Checkbutton(root, 
                             text="Include Digits", 
                             font=FONT,
                             justify="left", 
                             variable=digit_var,
                             command=digits_true)
digit_radio.grid(row=3, 
                 column=1, 
                 sticky='w')

special_radio = tk.Checkbutton(root, 
                               text="Include Special Characters", 
                               font=FONT,
                               justify="left", 
                               variable=special_var,
                               command=specials_true)
special_radio.grid(row=4, 
                   column=1, 
                   sticky='w')


# Mainloop for window
if __name__ == "main":
    root.mainloop()

