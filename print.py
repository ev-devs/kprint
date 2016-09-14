import sys
import os
from escpos.printer import Usb
from escpos.printer import Dummy, Serial
#from escpos import *
#import locale
#locale.setlocale( locale.LC_ALL, 'en_US.UTF8' )

#reload(sys)
#sys.setdefaultencoding('utf8')

Items = []
Cards = []
Cashes = []

with open(os.path.dirname(os.path.realpath(__file__)) + "/receipt.txt") as fp:

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
            #eventType = current_line[1]
            eventType = "s"
        if current_line[0] == "isEnglish":
            isEnglish = current_line[1]
        if current_line[0] == "ItemsBegin":
			ItemsLoop = True
        if current_line[0] == "ItemsEnd":
            ItemsLoop = False
        if ItemsLoop == True  and len(current_line) == 3:
			Items.append( (current_line[0], current_line[1], current_line[2]) )

        if current_line[0] == "BeginCashes":
            CardsLoop = False
            CashesLoop = True
        if current_line[0] == "EndCashes":
			CashesLoop = False

        if CashesLoop == True and len(current_line) == 2:
			Cashes.append( (current_line[0], current_line[1]) )

        if current_line[0] == "BeginCards":
            CardsLoop = True
            CashesLoop = False
        if current_line[0] == "EndCards":
			CardsLoop = False
        if CardsLoop == True and len(current_line) == 6:
			Cards.append( (current_line[0], current_line[1], current_line[2], current_line[3], current_line[4], current_line[5] ) )
fp.close()

with open(os.path.dirname(os.path.realpath(__file__)) + "/receipt.txt") as fp:

    CashesLoop = False
    Cashes = []

    for line in fp:
	current_line = line.strip().split(',')

	if current_line[0] == "BeginCashes":
            CashesLoop = True
        if current_line[0] == "EndCashes":
            CashesLoop = False
        if CashesLoop == True and len(current_line) == 2:
            Cashes.append( (current_line[0], current_line[1]) )


		#print current_line
eventType = "s"

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

def trimPrice(stri):
    #return str( locale.currency( float(stri) ) 
    #return stri
    return '${:,.2f}'.format(float(stri))

def trimBottomRight(str):
    if len(str) < 9:
        while len(str) is not 9:
            str = " " + str
    return str

def trimHeader(str):
    if (len(str) > 42):
        while len(str) > 42:
            str = str[:-1]

    return str


def printEnglish():
    stringasdf = "asdfasd"




def printSpanish(date, guid, city, state, receiptId, leader, cashier, subtotal, tax, total, payments, eventType, Items, Cashes, Cards):


    temp = leader.strip().split(' ')
    leader = ""
    for x in range(len(temp)):
        if (len(temp[x]) > 0):
            leader = leader + " " + temp[x].strip()

    event =   "Seminario  : " + city.strip() + ", " + state.strip()
    leader =  "Lider      : " + trimHeader( leader.strip() )
    cashier = "Cajero     : " + cashier.strip()



    #stuff
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
    p.text("Producto                 Qty     Precio\n")
    #       Items[x][0]              Items[x][1] + " " + Items[x][2] + "\n")

    for x in range(len(Items)):
        #print repr(trimPrice[x][2])
	p.text( u''.join( trimName( Items[x][0] )  + trimQty( Items[x][1] ) + trimPrice( Items[x][2] ) + "\n") )

    if len(Cards) > 0:
        p.set("center")
        p.text("\n")
        p.text("=====Pagos De Tarjeta=====")
        p.text("\n\n")
        p.set('left')

        for card in Cards:
            cardStr =           "Tipo De Tarjeta        : " + card[0] + "\n"
            cardStr = cardStr + "Numero De Cuenta       : " + card[1] + "\n"
            cardStr = cardStr + "Nombre En La Tarjeta   : " + card[2].strip() + "\n"
            cardStr = cardStr + "Codigo de Autorizacion : " + card[3] + "\n"
            cardStr = cardStr + "ID de transaccion      : " + card[4] + "\n"
            cardStr = cardStr + "Cantidad               : " + trimPrice( str(card[5]) ) + "\n"
            cardStr = cardStr + "\n"
            p.text(cardStr)

    if len(Cashes) > 0:
        p.set('center')
        p.text("\n")
        p.text('=====Pagos En Efectivo=====')
        p.text("\n\n")
        p.set('left')
        for cash in Cashes:
            cashStr =           "Efectivo Recibido  : " +  trimPrice ( str( cash[0]) )  + "\n"
            cashStr = cashStr + "Cambio             : " +  trimPrice ( str( cash[1]) ) + "\n"
            cashStr = cashStr + "\n"
            p.text(cashStr)



    p.text("\n\n\n")
    p.set("right")
    p.text("Total parcial   : " + trimBottomRight( trimPrice( str(subtotal) ) )   + "\n")
    p.text("Impuestos       : " + trimBottomRight( trimPrice( str(tax) ) )         + "\n")
    p.text("Total           : " + trimBottomRight( trimPrice( str(total) ) )       + "\n\n")

    p.set("Center", "A","B")
    p.text("Gracias!\n")
    p.set("Center", "A", "normal")
    p.text("Customer Copy\n")
    p.cut()





isEnglish = "false"
if isEnglish == "false":
    printSpanish(date, guid, city, state, receiptId, leader, cashier, subtotal, tax, total, payments, eventType, Items, Cashes, Cards)
if isEnglish == "true":
    printEnglish(date, guid, city, state, receiptId, leader, cashier, subtotal, tax, total, payments, eventType, Items, Cashes, Cards)
