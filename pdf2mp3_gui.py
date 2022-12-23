import PyQt5.QtWidgets as qtw
from PyQt5.QtWidgets import QDialog
import PyQt5.QtGui as qtg
from PyQt5.QtGui import QPixmap
import pyttsx3
import PyPDF2 as pypdf
import random
import os


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.resize(700, 700)
        labelFontSize = 13
        lineEditFontSize = 10
        comboBoxFontSize = 9

        # Window properties
        self.setWindowTitle("PDF2MP3")
        self.setLayout(qtw.QGridLayout())

        # Logo
        imageLabel = qtw.QLabel()
        logoPixmap = QPixmap("Logo/logo_updated.png")
 
        # adding image to label
        imageLabel.setPixmap(logoPixmap)
 
        # Optional, resize label to image size
        imageLabel.resize(logoPixmap.width(), logoPixmap.height())

        # PDF Name Label
        pdfNameLabel = qtw.QLabel("Enter the name of the PDF File")
        pdfNameLabel.setFont(qtg.QFont("Helvetica", labelFontSize))

        # MP3 Name Label
        mp3NameLabel = qtw.QLabel("Generate the MP3 file as")
        mp3NameLabel.setFont(qtg.QFont("Helvectica", labelFontSize))

        # PDF Name Entry Field
        pdfNameEntryField = qtw.QLineEdit()
        pdfNameEntryField.setObjectName("pdfName")
        pdfNameEntryField.setFont(qtg.QFont("Helvetica", lineEditFontSize))

        # Completer for the pdfNameEntryField
        completer = qtw.QCompleter(listOfPdfs)
        pdfNameEntryField.setCompleter(completer)

        # MP3 Name Entry Field
        mp3NameEntryField = qtw.QLineEdit()
        mp3NameEntryField.setObjectName("mp3Name")
        mp3NameEntryField.setFont(qtg.QFont("Helvetica", lineEditFontSize))
        mp3NameEntryField.setText(pdfNameEntryField.text())

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

        # Success Label
        successLabel = qtw.QLabel("this shows the success of the operation")
        successLabel.setFont(qtg.QFont("Helvetica", labelFontSize))
        # successLabel.resize(20, 3)
        successLabel.adjustSize()

        # Narrate Button to demonstrate the assistant's voice with the selected parameters
        narrateButton = qtw.QPushButton("Narrate", clicked=lambda:narrate())
        narrateButton.setFont(qtg.QFont("Helvetica", labelFontSize))
        narrateButton.setToolTip("Listen how the assistant sounds with the selected properties")

        # Create MP3 button
        createMp3Button = qtw.QPushButton("Generate MP3", clicked=lambda:pdf2mp3())
        createMp3Button.setFont(qtg.QFont("Helvetica", labelFontSize))

        # Close Button
        closeButton = qtw.QPushButton("Close", clicked=lambda:terminateProgram())
        closeButton.setFont(qtg.QFont("Helvetica", labelFontSize))

        # Adding widgets to the layout
        self.layout().addWidget(pdfNameLabel,           0, 0)
        self.layout().addWidget(pdfNameEntryField,      0, 1)
        self.layout().addWidget(mp3NameLabel,           1, 0)
        self.layout().addWidget(mp3NameEntryField,      1, 1)
        self.layout().addWidget(assistantLabel,         2, 0)
        self.layout().addWidget(assistantComboBox,      2, 1)
        self.layout().addWidget(speechRateLabel,        3, 0)
        self.layout().addWidget(speechRateEntryField,   3, 1)
        # self.layout().addWidget(successLabel,           4, 0)
        # self.layout().addWidget(qtw.QPushButton("Random"),           4, 1)
        self.layout().addWidget(narrateButton,          5, 0)
        self.layout().addWidget(createMp3Button,        5, 1)
        self.layout().addWidget(closeButton,            6, 0, 1, 2)


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
            pdfName = pdfNameEntryField.text() + ".pdf"
            mp3Name = mp3NameEntryField.text() + ".mp3"

            pdfPath = "PDF Files/" + pdfName
            mp3Path = "Audio Files/" + mp3Name

            if(os.path.exists(pdfPath)):
                # Read the pdf file and initialize the speaker
                pdfReader = pypdf.PdfFileReader(open(pdfPath, 'rb'))


                # Extract data from each page and convert into a speakable form
                for pageNumber in range(pdfReader.numPages):
                    data = pdfReader.getPage(pageNumber).extractText()
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
                pdfNameEntryField.setText("")
                mp3NameEntryField.setText("")
                successLabel.setText("Conversion successful")
                speechRateEntryField.setText("130")

            else:
                successLabel.setText("No such file found")
                # def button_clicked(self, s):
                # print("click", s)

                errorDialog = ErrorDialog()
                # errorDialog.setWindowTitle("Error")
                errorDialog.exec()

        # Function to terminate the program
        def terminateProgram():
            app.quit()

        self.show()


class ErrorDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Error")
        self.setLayout(qtw.QVBoxLayout())

        errorLabel = qtw.QLabel("The specified pdf file does not exist")

        self.layout().addWidget(errorLabel)


speaker = pyttsx3.init()
availableVoices = speaker.getProperty("voices")

listOfPdfs = []

for file in os.listdir("PDF Files"):
    if file.endswith(".pdf"):
        listOfPdfs.append(file[:-4])    # Removing the ".pdf" part because it is being added in the clicked method of generateMp3 button

app = qtw.QApplication([])
mainWindow = MainWindow()

app.exec_()