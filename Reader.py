import json
import pandas as pd
from xml.etree import ElementTree

class varNode():
	def __init__(self, nom, i):
		self.nombre = nom
		self.index = i

class FileReader():
	def __init__(self):
		self.varList = []
		self.dataset = []
		self.data_frame = None

	def readTXT(self, File):
		self.varList = []
		self.dataset = []
		self.data_frame = None
		data = pd.read_table(File)
		i = 0
		for d in data:
			self.varList.append((varNode(d, i)))
			i+=1
		self.dataset = [[str(col) for col in row] for row in data.values]
		self.data_frame = data
		return True

	def readCSV(self, File):
		self.varList = []
		self.dataset = []
		self.data_frame = None
		data = pd.read_csv(File)
		i = 0
		for d in data:
			self.varList.append((varNode(d, i)))
			i+=1
		self.dataset = [[str(col) for col in row] for row in data.values]
		self.data_frame = data

	def writeCSV(self, File, Datos):
		F = open(File, 'w') 
		S = ''
		for d in Datos:
			for i in d:
				S += i+','
			S[-1] = '\n'
		F.write(S)
		F.close()
		return True

	def readXML(self, File):
		self.varList = []
		self.dataset = []
		arbol = ElementTree.parse(File)
		root =  arbol.getroot()
		self.varList = 	[varNode(root[0][i].tag, i) for i in range(len(root[0]))]
		self.dataset = [[col.text for col in row] for row in root]
		return True

	def readJSON(self, File):
		self.varList = []
		self.dataset = []
		data = json.load(open(File, 'r'))
		var = [d for d in data[0]]
		self.varList = [varNode(var[i], i) for i in range(len(var))]
		self.dataset = [list(d.values()) for d in data]
		return True
'''
Reader = FileReader()
Reader.readXML('dataset.xml')
print([(n.nombre, n.index) for n in Reader.varList])
print(Reader.dataset[0])
'''