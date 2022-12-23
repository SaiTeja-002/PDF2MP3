import pyttsx3
import PyPDF2 as pypdf
import random

# A function that takes the name of a pdf file and converts it into an audio file
def pdf2mp3():
    # Take the name of the pdf as an input from the user
    pdfName = input("Enter the name of the pdf without extension : ")
    mp3Name = pdfName + ".mp3"
    pdfName = pdfName + ".pdf"

    pdfPath = "PDF Files/" + pdfName
    mp3Path = "Audio Files/" + mp3Name


    # Read the pdf file and initialize the speaker
    pdfReader = pypdf.PdfFileReader(open(pdfPath, 'rb'))


    # Extract data from each page and convert into a speakable form
    for pageNumber in range(pdfReader.numPages):
        data = pdfReader.getPage(pageNumber).extractText()
        cleanData = data.strip().replace("\n", "    ")


    # Setting the properties of the audio file
    speedRate = int(input("Please select the speach rate (Recommended value - 130) : "))
    speaker.setProperty("rate", speedRate)


    # Converting the cleanData into an mp3 file
    speaker.save_to_file(cleanData, mp3Path)

    speaker.runAndWait()
    speaker.stop()


speaker = pyttsx3.init()

speech = "Warm greetings master!. I am really happy to serve you today. What would you like me to do for you?"
# speaker.say(speech)
# speaker.runAndWait()

availableVoices = speaker.getProperty("voices")
print(len(availableVoices))
print(availableVoices)

for i in range(len(availableVoices)):
    print(availableVoices[i].id)
    speaker.setProperty("voice", availableVoices[i].id)

    speaker.say(speech)
    speaker.runAndWait()

speaker.stop()

# Optimum rate - 130

# while(True):
#     speedRate = int(input("Enter the desired speed rate : "))
#     speaker.setProperty("rate", speedRate)
#     speaker.say(speech)
#     speaker.runAndWait()