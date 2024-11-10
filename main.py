import tkinter as tk
import math
import operator

#not good leave
class ScientificCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Scientific Calculator")
        master.configure(bg='silver')

        self.display = tk.Entry(master, font=("Arial", 24), width=30, justify='right', bd=10, relief="sunken", bg='white')
        self.display.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

        self.buttons = {}
        self.create_buttons()

        self.radians = True
        # Map valid operators for safer evaluation
        self.operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '**': operator.pow,
        }
        self.master.bind("<Key>", self.keyboard_input)

    def create_buttons(self):
        buttons = [
            'C', '(', ')', '/', 'sqrt',
            '7', '8', '9', '*', 'x^y',
            '4', '5', '6', '-', 'sin',
            '1', '2', '3', '+', 'cos',
            '0', '.', '=', 'tan', '1/x',
            'arcsin', 'arccos', 'arctan', 'Rad', 'exp(x)',
            'π', '+/-', '%', 'ln', 'log10', 'x^2'
        ]

        row = 1
        col = 0
        for i, button in enumerate(buttons):
            command = lambda x=button: self.click(x)
            self.buttons[button] = tk.Button(self.master, text=button, font=("Arial", 18), command=command, height=2, width=5, bd=5, relief="raised", bg='lightgray')
            self.buttons[button].grid(row=row, column=col, sticky='nsew', padx=5, pady=5)
            col += 1
            if col > 4:
                col = 0
                row += 1

    def keyboard_input(self, event):
        # If key is a number or operator, only insert if it has no assigned button to avoid duplication
        if event.char.isdigit() or event.char in '+-*/()':
            # Only insert if it’s not also triggered by a button click
            if event.char not in self.buttons:
                self.display.insert(tk.END, event.char)
        elif event.char == '.' and '.' not in self.display.get():
            self.display.insert(tk.END, event.char)
        elif event.keysym == "Return":
            self.evaluate_expression()
        elif event.keysym == "BackSpace":
            self.display.delete(len(self.display.get()) - 1)


    def click(self, key):
        if key == '=':
            self.evaluate_expression()
        elif key == 'C':
            self.display.delete(0, tk.END)
        elif key == '+/-':
            self.toggle_sign()
        elif key == 'x^2':
            self.square()
        elif key in ['sin', 'cos', 'tan']:
            self.trig_function(key)
        elif key in ['arcsin', 'arccos', 'arctan']:
            self.inverse_trig_function(key)
        elif key == 'sqrt':
            self.square_root()
        elif key == 'x^y':
            self.display.insert(tk.END, '**')
        elif key == 'exp(x)':
            self.exponential()
        elif key == '1/x':
            self.reciprocal()
        elif key == 'Rad':
            self.toggle_radians()
        elif key == 'π':
            self.display.insert(tk.END, str(math.pi))
        elif key == 'ln':
            self.natural_log()
        elif key == 'log10':
            self.log_base_10()
        else:
            self.display.insert(tk.END, key)

    def evaluate_expression(self):
        try:
            expression = self.display.get()
            if '%' in expression:
                nums = expression.split('%')
                result = float(nums[0]) * float(nums[1]) / 100
            else:
                result = self.safe_eval(expression)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
        except Exception as e:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, f"Error: {str(e)}")

    def safe_eval(self, expression):
        # A safer evaluation function with allowed operators
        tokens = expression.split()
        result = None
        for i, token in enumerate(tokens):
            if token.isdigit():
                result = float(token) if result is None else self.operators[op](result, float(token))
            elif token in self.operators:
                op = token
        return result

    def toggle_sign(self):
        try:
            current_value = float(self.display.get())
            new_value = -current_value
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(new_value))
        except:
            self.display.insert(tk.END, "Error: Invalid Input")

    def square(self):
        try:
            value = float(self.display.get())
            result = value ** 2
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
        except:
            self.display.insert(tk.END, "Error: Invalid Input")

    def trig_function(self, func):
        try:
            value = float(self.display.get())
            if not self.radians:
                value = math.radians(value)
            result = getattr(math, func)(value)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
        except:
            self.display.insert(tk.END, "Error: Invalid Input")

    def inverse_trig_function(self, func):
        try:
            value = float(self.display.get())
            if func in ['arcsin', 'arccos'] and (value < -1 or value > 1):
                raise ValueError("Input out of range")
            result = getattr(math, 'a' + func[3:])(value)
            if not self.radians:
                result = math.degrees(result)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
        except Exception as e:
            self.display.insert(tk.END, f"Error: {str(e)}")

    def square_root(self):
        try:
            result = math.sqrt(float(self.display.get()))
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
        except:
            self.display.insert(tk.END, "Error: Invalid Input")

    def exponential(self):
        try:
            value = float(self.display.get())
            result = math.exp(value)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
        except:
            self.display.insert(tk.END, "Error: Invalid Input")

    def reciprocal(self):
        try:
            result = 1 / float(self.display.get())
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
        except:
            self.display.insert(tk.END, "Error: Invalid Input")

    def toggle_radians(self):
        self.radians = not self.radians
        self.buttons['Rad'].config(text="Rad" if self.radians else "Deg")

    def natural_log(self):
        try:
            value = float(self.display.get())
            result = math.log(value)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
        except:
            self.display.insert(tk.END, "Error: Invalid Input")

    def log_base_10(self):
        try:
            value = float(self.display.get())
            result = math.log10(value)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
        except:
            self.display.insert(tk.END, "Error: Invalid Input")


root = tk.Tk()
for i in range(1, 7):
    root.grid_rowconfigure(i, weight=1)
for i in range(5):
    root.grid_columnconfigure(i, weight=1)
calculator = ScientificCalculator(root)
root.mainloop()
