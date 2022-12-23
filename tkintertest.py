path = "C:\Users\teja0\OneDrive - iiit-b\IIITB-OneDrive\PersonalProjects\PDF2MP3\PDF Files\Assignment-6.pdf"

mp3Path = path[:-3]
mp3Path += ".mp3"

# path = path.replace("\\", "#")
# lst = path.split("#")

print(mp3Path)



def downloadMP3():
    fileName = QFileeDialog.getOpenFileName(self, "Open File", "", "MP3 Files (*.mp3)")

    if(fileName):
        print(str(fileName))