# ############################################################################
#
# Base 64 encode / decode
#
# Can be run from command-line, or opens UI with no arguments
# arguments: [inputfilename] [outputfilename] [coding]
#
#   coding = b64encode | b64decode
##
# ############################################################################

import base64
import sys
import tkinter as Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

# ############################################################################
# constants

BASE64ENCODING     = 'b64encode'
BASE64DECODING     = 'b64decode'
B64ENCODECHUNKSIZE = 3*1024  # must be a multiple of 3
B64DECODECHUNKSIZE = 4*1024  # must be a multiple of 4

# ############################################################################

def stream_file(input, blocksize):
    eof=False
    while not eof:
        block = input.read(blocksize)
        yield block
        if not block: eof=True

# ############################################################################

def Base64Encode(inputFilename, outputFilename):
    input = open(inputFilename, 'rb')
    stream = stream_file(input, B64ENCODECHUNKSIZE)
    output = open(outputFilename, 'wb')

    try:
        for chunk in stream:
            output.write(base64.b64encode(chunk))
    finally:
        output.close()
        input.close()

# ############################################################################

def Base64Decode(inputFilename, outputFilename):
    input = open(inputFilename, 'rb')
    stream = stream_file(input, B64DECODECHUNKSIZE)
    output = open(outputFilename, 'wb')

    for chunk in stream:
        output.write(base64.b64decode(chunk))

    output.close()
    input.close()

# ############################################################################

def GenerateOutput(input, output, coding):

    if coding==BASE64ENCODING:
        return Base64Encode(input, output)
    elif coding==BASE64DECODING:
        return Base64Decode(input, output)
    else:
        print(f"Unsupported encoding: coding")

    print("Done.")


# ############################################################################

class Application(Tk.Frame):

    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        gridrow = 0

        self.inputButton = Tk.Button(self, text='Input File...', command=self.setInputFile)
        self.inputButton.grid(sticky=Tk.NE)
        self.inputFilename = Tk.Entry(self, text="", width=80)
        self.inputFilename.grid(row=gridrow, column=1)
        gridrow += 1

        self.outputButton = Tk.Button(self, text='Output File...', command=self.setOutputFile)
        self.outputButton.grid(sticky=Tk.NE)
        self.outputFilename = Tk.Entry(self, text="", width=80)
        self.outputFilename.grid(row=gridrow, column=1)
        gridrow += 1

        self.coding = Tk.StringVar()
        self.radioEncode = Tk.Radiobutton(self, text='Base 64 Encode', value=BASE64ENCODING, variable=self.coding)
        self.radioEncode.grid(row=gridrow, column=0)
        self.radioDecode = Tk.Radiobutton(self, text='Base 64 Decode', value=BASE64DECODING, variable=self.coding)
        self.radioDecode.grid(row=gridrow, column=1)
        self.coding.set(BASE64ENCODING)
        gridrow += 1

        self.goButton = Tk.Button(self, text="Go", command=self.generateOutput)
        self.goButton.grid(row=gridrow, columnspan=2)

    def setInputFile(self):
        self.inputfilename = askopenfilename(filetypes = (("any file","*.*"),("all files","*.*")))
        self.inputFilename.delete(0, Tk.END)
        self.inputFilename.insert(0, self.inputfilename)

    def setOutputFile(self):
        self.outputfilename = asksaveasfilename(filetypes = (("any file","*.*"),("all files","*.*")))
        self.outputFilename.delete(0, Tk.END)
        self.outputFilename.insert(0, self.outputfilename)

    def generateOutput(self):
        input = self.inputFilename.get()
        output = self.outputFilename.get()
        coding = self.coding.get()

        GenerateOutput(input, output, coding)


# ############################################################################

args = len(sys.argv) - 1
if args < 1:
    app = Application()
    app.master.title('Base 64 Encode/Decode')
    app.mainloop()
elif args < 3:
    print("Usage: encode.py inputfilename outputfilename coding")
    print("coding = b64encode | b64decode")
else:
    # arguments: [inputFilename] [outputFilename] [coding]
    inputFilename = sys.argv[1]
    outputFilename = sys.argv[2]
    coding = sys.argv[3]

    GenerateOutput(inputFilename, outputFilename, coding)

# ############################################################################
