import tkinter as tk

def show_selection():
    selected_indices = listbox.curselection()
    selected_items = [listbox.get(i) for i in selected_indices]
    label.config(text="Selected item(s): " + ", ".join(selected_items))

root = tk.Tk()

listbox = tk.Listbox(root, height=5,selectmode='multiple')
listbox.pack()

listbox.insert(tk.END, "Item 1")
listbox.insert(tk.END, "Item 2")
listbox.insert(tk.END, "Item 3")
listbox.insert(tk.END, "Item 4")
listbox.insert(tk.END, "Item 5")

button = tk.Button(root, text="Show selection", command=show_selection)
button.pack()

label = tk.Label(root, text="")
label.pack()

root.mainloop()