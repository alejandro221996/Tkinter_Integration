import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from sympy import symbols, integrate, lambdify, sin, cos, tan, sinh, cosh, tanh


class IntegrationApp:
    def __init__(self, master):
        self.master = master
        master.title("Function Integration App")

        # Create and place input widgets
        self.entry_function = ttk.Entry(master, width=40)
        self.entry_function.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

        # Create buttons for common operations
        ttk.Button(master, text="x", command=lambda: self.insert_symbol("x")).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(master, text="sin", command=lambda: self.insert_function("sin")).grid(row=0, column=4, padx=5,
                                                                                         pady=5)
        ttk.Button(master, text="cos", command=lambda: self.insert_function("cos")).grid(row=0, column=5, padx=5,
                                                                                         pady=5)
        ttk.Button(master, text="tan", command=lambda: self.insert_function("tan")).grid(row=0, column=6, padx=5,
                                                                                         pady=5)
        ttk.Button(master, text="sinh", command=lambda: self.insert_function("sinh")).grid(row=0, column=7, padx=5,
                                                                                           pady=5)
        ttk.Button(master, text="cosh", command=lambda: self.insert_function("cosh")).grid(row=0, column=8, padx=5,
                                                                                           pady=5)
        ttk.Button(master, text="tanh", command=lambda: self.insert_function("tanh")).grid(row=0, column=9, padx=5,
                                                                                           pady=5)
        ttk.Button(master, text="^", command=lambda: self.insert_symbol("**")).grid(row=0, column=10, padx=5, pady=5)

        # Create number buttons
        for i in range(10):
            ttk.Button(master, text=str(i), command=lambda i=i: self.insert_number(i)).grid(row=1, column=i, padx=5,
                                                                                            pady=5)

        # Create operator buttons
        ttk.Button(master, text="+", command=lambda: self.insert_operator("+")).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(master, text="-", command=lambda: self.insert_operator("-")).grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(master, text="*", command=lambda: self.insert_operator("*")).grid(row=2, column=2, padx=5, pady=5)
        ttk.Button(master, text="/", command=lambda: self.insert_operator("/")).grid(row=2, column=3, padx=5, pady=5)
        ttk.Button(master, text="Reset", command=self.reset_plot).grid(row=2, column=4, padx=5, pady=5)

        self.btn_integrate = ttk.Button(master, text="Integrate", command=self.integrate_and_plot, width=20)
        self.btn_integrate.grid(row=2, column=5, padx=10, pady=10)

        # Create a label to display the current function
        self.label_function = ttk.Label(master, text="Function to Integrate:")
        self.label_function.grid(row=4, column=0, columnspan=6, padx=5, pady=5)

        # Create a Matplotlib figure with modified width and height (in inches)
        self.fig = Figure(figsize=(14, 8), dpi=100)
        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.plot_canvas.get_tk_widget().grid(row=3, column=0, columnspan=12, padx=5, pady=5)

        # Bind the KeyRelease event to update the label
        self.entry_function.bind("<KeyRelease>", self.update_label)

    def insert_symbol(self, symbol):
        # Insert a symbol into the entry widget
        current_text = self.entry_function.get()
        self.entry_function.delete(0, tk.END)
        self.entry_function.insert(tk.END, current_text + symbol)
        self.update_label()

    def insert_function(self, func):
        # Insert a function into the entry widget
        current_text = self.entry_function.get()
        self.entry_function.delete(0, tk.END)
        self.entry_function.insert(tk.END, current_text + f"{func}()")
        self.update_label()

    def insert_number(self, number):
        # Insert a number into the entry widget
        current_text = self.entry_function.get()
        self.entry_function.delete(0, tk.END)
        self.entry_function.insert(tk.END, current_text + str(number))
        self.update_label()

    def reset_plot(self):
        # Clear the entry widget and reset the plot canvas
        self.entry_function.delete(0, tk.END)
        self.label_function.config(text="Function to Integrate:")
        self.fig.clf()
        self.plot_canvas.draw()

    def insert_operator(self, operator):
        # Insert an operator into the entry widget
        current_text = self.entry_function.get()
        if current_text and current_text[-1] not in "+-*/":
            self.entry_function.delete(0, tk.END)
            self.entry_function.insert(tk.END, current_text + operator)
        self.update_label()

    def update_label(self, event=None):
        # Update the label to display the current function
        current_function = self.entry_function.get()
        self.label_function.config(text=f"Function to Integrate: {current_function}")

    def integrate_and_plot(self):
        try:
            # Get the input function from the entry
            input_function = self.entry_function.get()

            # Define the symbolic variable and the function to integrate
            x = symbols('x')
            symbolic_function = eval(input_function)
            integral_result = integrate(symbolic_function, x)

            # Clear previous plot
            self.fig.clf()

            # Create a new subplot and plot the integrated function with the constant 'C'
            ax = self.fig.add_subplot(111)
            x_vals = np.linspace(0, 10, 100)
            y_vals = [lambdify(x, integral_result.subs('C', 0))(val) for val in x_vals]
            ax.plot(x_vals, y_vals, label=f'Integrated Function: {integral_result} + C')
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
            ax.set_title('Integrated Function Plot')
            ax.legend()

            # Redraw the canvas
            self.plot_canvas.draw()

        except Exception as e:
            # Show an error message if an exception occurs
            tk.messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = IntegrationApp(root)
    root.mainloop()
