from tkinter import * 
from tkinter import filedialog
from greenBerry import greenBerry_eval

file_dir = ""
old_tags1 = [""]
old_tags2 = []
times_run = 0
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

    def initUI(self):

        self.parent.title("greenBerry IDE")
        self.pack(fill=BOTH, expand=1)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        runMenu = Menu(menubar)
        fileMenu.add_command(label="Save", command = self.save_command, accelerator="Ctrl+S")
        fileMenu.add_command(label="Save As", command = self.save_as_command, accelerator="Ctrl+Shift+S")
        fileMenu.add_command(label="Open", command = self.onOpen, accelerator="Ctrl+O")
        menubar.add_cascade(label="File", menu=fileMenu)

        runMenu.add_command(label="Run", command = self.run_command, accelerator="F5")
        menubar.add_cascade(label="Run", menu=runMenu, command = self.onOpen)        

        self.bind_all("<F5>", self.run_command)
        self.bind_all("<Control-o>", self.onOpen)
        self.bind_all("<Control-s>", self.save_command)
        self.bind_all("<Control-S>", self.save_as_command)
        self.bind_all("<Key>", self.color_text)

        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)
        
    def onOpen(self, event=0):
        global file_dir
        
        ftypes = [("greenBerry files", "*.gb"), ("All files", "*")]
        file = filedialog.askopenfile(filetypes = ftypes)

        if file != None:
            ile_dir = file.name
            self.parent.title("greenBerry IDE" + " - " + file.name.replace("/", "\\"))
            self.txt.delete("1.0", END+"-1c")
            text = self.readFile(file.name)
            self.txt.insert(END, text)
            self.color_text()

    def readFile(self, filename):
        f = open(filename, "r")
        text = f.read()
        return text

    def save_command(self, event=0):
        global file_dir
        
        try:
            self.readFile(file_dir)
            
            with open(file_dir, "w") as file:
                file.write(self.txt.get("1.0", END+"-1c"))
        except:
            self.save_as_command()

    def save_as_command(self, event=0):
        global file_dir
        
        file = filedialog.asksaveasfile(mode="w", defaultextension=".gb", filetypes=(("greenBerry files", "*.gb"), ("All files", "*")))
        if file != None:
            self.parent.title("greenBerry IDE" + " - " + file.name.replace("/", "\\"))
            file_dir = file.name
            data = self.txt.get("1.0", END+"-1c")
            file.write(data)
            file.close()
    
    def run_command(self, event=0):
        x = self.txt.get("1.0", END+"-1c")
            
        greenBerry_eval(x)
        print("="*30)

    def color_text(self, event=0):
        global old_tags1, old_tags2
        global times_run

        times_run += 1
                         
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
                    
        old_i = ["", ":", "1.0"]
        old_tag = ""
        if len(old_tags1) <= 2:
            old_tags1 *= len(words)
        tag_index = -1

        for i in words:
            
            i1 = i
            i = i.split()
            tag_index += 1
            
            if len(i) < 3:
                i.insert(0, " ")

            if len(old_i) < 3:
                old_i.insert(0, " ")

            if i[0] in color1:
                self.txt.tag_remove(old_tags1[tag_index], old_i[2], str(i[2].split(".")[0]) + "." + str(int(i[2].split(".")[1])+len(i[0])))
                self.txt.tag_add("color1", str(i[2].split(".")[0]) + "." + str(int(i[2].split(".")[1])-len(i[0])), i[2])
                self.txt.tag_config("color1", foreground="#9a1777")
                old_tags2.append("color1")
                
            elif i[0] in color2:
                self.txt.tag_remove(old_tags1[tag_index], old_i[2], str(i[2].split(".")[0]) + "." + str(int(i[2].split(".")[1])+len(i[0])))
                self.txt.tag_add("color2", str(i[2].split(".")[0]) + "." + str(int(i[2].split(".")[1])-len(i[0])), i[2])
                self.txt.tag_config("color2", foreground="orange")
                old_tags2.append("color2")
                
            elif i[0] in color3:
                self.txt.tag_remove(old_tags1[tag_index], old_i[2], str(i[2].split(".")[0]) + "." + str(int(i[2].split(".")[1])+len(i[0])))
                self.txt.tag_add("color3", str(i[2].split(".")[0]) + "." + str(int(i[2].split(".")[1])-len(i[0])), i[2])
                self.txt.tag_config("color3", foreground="#e60000")
                old_tags2.append("color3")

            elif i[0][0] in color4:
                self.txt.tag_remove(old_tags1[tag_index], old_i[2], str(i[2].split(".")[0]) + "." + str(int(i[2].split(".")[1])+len(i[0])))
                self.txt.tag_add("color4", str(i[2].split(".")[0]) + "." + str(int(i[2].split(".")[1])-len(i[0])), str(i[2].split(".")[0]) + "." + str(int(i[2].split(".")[1])-len(i[0].split("@")[1])))
                self.txt.tag_config("color4", foreground="orange")
                old_tags2.append("color4")

            elif i[0] in color5:
                self.txt.tag_remove(old_tags1[tag_index], old_i[2], str(i[2].split(".")[0]) + "." + str(int(i[2].split(".")[1])+len(i[0])))
                self.txt.tag_add("color5", str(i[2].split(".")[0]) + "." + str(int(i[2].split(".")[1])-len(i[0])), i[2])
                self.txt.tag_config("color5", foreground="#00cc00")
                old_tags2.append("color5")

            else:
                self.txt.tag_remove(old_tags1[tag_index], old_i[2], str(i[2].split(".")[0]) + "." + str(int(i[2].split(".")[1])+len(i[0])))
                self.txt.tag_add("color", str(i[2].split(".")[0]) + "." + str(int(i[2].split(".")[1])-len(i[0])), i[2])
                self.txt.tag_config("color", foreground="black")
                old_tags2.append("color")
                
            old_i = i1
            old_i = old_i.split()

        old_tags1 = old_tags2 + [""]
        old_tags2 = []

root = Tk()
top = Frame(root)
top.pack(fill=BOTH, expand=0)

bottom = Frame(root)
bottom.pack()

ex = Files(root)
ex.pack(side="bottom")

root.geometry("600x500-600-150")
root.mainloop()
