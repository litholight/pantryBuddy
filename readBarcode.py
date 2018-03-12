
import zxing
reader = zxing.BarCodeReader()
barcode = reader.decode("peanut_butter.jpg")
print(barcode)
