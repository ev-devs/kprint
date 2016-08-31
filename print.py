import sys
import os
from escpos.printer import Usb

#with open('reciepts.txt') as fp
#	for line in fp
#		current_line = line.split(',')
#		print(current_line)


barcode_num = "1234567890123"
event = "Seminario: Los Angeles, CA"
date = "Date:"
time = "Time:"
leader = "Lider: "
item1 = "Como ganase a la gent...     1       14.00"
item2 = "La magia de pensar en...     1       10.00"
item3 = "El lado positivo de e...     1       14.00"
itemList =[item1,item2, item3]

""" Seiko Epson Corp. Receipt Printer M129 Definitions (EPSON TM-T88IV) """
p = Usb(0x04b8,0x0202,0)
p.set("Center")

p.image( os.path.dirname(os.path.realpath(__file__)) + "/logo.jpg")

p.text("\nDate: 08/11/16 ")
p.text("Time: 3:43\n")
p.barcode(barcode_num, "EAN13")
p.text("\n")
p.text(event + "\n")
p.text(leader + "Juan and Alicia Ruelas\n\n")
p.set("left")
p.text("Item\t                  Qnt       Price\n")

for x in range(len(itemList)):
	p.text(itemList[x] + "\n")

p.set("right")
p.text("\n\n\n")
p.text("Tax:   5.25\n")
p.text("Total:   43.25\n")
p.text("Cash Payment:   100.00\n")
p.text("Change:   56.75\n")
p.set("Center", "A","B")
p.text("Gracias!\n")
p.set("Center", "A", "normal")
p.text("Customer Copy\n")
p.cut()
