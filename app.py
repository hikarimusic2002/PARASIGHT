import os
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import ImageTk ,Image
import torch
import textwrap
import pandas as pd


class App(TkinterDnD.Tk):

    def __init__(self):

        # Initialize
        TkinterDnD.Tk.__init__(self)
        self.title("PARASIGHT")

        # Setup
        self.setup()

    def setup(self):

        # Theme
        theme = os.path.join(os.path.dirname(__file__), "azure.tcl")
        self.tk.call("source", theme)
        self.tk.call("set_theme", "light")

        # Configure
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)
        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=30)

        # Master Frame
        master = Master(self, self)
        master.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Sizegrip
        self.sizegrip = ttk.Sizegrip(self)
        self.sizegrip.grid(row=1, column=1, padx=5, pady=5)

        # Set Minimun Size
        self.minsize(int(self.winfo_screenwidth() * 5 / 6), int(self.winfo_screenheight() * 5 / 6))
        x_coordinate = int(self.winfo_screenwidth() / 12)
        y_coordinate = int(self.winfo_screenheight() / 12)
        self.geometry("+{}+{}".format(x_coordinate, y_coordinate))
        
class Master(ttk.Frame):

    def __init__(self, parent, master):

        # Initialize
        ttk.Frame.__init__(self, parent)
        self.master = master

        # Setup
        self.setup() 

    def setup(self):

        # Configure
        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=0, weight=1, uniform="fred")
        self.columnconfigure(index=1, weight=1, uniform="fred")

        # Drag and Drop
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', lambda e: self.new_image(e.data))

        # Image initial
        self.image_frame_0 = ttk.Frame(self)
        self.image_frame_0.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.image_frame_0.rowconfigure(index=0, weight=1)
        self.image_frame_0.rowconfigure(index=2, weight=1)
        self.image_frame_0.columnconfigure(index=0, weight=1)
        
        self.intro_1 = ttk.Label(self.image_frame_0, text="Please Drag an Image Here")
        self.intro_1.grid(row=0, column=0, padx=5, pady=5, sticky="s")

        self.intro_2 = ttk.Label(self.image_frame_0, text="or")
        self.intro_2.grid(row=1, column=0, padx=5, pady=5)

        self.intro_3 = ttk.Button(self.image_frame_0, text="Open Example")
        self.intro_3.config(command=lambda: self.new_image(os.path.join(os.path.dirname(__file__), "data/images/example.jpg")))
        self.intro_3.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        
        # Image
        self.image_frame = ttk.Frame(self)
        self.image_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.image_frame.rowconfigure(index=0, weight=1)
        self.image_frame.columnconfigure(index=0, weight=1)
        
        self.img_label = tk.Label(self.image_frame)
        self.img_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.image_frame_0.tkraise()
        
        # Result
        self.result_frame = ttk.Frame(self)
        self.result_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.result_frame.rowconfigure(index=1, weight=1)
        self.result_frame.columnconfigure(index=0, weight=1)

        # Option
        self.option_frame = ttk.Frame(self.result_frame)
        self.option_frame.grid(row=0, column=0, sticky="nsew")
        self.option_frame.columnconfigure(index=1, weight=1)

        self.parasite_label = ttk.Label(self.option_frame, text="Parasite:")
        self.parasite_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.parasite_var = tk.StringVar(value="")
        self.parasite_list = [""]
        self.parasite_menu = ttk.OptionMenu(
            self.option_frame, self.parasite_var, *self.parasite_list, command=lambda e: self.new_result
        )
        self.parasite_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.cdc_info_label = ttk.Label(self.option_frame, text="CDC Info:")
        self.cdc_info_label.grid(row=1, column=0, padx=5, pady=5)

        self.cdc_info_frame = ttk.Frame(self.option_frame)
        self.cdc_info_frame.grid(row=1, column=1, sticky="nsew")
        self.cdc_info_var = tk.StringVar(value="disease")
        self.cdc_info_list = ["disease", "diagnosis", "treatment"]
        self.cdc_info_item = {}
        for i, var in enumerate(self.cdc_info_list):
            self.cdc_info_item[i] = ttk.Radiobutton(self.cdc_info_frame)
            self.cdc_info_item[i].config(text=var.capitalize())
            self.cdc_info_item[i].config(variable=self.cdc_info_var, value=var)
            self.cdc_info_item[i].config(command=self.new_result)
            self.cdc_info_item[i].grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
        
        # CDC frame
        self.cdc_frame = {}
        self.cdc_text = {}

        self.cdc_frame[""] = ttk.Frame(self.result_frame)
        self.cdc_frame[""].grid(row=1, column=0, sticky="nsew")
        de_font = font.nametofont("TkDefaultFont")
        for var in self.cdc_info_list:
            self.cdc_frame[var] = ttk.Frame(self.result_frame)
            self.cdc_frame[var].grid(row=1, column=0, sticky="nsew")
            self.cdc_text[var] = ttk.Label(self.cdc_frame[var], font=(de_font, 12))
            self.cdc_text[var].grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.treatment_tree = ttk.Treeview(self.cdc_frame["treatment"], height=5)
        self.treatment_tree.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        #self.scrollbar_y = ttk.Scrollbar(self, orient="vertical")
        #self.scrollbar_y.grid(row=0, column=1, sticky="nsew")
        self.scrollbar_x = ttk.Scrollbar(self.cdc_frame["treatment"], orient="horizontal")
        self.scrollbar_x.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        
        #self.treeview.config(yscrollcommand=self.scrollbar_y.set)
        #self.scrollbar_y.config(command=self.treeview.yview)
        self.treatment_tree.config(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.config(command=self.treatment_tree.xview)

        self.cdc_frame[""].tkraise()
        
        

        # Model
        self.model = torch.hub.load(os.getcwd(), 'custom', source='local', path = "weights", force_reload = True)

        # CDC Info
        self.parasite_info = {}



    def new_image(self, img_path):

        geometry = self.winfo_toplevel().geometry()

        # Input image
        self.img_0 = Image.open(img_path)
        x, y = self.img_0.size
        y = int(900 * y / x)
        x = int(900)
        self.img_0 = self.img_0.resize((x, y))
        self.img = Image.new(self.img_0.mode, (1000, y), (255,255,255))
        self.img.paste(self.img_0, (0,0))

        width = self.img_label.winfo_width()
        height = self.img_label.winfo_height()
        x, y = self.img.size
        zoom = min(width/x, height/y)
        self.img = self.img.resize((int(zoom*x), int(zoom*y)))

        # Inference
        self.res = self.model(self.img, size=640)
        self.res.render()
        self.res_img = Image.fromarray(self.res.imgs[0])

        # Resize
        width = self.img_label.winfo_width()
        height = self.img_label.winfo_height()
        x, y = self.res_img.size
        zoom = min(width/x, height/y)
        self.res_img = self.res_img.resize((int(zoom*x), int(zoom*y)))

        # Show
        self.res_show = ImageTk.PhotoImage(self.res_img)
        self.img_label.config(image=self.res_show)
        self.image_frame.tkraise()
        self.winfo_toplevel().geometry(geometry)

        # Change menu
        self.pred_list = {}
        for i in self.res.pred[0][:, 5].tolist():
            i = int(i)
            if i not in self.pred_list:
                self.pred_list[i] = self.res.names[i]
        self.parasite_list = list(self.pred_list.values())

        self.parasite_var.set("")
        self.parasite_menu["menu"].delete(0, "end")
        if self.parasite_list:
            for par in self.parasite_list:
                self.parasite_menu["menu"].add_command(label=par, command=tk._setit(self.parasite_var, par))
            self.parasite_var.set(self.parasite_list[0])
            self.new_result()

    
    def new_result(self):

        parasite = self.parasite_var.get()
        cdc_info = self.cdc_info_var.get()
        parasite = parasite.replace(" ", "_")

        if not parasite:
            self.cdc_frame[""].tkraise()
            return

        if parasite not in self.parasite_info:
            with open(os.path.join(os.path.dirname(__file__), "CDC/"+parasite+"/disease.txt")) as f:
                #disease = textwrap.fill(f.read(), 80)
                cin = f.read()
                disease = '\n'.join(['\n'.join(textwrap.wrap(line, 80,break_long_words=False, replace_whitespace=False))
                    for line in cin.splitlines()])
            with open(os.path.join(os.path.dirname(__file__), "CDC/"+parasite+"/diagnosis.txt")) as f:
                #diagnosis = textwrap.fill(f.read(), 80)
                cin = f.read()
                diagnosis = '\n'.join(['\n'.join(textwrap.wrap(line, 80,break_long_words=False, replace_whitespace=False))
                    for line in cin.splitlines()])
            with open(os.path.join(os.path.dirname(__file__), "CDC/"+parasite+"/treatment.txt")) as f:
                #treatment = textwrap.fill(f.read(), 80, replace_whitespace=False)
                cin = f.read()
                treatment = '\n'.join(['\n'.join(textwrap.wrap(line, 80,break_long_words=False, replace_whitespace=False))
                    for line in cin.splitlines()])
            table = pd.read_csv(os.path.join(os.path.dirname(__file__), "CDC/"+parasite+"/table.csv"))
            self.parasite_info[parasite] = {"disease":disease, "diagnosis":diagnosis, "treatment":treatment, "table":table}

        for var in self.cdc_info_list:
            self.cdc_text[var].configure(text=self.parasite_info[parasite][var])

        # Treeview
        for item in self.treatment_tree.get_children():
            self.treatment_tree.delete(item)
        self.treatment_tree.config(column=())

        table = self.parasite_info[parasite]["table"]
        width = [100]*len(table.columns)

        self.treatment_tree.config(columns=table.columns.tolist())
        self.treatment_tree.column("#0", anchor="center", minwidth=0, stretch="no")

        for i, col in enumerate(table.columns.tolist()):
            self.treatment_tree.column(col, anchor="center", minwidth=100, width=100)
            self.treatment_tree.heading(col, text=col, anchor="center")
            width[i] = max(width[i],len(col)*10)

        if len(table.columns) == 0 :
            self.treatment_tree.config(columns=[1])
            self.treatment_tree.column(1, anchor="center", minwidth=100, width=100)
            self.treatment_tree.heading(1, text="", anchor="center")

        for i in range(len(table)):
            value = []
            for j in range(len(table.columns)):
                temp = str(table.iloc[i][j])
                value.append(temp)
                width[j] = max(width[j], len(temp)*7+50)
            self.treatment_tree.insert(parent="", index="end", text="", values=value)

        self.treatment_tree.column('#0', minwidth=0, width=0, stretch="no")
        for i, col in enumerate(table.columns.tolist()):
            self.treatment_tree.column(col, minwidth=width[i])

        self.treatment_tree.update()

        self.cdc_frame[cdc_info].tkraise()



if __name__ == "__main__":
    root = App()
    root.mainloop()