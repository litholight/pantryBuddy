
import zxing
import os
#from upcdb import UPCDB

barcodes = []
reader = zxing.BarCodeReader()
for file in os.listdir("./frames"):
    if file.endswith(".jpg"):
        pictureDecode = reader.decode("./frames/" + file)
        if pictureDecode not in barcodes and pictureDecode is not None:
            barcodes.append(pictureDecode)

file1 = open("barcode.txt",'w')
file1.write(barcodes.__str__()[10:22])
file1.close()

