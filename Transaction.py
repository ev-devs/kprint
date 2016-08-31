import json
import pymongo
from escpos.printer import Usb
from pymongo import MongoClient
from bson import BSON
from bson import json_util



class Transaction:

    def __init__(self, GUID):
        self.client = MongoClient('localhost', 27017)

        if self.client == None:
            print "could no connect to the mongo database"

        self.db = self.client.transactions
        self.collection = self.db.transactions
        self.guid = GUID
        self.trans = self.collection.find_one({ "guid" : self.guid})

        self.transDumpJSON = json.dumps(self.trans, sort_keys=True, indent=4, default=json_util.default)
        self.loadJSON = json.loads(self.transDumpJSON)

        self.platinum = ""
        self.total = ""
        self.subtotal = ""
        self.location = ""
        self.tax = ""

        self.cashes = []
        self.cards = []
        self.items = []


    def parseJSON(self):

        for key in self.loadJSON:

            if key == "platinum":
                self.platinum = self.loadJSON[key]
            if key == "total":
                self.platinum = self.loadJSON[key]
            if key == "subtotal":
                self.subtotal = self.loadJSON[key]
            if key == "location":
                self.location = self.loadJSON[key]
            if key == "tax":
                self.tax = self.loadJSON[key]
            if key == "cashes":
                self.parseCashes(self.loadJSON[key])
            if key == "cards":
                self.parseCards(self.loadJSON[key])
                #print self.loadJSON[key]
            if key == "items":
                self.parseItems(self.loadJSON[key])


            #print self.loadJSON[key]


    def parseCashes(self, cashesObj):
        cashesDumpJSON = json.dumps(cashesObj, sort_keys=True, indent=4, default=json_util.default)
        cashesLoadJSON = json.loads(cashesDumpJSON)

        for key in cashesLoadJSON:
            print cashesLoadJSON[key]


    def parseCards(self, cardsArr):
        cardsDumpJSON = json.dumps(cardsArr[0], sort_keys=True, indent=4, default=json_util.default)
        cardsLoadJSON = json.loads(cardsDumpJSON)

        newCardsArr = []

        #for key in cardsArr:
        #    print cardsArr[key]
        #print json.dumps(cardsArr[0], sort_keys=True, indent=4, default=json_util.default)

        tempCard =
        for key in cardsLoadJSON:
            if key == "amount":

            print cardsLoadJSON[key]



    def parseItems(self, itemsObj):
        test = ""
    def doEverything(self):
        self.parseJSON()


#class Transaction:

#	def __init__(self, GUID):
#       client = MongoClient('localhost', 27017)
#        db = client.transactions
#        collection = db.transactions
 #       guid = GUID


#cur_trans = collection.find_one({"guid": guid})
#cur_trans = json.dumps(cur_trans, sort_keys=True, indent=4, default=json_util.default)
#cur_trans = json.loads(cur_trans)

#for key in cur_trans:
#	if key == "guid":transactions
#		print cur_trans[key]