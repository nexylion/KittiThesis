from glob import glob
from pathlib import Path
import re

import argparse

from PIL import Image

errorCounts = 0


def xmlCreator(path):
    f = open(path, "r")
    text = f.read()
    f.close()
    text = str(re.findall('"description":.+?(?=\")', text)[0][15:])
    imgPath = Path("./images/" + Path(path).stem + ".png")
    img = Image.open(imgPath)  # beolvasni a képet a sorról
    filename = Path(path).stem
    # Page xml template
    xmlTemplate = '''<?xml version="1.0" encoding="UTF-8"?>
                    <PcGts xmlns="http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15 http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15/pagecontent.xsd">
                        <Metadata>
                        <Creator></Creator>
                        <Created>2017-05-03T10:20:47</Created>
                        <LastChange>2018-01-24T12:14:17</LastChange></Metadata>
                        <Page imageFilename="{path}" imageWidth="{width}" imageHeight="{height}">
                        <TextRegion id="textblock_{id} ">
                        <Coords points="0,0 0,{heightsub} {widthsub},{heightsub} {widthsub},0"/>
                        <TextLine id="line_{id}">
                            <Baseline points="0,{heightsub} {widthsub},{heightsub}"/>
                            <Coords points="0,0 0,{heightsub} {widthsub},{heightsub} {widthsub},0"/>
                        <TextEquiv><Unicode>{unicode}</Unicode></TextEquiv>
                        </TextLine>
                        </TextRegion>
                    </Page></PcGts>'''
    xml = xmlTemplate.format(path="../images/" + filename + ".png", width=img.width, height=img.height,
                             widthsub=img.width - 1, heightsub=img.height - 1, id=filename, unicode=text)
    w = open(Path("./results/" + filename + ".xml"), "w")
    w.write(xml)
    w.close()


if __name__ == '__main__':

    # argument kezelés
    argParser = argparse.ArgumentParser()
    argParser.add_argument("--imgpath", help="path to images")
    argParser.add_argument("--textpath", help="path to text")
    args = argParser.parse_args()

    imgPath = args.imgpath
    textPath = args.textpath
    images = glob(imgPath + "/*.jpg")
    for textpath in sorted(glob(textPath + "/*.json")):
        imgPath = imgPath + Path(textpath).stem + ".jpg"
        if imgPath in images:
            xmlCreator(textpath)
        else:
            print("no img found for this file " + Path(textpath).name)
