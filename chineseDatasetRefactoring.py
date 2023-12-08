import argparse
from glob import glob
from pathlib import Path
import struct

import cv2
import numpy



def dgrlFileread(path,counter): # dgrl formátumú fájl beolvasása és formázása (http://www.nlpr.ia.ac.cn/databases/Download/DGRLRead.cpp.pdf alapján)
    print("called")
    file = open(path, "rb")
    dgrlhsize, = struct.unpack('i', file.read(4))
    dgrlcode = file.read(8).decode().rstrip("\x00")
    illuslen = dgrlhsize - 36
    illustr = file.read(illuslen).decode().rstrip("\x00")
    codetype = file.read(20).decode().rstrip("\x00")
    codelen, = struct.unpack('h', file.read(2))
    bittspp, = struct.unpack('h', file.read(2))

    #ezek után az oldal adatai jönnek
    pageHei, = struct.unpack('i', file.read(4))
    pageWid, = struct.unpack('i', file.read(4))
    lineNumber, = struct.unpack('i', file.read(4))

    #itt kezdödnek a sorok adatai
    for i in range(lineNumber):
        charNumber, = struct.unpack('i', file.read(4))
        label = file.read(codelen*charNumber)
        label=label.decode("gb2312", 'ignore').replace('\x00','')
        print(label)
        lineTop, = struct.unpack('i', file.read(4))
        lineLeft, = struct.unpack('i', file.read(4))
        lineHei, = struct.unpack('i', file.read(4))
        lineWid, = struct.unpack('i', file.read(4))
        lineImg = []
        for j in range(lineHei):
            lineImg.append(numpy.array(list(file.read(lineWid))))
        lineImg = numpy.array(lineImg)
        imagepath="./results/img"+counter+str(i)+".png"
        cv2.imwrite(imagepath, lineImg)

        #Page xml template
        xml_template = '''<?xml version="1.0" encoding="UTF-8"?>
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
        xml = xml_template.format(path="img"+counter+str(i)+".png" ,width=lineWid,height=lineHei,widthsub=lineWid-1,heightsub=lineHei-1, id=counter+str(i), unicode=label)
        w = open(Path("./results/xml"+counter+str(i)+".xml"), "w")
        w.write(xml)
        w.close()


if __name__ == '__main__':

    argParser = argparse.ArgumentParser()
    argParser.add_argument("--path", nargs='?', help="path to dgrl files")

    args = argParser.parse_args()
    if args.path:
        path=args.path
    index = 0
    for file in glob(path + "/*.dgrl"):

        dgrlFileread(file, "f"+str(index)+"l")
        index = index + 1

