from tkinter import * 
from tkinter import filedialog
from greenBerry import greenBerry_eval

class Files(Frame):
    global file_text

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
        fileMenu.add_command(label="Save As", command = self.save_command)
        fileMenu.add_command(label="Open", command = self.onOpen)
        menubar.add_cascade(label="File", menu=fileMenu)

        runMenu.add_command(label="Run", command = self.run_command)
        menubar.add_cascade(label="Run", menu=runMenu, command = self.onOpen)        

        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)

    def onOpen(self):
        ftypes = [('greenBerry files', '*.gb'), ('All files', '*')]
        dlg = filedialog.Open(self, filetypes = ftypes)
        fl = dlg.show()

        if fl != '':
            self.txt.delete('1.0', END)
            text = self.readFile(fl)
            self.txt.insert(END, text)

    def readFile(self, filename):
        f = open(filename, "r")
        text = f.read()
        return text

    def save_command(self):
        file = filedialog.asksaveasfile(mode='w')
        if file != None:
                data = self.txt.get('1.0', END+'-1c')
                file.write(data)
                file.close()

    def run_command(self):
        x = self.txt.get('1.0', END+'-1c')
            
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
