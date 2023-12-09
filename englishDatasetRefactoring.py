import argparse
from pathlib import Path
import re
from glob import glob
import html
from PIL import Image


# ennél a datasetnél a képek már jó formátumban voltak de az xml dokumentumot átt kell formálni.
def xmlCreator(imgPath, text):
    img = Image.open(imgPath)  # beolvasni a képet a sorról
    filename = Path(imgPath).stem
    # Page xml template
    xmlTemplate = '''<?xml version="1.0" encoding="UTF-8"?>
            <PcGts xmlns="http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15 http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15/pagecontent.xsd">
            	<Metadata>
            	<Creator></Creator>
            	<Created>2017-05-03T10:20:47</Created>
            	<LastChange>2018-01-24T12:14:17</LastChange></Metadata>
            	<Page imageFilename="{path}" imageWidth="{width}" imageHeight="{height}">
            	<TextRegion id="textblock_{id}">
    			<Coords points="0,0 0,{heightsub} {widthsub},{heightsub} {widthsub},0"/>
    			<TextLine id="line_{id}">
    				<Baseline points="0,{heightsub} {widthsub},{heightsub}"/>
    				<Coords points="0,0 0,{heightsub} {widthsub},{heightsub} {widthsub},0"/>
    			<TextEquiv><Unicode>{unicode}</Unicode></TextEquiv>
    			</TextLine>
    			</TextRegion>
            </Page></PcGts>'''
    xml = xmlTemplate.format(path=imgPath, width=img.width, height=img.height,
                             widthsub=img.width - 1, heightsub=img.height - 1, id=filename, unicode=text)
    w = open(Path("./results/" + filename + ".xml"), "w")
    w.write(xml)
    w.close()


def readXml(xmlPath):
    f = open(xmlPath, "r")
    text = f.read()
    lines = re.findall('<line.*text=.*>', text)
    texts = []
    for line in lines:
        text = str(re.findall("text=.+?(?=\")", line)[0][6:])
        text = html.unescape(html.unescape(text))
        texts.append(text)
    return texts


if __name__ == '__main__':

    # argument kezelés
    argParser = argparse.ArgumentParser()
    argParser.add_argument("--imgpath", help="path to images")
    argParser.add_argument("--textpath", help="path to text")
    args = argParser.parse_args()

    imgPath = args.imgpath
    textPath = args.textpath
    unicodes = []
    for file in sorted(glob(textPath + "/*.xml")):
        unicodes = unicodes + readXml(file)
    i = 0
    imgPaths = sorted(glob(imgPath + "/*.png"))
    for unicode in unicodes:
        xmlCreator(imgPaths[i], unicode)
        i += 1
