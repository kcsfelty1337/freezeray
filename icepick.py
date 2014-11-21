import json
import urllib
import operator
from collections import OrderedDict
import MySQLdb


class icePick:
	def __init__(self):
		self.badItems = ['Big Kill','Unarmed Combat','Apoco-Fists','Bat Outta Hell','Bread Bite'] # Note on badItems: these items are difficult to get, so DO NOT use these for kits
		self.pristineParts = ['Pristine Robot Brainstorm Bulb','Pristine Robot Currency Digester']
		self.battlewornParts = ['Battle-Worn Robot Money Furnace','Battle-Worn Robot Taunt Processor','Battle-Worn Robot KB-808']
		self.reinforcedParts = ['Reinforced Robot Emotion Detector','Reinforced Robot Bomb Stabilizer','Reinforced Robot Humor Suppression Pump']
		self.weaponList = self.getWeapons()
		self.d = MySQLdb.connect(user='felty005',passwd='9m3rm6',db='felty005_tf2')
		self.dbc = self.d.cursor()

	def toBaseKit(self,item):
		return "Killstreak " + item + " Kit"
	def toSpecKit(self,item):
		return "Specialized Killstreak " + item + " Kit"
	def toProfKit(self,item):
		return "Professional Killstreak " + item + " Kit"
	def toSpecFab(self,item):
		return "Specialized Killstreak " + item + " Kit Fabricator"
	def toProfFab(self,item):
		return "Professional Killstreak " + item + " Kit Fabricator"
	def getPrice(self,item):
		#TODO Query data from SQL server, should make program MUCH faster.
		data = []
		self.d.query('SELECT * FROM marketData WHERE item = "{0}"'.format(item))
		r = self.d.store_result()
		a = r.fetch_row(0,1)
		for x in a:
			data.append(x['basickit'])
		return data
	def getWeapons(self):
		return  open("weaponNames","r").read().splitlines()
	def getBackpackItems(self):
		pass
	def sortDict(self,data,rev=False): #pass a dict {s:n} to sort by n, pass reverse=True to go from highest to lowest
		sortedData = sorted(data.items(),key=operator.itemgetter(1),reverse=rev)
		return sortedData
	def cheapSpecKit(self):
		difs = {}
		for i in self.weaponList:
			data = self.getPrice(self.toSpecKit(i))
			print data
			try:
				if i not in self.badItems:
					difs[i] = data
			except: pass
		print self.sortDict(difs)
		return self.sortDict(difs)[0]
	def cheapBasicKit(self):
	        difs = {}
	        for i in self.weaponList:
	                data = self.getPrice(self.toBaseKit(i))
	                try:
	                        if i not in self.badItems:
	                                difs[i] = data
	                except: pass
	        return self.sortDict(difs)[0]
	def averagePrice(self,parts):
	        total = 0
	        for i in parts:
			total += self.getPrice(i)
	        return total/len(parts)
	def costBuildProf(self):
		total = 0
		total += self.cheapSpecKit()[1]*2
		total += self.averagePrice(self.battlewornParts)*16
		total += self.averagePrice(self.reinforcedParts)*6
		total += self.averagePrice(self.pristineParts)*3
		return total
	def costBuildSpec(self):
	        total = 0
	        total += self.cheapBasicKit()[1]
	        total += self.averagePrice(self.battlewornParts)*24
	        total += self.averagePrice(self.reinforcedParts)*5
	        return total
	def profitableProf(self):	
		costMaterials =self.costBuildProf()
		profProfit = {}
		for x in self.weaponList:
			try:
				profProfit[x] = self.getPrice(self.toProfKit(x))/1.15 - costMaterials - self.getPrice(self.toProfFab(x))
				print "{0:40} {1:5}".format(x,profProfit[x])
			except: pass
		return self.sortDict(profProfit,True)
	def profitableSpec(self):
	        self.costMaterials = costBuildSpec()
	        specProfit = {}
	        for x in self.weaponNames:
	                try:
	                        specProfit[x] = self.getPrice(self.toSpecKit(x))/1.15 - costMaterials - self.getPrice(self.toSpecFab(x))
	                        print "{0:40} {1:5}".format(x,specProfit[x])
	                except: pass
	        return self.sortDict(specProfit,True)
	def queryPriceAPI(self,item):
		url = "http://steamcommunity.com/market/priceoverview/?country=US&currency=1&appid=440&market_hash_name="
                query = url + item
		try: result = json.load(urllib.urlopen((query)))
		except: result = ''
                try: return float(result['lowest_price'].replace('&#36;',''))
                except: return 0
	def updatePrices(self):
		for i in self.weaponList:
			basickit = self.queryPriceAPI(self.toBaseKit(i))
			speckit =  self.queryPriceAPI(self.toSpecKit(i))
			specfab =  self.queryPriceAPI(self.toSpecFab(i))
			profkit =  self.queryPriceAPI(self.toProfKit(i))
			proffab =  self.queryPriceAPI(self.toProfFab(i))
			print "{0:40}|{1:5}|{2:5}|{3:5}|{4:5}|{5:5}".format(i,basickit,speckit,specfab,profkit,proffab)
			push = u'INSERT INTO marketData (item,basickit,speckit,specfab,profkit,proffab) values ("{0}",{1},{2},{3},{4},{5})'.format(i,basickit,speckit,specfab,profkit,proffab)
			self.dbc.execute(push)
		for i in self.battlewornParts:
                        price = self.queryPriceAPI(i)
                        push = u'insert into marketData (item,basickit) values ("{0}",{1})'.format(i,price)
			print "{0:40} {1:5}".format(i,price)
			self.dbc.execute(push)
		for i in self.reinforcedParts:
                        price = self.queryPriceAPI(i)
                        push = u'insert into marketData (item,basickit) values ("{0}",{1})'.format(i,price)
			print "{0:40} {1:5}".format(i,price)
			self.dbc.execute(push)
		for i in self.pristineParts:
                        price = self.queryPriceAPI(i)
                        push = u'insert into marketData (item,basickit) values ("{0}",{1})'.format(i,price)
			print "{0:40} {1:5}".format(i,price)
			self.dbc.execute(push)
		self.d.commit()
mine = icePick()
for i in mine.weaponList:
	prices = mine.getPrice(i)
	print '{0:40} | {1}'.format(i,sum(prices)/len(prices))
