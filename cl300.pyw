from os import listdir, chdir, startfile
from os.path import isfile, join, getmtime

from xml.etree import ElementTree as ET
import tkinter as tk
from reportlab.lib import colors
from reportlab.lib.pagesizes import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

__author__ = "Wojciech Trojanowski"
__copyright__ = "Copyright 2020, Wojciech Trojanowski"
__credits__ = ["Wojciech Trojanowski"]
__license__ = "MIT License"
__version__ = "1.0.0"
__maintainer__ = "Wojciech Trojanowski"
__email__ = "rukavina.andrei@gmail.com"
__status__ = "Dev"

# App config
path_in = "C:/input/"
path_out = "C:/output/"
nsCommon = "{http://www.joia.or.jp/standardized/namespaces/Common}"
nsLM = "{http://www.joia.or.jp/standardized/namespaces/LM}"

# Define Measure class
class Measure:
    def __init__ (self, file, name, surname, id, path_in="input", path_out="output"):
        self.file = file
        self.f = f(file)
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

    def generateDoc (self):
        doc = SimpleDocTemplate(join(path_out, fe(self.f)))
        styles = getSampleStyleSheet()
        elements = []

        # Draw patient details
        elements.append(Paragraph('TOPCON CL300 Doc', style=styles['h2']))

        textobject_common = self.details['date'] + ' ' + self.details['time'] + '<br/><br/>'
        elements.append(Paragraph(textobject_common, style=styles['Normal']))

        textobject_patient_name = 'Name: ' + self.details['patientName']
        textobject_patient_surname = 'Surame: ' + self.details['patientSurname']
        textobject_patient_id = 'Personal Number: ' + self.details['patientId'] + '<br/><br/>'
        elements.append(Paragraph(textobject_patient_name, style=styles['Normal']))
        elements.append(Paragraph(textobject_patient_surname, style=styles['Normal']))
        elements.append(Paragraph(textobject_patient_id, style=styles['Normal']))

        # Draw table with measure data
        data_measure = [['Eye', 'Left', '', 'Eye', 'Right'],
                ['Sphere', self.details['lSphere'], '', 'Sphere', self.details['rSphere']],
                ['Cylinder', self.details['lCylinder'], '', 'Cylinder', self.details['rCylinder']],
                ['Axis', self.details['lAxis'], '', 'Axis', self.details['rAxis']]]
        
        t=Table(data_measure,5*[1*inch], 4*[0.4*inch])
        t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'LEFT'),
        ('INNERGRID', (0,0), (1,3), 0.25, colors.black),
        ('INNERGRID', (3,0), (4,3), 0.25, colors.black)
        ]))

        # Save document
        elements.append(t)
        doc.build(elements)

# Decapsulate file from path
f = lambda x: x.split(path_in)[1]

# Convert file extension to pdf
fe = lambda x: x.split('.')[0] + ".pdf"

# Search for files in input path
chdir(path_in)
files = filter(isfile, listdir(path_in))
files = [join(path_in, f) for f in files if "xml" in f]
files.sort(key=lambda x: getmtime(x), reverse=True)

# Generate doc - click button event
def processData (event):
    selected = files[lbox.curselection()[0]]
    name = entry_name.get()
    surname = entry_surname.get()
    id = entry_id.get()

    measure = Measure(selected, name, surname, id)
    print(measure.getDetails())

    if len(list(measure.details)) > 0:
        measure.generateDoc()
        entry_name.delete(0, tk.END)
        entry_surname.delete(0, tk.END)
        entry_id.delete(0, tk.END)
    
def exploreInputPath (event):
    startfile(path_out)

# Create GUI
window = tk.Tk()
window.title("TOPCON CL300 Doc converter - SPEKTRUM Sp. z o.o.")

lbox = tk.Listbox(window, selectmode="SINGLE", width="60")

label_section_name = tk.Label(window, text="Additional details", font=(None, 10, "bold"))
label_name = tk.Label(window, text="Name")
label_surname = tk.Label(window, text="Surname")
label_id = tk.Label(window, text="Personal Number")
entry_name = tk.Entry(window)
entry_surname = tk.Entry(window)
entry_id = tk.Entry(window)

label_glass_type = tk.Label(window, text="Glass type")
glass_type = tk.StringVar()
radio_glasstype_1 = tk.Radiobutton(window, text="for distance vision", variable=glass_type, value="for distance vision")
radio_glasstype_2 = tk.Radiobutton(window, text="for near vision", variable=glass_type, value="for near vision")
glass_type.set("for distance vision")

button_submit = tk.Button(window, text="Generate PDF")
button_explore = tk.Button(window, text="Explore output")

lbox.grid(row=0, column=0, rowspan=8, columnspan=2, padx=10, pady=(0, 10))

label_section_name.grid(row=0, column=2, padx=(0, 10), pady=(10, 10))
label_name.grid(row=1, column=2)
entry_name.grid(row=2, column=2, padx=(0, 10))
label_surname.grid(row=3, column=2)
entry_surname.grid(row=4, column=2, padx=(0, 10))
label_id.grid(row=5, column=2)
entry_id.grid(row=6, column=2, padx=(0, 10))
label_glass_type.grid(row=7, column=2, pady=(20, 0))
radio_glasstype_1.grid(row=8, column=2, sticky=tk.W)
radio_glasstype_2.grid(row=9, column=2, sticky=tk.W)

button_submit.grid(column=0, row=9, padx=10, pady=(0, 10), sticky=tk.W+tk.E)
button_explore.grid(column=1, row=9, padx=10, pady=(0, 10), sticky=tk.W+tk.E)

# Feed listbox with files
for file in files:
    lbox.insert(tk.END, f(file))

# Bind actions
button_submit.bind('<Button-1>', processData)
button_explore.bind('<Button-1>', exploreInputPath)

# Begin mainloop
window.mainloop()