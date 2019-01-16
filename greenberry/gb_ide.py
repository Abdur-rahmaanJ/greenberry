import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
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


class MessageBox(tk.simpledialog.Dialog):
    """Similar to tk.messagebox but updates parent if destroyed"""
    
    def __init__(self, parent, title, message):
        self.messageText = message
        tk.simpledialog.Dialog.__init__(self, parent, title)
        
    def body(self, master):
        self.frame = tk.Frame(master)
        self.message = tk.Message(self.frame, text=self.messageText)
        self.btn_cancel = tk.Button(
            self.frame, text="Cancel", command=self.cancel
        )
        self.bind('<Return>', self.cancel)
        
        self.frame.grid(column=0, row=0, sticky="NSEW")
        self.message.grid(column=0, row=1)
        self.btn_cancel.grid(column=0, row=2)
        
        return self.btn_cancel
        
    def destroy(self):
        """Update parent when destroyed"""
        self.parent.messageOpen = False
        super(MessageBox, self).destroy()
        
    def buttonbox(self):
        """Override default simpledialog.Dialog buttons"""
        pass
        

class SearchDialog(tk.simpledialog.Dialog):
    """Dialog for text find and replace"""
    
    def __init__(self, parent, txt, old_text, title="Find and replace"):
        self.txt = txt
        self.messageOpen = False
        self.messageRef = None
        tk.simpledialog.Dialog.__init__(self, parent, title)
    
    def body(self, master):
        """Create dialog body, return widget with initial focus"""
        
        # Vars
        self.search_text = tk.StringVar()
        self.replace_text = tk.StringVar()
        self.isCaseSensitive = tk.IntVar()
        self.isCaseSensitive.set(1)
        self.isBackward = tk.IntVar()
        self.isRegExp = tk.IntVar()
        
        # Widgets
        self.frame = tk.Frame(master)
        self.frame_btn = tk.Frame(self.frame)
        self.frame_check = tk.Frame(self.frame)
        self.frame_entry = tk.Frame(self.frame)
        self.search_entry = tk.Entry(
            self.frame_entry, width=20, textvariable=self.search_text
        )
        self.replace_entry = tk.Entry(
            self.frame_entry, width=20, textvariable=self.replace_text
        )
        self.check_case = tk.Checkbutton(
            self.frame_check, text="Case sensitive", var=self.isCaseSensitive
        )
        self.check_search_backward = tk.Checkbutton(
            self.frame_check, text="Search backward", var=self.isBackward
        )
        self.check_regexp = tk.Checkbutton(
            self.frame_check, text="Use regular expression", var=self.isRegExp
        )
        self.btn_search = tk.Button(
            self.frame_btn, text="Find", command=self.search
        )
        self.btn_replace = tk.Button(
            self.frame_btn, text="Replace", command=self.replace
        )
        self.btn_search_and_replace = tk.Button(
            self.frame_btn, text="Find and Replace", command=self.search_and_replace
        )
        self.btn_cancel = tk.Button(
            self.frame, text="Cancel", command=self.cancel
        )
        
        # Frame placements
        self.frame.grid(column=0, row=0, sticky="NSEW")
        self.btn_cancel.grid(column=1, row=1, sticky='E', padx=(4,8), pady=(4,8))
        
        self.frame_entry.grid(column=0, row=0)
        tk.Label(self.frame_entry, text="Find:").grid(column=0, row=0, sticky='W')
        self.search_entry.grid(column=1, row=0)
        tk.Label(self.frame_entry, text="Replace:").grid(column=0, row=1, sticky='W', pady=(6,12))
        self.replace_entry.grid(column=1, row=1, pady=(6,12))
        
        self.frame_btn.grid(column=0, row=1, padx=(8,4), pady=(4,8))
        self.btn_search.grid(column=0, row=0, sticky='W')
        self.btn_replace.grid(column=1, row=0, sticky='W', padx=(2,10))
        self.btn_search_and_replace.grid(column=2, row=0, sticky='E')
        
        self.frame_check.grid(column=1, row=0, pady=(6,12))
        self.check_case.grid(column=0, row=0, sticky='W')
        self.check_search_backward.grid(column=0, row=1, sticky='W')
        self.check_regexp.grid(column=0, row=2, sticky='W')
        
        return self.search_entry
        
    def _createMessage(self, text):
        """Create MessageBox, update state; recreate if already open"""
        if self.messageOpen:
            self._destroyMessage()
        self.messageRef = MessageBox(self, title='', message=text)
        self.messageOpen = True
        
    def _destroyMessage(self):
        """Destroy MessageBox and update message state"""
        if self.messageOpen:
            self.messageRef.destroy()
            self.messageRef = None
            self.messageOpen = False
        
    def _searchData(self):
        """Return snapshot of dialog vars relevant to _search"""
        return {
            'caseSensitive': self.isCaseSensitive.get(),
            'backwards': self.isBackward.get(),
            'regexp': self.isRegExp.get(),
            'search_text': self.search_text.get(),
            'replace_text': self.replace_text.get()
        }
        
    def _search(self, doSearch, doReplace):
        """Internal method to search and/or replace"""
        if not doSearch and not doReplace:
            return
        
        self.txt.tag_configure('found', background='#aaaaaa')
        self.txt.tag_configure('replaced', background='#aaaaaa')
        data = self._searchData()
        n_search = len(data['search_text'])
        n_replace = len(data['replace_text'])
        if doSearch and not n_search > 0:
            return
            
        if doSearch:
            if data['backwards']:
                self.txt.mark_set('search_start', 'insert')
                self.txt.mark_set('search_end', '1.0' + '-1c')
            else:
                self.txt.mark_set('search_start', 'insert')
                self.txt.mark_set('search_end', 'end')
                
            if data['caseSensitive']:
                nocase = 0
            else:
                nocase = 1
            
            start = self.txt.search(
                data['search_text'], 
                self.txt.index('search_start'), 
                stopindex=self.txt.index('search_end'),
                backwards=data['backwards'],
                nocase=nocase,
                regexp=data['regexp']
            )
            if start:
                end = start + '+{0}c'.format(n_search)
                self.txt.tag_add('found', start, end)
                if data['backwards']:
                    self.txt.mark_set('insert', start)
                else:
                    self.txt.mark_set('insert', end)
            else: # if no results found
                self._createMessage('No matches found.')
                return

        if doReplace:
            foundRanges = self.txt.tag_ranges('found')
            if not foundRanges:
                # If no 'found' tags, then do a search instead
                self._search(doSearch=True, doReplace=False)
                return
            foundStarts = [idx for i, idx in enumerate(foundRanges) if i % 2 == 0]
            foundEnds   = [idx for i, idx in enumerate(foundRanges) if i % 2 == 1]
            for foundStart, foundEnd in zip(foundStarts, foundEnds):
                self.txt.delete(foundStart, foundEnd)
                self.txt.insert(foundStart, data['replace_text'], ('replaced',))                
    
    def search(self, event=0):
        """Command for Search button"""
        self._search(doSearch=True, doReplace=False)
    
    def replace(self, event=0):
        """Command for Replace button"""
        self._search(doSearch=False, doReplace=True)
    
    def search_and_replace(self, event=0):
        """Command for Search and Replace button"""
        self._search(doSearch=True, doReplace=True)
        
    def destroy(self):
        """Add text tag cleanup to simpledialog.Dialog destroy"""
        self.txt.tag_remove('found', '1.0', 'end')
        self.txt.tag_remove('replaced', '1.0', 'end')
        super(SearchDialog, self).destroy()
        
    def buttonbox(self):
        """Override default simpledialog.Dialog buttons"""
        pass


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
        searchMenu = tk.Menu(menubar)
        fileMenu.add_command(label="Save", command = self.save_file, accelerator="Ctrl+S")
        fileMenu.add_command(label="Save As", command = self.save_as_command, accelerator="Ctrl+Shift+S")
        fileMenu.add_command(label="Open", command = self.open_file, accelerator="Ctrl+O")
        menubar.add_cascade(label="File", menu=fileMenu)

        runMenu.add_command(label="Run", command = self.run_command, accelerator="F5")
        menubar.add_cascade(label="Run", menu=runMenu, command = self.open_file) 
        
        searchMenu.add_command(label="Find and replace", command=self.search_command, accelerator="Ctrl+F")
        menubar.add_cascade(label="Search", menu=searchMenu)       

        self.bind_all("<F5>", self.run_command)
        self.bind_all("<Control-o>", self.open_file)
        self.bind_all("<Control-s>", self.save_file)
        self.bind_all("<Control-S>", self.save_as_command)
        self.bind_all("<Control-f>", self.search_command)
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
            
    def search_command(self, event=0):
        d = SearchDialog(
            self.parent, txt = self.txt, old_text = self.old_text, 
            title="Find and replace"
        )

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
