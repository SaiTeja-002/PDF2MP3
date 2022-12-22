import pyttsx3
import PyPDF2 as pypdf

# Take the name of the pdf as an input from the user
pdfName = input("Enter the name of the pdf without extension : ")
mp3Name = pdfName + ".mp3"
pdfName = pdfName + ".pdf"


# Read the pdf file and initialize the speaker
pdfReader = pypdf.PdfFileReader(open(pdfName, 'rb'))
speaker = pyttsx3.init()


# Extract data from each page and convert into a speakable form
for pageNumber in range(pdfReader.numPages):
    data = pdfReader.getPage(pageNumber).extractText()
    cleanData = data.strip().replace("\n", "    ")


# Converting the cleanData into an mp3 file
speaker.save_to_file(cleanData, mp3Name)

speaker.runAndWait()
speaker.stop()