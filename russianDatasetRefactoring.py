
from glob import glob
from pathlib import Path
import re
import cv2

import argparse

from PIL import Image

errorCounts = 0


def imagetoBinary(path):

    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  # bináris kép készitése
    cv2.imwrite("./images/" + Path(path).stem + ".png", thresh)

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
    #alapértelmezett utvonalak a gyors teszteléshez
    imgPath = "/home/nexylion/Letöltések/HKR_Dataset_Words_Public/20200923_Dataset_Words_Public/img"
    textPath = "/home/nexylion/Letöltések/HKR_Dataset_Words_Public/20200923_Dataset_Words_Public/ann"
    #argument kezelés
    argParser = argparse.ArgumentParser()
    argParser.add_argument("--imgpath", nargs='?', help="path to images", default=imgPath)
    argParser.add_argument("--img", action='store_true')
    argParser.add_argument("--xml", action='store_true')
    argParser.add_argument("--textpath", nargs='?', help="path to text", default=textPath)
    args = argParser.parse_args()
    if (args.img == False and args.xml == False):
        print("Use '--img' if you want binarize images or '--xml' if you want to create the xml files")

    if (args.img):
        for imgpath in sorted(glob(imgPath + "/*.jpg")):
            imagetoBinary(imgpath)
    if (args.xml):
        images = glob("./images/*.png")
        for textpath in sorted(glob(textPath + "/*.json")):
            imgPath = "./images/" + Path(textpath).stem + ".png"
            if imgPath in images:
                xmlCreator(textpath)
            else:
                print("no img found for this file " + Path(textpath).name)
