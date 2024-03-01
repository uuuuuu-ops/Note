import tkinter as tk
from tkinter import ttk, messagebox, font
import json
from ttkbootstrap import Style

# Main window
root = tk.Tk()
root.title("My GUI")
root.geometry("500x500")
style = Style(theme ='journal')
style = ttk.Style()


font_name = tk.StringVar(root)
font_name.set("Arial")
font_size = tk.StringVar(root)
font_size.set("12")

# Function to change font
def change_font():
    selected_font = font_name.get()
    selected_size = font_size.get()

    # Configure font for text areas in each notebook tab
    for tab in notebook.tabs():
        tab_content = notebook.nametowidget(tab)
        for widget in tab_content.winfo_children():
            if isinstance(widget, tk.Text):
                widget.config(font=(selected_font, selected_size))
# Notebook to hold notes
notebook = ttk.Notebook(root)

#load saved notes
notes = {}
try:
    with open ("notes.json") as f:
        notes = json.load(f)
except FileNotFoundError:
    pass

#create notebook to hold notes
notebook = ttk.Notebook(root)
notebook.pack(padx = 10, pady = 10 , fill = tk.BOTH , expand = True)

#func to add notes
def add_note():
    # tab to the notes
    note_frame = ttk.Frame(notebook, padding=10)
    notebook.add(note_frame, text="New note")

    # title and content
    title_label = ttk.Label(note_frame, text="Title:")
    title_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")

    title_entry = ttk.Entry(note_frame, width=40)
    title_entry.grid(row=0, column=1, padx=10, pady=10)

    content_label = ttk.Label(note_frame, text="Content:")
    content_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")

    content_entry = tk.Text(note_frame, width=40, height=10)
    content_entry.grid(row=1, column=1, padx=10, pady=10)

    # func to save note
    def save_note():
        # get content
        title = title_entry.get()
        content = content_entry.get("1.0", tk.END)

        # add note to dictionary
        notes[title] = {"content": content.strip(), "font": {"name": font_name.get(), "size": font_size.get()}}

        # save the notes dictionary to the file
        with open("notes.json", "w") as f:
            json.dump(notes, f)

        # Add the note to the notebook with font settings applied
        note_content = tk.Text(notebook, width=40, height=10, font=(font_name.get(), font_size.get()))
        note_content.insert(tk.END, content)
        notebook.forget(notebook.select())
        notebook.add(note_content, text=title)

    # Add save button to frame
    save_button = ttk.Button(note_frame, text="Save", command=save_note, style=("secondary.TButton"))
    save_button.grid(row=2, column=0, padx=10, pady=10)
def load_notes():
    try:
        with open("notes.json") as f:
            notes = json.load(f)

        for title, data in notes.items():
            if isinstance(data, dict):  # Check if data is a dictionary
                # Retrieve content and font settings
                content = data.get("content", "")
                font_settings = data.get("font", {})
                font_name.set(font_settings.get("name", "Arial"))
                font_size.set(font_settings.get("size", "12"))

                # Add note to the notebook with font settings applied
                note_content = tk.Text(notebook, width=40, height=10, font=(font_name.get(), font_size.get()))
                note_content.insert(tk.END, content)
                notebook.add(note_content, text=title)

    except FileNotFoundError:
        pass
#call load notes when starts app
load_notes()

# Dropdown menu for font selection
font_box = ttk.Combobox(root, textvariable=font_name, values=font.families(), state="readonly", width=20)
font_box.pack(side=tk.LEFT, padx=10, pady=10)
font_box.bind("<<ComboboxSelected>>", lambda event: change_font())

# Dropdown menu for font size selection
size_box = ttk.Combobox(root, textvariable=font_size, values=[8, 10, 12, 14, 16, 18, 20], state="readonly", width=5)
size_box.pack(side=tk.LEFT, padx=10, pady=10)
size_box.bind("<<ComboboxSelected>>", lambda event: change_font())

# Call the change_font function to apply the initial font settings
change_font()

def delete_note():
    #get the current tab index
    current_tab= notebook.index(notebook.select())
    #get title to delete
    note_title = notebook.tab(current_tab,"text")
    #show information
    confirm = messagebox.askyesno("Delete Note",f"Are you sure you want to delete {note_title}?")

    if confirm:
        #Remove
        notebook.forget(current_tab)
        #remove from dictionary
        notes.pop(note_title)
        #Save the dictionary to the file
        with open("notes.json","w") as f:
            json.dump(notes,f)


#Add buttons to the main window
new_button = ttk.Button(root,text="New note",command=add_note,style = ("info.TButton"))
new_button.pack(side=tk.LEFT,padx=10,pady=10)


delete_button = ttk.Button(root,text="Delete note",command=delete_note,style = ("primary.TButton"))
delete_button.pack(side=tk.LEFT,padx=10,pady=10)
root.mainloop()
