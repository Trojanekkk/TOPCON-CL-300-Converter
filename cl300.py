from os import listdir, chdir, startfile
from os.path import isfile, join, getmtime
from xml.etree import ElementTree as ET
import tkinter as tk

# App config
path_in = "C:/input/"
path_out = "C:/output/"
nsCommon = "{http://www.joia.or.jp/standardized/namespaces/Common}"
nsLM = "{http://www.joia.or.jp/standardized/namespaces/LM}"

# Define Measure class
class Measure:
    def __init__ (self, file, name, surname, id, path_in="input", path_out="output"):
        self.file = file
        tree = ET.parse(join(path_in, file))
        self.root = tree.getroot()

        self.details = {
            'date': self.getObj("./Common/Date", nsCommon).text,
            'time' : self.getObj("./Common/Time", nsCommon).text,
            'measuer_id' : self.getObj("./Common/Patient/ID", nsCommon).text,

            'lensType' : self.getObj("./Measure/LensType", nsLM).text,

            'rSphere' : self.getObj("./Measure/LM/R/Sphere", nsLM).text,
            'rCylinder' : self.getObj("./Measure/LM/R/Cylinder", nsLM).text,
            'rAxis' : self.getObj("./Measure/LM/R/Axis", nsLM).text,
            'rAdd1Unit' : self.getObj("./Measure/LM/R/Add1", nsLM).attrib['unit'],
            'rAdd2Unit' : self.getObj("./Measure/LM/R/Add2", nsLM).attrib['unit'],
            'rHPrism' : self.getObj("./Measure/LM/R/H", nsLM).attrib['Prism'],
            'rVPrism' : self.getObj("./Measure/LM/R/V", nsLM).attrib['Prism'],

            'lSphere' : self.getObj("./Measure/LM/L/Sphere", nsLM).text,
            'lCylinder' : self.getObj("./Measure/LM/L/Cylinder", nsLM).text,
            'lAxis' : self.getObj("./Measure/LM/L/Axis", nsLM).text,
            'lrAdd1Unit' : self.getObj("./Measure/LM/L/Add1", nsLM).attrib['unit'],
            'lAdd2Unit' : self.getObj("./Measure/LM/L/Add2", nsLM).attrib['unit'],
            'lHPrism' : self.getObj("./Measure/LM/L/H", nsLM).attrib['Prism'],
            'lVPrism' : self.getObj("./Measure/LM/L/V", nsLM).attrib['Prism'],

            'patientName' : name,
            'patientSurname' : surname,
            'patientId' : id
        }

    def getObj (self, path, ns):
        return self.root.find(path.replace("/", "/{0}").format(ns))

    def getDetails (self):
        return self.details

# Search for files in input path
chdir(path_in)
files = filter(isfile, listdir(path_in))
files = [join(path_in, f) for f in files if "xml" in f]
files.sort(key=lambda x: getmtime(x), reverse=True)
f = lambda x: x.split(path_in)[1]

# Generate doc - click button event
def generateDoc (event):
    selected = files[lbox.curselection()[0]]
    name = entry_name.get()
    surname = entry_surname.get()
    id = entry_id.get()

    measure = Measure(selected, name, surname, id)
    print(measure.getDetails())

    if len(list(measure.details)) > 0:
        entry_name.delete(0, tk.END)
        entry_surname.delete(0, tk.END)
        entry_id.delete(0, tk.END)
    
def exploreInputPath (event):
    startfile(path_out)

# Create GUI
window = tk.Tk()
window.title("TOPCON CL300 Doc converter - SPEKTRUM Sp. z o.o.")

lbox = tk.Listbox(window, selectmode="SINGLE")

label_name = tk.Label(window, text="Imię")
label_surname = tk.Label(window, text="Nazwisko")
label_id = tk.Label(window, text="PESEL")
entry_name = tk.Entry(window)
entry_surname = tk.Entry(window)
entry_id = tk.Entry(window)
button_submit = tk.Button(window, text="Generuj dokument")
button_explore = tk.Button(window, text="Otwórz folder wyjsciowy")

lbox.grid(row=0, column=0, rowspan=6, padx=10, pady=10)
label_name.grid(row=0, column=1)
entry_name.grid(row=1, column=1, padx=(0, 10))
label_surname.grid(row=2, column=1)
entry_surname.grid(row=3, column=1, padx=(0, 10))
label_id.grid(row=4, column=1)
entry_id.grid(row=5, column=1, padx=(0, 10))
button_submit.grid(pady=(0, 10))
button_explore.grid(pady=(0, 10))

# Feed listbox with files
for file in files:
    lbox.insert(tk.END, f(file))

# Bind actions
button_submit.bind('<Button-1>', generateDoc)
button_explore.bind('<Button-1>', exploreInputPath)

# Begin mainloop
window.mainloop()