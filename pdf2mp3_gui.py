import PyQt5.QtWidgets as qtw
from PyQt5.QtWidgets import QDialog, QFileDialog
import PyQt5.QtGui as qtg
from PyQt5.QtCore import Qt, QUrl
import pyttsx3
import PyPDF2 as pypdf
import random
import os
import sys


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.resize(1100, 500)
        labelFontSize = 13
        lineEditFontSize = 10
        comboBoxFontSize = 9

        # Window properties
        self.setWindowTitle("PDF2MP3")
        self.setLayout(qtw.QGridLayout())

        # Setting the logo as the icon
        self.setWindowIcon(qtg.QIcon('Logo/logo_updated.png'))

        # Select PDF files
        pdfFileSelectorButton = qtw.QPushButton("Select File", clicked=lambda:openFileSelector())
        pdfFileSelectorButton.setFont(qtg.QFont("Helvetica", lineEditFontSize))

        # Select Directory and file Name
        mp3FileSelectorButton = qtw.QPushButton("Select directory", clicked=lambda:getSaveFileName())
        mp3FileSelectorButton.setFont(qtg.QFont("Helvetica", lineEditFontSize))

        # PDF File Selector Entry Field (Un-Editable)
        pdfFileSelectorLineEdit = qtw.QLineEdit()

        pdfFileSelectorLineEdit.setStyleSheet("QLineEdit"
                                            "{"
                                            "background : gray;"
                                            "}")
  
        pdfFileSelectorLineEdit.setReadOnly(True)

        # Mp3 File Selector Entry Field
        mp3FileSelectorLineEdit = qtw.QLineEdit()

        mp3FileSelectorLineEdit.setStyleSheet("QLineEdit"
                                            "{"
                                            "background : gray;"
                                            "}")
    
        mp3FileSelectorLineEdit.setReadOnly(True)

        # Assistant Label
        assistantLabel = qtw.QLabel("Choose your assistant")
        assistantLabel.setFont(qtg.QFont("Helvetica", labelFontSize))

        # Assistant Combo Box
        assistantComboBox = qtw.QComboBox()
        assistantComboBox.setFont(qtg.QFont("Helvetica", comboBoxFontSize))

        for i in range(len(availableVoices)):
            assistantComboBox.addItem(availableVoices[i].name, availableVoices[i].id)

        # Speech Rate Label
        speechRateLabel = qtw.QLabel("Speech Rate")
        speechRateLabel.setFont(qtg.QFont("Helvectica", labelFontSize))

        # Speech Rate Entry Field with a default value of 130
        speechRateEntryField = qtw.QLineEdit()
        speechRateEntryField.setObjectName("speechRate")
        speechRateEntryField.setFont(qtg.QFont("Helvetica", lineEditFontSize))
        speechRateEntryField.setText("130")

        # Narrate Button to demonstrate the assistant's voice with the selected parameters
        narrateButton = qtw.QPushButton("Narrate", clicked=lambda:narrate())
        narrateButton.setFont(qtg.QFont("Helvetica", labelFontSize))
        narrateButton.setToolTip("Listen how the assistant sounds with the selected properties")

        # Create MP3 button
        createMp3Button = qtw.QPushButton("Create MP3", clicked=lambda:pdf2mp3())
        createMp3Button.setFont(qtg.QFont("Helvetica", labelFontSize))

        # Close Button
        closeButton = qtw.QPushButton("Close", clicked=lambda:terminateProgram())
        closeButton.setFont(qtg.QFont("Helvetica", labelFontSize))


        self.layout().addWidget(pdfFileSelectorButton,    0, 0, 1, 1)
        self.layout().addWidget(pdfFileSelectorLineEdit,  0, 1, 1, 1)
        self.layout().addWidget(mp3FileSelectorButton,    1, 0, 1, 1)
        self.layout().addWidget(mp3FileSelectorLineEdit,  1, 1, 1, 1)
        self.layout().addWidget(assistantLabel,         2, 0, 1, 1)
        self.layout().addWidget(assistantComboBox,      2, 1, 1, 2)
        self.layout().addWidget(speechRateLabel,        3, 0, 1, 1)
        self.layout().addWidget(speechRateEntryField,   3, 1, 1, 2)
        self.layout().addWidget(narrateButton,          4, 0, 1, 1)
        self.layout().addWidget(createMp3Button,        4, 1, 1, 1)

        # Function to open the file explorer to select the desired directory
        def openDirectorySelector():
            global mp3Path
            mp3Path = QFileDialog.getExistingDirectory(self, caption='Select a folder')
            
        # Function to open the file explorer and select the desired PDF file
        def openFileSelector():
            global pdfPath
            fileName, _ = QFileDialog.getOpenFileName(self, "Select a PDF File", "", "PDF Files (*.pdf)")

            if(fileName):
                pdfPath = fileName

            pdfFileSelectorLineEdit.setText(pdfPath)

        # Function to open the file explorer and save the mp3 file at a desired location
        def getSaveFileName():
            global mp3Path
            response, _ = QFileDialog.getSaveFileName(caption="Save as", filter="MP3 File (*.mp3)")
            
            if(response):
                mp3Path = response

            mp3FileSelectorLineEdit.setText(mp3Path)

        # Funciton to demonstrate the assistant's properties
        def narrate():
            speech = "Hello! I am your narrator and this is the pace at which I narrate your Audio File"

            assistantId = assistantComboBox.currentData()
            speechRate = int(speechRateEntryField.text())

            # Setting the properties of the assistant
            speaker.setProperty("voice", assistantId)
            speaker.setProperty("rate", speechRate)

            speaker.say(speech)
            speaker.runAndWait()

        # Function to convert the PDF file into the MP3 file
        def pdf2mp3():
            if(os.path.exists(pdfPath) and pdfPath.endswith(".pdf")):
                
                # Read the pdf file
                pdfReader = pypdf.PdfFileReader(open(pdfPath, 'rb'))

                # Extract data from each page and convert into a speakable form
                data = ""
                for pageNumber in range(pdfReader.numPages):
                    data += pdfReader.getPage(pageNumber).extractText()
                
                formattedData = data.strip().replace("\n", "    ")

                # Getting the properties of the assistant from their respective entry fields
                assistantId = assistantComboBox.currentData()
                speechRate = int(speechRateEntryField.text())

                # Setting the properties of the assistant
                speaker.setProperty("voice", assistantId)
                speaker.setProperty("rate", speechRate)

                # Converting the formattedData into an mp3 file
                speaker.save_to_file(formattedData, mp3Path)

                speaker.runAndWait()
                speaker.stop()

                # Clearing the Entry Fields
                pdfFileSelectorLineEdit.setText("")
                mp3FileSelectorLineEdit.setText("")
                speechRateEntryField.setText("130")

            else:
                errorDialog = ErrorDialog()

                errorDialog.exec()

        # Function to terminate the program
        def terminateProgram():
            app.quit()

        self.show()


# A dialog box that pops up if the entered pdf path doesn't exist
class ErrorDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Error")
        self.setLayout(qtw.QVBoxLayout())

        errorLabel = qtw.QLabel("The specified pdf file does not exist")

        self.layout().addWidget(errorLabel)


# Used to create drop-able line edits to simply drag and drop the PDF file
class DropLineEdit(qtw.QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            global droppedFile

            event.setDropAction(Qt.CopyAction)
            event.accept()

            file = event.mimeData().urls()[0]
            droppedFile = str(file.toLocalFile())

            self.setText(droppedFile)

        else:
            event.ignore()


speaker = pyttsx3.init()
availableVoices = speaker.getProperty("voices")

droppedFile = ""
mp3Path = ""
pdfPath = ""

app = qtw.QApplication([])
mainWindow = MainWindow()

app.exec_()