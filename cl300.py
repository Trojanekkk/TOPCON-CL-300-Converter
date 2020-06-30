from os import listdir
from os.path import isfile, join
from xml.etree import ElementTree as ET

path_in = "in"
path_out = "out"
nsCommon = "{http://www.joia.or.jp/standardized/namespaces/Common}"
nsLM = "{http://www.joia.or.jp/standardized/namespaces/LM}"

def getObj (path, ns):
    return root.find(path.replace("/", "/{0}").format(ns))

files = [file for file in listdir(path_in) if isfile(join(path_in , file))]

for file in files:
    tree = ET.parse(join(path_in, file))
    root = tree.getroot()

    date = getObj("./Common/Date", nsCommon).text
    time = getObj("./Common/Time", nsCommon).text
    measuer_id = getObj("./Common/Patient/ID", nsCommon).text

    lensType = getObj("./Measure/LensType", nsLM).text

    rSphere = getObj("./Measure/LM/R/Sphere", nsLM).text
    rCylinder = getObj("./Measure/LM/R/Cylinder", nsLM).text
    rAxis = getObj("./Measure/LM/R/Axis", nsLM).text
    rAdd1Unit = getObj("./Measure/LM/R/Add1", nsLM).attrib['unit']
    rAdd2Unit = getObj("./Measure/LM/R/Add2", nsLM).attrib['unit']
    rHPrism = getObj("./Measure/LM/R/H", nsLM).attrib['Prism']
    rVPrism = getObj("./Measure/LM/R/V", nsLM).attrib['Prism']

    lSphere = getObj("./Measure/LM/L/Sphere", nsLM).text
    lCylinder = getObj("./Measure/LM/L/Cylinder", nsLM).text
    lAxis = getObj("./Measure/LM/L/Axis", nsLM).text
    lrAdd1Unit = getObj("./Measure/LM/L/Add1", nsLM).attrib['unit']
    lAdd2Unit = getObj("./Measure/LM/L/Add2", nsLM).attrib['unit']
    lHPrism = getObj("./Measure/LM/L/H", nsLM).attrib['Prism']
    lVPrism = getObj("./Measure/LM/L/V", nsLM).attrib['Prism']
