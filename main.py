import ttkbootstrap as ttk
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import tkinterdnd2
from pipeline_flat import run


class DropZone_Frame(ttk.Frame):
    def __init__(self,parent,label_text,**kwargs):
        super().__init__(parent, **kwargs)
        self.label_text = label_text
        self.full_path = ""
        self.file_path_var = tk.StringVar(value="Drag & Drop\nor click to browse")
        self.widgets()
        self.placement()
        self.bindings()

    def widgets(self):
        self.header_lbl = ttk.Label(self, text=self.label_text, font=("Helvetica", 12, "bold"), anchor='center')
        self.drop_lbl = ttk.Label(self, textvariable=self.file_path_var, anchor="center", width=30)
        

    def placement(self):
        self.header_lbl.grid(row=0, column=0, pady=(0, 5), sticky="ew")
        self.drop_lbl.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def bindings(self):
        self.drop_lbl.drop_target_register(tkinterdnd2.DND_FILES)
        self.drop_lbl.dnd_bind("<<Drop>>", self.on_drop)
        self.drop_lbl.bind("<Button-1>", self.on_browse)

    #event handlers
    def on_drop(self, event):
        path = event.data.strip("{}")
        if path.endswith(".docx"):
            self.full_path = path
            p = Path(path)
            self.file_path_var.set(f"{p.parent.name}/{p.name}")

    def on_browse(self, event):
        path = filedialog.askopenfilename(filetypes=[("Word Documents", "*.docx")])
        if path:
            self.full_path = path
            p = Path(path)
            self.file_path_var.set(f"{p.parent.name}/{p.name}")


class MainApp(tkinterdnd2.Tk):
    def __init__(self):
        super().__init__()
        ttk.Style(theme="pulse")
        self.title("doc-x-diff")
        self.geometry("600x320")
        self.widgets()
        self.placement()
       

    def widgets(self):
        self.old_zone = DropZone_Frame(self, "Old Version", bootstyle="primary", padding=10)
        self.new_zone = DropZone_Frame(self, "New Version", bootstyle="primary", padding=10)
        self.compare_btn = ttk.Button(self, text="Generate Diff", bootstyle="primary", command=self.on_compare)
    
    def placement(self):
        self.old_zone.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.new_zone.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.compare_btn.grid(row=1, column=0, columnspan=2, pady=10)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def on_compare(self):
        save_path = self.on_save()
        if save_path:
            run(self.old_zone.full_path, self.new_zone.full_path, save_path)
            messagebox.showinfo("Success", f"Diff file saved to:\n{save_path}")
        
        

    def on_save(self):
        return filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Word Documents", "*.docx")]
        )


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
