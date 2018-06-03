from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from greenBerry import greenBerry_eval

file_dir = ""
old_text = ""
color1 = ["var", "print", "set", "debug", "plot"]
color2 = ["string", "eval", "times", "action", "of", "to", "attribute",
          "bool"]
color3 = ["=", "<", "<=", ">", ">=", "if", "for"]
color4 = ["@"]
color5 = ["make", "see", "add", "class", "func", "call"]

class Files(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)   

        self.parent = parent        
        self.initUI()
        parent.protocol("WM_DELETE_WINDOW", self.wclose)

    def initUI(self):
        global old_text

        self.parent.title("greenBerry IDE - Untitlted")
        self.pack(fill=BOTH, expand=1)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        runMenu = Menu(menubar)
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

        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)
        old_text = self.txt.get("1.0", END+"-1c")

    def key_pressed(self, event=0):
        self.color_text() #run syntax highlighting
        
        global old_text

        a = self.parent.title()

        if self.txt.get("1.0", END+"-1c") != old_text and a[0] != "*":
            self.parent.title("*" + self.parent.title())
            
        elif self.txt.get("1.0", END+"-1c") == old_text and a[0] == "*":
            self.parent.title(self.parent.title()[1:])
                    
    def open_file(self, event=0):
        global file_dir, old_text

        self.txt.delete(INSERT) #Ctrl+o causes a new line so we need to delete it
        
        ftypes = [("greenBerry files", "*.gb"), ("All files", "*")]
        file = filedialog.askopenfile(filetypes = ftypes)

        if file != None:
            file_dir = file.name
            self.parent.title("greenBerry IDE" + " - " + file.name.replace("/", "\\"))
            self.txt.delete("1.0", END+"-1c")
            text = self.read_file(file.name)
            self.txt.insert(END, text)
            old_text = self.txt.get("1.0", END+"-1c")
            self.key_pressed()

    def read_file(self, filename):
        f = open(filename, "r")
        text = f.read()
        return text

    def save_file(self, event=0):
        global file_dir, old_text
        
        try:
            
            self.read_file(file_dir)
            
            with open(file_dir, "w") as file:
                file.write(self.txt.get("1.0", END+"-1c"))
                file.close()
                old_text = self.txt.get("1.0", END+"-1c")
                self.key_pressed()

        except:
            self.save_as_command()

    def save_as_command(self, event=0):
        global file_dir, old_text
        
        file = filedialog.asksaveasfile(mode="w", defaultextension=".gb", filetypes=(("greenBerry files", "*.gb"), ("All files", "*")))
        if file != None:
            self.parent.title("greenBerry IDE" + " - " + file.name.replace("/", "\\"))
            file_dir = file.name
            data = self.txt.get("1.0", END+"-1c")
            file.write(data)
            file.close()
            old_text = self.txt.get("1.0", END+"-1c")
    
    def run_command(self, event=0):
        global file_dir, old_text
        
        x = self.txt.get("1.0", END+"-1c")

        if x == old_text:
            greenBerry_eval(self.read_file(file_dir))
            print("="*30)
            
        elif messagebox.askokcancel("Save before run", "Your file must be saved before running.\nPress OK to save.") == True:
            self.save_file()
            try:
                greenBerry_eval(self.read_file(file_dir))
                print("="*30)
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
        file_text = self.txt.get("1.0", END+"-1c") + " "
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
                
root = Tk()
top = Frame(root)
top.pack(fill=BOTH, expand=0)

bottom = Frame(root)
bottom.pack()

ex = Files(root)
ex.pack(side="bottom")

root.geometry("600x500-600-150")
root.mainloop()
