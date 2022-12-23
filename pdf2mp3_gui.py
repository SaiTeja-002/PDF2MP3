import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import pyttsx3
import PyPDF2 as pypdf
import random

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.resize(1100, 700)
        labelFontSize = 13
        lineEditFontSize = 10
        comboBoxFontSize = 9

        # Window properties
        self.setWindowTitle("PDF2MP3")
        self.setLayout(qtw.QVBoxLayout())

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

        pdfNameEntryField.move(600, 300)        # Damn it Didnt work

        # MP3 Name Entry Field
        mp3NameEntryField = qtw.QLineEdit()
        mp3NameEntryField.setObjectName("mp3Name")
        mp3NameEntryField.setFont(qtg.QFont("Helvetica", lineEditFontSize))
        mp3NameEntryField.setText(pdfNameEntryField.text())

        # Assistant Label
        assistantLabel = qtw.QLabel("Choose the assistant you would like to narrate")
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

        # Create MP3 button
        createMp3Button = qtw.QPushButton("Generate MP3", clicked=lambda:pdf2mp3())
        createMp3Button.setFont(qtg.QFont("Helvetica", labelFontSize))


        # Adding widgets to the layout
        self.layout().addWidget(pdfNameLabel)
        self.layout().addWidget(pdfNameEntryField)
        self.layout().addWidget(mp3NameLabel)
        self.layout().addWidget(mp3NameEntryField)
        self.layout().addWidget(assistantLabel)
        self.layout().addWidget(assistantComboBox)
        self.layout().addWidget(speechRateLabel)
        self.layout().addWidget(speechRateEntryField)
        self.layout().addWidget(narrateButton)
        self.layout().addWidget(createMp3Button)

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
            speechRateEntryField.setText("130")

        self.show()


speaker = pyttsx3.init()
availableVoices = speaker.getProperty("voices")

app = qtw.QApplication([])
mainWindow = MainWindow()

app.exec_()