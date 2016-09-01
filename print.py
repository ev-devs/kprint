import sys
import os
from escpos.printer import Usb
from escpos.printer import Dummy, Serial

with open(os.path.dirname(os.path.realpath(__file__)) + "/receipt.txt") as fp:

	Items = []
	Cards = []
	Cashes = []

	ItemsLoop = False
	CashesLoop = True
	CardsLoop = True


	for line in fp:
		# first we need to split it into an array of strings
		current_line = line.strip().split(',')

		if current_line[0] == "date":
			date = current_line[1]
		if current_line[0] == 'guid':
			guid = current_line[1]


		if current_line[0] == "city":
			city = current_line[1]
		if current_line[0] == "state":
			state = current_line[1]
		if current_line[0] == "recieptId":
			recieptId = current_line[1]

		if current_line[0] == "leader":
			leader = current_line[1]

		if current_line[0] == "subtotal":
			subtotal = current_line[1]
		if current_line[0] == "tax":
			tax = subtotal[1]
		if current_line[0] == "total":
			total = current_line[1]
		if current_line[0] == "payments":
			payments = current_line[1]


		if current_line[0] == "ItemsBegin":
			ItemsLoop = True
		if current_line[0] == "ItemsEnd":
			ItemsLoop = False
		if ItemsLoop == True  and len(current_line) == 3:
			Items.append( (current_line[0], current_line[1], current_line[2]) )
		if current_line[0] == "BeginCashes":
			CashesLoop = True
		if current_line[0] == "EndCashes":
			CashesLoop = False
		if CashesLoop == True and len(current_line) == 2:
			Cashes.append( (current_line[0], current_line[1]) )
		if current_line[0] == "BeginCards":
			CardsLoop = True
		if current_line[0] == "EndCards":
			CardsLoop = False
		if CardsLoop == True and len(current_line) == 6:
			Cards.append( (current_line[0], current_line[1], current_line[2], current_line[3], current_line[3], current_line[4], current_line[5]) )

		#print current_line


barcode_num = guid
event = "Seminario: Los Angeles, CA"
date = "Date:"
time = "Time:"
leader = "Lider: "
item1 = "Como ganase a la gent...     1       14.00"
item2 = "La magia de pensar en...     1       10.00"
item3 = "El lado positivo de e...     1       14.00"
itemList = [item1,item2, item3]

""" Seiko Epson Corp. Receipt Printer M129 Definitions (EPSON TM-T88IV) """
p = Usb(0x04b8,0x0202,0)
p.set("Center")

p.image( os.path.dirname(os.path.realpath(__file__)) + "/logo.jpg")

p.text("\nDate: 08/11/16 ")
p.text("Time: 3:43\n")
#p.barcode("{B012ABCDabcd" + "1234567891", "CODE128", function_type="B", width=2, font="B")
p.barcode("200002687132", "EAN13")

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
