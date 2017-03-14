#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
360fy - A simple 360' video creator
author: 360fy team(Girish Saunshi, Sapnesh Naik, Divya Hiremath, Nadeem Jamadar, Maitri Huggi)
contact: Sapnesh Naik <sapneshwk@gmail.com>
"""
import sys
from PyQt5.QtWidgets import (QDialog, QApplication, QWidget, QToolTip, QPushButton, QMessageBox, QGridLayout, QLineEdit, QHBoxLayout, QVBoxLayout, QLabel, QDesktopWidget, QFileDialog)
from PyQt5.QtGui import QIcon, QFont, QPixmap, QDesktopServices
from PyQt5.QtCore import Qt, QRect, QCoreApplication, QMetaObject, QUrl
import subprocess
from glob import glob
import cv2
import numpy as np
from SimpleCV import VideoStream, Display, Image, VirtualCamera
import os
import math
import urllib




#class Fy360 inhertits Qwidget class
class Fy360(QWidget):
    '''Three important things in object oriented programming are classes, data, and methods.
    Here we create a new class called Fy360. The Fy360 class inherits from the QWidget class.
    This means that we call two constructors: the first one for the Fy360 class and the second
     one for the inherited class.
    The super() method returns the parent object of the Fy360 class and we call its constructor.
    The __init__() method is a constructor method in Python language.'''
    def __init__(self):
        super(Fy360, self).__init__()
        self.initUI()


    #this fn executes when chooseVidIn is clicked
    def openInputVid(self):
        print bcolors.HEADER + "[360fy]------- Selecting input video\n" + bcolors.ENDC
        iFileName = QFileDialog.getOpenFileName(self, str("Open Video"), '', str("Video Files(*.avi *.mp4 *.mkv *.h264)"))
        print bcolors.OKGREEN + "[360fy]------- The input fle path is:{0}\n".format(iFileName[0]) + bcolors.ENDC
        self.inputPath.setText(str(iFileName[0]))
        self.iVidPath = iFileName[0]


    # this fn executes when chooseVidOut is clicked
    def saveOutputVid(self):
        print bcolors.HEADER +"[360fy]------- Selecting output video\n" + bcolors.ENDC
        oFileName = QFileDialog.getSaveFileName(self, str("Open Video"), self.iVidPath, str("Video Files (*.mp4)"), initialFilter='*.mp4')
        #check extension
        if oFileName[0].endswith('.mp4'):
            print bcolors.OKGREEN + "[360fy]------- The output file path is {0}\n".format(oFileName[0])+ bcolors.ENDC
            oFileNewName = oFileName[0]
            self.outputPath.setText(oFileNewName)
            self.oVidPath = oFileNewName
        #assigns extension only if file name is not null
        if oFileName[0] and not oFileName[0].endswith('.mp4'):
            print "[360fy]------- filename doesnt have an extension \n\t\t setting mp4 as default extension\n"
            oFileNewName = oFileName[0]
            oFileNewName += '.mp4'
            print "[360fy]------- The output file path is {0}\n".format(oFileNewName)
            self.outputPath.setText(oFileNewName)
            self.oVidPath = oFileNewName

        
        
    def check(self):
        checkIp = str(self.inputPath.text())
        checkOp = str(self.outputPath.text())
        if  checkIp != "" and checkOp != "":
            print "[360fy]------- Enabling Start button\n"
            self.startBut.setEnabled(True)
            self.startBut.setStyleSheet('QPushButton {background-color: white; color: A3C1DA; font-weight: bold ; font: 20px bold }')
            self.startBut.setToolTip('Click to begin processing 360° video')
            self.statusText.setText("Status: Ready to run")

        else:
            print "[360fy]------- Input or Output was not set Start button still disabled\n"
            self.startBut.setEnabled(False)
            self.startBut.setStyleSheet('QPushButton {background-color: gray; color: black; font-weight: bold ; font: 18px }')
 


    def new_dewarp(self):
        vidpath = self.iVidPath
        def isInROI(x, y, R1, R2, Cx, Cy):
            isInOuter = False
            isInInner = False
            xv = x-Cx
            yv = y-Cy
            rt = (xv*xv)+(yv*yv)
            if(rt < R2*R2):
                isInOuter = True
                if(rt < R1*R1):
                    isInInner = True
            return isInOuter and not isInInner

        def buildMap(Ws, Hs, Wd, Hd, R1, R2, Cx, Cy):
            map_x = np.zeros((Hd, Wd),np.float32)
            map_y = np.zeros((Hd, Wd),np.float32)
            rMap = np.linspace(R1, R1 + (R2 - R1), Hd)
            thetaMap = np.linspace(0, 0 + float(Wd) * 2.0 * np.pi, Wd)
            sinMap = np.sin(thetaMap)
            cosMap = np.cos(thetaMap)

            for y in xrange(0, int(Hd-1)):
                map_x[y] = Cx + rMap[y] * sinMap
                map_y[y] = Cy + rMap[y] * cosMap

            return map_x, map_y

        # do the unwarping
        def unwarp(img, xmap, ymap):
            output = cv2.remap(img.getNumpyCv2(), xmap, ymap, cv2.INTER_LINEAR)
            result = Image(output, cv2image=True)
            # return result
            return result

        disp = Display((800, 600))
        #disp = Display((1296,972))
        vals = []
        last = (0, 0)
        # Load the video from the rpi
        vc = VirtualCamera(vidpath, "video")
        # Sometimes there is crud at the begining, buffer it out
        for i in range(0, 10):
            img = vc.getImage()
            img.save(disp)
        # Show the user a frame let them left click the center
        #    of the "donut" and the right inner and outer edge
        # in that order. Press esc to exit the display
        while not disp.isDone():
            test = disp.leftButtonDownPosition()
            if test != last and test is not None:
                last = test
                print "[360fy]------- center = {0}\n".format(last)

                vals.append(test)
        print "[360fy]------- Dewarping video and generating frames using center, offset1, offset2\n"



        Cx = vals[0][0]
        Cy = vals[0][1]
        #print str(Cx) + " " + str(Cy)
        # Inner donut radius
        R1x = vals[1][0]
        R1y = vals[1][1]
        R1 = R1x-Cx
        #print str(R1)
        # outer donut radius
        R2x = vals[2][0]
        R2y = vals[2][1]
        R2 = R2x-Cx
        #print str(R2)
        # our input and output image siZes
        Wd = round(float(max(R1, R2)) * 2.0 * np.pi)
        #Wd = 2.0*((R2+R1)/2)*np.pi
        #Hd = (2.0*((R2+R1)/2)*np.pi) * (90/360)
        Hd = (R2-R1)
        Ws = img.width
        Hs = img.height
        # build the pixel map, this could be sped up
        print ("BUILDING MAP!")
 
        xmap, ymap = buildMap(Ws, Hs, Wd, Hd, R1, R2, Cx, Cy)
        print "MAP DONE!"

        result = unwarp(img, xmap, ymap)

        result.save(disp)

        i = 0
        print "[360fy]------- Storing frames into ../temp_data/frames\n"

        while img is not None:
            print "Frame Number: {0}".format(i)
            result = unwarp(img, xmap, ymap)
            result.save(disp)
            # Save to file
            fname = "../temp_data/frames/FY{num:06d}.png".format(num=i)
            result.save(fname)
    
            img = vc.getImage()
            i = i + 1
        if img is None:
            self.statusText.setText(str( "Status: Done"))
            disp.quit()

    def addFramesAudio(self):

        outputV= self.oVidPath
        outFrameRate = self.frameRate
        outResolution = self.resolution

        print "[360fy]------- Merging all frames to genenrate dewarped video\n"
        subprocess.call(['./merge.sh', outFrameRate, outResolution])
        print "[360fy]------- Adding original Audio to the dewarped video\n"    
        subprocess.call(['./add_audio.sh', outputV])
        print "[360fy]------- Process complete\n"
        print "[360fy]------- The 360° video is located at : {0}\n".format(outputV)


    def stripAudio(self):
        inputV = self.iVidPath
        self.resolution = subprocess.check_output(['./frame_size.sh', inputV])
        print "[360fy]-------Input video properties\n"
        print "[360fy]-------Video frame size = {0}\n".format(self.resolution)
        
        #print self.resolution
        self.frameRate = subprocess.check_output(['./frame_rate.sh', inputV])
        print "[360fy]-------Video frame rate = {0}\n".format(self.frameRate)

        print "[360fy]-------Stripping Audio from input video\n"
        subprocess.call(['ffmpeg', '-i', inputV, '-ab', '320k', '-ac', '2', '-ar', '44100' , '-vn' , '../temp_data/audio.mp3', '-y'])


    def cleanup(self):
        print "[360fy]------- Cleaning Up...\n"
        subprocess.call(['rm', '../temp_data/video.mp4', '../temp_data/audio.mp3'] + glob("../temp_data/frames/*"))
        print "[360fy]------- Enjoy!!\n"

    def showVid(self):

        self.Dialog = QDialog()
        self.Dialog.setObjectName("self.Dialog")
        self.Dialog.setWindowModality(Qt.ApplicationModal)
        self.Dialog.setEnabled(True)
        #self.Dialog.resize(543, 196)
        font = QFont()
        font.setPointSize(11)
        font.setItalic(False)
        self.Dialog.setFont(font)
        self.label = QLabel(self.Dialog)
        self.label.setGeometry(QRect(60, 10, 171, 31))
        self.label.setTextFormat(Qt.PlainText)
        self.label.setObjectName("label")
        self.label_2 = QLabel(self.Dialog)
        self.label_2.setGeometry(QRect(60, 50, 78, 17))
        font = QFont()
        font.setUnderline(True)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(Qt.PlainText)
        self.label_2.setObjectName("label_2")
        self.fileSize = QLabel(self.Dialog)
        self.fileSize.setGeometry(QRect(145, 50, 80, 17))
        self.fileSize.setObjectName("fileSize")
        self.label_3 = QLabel(self.Dialog)
        self.label_3.setGeometry(QRect(60, 80, 110, 17))
        font = QFont()
        font.setPointSize(11)
        font.setItalic(False)
        self.label_3.setFont(font)
        self.label_3.setTextFormat(Qt.PlainText)
        self.label_3.setObjectName("label_3")
        self.lineEdit = QLineEdit(self.Dialog)
        self.lineEdit.setGeometry(QRect(60, 100, 471, 33))
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.openButton = QPushButton(self.Dialog)
        self.openButton.setGeometry(QRect(60, 150, 151, 31))
        self.openButton.setObjectName("openButton")
        self.openFolderButton = QPushButton(self.Dialog)
        self.openFolderButton.setGeometry(QRect(220, 150, 151, 31))
        self.openFolderButton.setObjectName("openFolderButton")
        self.closeButtton = QPushButton(self.Dialog)
        self.closeButtton.setGeometry(QRect(380, 150, 151, 31))
        self.closeButtton.setObjectName("closeButtton")
        self.label_4 = QLabel(self.Dialog)
        self.label_4.setGeometry(QRect(10, 20, 41, 51))
        self.label_4.setText("")
        self.label_4.setPixmap(QPixmap("../resource/logo.png"))
        self.label_4.setObjectName("label_4")

        #self.retranslateUi(self.Dialog)
        QMetaObject.connectSlotsByName(self.Dialog)
        self.Dialog.setFixedSize(543,196)
        self.Dialog.setWindowFlags(self.Dialog.windowFlags() | Qt.WindowStaysOnTopHint)
        self.retranslateDoneUi(self.Dialog)
        self.closeButtton.clicked.connect(self.Dialog.close)
        #calls openfile fn to open o/p video in process complete dialog
        self.openButton.clicked.connect(self.openFile)
        #calls open_folder fn to open o/p video folder in process complete dialog
        self.openFolderButton.clicked.connect(self.open_folder)
        self.Dialog.exec_()

        #this is showVid!!!!

    def retranslateDoneUi(self, Dialog):
        _translate = QCoreApplication.translate
        self.Dialog.setWindowTitle(_translate("self.Dialog", "Process Complete"))
        self.label.setText(_translate("self.Dialog", "Process Complete"))
        self.label_2.setText(_translate("self.Dialog", "Video size : "))
        #self.fileSize.setText(_translate("self.Dialog", "TextLabel"))
        self.label_3.setText(_translate("self.Dialog", "Video saved as :"))
        self.openButton.setText(_translate("self.Dialog", "Open"))
        self.openFolderButton.setText(_translate("self.Dialog", "Open folder"))
        self.closeButtton.setText(_translate("self.Dialog", "close"))
        self.lineEdit.setText(str(self.oVidPath))
        #get filesizwe in megabyte
        self.fileS = os.path.getsize(self.oVidPath)
        self.fileM = self.convertSize()

        self.fileSize.setText(self.fileM)

        #close dialoge upon close button click

    #this fn is called when help is clicked
    def help_dialog(self):

        self.helpDialog = QDialog()
        self.helpDialog.setObjectName("self.helpDialog")
        self.helpDialog.setWindowModality(Qt.ApplicationModal)
        self.helpDialog.setFixedSize(362, 151)
        icon = QIcon()
        icon.addPixmap(QPixmap("../resource/logo.png"), QIcon.Normal, QIcon.Off)
        self.helpDialog.setWindowIcon(icon)
        self.helpDialog.setLayoutDirection(Qt.LeftToRight)
        self.helpDialog.setAutoFillBackground(False)
        self.helpDialog.setSizeGripEnabled(False)
        self.helpDialog.setModal(False)
        self.docButton = QPushButton(self.helpDialog)
        self.docButton.setGeometry(QRect(180, 100, 141, 41))
        icon1 = QIcon()
        icon1.addPixmap(QPixmap("../resource/Doc.png"), QIcon.Normal, QIcon.Off)
        self.docButton.setIcon(icon1)
        self.docButton.setObjectName("docButton")
        self.tubeButton = QPushButton(self.helpDialog)
        self.tubeButton.setGeometry(QRect(50, 100, 111, 41))
        icon2 = QIcon()
        icon2.addPixmap(QPixmap("../resource/YouTube.png"), QIcon.Normal, QIcon.Off)
        self.tubeButton.setIcon(icon2)
        self.tubeButton.setObjectName("tubeButton")
        self.label = QLabel(self.helpDialog)
        self.label.setGeometry(QRect(20, 10, 331, 21))
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QLabel(self.helpDialog)
        self.label_2.setGeometry(QRect(20, 30, 321, 21))
        font = QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QLabel(self.helpDialog)
        self.label_3.setGeometry(QRect(20, 50, 221, 20))
        font = QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QLabel(self.helpDialog)
        self.label_4.setGeometry(QRect(30, 80, 211, 17))
        font = QFont()
        font.setPointSize(8)
        font.setItalic(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.retranslate_help_ui(self.helpDialog)
        QMetaObject.connectSlotsByName(self.helpDialog)

        self.helpDialog.exec_()



    #help_dialog calls this inturn to set some labels messages
    def retranslate_help_ui(self, helpDialog):

        _translate = QCoreApplication.translate
        self.helpDialog.setWindowTitle(_translate("self.helpDialog", "Help"))
        self.docButton.setText(_translate("self.helpDialog", "Documentation"))
        self.tubeButton.setText(_translate("self.helpDialog", "YouTube"))
        self.label.setText(_translate("self.helpDialog", "If you have trouble understanding something"))
        self.label_2.setText(_translate("self.helpDialog", "please consider reading the documentation"))
        self.label_3.setText(_translate("self.helpDialog", "or watching the tutorial videos."))
        self.label_4.setText(_translate("self.helpDialog", "* Internet Charges may apply"))





    def open_folder(self):

        dirPath = os.path.dirname(os.path.abspath(self.oVidPath))
        QDesktopServices.openUrl(QUrl.fromLocalFile(dirPath))
        self.Dialog.close()

    def openFile(self):


        QDesktopServices.openUrl(QUrl.fromLocalFile(self.oVidPath))
        self.Dialog.close()



    def convertSize(self):
        size_bytes = self.fileS
        if (size_bytes == 0):
            return '0B'
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1000)))
        p = math.pow(1000, i)
        s = round(size_bytes/p, 2)
        return '%s %s' % (s, size_name[i])

   

    def startMessage(self):
        self.statusText.setText("Status: Waiting for confirmation")
        print "[360fy]------- Starting the process\n"
        print "[360fy]------- [ Note ] When the Preview is shown, click at the Center of the image,\n\t\t moving to right click on the Begining of the useful image \n\t\t and then click on the ending of the useful Image"

        reply = QMessageBox.question(self, 'Please Note',
            "When the Preview is shown, click at the Center of the image, moving to right click on the Begining of the useful image and then click on the ending of the useful Image", QMessageBox.Ok)

            

        if reply == QMessageBox.Ok:
            self.statusText.setText("Status: Running")
            self.stripAudio()
            self.new_dewarp()
            self.addFramesAudio()
            self.cleanup()
            self.showVid()

    def closeAction(self):
        replyc = QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if replyc == QMessageBox.Yes:
            self.cleanup()
            exit()
        
            



    def initUI(self):
        #set up a grid layout
        grid = QGridLayout()
        self.setLayout(grid)
        grid.setSpacing(10)
        #call center method
        self.center()
       
            
        #inputHead = QLabel("INPUT")
        inputLabel = QLabel('Select Video:')
        outputLabel = QLabel('Save As:')
        self.startBut = QPushButton("Start")
        self.startBut.setStyleSheet('QPushButton {background-color: gray; color: black; font-weight: bold ; font: 18px }')
        self.startBut.setDisabled(True)
        self.startBut.setToolTip('Please select Input video and Output location first')
        self.startBut.setFixedWidth(200)
        self.startBut.setFixedHeight(55)

        self.closeBut = QPushButton("Close")
        self.closeBut.setStyleSheet('QPushButton { color: red;}')
        closeIcon = QIcon('../resource/exit.png')
        self.closeBut.setIcon(closeIcon)
        self.closeBut.clicked.connect(self.closeAction)

        self.helpBut = QPushButton("Help")
        self.helpBut.setStyleSheet('QPushButton { color: green;}')
        self.helpBut.setFixedWidth(87)
        helpIcon = QIcon('../resource/help.png')
        self.helpBut.setIcon(helpIcon)
        startIcon = QIcon('../resource/logo.png')
        self.startBut.setIcon(startIcon)
 

        chooseVidIn = QPushButton("Browse...")
        chooseVidOut = QPushButton("Browse...")
        self.inputPath = QLineEdit(self)
        self.inputPath.setPlaceholderText("Select video to be converted")
        self.inputPath.setReadOnly(True)

        self.outputPath = QLineEdit(self)
        self.outputPath.setPlaceholderText("Select where to save the converted video")
        self.outputPath.setReadOnly(True)

        self.statusText = QLabel("Status: Waiting for Input and Output path")
        self.statusText.setStyleSheet('QLabel {background-color: #D3D3D3; }')
        #below two lines enable startbutton if both paths are spaecified
        self.inputPath.textChanged[str].connect(self.check)
        self.outputPath.textChanged[str].connect(self.check)


        #call open input vid function
        chooseVidIn.clicked.connect(self.openInputVid)
        #call save location function
        chooseVidOut.clicked.connect(self.saveOutputVid)
        #call new_dewarp function 
        self.startBut.clicked.connect(self.startMessage)
        
        self.helpBut.clicked.connect(self.help_dialog)



        QToolTip.setFont(QFont('SansSerif', 10))
        chooseVidIn.setToolTip('Select video to be converted')
        chooseVidOut.setToolTip('Select where to save the final 360° video')

        
        grid.addWidget(inputLabel, 1, 1)
        grid.addWidget(self.inputPath, 1, 2)
        grid.addWidget(chooseVidIn, 1, 3)
        grid.addWidget(outputLabel, 2, 1)
        grid.addWidget(self.outputPath, 2, 2)
        grid.addWidget(chooseVidOut, 2, 3)
        #grid.addWidget(startBut, 3,1)
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        vbox1 = QVBoxLayout()
        # hbox2 = QHBoxLayout()
        # vbox2 = QVBoxLayout()
        
        #Qt::AlignLeft
        hbox.addWidget(self.startBut)
        vbox.addLayout(hbox)
        grid.addLayout(vbox, 4, 2, 1, 1)
        hbox1.addWidget(self.closeBut)
        vbox1.addLayout(hbox1)
        grid.addLayout(vbox1, 5, 3, 1, 1)
        grid.addWidget(self.helpBut, 5, 2, Qt.AlignRight)
        grid.addWidget(self.statusText, 5, 2, Qt.AlignCenter)    


        self.inputPath.sizePolicy().setHorizontalStretch(1)

        #set initial window size (doesn't matter if the program is opened in showMaximized mode)
        #self.setGeometry(300, 300, 300, 220) 
        #title bar name
        self.setWindowTitle("360fy - A Simple 360° Video Creator") 
        # set logo
        self.setWindowIcon(QIcon('../resource/logo.png'))
        self.setMinimumSize(814, 350)
        self.show()

    #open app at center of screen
    def center(self):
        fg = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        self.move(fg.topLeft())

    #confirm close(CLICKING x) event
    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.cleanup()
            event.accept()
        else:
            event.ignore()
        
#for colored terminal output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Fy360()
    sys.exit(app.exec_())