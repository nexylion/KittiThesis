from glob import glob
from pathlib import Path

import cv2
import argparse

from PIL import Image

errorCounts = 0


def imageCropping(path):
    original = cv2.imread(path)
    image = original.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]  # making binary image
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    if len(cnts):
        cntFirst = next((x for x in cnts if cv2.contourArea(x) > 20),
                        cnts[0])  # search for the first big enough contour

        x, y, w, h = cv2.boundingRect(cntFirst)
        leftMost = x
        rightMost = x + w
        upMost = y
        downMost = y + h

        for c in cnts:
            if cv2.contourArea(c) > 20:
                x, y, w, h = cv2.boundingRect(c)
                if x < leftMost:
                    leftMost = x
                if x + w > rightMost:
                    rightMost = x + w
                if y < upMost:
                    upMost = y
                if y + h > downMost:
                    downMost = y + h

        # kirajzolás
        # cv2.rectangle(image, (leftMost,upMost) , (rightMost,downMost), (124,252,0), 16)
        # cv2.imshow('image', image)
        # cv2.waitKey()
        cv2.imwrite("./images/" + Path(path).stem + ".png", original[upMost:downMost, leftMost:rightMost])
    else:
        cv2.imwrite("./images/" + Path(path).stem + ".png", original)
        print("did not find contours")


def xmlCreator(path):
    f = open(path, "r", encoding="windows-1256")
    text = f.read()
    f.close()

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
                        <TextLine id="line_{id}" readingDirection="right-to-left">
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

    argParser = argparse.ArgumentParser()
    argParser.add_argument("--imgpath", nargs='?', help="path to images")
    argParser.add_argument("--img", action='store_true')
    argParser.add_argument("--xml", action='store_true')
    argParser.add_argument("--textpath", nargs='?', help="path to text")

    args = argParser.parse_args()
    if (args.img == False and args.xml == False):
        print("Use '--img' if you want crop images or '--xml' if you want to create the xml files")

    if (args.img):
        imgPath = args.imgpath
        for imgpath in sorted(glob(imgPath + "/*.tif")):
            imageCropping(imgpath)
    if (args.xml):
        textPath = args.textpath
        images = glob("./images/*.png")
        for textpath in sorted(glob(textPath + "/*.txt")):
            imgPath = "./images/" + Path(textpath).stem + ".png"
            if imgPath in images:
                xmlCreator(textpath)
            else:
                print("no img found for this file " + Path(textpath).name)
