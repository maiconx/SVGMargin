import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import messagebox
import os
import shutil
from datetime import datetime

files_dropped = []

def adjust_viewbox_margin(margin, vList_final):
    vList_final[0] = str(float(vList_final[0]) - margin)
    vList_final[1] = str(float(vList_final[1]) - margin)
    vList_final[2] = str(float(vList_final[2]) + 2 * margin)
    vList_final[3] = str(float(vList_final[3]) + 2 * margin)
    return vList_final

def process_files():
    if not files_dropped:
        messagebox.showwarning("Aviso", "Arraste pelo menos um arquivo SVG.")
        return

    try:
        margin = float(entry_margin.get()) if entry_margin.get().strip() else 2.0
    except ValueError:
        margin = 2.0

    create_backup = backup_var.get()

    if create_backup:
        os.makedirs("Backup", exist_ok=True)

    for path in files_dropped:
        if not path.lower().endswith(".svg"):
            continue

        if create_backup:
            filename = os.path.basename(path)
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            backup_name = f"{timestamp}_{filename}"
            backup_path = os.path.join("Backup", backup_name)
            shutil.copy2(path, backup_path)

        with open(path, "rt") as fin:
            data = fin.read()

        char1 = 'viewBox="'
        char2 = '">'
        viewBox = data[data.find(char1) + 9: data.find(char2)]
        vList = viewBox.split()

        vList_final = adjust_viewbox_margin(margin, vList)
        vFinal = ' '.join(vList_final)
        data = data.replace(viewBox, vFinal)

        with open(path, "wt") as fout:
            fout.write(data)

    messagebox.showinfo("Sucesso", "Margin adjustment completed.")

def on_drop(event):
    global files_dropped
    files_dropped = root.tk.splitlist(event.data)
    drop_area.configure(state="normal")
    drop_area.delete("1.0", "end")
    drop_area.insert("1.0", "\n".join(files_dropped))
    drop_area.configure(state="disabled")

# Interface
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = TkinterDnD.Tk()
root.title("SVG Margin Adjuster")
root.geometry("500x350")
root.configure(bg="#222222")

frame = ctk.CTkFrame(master=root, width=480, height=330)
frame.pack(pady=20, padx=10)

label_info = ctk.CTkLabel(master=frame, text="Drag and drop SVG files below", font=("Arial", 16))
label_info.pack(pady=10)

drop_area = ctk.CTkTextbox(master=frame, width=400, height=80)
drop_area.insert("1.0", "Drop SVG files here")
drop_area.configure(state="disabled")
drop_area.pack(pady=5)
drop_area.drop_target_register(DND_FILES)
drop_area.dnd_bind('<<Drop>>', on_drop)

entry_margin = ctk.CTkEntry(master=frame, placeholder_text="Enter margin (default is 2.0)")
entry_margin.configure(width=170)
entry_margin.pack(pady=10)

backup_var = ctk.BooleanVar(value=True)
backup_checkbox = ctk.CTkCheckBox(master=frame, text="Create backup", variable=backup_var)
backup_checkbox.pack(pady=5)

btn_ok = ctk.CTkButton(master=frame, text="OK", command=process_files)
btn_ok.pack(pady=10)

root.mainloop()
