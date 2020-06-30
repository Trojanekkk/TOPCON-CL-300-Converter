from os import listdir
from os.path import isfile, join
from xml.etree import ElementTree as ET

path_in = "input"
path_out = "output"
nsCommon = "{http://www.joia.or.jp/standardized/namespaces/Common}"
nsLM = "{http://www.joia.or.jp/standardized/namespaces/LM}"

class Measure:
    def __init__ (self, file, path_in="input", path_out="output"):
        self.file = file
        tree = ET.parse(join(path_in, file))
        self.root = tree.getroot()

    def getObj (self, path, ns):
        return self.root.find(path.replace("/", "/{0}").format(ns))

    def getDetails(self):
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
            'lVPrism' : self.getObj("./Measure/LM/L/V", nsLM).attrib['Prism']
        }

files = [file for file in listdir(path_in) if isfile(join(path_in , file))]

for file in files:
    measure = Measure(file)
    measure.getDetails()
    print(measure.details)