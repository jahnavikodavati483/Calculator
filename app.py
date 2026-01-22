import tkinter as tk
import ui

root = tk.Tk()
root.title("Scientific Calculator")
root.geometry("420x720")

ui.build_ui(root)

root.mainloop()
