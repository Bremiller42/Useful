import tkinter as tk
from tkinter import ttk
from tkinter.font import Font


class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")
        master.geometry("370x325")
        master.resizable(True, True)
        button_font = Font(family="Helvetica", size=20, weight="bold")
        readback_font = Font(family="Helvetica", size=30, weight="bold")

        self.text_frame = tk.Frame(master, borderwidth=2, relief="groove")
        self.text_frame.grid(row=0, column=0, columnspan=4, rowspan=2, sticky='nsew')


        self.textbox = tk.Text(self.text_frame, height=1, font=readback_font, width=16, state="disabled",
                               borderwidth=0, relief="flat")
        self.textbox.pack(side="bottom", fill="both", expand=True)

        self.textbox2 = tk.Text(self.text_frame, height=1, font=readback_font, width=16, state="disabled",
                                borderwidth=0, relief="flat")
        self.textbox2.pack(side="top", fill="both", expand=True)

        button_width = 5
        tall_button_width = 4
        button_height = 10

        style = ttk.Style()
        style.configure("Custom.TButton", font=button_font, width=button_width, height=button_height)
        style.configure("Zero.TButton", font=button_font, width=(button_width * 2 + 1), height=button_height)
        style.configure("Right.TButton", font=button_font, width=tall_button_width, height=(button_height * 2 + 1))

        # Button Setup
        self.button_clear = ttk.Button(master, text="Clear", style="Custom.TButton",
                                       command=lambda: self.clear_text())
        self.button_clear.grid(row=2, column=0, stick="nsew")

        self.button_divide = ttk.Button(master, text="/", style="Custom.TButton",
                                        command=lambda: self.update_text("/"))
        self.button_divide.grid(row=2, column=1, stick="nsew")

        self.button_add = ttk.Button(master, text="+", style="Right.TButton",
                                     command=lambda: self.update_text("+"))
        self.button_add.grid(row=3, column=3, rowspan=2, sticky="nsew")

        self.button_multiply = ttk.Button(master, text="*", style="Custom.TButton",
                                          command=lambda: self.update_text("*"))
        self.button_multiply.grid(row=2, column=2, stick="nsew")

        self.button_subtract = ttk.Button(master, text="-", style="Custom.TButton",
                                          command=lambda: self.update_text("-"))
        self.button_subtract.grid(row=2, column=3, stick="nsew")

        self.button_1 = ttk.Button(master, text="1", style="Custom.TButton",
                                   command=lambda: self.update_text("1"))
        self.button_1.grid(row=3, column=0, stick="nsew")

        self.button_2 = ttk.Button(master, text="2", style="Custom.TButton",
                                   command=lambda: self.update_text("2"))
        self.button_2.grid(row=3, column=1, stick="nsew")

        self.button_3 = ttk.Button(master, text="3", style="Custom.TButton",
                                   command=lambda: self.update_text("3"))
        self.button_3.grid(row=3, column=2, stick="nsew")

        self.button_4 = ttk.Button(master, text="4", style="Custom.TButton",
                                   command=lambda: self.update_text("4"))
        self.button_4.grid(row=4, column=0, stick="nsew")

        self.button_5 = ttk.Button(master, text="5", style="Custom.TButton",
                                   command=lambda: self.update_text("5"))
        self.button_5.grid(row=4, column=1, stick="nsew")

        self.button_6 = ttk.Button(master, text="6", style="Custom.TButton",
                                   command=lambda: self.update_text("6"))
        self.button_6.grid(row=4, column=2, stick="nsew")

        self.button_7 = ttk.Button(master, text="7", style="Custom.TButton",
                                   command=lambda: self.update_text("7"))
        self.button_7.grid(row=5, column=0, stick="nsew")

        self.button_8 = ttk.Button(master, text="8", style="Custom.TButton",
                                   command=lambda: self.update_text("8"))
        self.button_8.grid(row=5, column=1, stick="nsew")

        self.button_9 = ttk.Button(master, text="9", style="Custom.TButton",
                                   command=lambda: self.update_text("9"))
        self.button_9.grid(row=5, column=2, stick="nsew")

        self.button_dec = ttk.Button(master, text=".", style="Custom.TButton",
                                     command=lambda: self.update_text("."))
        self.button_dec.grid(row=6, column=0, stick="nsew")

        self.button_0 = ttk.Button(master, text="0", style="Zero.TButton",
                                   command=lambda: self.update_text("0"))
        self.button_0.grid(row=6, column=1, columnspan=2, stick="nsew")

        self.button_enter = ttk.Button(master, text="Enter", style="Right.TButton",
                                       command=self.evaluate)
        self.button_enter.grid(row=5, column=3, rowspan=2, sticky="nsew")

        self.current_text = ""
        # Allow buttons to resize with resizing
        for i in range(7):
            master.grid_rowconfigure(i, weight=1)
        for i in range(4):
            master.grid_columnconfigure(i, weight=1)

        # Bind keyboard events to the root window
        master.bind('<KeyPress>', self.key_press_event)

    def key_press_event(self, event):
        key = event.char
        if event.keysym == 'Delete':
            # Clear the text in the input textbox
            self.clear_all()
        if event.keysym == 'BackSpace':
            # Delete last character in input field
            self.textbox.configure(state="normal")
            self.textbox.delete("end-2c")
            self.textbox.configure(state="disabled")
            self.current_text = self.textbox.get("1.0", "end-1c")
        if key.isdigit() or key in ['+', '-', '*', '/', '.', '\r']:
            # For digits, operators, decimal point, and Enter key
            if key == '\r':
                # For Enter key, simulate button press
                self.evaluate()
            else:
                # For other keys, simulate button press
                self.update_text(key)

    def update_text(self, text):
        # Insert the button's text into the text box
        self.textbox.configure(state="normal")
        self.textbox.insert(tk.END, text)
        self.textbox.tag_configure("right", justify='right')
        self.textbox.tag_add("right", "1.0", "end")
        self.textbox.configure(state="disabled")
        self.current_text += text

    def clear_text(self):
        # Clear first textbox
        self.textbox.configure(state="normal")
        self.textbox.delete(1.0, tk.END)
        self.textbox.configure(state="disabled")
        self.current_text = ""

    def clear_all(self):
        # Clear all the text boxes
        self.textbox.configure(state="normal")
        self.textbox.delete(1.0, tk.END)
        self.textbox.configure(state="disabled")
        self.textbox2.configure(state="normal")
        self.textbox2.delete(1.0, tk.END)
        self.textbox2.configure(state="disabled")
        self.current_text = ""

    def evaluate(self):

        try:
            # Check if the first textbox starts with an operator
            if self.current_text.startswith(('+', '-', '*', '/')):
                # Apply the operator to the number in the second textbox
                operator = self.current_text[0]
                number = float(self.textbox2.get("1.0", tk.END))
                if operator == '+':
                    result = number + float(self.current_text[1:])
                elif operator == '-':
                    result = number - float(self.current_text[1:])
                elif operator == '*':
                    result = number * float(self.current_text[1:])
                elif operator == '/':
                    result = number / float(self.current_text[1:])
                else:
                    raise ValueError("Invalid operator")

                # Show the result in the second text box
                self.textbox2.configure(state="normal")
                self.textbox2.delete(1.0, tk.END)
                self.textbox2.insert(tk.END, str(result))  # Insert the result into the second text box
                self.textbox2.tag_configure("right", justify='right')
                self.textbox2.tag_add("right", "1.0", "end")
                self.textbox2.configure(state="disabled")
            else:
                # Evaluate the expression and show the result in the second text box
                result = eval(self.current_text)
                self.textbox2.configure(state="normal")
                self.textbox2.delete(1.0, tk.END)
                self.textbox2.insert(tk.END, str(result))  # Insert the result into the second text box
                self.textbox2.tag_configure("right", justify='right')
                self.textbox2.tag_add("right", "1.0", "end")
                self.textbox2.configure(state="disabled")

            # Clear the first text box
            self.clear_text()
        except Exception as e:
            self.textbox.configure(state="normal")
            self.textbox.delete(1.0, tk.END)
            self.textbox.insert(tk.END, "Err")
            self.textbox.tag_configure("right", justify='right')
            self.textbox.tag_add("right", "1.0", "end")
            self.textbox.configure(state="disabled")
            self.current_text = ""


def main():
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
