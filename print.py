import sys
import os
from escpos.printer import Usb
from escpos.printer import Dummy, Serial
import locale
locale.setlocale( locale.LC_ALL, '' )

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
			date = current_line[1].split(' ')
			date = date[0] + " " + date[1] + " " + date[2]+ " " + date[3]+ " " + date[4]
		if current_line[0] == 'guid':
			guid = current_line[1]


		if current_line[0] == "city":
			city = current_line[1]
		if current_line[0] == "state":
			state = current_line[1]
		if current_line[0] == "receiptId":
			receiptId = current_line[1]

		if current_line[0] == "leader":
			leader = current_line[1]
		if current_line[0] == "cashier":
			cashier = current_line[1]
		if current_line[0] == "subtotal":
			subtotal = current_line[1]
		if current_line[0] == "tax":
			tax = current_line[1]
		if current_line[0] == "total":
			total = current_line[1]
		if current_line[0] == "payments":
			payments = current_line[1]
        if current_line[0] == "eventType":
            eventType = current_line[1]


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


def trimName(str):
    if len(str) > 19 :
        while len(str) is not 19:
            str = str[:-1]
            if str[len(str) - 1] == " ":
                str = str[:-1] + "."
    if len(str) < 19:
        while len(str) is not 19:
            str = str + "."
    return str + "...   "


def trimQty(str):
    while len(str) is not 5:
        str = str + " "
    return str + "   "

def trimPrice(str):
    return locale.currency( float(str) )


event =   "        Seminario: " + city.strip() + ", " + state.strip()
leader =  "        Lider:     " + leader.strip()
cashier = "        Cajero:    " + cashier.strip()















""" Seiko Epson Corp. Receipt Printer M129 Definitions (EPSON TM-T88IV) """
p = Usb(0x04b8,0x0202,0)
p.set("Center")

p.image( os.path.dirname(os.path.realpath(__file__)) + "/logo.jpg")

p.text(date + "\n")
p.barcode( receiptId.strip() , "EAN13")
p.text("\n")

p.set("left")
p.text(event + "\n")
p.text(leader + "\n")
p.text(cashier + "\n")
p.text("\n")


p.set("left")

#				22		       3   4   3   5
#       1234567890123456789011   1234     12345
p.text("Item                     Qnt     Price\n")
#       Items[x][0]              Items[x][1] + " " + Items[x][2] + "\n")

for x in range(len(Items)):
	p.text( trimName( Items[x][0] )  + trimQty( Items[x][1] ) + trimPrice( Items[x][2] ) + "\n")

p.set("right")
p.text("\n\n\n")
p.text("Tax: " + tax + "\n")
#p.text("Total: "  \n")

p.text("Cash Payment:   100.00\n")
p.text("Change:   56.75\n")
p.set("Center", "A","B")
p.text("Gracias!\n")
p.set("Center", "A", "normal")
p.text("Customer Copy\n")
p.cut()
