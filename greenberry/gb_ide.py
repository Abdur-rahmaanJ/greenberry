import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import tkinter.scrolledtext as tkst
import subprocess

color1 = ["var", "print", "set", "debug", "plot"]
color2 = ["string", "eval", "times", "action", "attribute",
          "bool"]
color3 = ["=", "<", "<=", ">", ">=", "if", "for"]
color4 = ["@"]
color5 = ["make", "see", "add", "class", "func", "call"]


###### needed for line numbers ######
class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        self.delete("all")

        i = self.textwidget.index("@0,0")

        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tkst.ScrolledText.__init__(self, *args, **kwargs)

        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        try:
            cmd = (self._orig,) + args
            result = self.tk.call(cmd)

            if (args[0] in ("insert", "replace", "delete") or 
                args[0:3] == ("mark", "set", "insert") or
                args[0:2] == ("xview", "moveto") or
                args[0:2] == ("xview", "scroll") or
                args[0:2] == ("yview", "moveto") or
                args[0:2] == ("yview", "scroll")
            ):
                self.event_generate("<<Change>>", when="tail")

            return result
        
        except: # this prevents error '_tkinter.TclError: text doesn't contain any characters tagged with "sel"'
            pass
###### needed for line numbers ######


class Files(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)   

        self.parent = parent        
        parent.protocol("WM_DELETE_WINDOW", self.wclose)

        self.parent.title("greenBerry IDE - Untitled")
        self.pack(fill="both", expand=True)

        menubar = tk.Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = tk.Menu(menubar)
        runMenu = tk.Menu(menubar)
        fileMenu.add_command(label="Save", command = self.save_file, accelerator="Ctrl+S")
        fileMenu.add_command(label="Save As", command = self.save_as_command, accelerator="Ctrl+Shift+S")
        fileMenu.add_command(label="Open", command = self.open_file, accelerator="Ctrl+O")
        menubar.add_cascade(label="File", menu=fileMenu)

        runMenu.add_command(label="Run", command = self.run_command, accelerator="F5")
        menubar.add_cascade(label="Run", menu=runMenu, command = self.open_file)        

        self.bind_all("<F5>", self.run_command)
        self.bind_all("<Control-o>", self.open_file)
        self.bind_all("<Control-s>", self.save_file)
        self.bind_all("<Control-S>", self.save_as_command)
        self.bind_all("<Key>", self.key_pressed)

        self.run_button = tk.Button(root, command=self.run_command)
        self.run_photo = tk.PhotoImage(file="../docs/run_button.png")
        self.run_button.config(image=self.run_photo, height=20, width=20)
        self.run_button.pack()

        self.txt = CustomText(self)
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.txt)

        self.linenumbers.pack(side="left", fill="y")
        self.txt.pack(side="right", fill="both", expand=True)

        self.txt.bind("<<Change>>", self._on_change)
        self.txt.bind("<Configure>", self._on_change)

        self.old_text = self.txt.get("1.0", "end"+"-1c")
        self.file_dir = ""

        self.first = True

    def _on_change(self, event):
        self.linenumbers.redraw()
        
    def _on_change2(self, event):
            self.linenumbers2.redraw()
        
    def key_pressed(self, event=0):
        self.color_text() #run syntax highlighting
        
        a = self.parent.title()

        if self.txt.get("1.0", "end"+"-1c") != self.old_text and a[0] != "*":
            self.parent.title("*" + self.parent.title())
            
        elif self.txt.get("1.0", "end"+"-1c") == self.old_text and a[0] == "*":
            self.parent.title(self.parent.title()[1:])

        self.txt.yview_pickplace("insert")
                    
    def open_file(self, event=0):
        self.txt.delete("insert") #Ctrl+o causes a new line so we need to delete it
        
        ftypes = [("greenBerry files", "*.gb"), ("All files", "*")]
        file = filedialog.askopenfile(filetypes = ftypes)

        if file != None:
            self.file_dir = file.name
            self.parent.title("greenBerry IDE" + " - " + file.name.replace("/", "\\"))
            self.txt.delete("1.0", "end"+"-1c")
            text = self.read_file(file.name)
            self.txt.insert("end", text)
            self.old_text = self.txt.get("1.0", "end"+"-1c")
            self.key_pressed()

    def read_file(self, filename):
        f = open(filename, "r")
        text = f.read()
        return text

    def save_file(self, event=0):
        try:            
            with open(self.file_dir, "w") as file:
                file.write(self.txt.get("1.0", "end"+"-1c"))
                file.close()
                self.old_text = self.txt.get("1.0", "end"+"-1c")
                self.key_pressed()
        except:
            self.save_as_command()

    def save_as_command(self, event=0):
        file = filedialog.asksaveasfile(mode="w", defaultextension=".gb", filetypes=(("greenBerry files", "*.gb"), ("All files", "*")))
        if file != None:
            self.parent.title("greenBerry IDE" + " - " + file.name.replace("/", "\\"))
            self.file_dir = file.name
            data = self.txt.get("1.0", "end"+"-1c")
            file.write(data)
            file.close()
            self.old_text = self.txt.get("1.0", "end"+"-1c")
    
    def run_command(self, event=0):
        x = self.txt.get("1.0", "end"+"-1c")

        if x == self.old_text and x != "":
            if self.first == True:
                self.outwin = tk.Toplevel(root)
                self.outwin.title("greenBerry IDE - output")
                self.outwin.geometry("600x640")
                
                self.txtout = CustomText(self.outwin)
                
                self.linenumbers2 = TextLineNumbers(self.outwin, width=30)
                self.linenumbers2.attach(self.txtout)

                self.linenumbers2.pack(side="left", fill="y")
                self.txtout.pack(fill="both", expand=True)

                self.txtout.bind("<<Change>>", self._on_change2)
                self.txtout.bind("<Configure>", self._on_change2)
            
            proc = subprocess.Popen(["python", "-c", "import greenBerry; greenBerry.greenBerry_eval(\"\"\"{0}\"\"\")".format(self.read_file(self.file_dir))], stdout=subprocess.PIPE)
            out = proc.communicate()[0][:-2]
            
            self.txtout.config(state="normal")
            if self.first != True:
                self.txtout.insert("end", "\n"+"="*25+"NEW RUN"+"="*25+"\n")
            else:
                self.first = False
            self.txtout.insert("end", out)
            self.txtout.config(state="disabled")

            self.txtout.tag_add("colorout", "1.0", "end")
            self.txtout.tag_config("colorout", foreground="blue")

            self.txtout.yview_pickplace("end")
            
            
        elif messagebox.askokcancel("Save before run", "Your file must be saved before running.\nPress OK to save.") == True:
            self.save_file()
            try:
                if self.first == True:
                    self.outwin = tk.Toplevel(root)
                    self.outwin.title("greenBerry IDE - output")
                    self.outwin.geometry("600x640")
                    
                    self.txtout = CustomText(self.outwin)
                    
                    self.linenumbers2 = TextLineNumbers(self.outwin, width=30)
                    self.linenumbers2.attach(self.txtout)

                    self.linenumbers2.pack(side="left", fill="y")
                    self.txtout.pack(fill="both", expand=True)

                    self.txtout.bind("<<Change>>", self._on_change2)
                    self.txtout.bind("<Configure>", self._on_change2)
                
                proc = subprocess.Popen(["python", "-c", "import greenBerry; greenBerry.greenBerry_eval(\"\"\"{0}\"\"\")".format(self.read_file(self.file_dir))], stdout=subprocess.PIPE)
                out = proc.communicate()[0][:-2]
                
                self.txtout.config(state="normal")
                if self.first != True:
                    self.txtout.insert("end", "\n"+"="*25+"NEW RUN"+"="*25+"\n")
                else:
                    self.first = False
                self.txtout.insert("end", out)
                self.txtout.config(state="disabled")

                self.txtout.tag_add("colorout", "1.0", "end")
                self.txtout.tag_config("colorout", foreground="blue")

                self.txtout.yview_pickplace("end")
            
            except:
                self.run_command()

    def wclose(self, event=0):
        if self.parent.title()[0] == "*":
            save = messagebox.askyesnocancel("Save file", "You have unsaved changes.\nDo you want to save before closing?")

            if save == True:
                self.save_file()
                if self.parent.title()[0] == "*":
                    self.wclose()
                else:
                    root.destroy()

            elif save == False:
                root.destroy()
        else:
            root.destroy()
        

    def color_text(self, event=0):         
        file_text = self.txt.get("1.0", "end"+"-1c") + " "
        words = []
        line = 1
        column = -1
        word = ""

        for char in file_text:
            word += char
            column += 1
            if char == "\n":
                words.append(word[:-1] + " : " + str(line) + "." + str(column))
                word = ""
                line += 1
                column = -1

            if char == " ":
                words.append(word[:-1] + " : " + str(line) + "." + str(column))
                word = ""

        for tag in self.txt.tag_names(): #deletes all tags so it can refresh them later
            self.txt.tag_delete(tag)

        for i in words:
            
            i = i.split()
            
            if len(i) < 3:
                i.insert(0, " ")

            if i[0] in color1:
                self.txt.tag_add("color1", str(i[2].split(".")[0]) + "." + str(int(i[2].split(".")[1])-len(i[0])), i[2])
                self.txt.tag_config("color1", foreground="#9a1777")
                
            elif i[0] in color2:
                self.txt.tag_add("color2", str(i[2].split(".")[0]) + "." + str(int(i[2].split(".")[1])-len(i[0])), i[2])
                self.txt.tag_config("color2", foreground="orange")
                
            elif i[0] in color3:
                self.txt.tag_add("color3", str(i[2].split(".")[0]) + "." + str(int(i[2].split(".")[1])-len(i[0])), i[2])
                self.txt.tag_config("color3", foreground="#e60000")

            elif i[0][0] in color4:
                self.txt.tag_add("color4", str(i[2].split(".")[0]) + "." + str(int(i[2].split(".")[1])-len(i[0])), str(i[2].split(".")[0]) + "." + str(int(i[2].split(".")[1])-len(i[0])+1))
                self.txt.tag_config("color4", foreground="orange")

            elif i[0] in color5:
                self.txt.tag_add("color5", str(i[2].split(".")[0]) + "." + str(int(i[2].split(".")[1])-len(i[0])), i[2])
                self.txt.tag_config("color5", foreground="#00cc00")

root = tk.Tk()

ex = Files(root)
ex.pack(side="bottom")

root.geometry("600x640")
root.iconbitmap(default='../docs/favicon.ico')

root.mainloop()
