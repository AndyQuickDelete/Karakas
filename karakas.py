from tkinter import *
from tkinter import font
from tkinter import ttk
from wordhoard import Synonyms
import sqlite3
import sys
import os
from threading import *
import platform

if platform.system() == 'Darwin':
    from Cocoa import NSApplication, NSImage
    if getattr(sys, 'frozen', False):
        connection = sqlite3.connect(os.path.join(sys._MEIPASS, "starsky.db"), check_same_thread=False)
    else:
        connection = sqlite3.connect("starsky.db", check_same_thread=False)
        
if platform.system() == 'Windows':
    connection = sqlite3.connect("starsky.db", check_same_thread=False)

cursor = connection.cursor()


def refresh():
    root.update()
    root.after(1000, refresh)


def display_karakas(event):
    listbox1.delete(0, END)
    value = n.get().strip()
    if value == "--- ---":
        n.set('')
    else:
        for row in cursor.execute("SELECT * FROM karakas WHERE sign_planet_house=?", (value, )):
            listbox1.insert(END, row[0])
        listbox1.insert(END, "")
        refresh()


def related_synonyms(output):
    synonym = Synonyms(output)
    listbox3.delete(0, END)
    results = synonym.find_synonyms()
    if results == "" or results == [] or results == None or "No synonyms" in results or "Please verify" in results:
        listbox3.insert(END, "No synonyms for this selection")
    else:
        for line in results: # for i, line in enumerate(results):
            listbox3.insert(END, line)
        listbox3.insert(END, "")
        listbox3.insert(END, "")
        refresh()

    
def get_related_karakas(event):
    listbox2.delete(0, END)
    index = listbox1.curselection()[0]
    output = listbox1.get(index)
    value = output.strip()
    value = value[:4]
    
    for row in cursor.execute("SELECT * FROM karakas WHERE karaka LIKE '%'||?||'%'", (value, )):
        mystr = row[0] + " - " + row[1]
        listbox2.insert(END, mystr)
    listbox2.insert(END, "")
    listbox2.insert(END, "")
    refresh()

    mythread = Thread(target=related_synonyms, args=(output,))
    mythread.start()

    
def display_wordhoard(event):
    index = listbox3.curselection()[0]
    output = listbox3.get(index)
    value = output.strip()
    value = value[:4]
            
    listbox2.delete(0, END)
            
    for row in cursor.execute("SELECT * FROM karakas WHERE karaka LIKE '%'||?||'%'", (value, )):
        mystr = row[0] + " - " + row[1]
        listbox2.insert(END, mystr)    
    listbox2.insert(END, "")
    listbox2.insert(END, "")
    refresh()

    mythread = Thread(target=related_synonyms, args=(output,))
    mythread.start()

def search(event):
    listbox2.delete(0, END)
    output = entry.get()
    value = output.strip()
    value = value[:4]
    
    for row in cursor.execute("SELECT * FROM karakas WHERE karaka LIKE '%'||?||'%'", (value, )):
        mystr = row[0] + " - " + row[1]
        listbox2.insert(END, mystr)
    listbox2.insert(END, "")
    listbox2.insert(END, "")
    
    entry.delete(0, END)
    refresh()



root = Tk()

if platform.system() == 'Darwin':
    if getattr(sys, 'frozen', False):
        ns_application = NSApplication.sharedApplication()
        logo_ns_image = NSImage.alloc().initByReferencingFile_(os.path.join(sys._MEIPASS, "northstar.icns"))
        ns_application.setApplicationIconImage_(logo_ns_image)
    else:
        ns_application = NSApplication.sharedApplication()
        logo_ns_image = NSImage.alloc().initByReferencingFile_("northstar.icns")
        ns_application.setApplicationIconImage_(logo_ns_image)

if platform.system() == 'Windows':
    root.wm_iconbitmap("northstar.ico")

root.geometry("700x400")
root.title("Karakas")

if platform.system() == 'Darwin':
    if getattr(sys, 'frozen', False):
        root.option_readfile(os.path.join(sys._MEIPASS, "optionDB"))
    else:
        root.option_readfile("optionDB")
        
if platform.system() == 'Windows':
    root.option_readfile("optionDB")
    
root.option_add("*selectBackground", "#5db2ff")
root.option_add("*selectForeground", "white")
bigfont = font.Font(family="Segoe UI", size=13)
root.option_add("*TCombobox*Listbox*Font", bigfont)

frame = Frame(root, width=640)
n = StringVar(value='Select a sign, planet or house to view it\'s karakas') 
karakas = ttk.Combobox(frame, textvariable=n)
karakas['values'] = (
    'Aries', 
    'Taurus',
    'Gemini',
    'Cancer',
    'Leo',
    'Virgo',
    'Libra',
    'Scorpio',
    'Sagittarius',
    'Capricorn',
    'Aquarius',
    'Pisces',
    '--- ---',
    'Sun', 
    'Moon',
    'Mars',
    'Mercury',
    'Jupiter',
    'Venus',
    'Saturn',
    'Rahu',
    'Ketu',
    '--- ---',
    'House 1', 
    'House 2',
    'House 3',
    'House 4',
    'House 5',
    'House 6',
    'House 7',
    'House 8',
    'House 9',
    'House 10',
    'House 11',
    'House 12')
karakas.bind("<<ComboboxSelected>>", display_karakas)
karakas.pack(fill=BOTH, expand=True)
frame.pack(fill=X)

frame = Frame(root)

scrollbar1 = Scrollbar(frame, orient=VERTICAL)
scrollbar1.pack(side=LEFT, fill=Y)
listbox1 = Listbox(frame, selectmode=SINGLE)
listbox1.pack(side=LEFT, fill=BOTH, expand=True)
scrollbarx1 = Scrollbar(listbox1, orient=HORIZONTAL)
scrollbarx1.pack(side=BOTTOM, fill=X)
listbox1.bind('<Double-1>', get_related_karakas)
listbox1.config(yscrollcommand=scrollbar1.set, xscrollcommand=scrollbarx1.set)
scrollbar1.config(command=listbox1.yview)
scrollbarx1.config(command=listbox1.xview)

scrollbar2 = Scrollbar(frame, orient=VERTICAL)
scrollbar2.pack(side=LEFT, fill=Y)
listbox2 = Listbox(frame)
listbox2.pack(side=LEFT, fill=BOTH, expand=True)
scrollbarx2 = Scrollbar(listbox2, orient=HORIZONTAL)
scrollbarx2.pack(side=BOTTOM, fill=X)
listbox2.config(yscrollcommand=scrollbar2.set, xscrollcommand=scrollbarx2.set)
scrollbar2.config(command=listbox2.yview)
scrollbarx2.config(command=listbox2.xview)

scrollbar3 = Scrollbar(frame, orient=VERTICAL)
scrollbar3.pack(side=LEFT, fill=Y)
listbox3 = Listbox(frame)
listbox3.pack(side=LEFT, fill=BOTH, expand=True)
scrollbarx3 = Scrollbar(listbox3, orient=HORIZONTAL)
scrollbarx3.pack(side=BOTTOM, fill=X)
listbox3.bind('<Double-1>', display_wordhoard)
listbox3.config(yscrollcommand=scrollbar3.set, xscrollcommand=scrollbarx3.set)
scrollbar3.config(command=listbox3.yview)
scrollbarx3.config(command=listbox3.xview)

frame.pack(fill=BOTH, expand=True)

frame = Frame(root)

label = Label(frame, text="Enter a keyword and hit <return>")
label.pack(side=LEFT)
entry = Entry(frame)
entry.pack(fill=X, expand=True)
entry.bind("<Return>", search)
frame.pack(fill=X)

root.mainloop()
