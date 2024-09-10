import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
from stock import daliy_return_chart, moving_average_chart, relation_pv_chart


# Initialize Tkinter and Matplotlib Figure
root = tk.Tk()
fig, ax = plt.subplots()

# Tkinter Application
frame = tk.Frame(root)
label = tk.Label(text="Stock Analysis")
label.config(font=("Courier", 32))
label.pack()
frame.pack()

filter_var = tk.StringVar()
filter_options = ['Daliy Return', 'Moving Average', 'Close price VS Volume']
filter_combobox = ttk.Combobox(frame, textvariable=filter_var, values=filter_options)
filter_combobox.pack(pady=10)

stock_var = tk.StringVar()
stock_options = ["2888.HK", "0005.HK", "2388.HK"]
stock_combobox = ttk.Combobox(frame, textvariable=stock_var, values=stock_options)
stock_combobox.pack(pady=10)

# Create Canvas
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Plot data on Matplotlib Figure
def filter_data(show_save):
    selected_stock = stock_var.get()
    filter_option = filter_var.get()
    # result_text.delete('1.0', tk.END)
    if ax.lines:
        ax.clear()  # Clear previous plot
    if filter_option == 'Daliy Return':
        daliy_return_chart(ax,selected_stock)
        ax.grid(True)
        if show_save == 'save':
            fig.savefig(f'./daliy_return_{selected_stock}.png')
    elif filter_option == 'Moving Average':
        moving_average_chart(ax,selected_stock)
        ax.grid(True)
        if show_save == 'save':
            fig.savefig(f'./moving_average_{selected_stock}.png')
    elif filter_option == 'Close price VS Volume':
        relation_pv_chart(ax, selected_stock)
        ax.grid(True)
        if show_save == 'save':
            fig.savefig(f'./relation_pv_{selected_stock}.png')
    if filter_option != '' and show_save == 'show':
        canvas.draw()
    elif filter_option != '' and show_save =='save':
        # result_text.delete('1.0', tk.END)
        # result_text.insert(tk.END, 'Image is downloaded.')
        messagebox.showinfo(title='Notice', message="Image is downloaded.")
        canvas.draw()
    else:
        # result_text.delete('1.0', tk.END)
        # result_text.insert(tk.END, 'Data should not be empty.')
        messagebox.showwarning(title='Warning', message="Data should not be empty.")

def filter_show():
    filter_data('show')

def filter_save():
    filter_data('save')

show_button = tk.Button(frame, text="Filter", command=filter_show)
show_button.pack(pady=10)

save_button = tk.Button(frame, text="Save Filtered Result", command=filter_save)
save_button.pack(pady=10)

# result_text = tk.Text(frame, height=10, width=40)
# result_text.pack(pady=20)

# filter_data('show')
root.mainloop()