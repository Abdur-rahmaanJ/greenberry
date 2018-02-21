from tkinter import * 
from tkinter import filedialog
from greenBerry import greenBerry_eval

file_dir = ""

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
        print("="*25)

root = Tk()
top = Frame(root)
top.pack(fill=BOTH, expand=0)

bottom = Frame(root)
bottom.pack()

ex = Files(root)
ex.pack(side="bottom")

root.geometry("600x500-600-150")
root.mainloop()
