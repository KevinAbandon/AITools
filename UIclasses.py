import kivy

from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput	import TextInput 
from kivy.uix.actionbar import ActionBar
from kivy.uix.actionbar import ActionGroup
from kivy.uix.actionbar import ActionItem
from kivy.uix.actionbar import ActionView
from kivy.uix.actionbar import ActionButton, ActionPrevious
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView

from kivy.lang import Builder

from Metodos import *

Builder.load_file('UI.kv')

class MainBar(ActionBar):
	def __init__(self, frun, fplot, fclose,**kwargs):
		super(MainBar, self).__init__(**kwargs)
		self.background_color=[1.7,1.7,1.7,1]
		self.fRUN = frun
		self.fPLOT =fplot 
		self.fCLOSE = fclose

class MetodosMenu(BoxLayout):
	def __init__(self, reader,**kwargs):
		super(MetodosMenu, self).__init__(**kwargs)
		self.READER = reader
		self.MetodoName = 'SELECT'
		self.CM = ConfigMenu(loadFileFunc=self.loadFile, selectMedotoFunc=self.selectMetodo)
		self.CU = ConfigUtilities(varL = self.READER.varList)
		self.add_widget(self.CM)
		self.add_widget(self.CU)

	def loadFile(self):
		tipo = str(self.CM.ArchivoType)
		archivo = self.CM.ArchivoName
		if(tipo != 'SELECT' and archivo != ''):
			if(tipo == 'TXT'):
				self.READER.readTXT(archivo)
			elif(tipo == 'CSV'):
				self.READER.readCSV(archivo)
			elif(tipo == 'XML'):
				self.READER.readXML(archivo)
			elif(tipo == 'JSON'):
				self.READER.readJSON(archivo)
			else:
				print('Tipo de archivo no permitido.\n')

		else:
			print('Error, parametros incorrectos.\n')

		self.CU.triggerTransition(self.MetodoName)
		print(self.READER.data_frame)
		self.setValueList()
		self.CU.dataframe = self.READER.data_frame

	def setValueList(self):
		self.CU.varList = self.READER.varList

	def selectMetodo(self, text):
		self.MetodoName = text
		print('Metodo: '+self.MetodoName)
		self.CU.triggerTransition(text)

	def getResultbox(self, rb):
		self.CU.resultbox = rb


class ConfigMenu(BoxLayout):
	def __init__(self, loadFileFunc, selectMedotoFunc,**kwargs):
		super(ConfigMenu, self).__init__(**kwargs)
		self.size_hint= (1.0, 0.2)
		self.ArchivoType = 'SELECT'
		self.ArchivoName = ''
		self.LFF = loadFileFunc
		self.SMF = selectMedotoFunc

	def selectTipoArchivo(self, text):
		self.ArchivoType = text
		print('Tipo de Archivo: '+self.ArchivoType)

	def getFileName(self, text):
		self.ArchivoName = text
		print('Nombre de Archivo: '+self.ArchivoName)


class ConfigUtilities(BoxLayout):
	def __init__(self, varL,**kwargs):
		super(ConfigUtilities, self).__init__(**kwargs)
		self.dataframe = None
		self.varList = varL
		self.MetodoActual = BoxLayout()
		self.resultbox = None

	def setVarButtons(self):
		Box = BoxLayout(orientation='vertical')
		Scroll = ScrollView(size_hint=(0.7, 0.8),pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
		varView = GridLayout(cols=1, padding=10, spacing=10,
                size_hint=(None, None), width=500)
		varView.bind(minimum_height=varView.setter('height'))
		Box.add_widget(Label(text='Seleccion de Variables:',pos_hint={'center_x': .5, 'center_y': .5}, size_hint=(1, .1)))
		try:
			for v in self.varList:
				varView.add_widget(TG(text=str(v.nombre), contenido=v,
					downfunc = self.addVartoList, normalfunc=self.removeVartoList,
					size=(157, 27), pos_hint={'center_x': .5, 'center_y': .5}))
			Scroll.add_widget(varView)
		except:
			print('Data Frame vacio.')
		Box.add_widget(Scroll)
		self.MetodoActual.add_widget(Box)

	def setVarIndices(self):
		Box = BoxLayout(orientation='vertical')
		Scroll = ScrollView(size_hint=(0.7, 0.8),pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
		varView = GridLayout(cols=1, padding=10, spacing=10,
                size_hint=(None, None), width=500)
		varView.bind(minimum_height=varView.setter('height'))
		Box.add_widget(Label(text='Seleccion de Elementos:', pos_hint={'center_x': .5, 'center_y': .5}, size_hint=(1, .1)))
		i = 0
		try:
			for v in self.dataframe.iloc:
				varView.add_widget(TG(text=str(v[0]), contenido=i,
					downfunc = self.addVartoIndexList, normalfunc=self.removeVartoIndexList,
					size=(157, 27), pos_hint={'center_x': .5, 'center_y': .5}))
				i += 1
			Scroll.add_widget(varView)
		except:
			print('Data Frame vacio.')
		
		Box.add_widget(Scroll)
		self.MetodoActual.add_widget(Box)

	def varPredict(self):
		self.MetodoActual.Spin.values = set([v.nombre for v in self.varList])

	def addVartoList(self, v):
		self.MetodoActual.utilVars.append(v)
		
	def removeVartoList(self, v):
		self.MetodoActual.utilVars.remove(v)
		
	def addVartoIndexList(self, i):
		self.MetodoActual.indices.append(i)
		print(self.MetodoActual.indices)
		
	def removeVartoIndexList(self, i):
		self.MetodoActual.indices.remove(i)
		print(self.MetodoActual.indices)
		
	def triggerTransition(self, text):
		self.clear_widgets()
		if(text =="APRIORI"):
			print("Apriori")
			self.MetodoActual = AprioriConfig()
			self.setVarButtons()

		if(text =="PEARSON"):
			print("Pearson")
			self.MetodoActual = PearsonConfig()
			self.setVarButtons()

		if(text == "EUCLIDEAN"):
			print("Euclidean")
			self.MetodoActual = EuclideanConfig()
			self.setVarButtons()
			self.setVarIndices()

		if(text=="KMEANS"):
			print("KMeans")
			self.MetodoActual = KMeansConfig()
			self.setVarButtons()

		if(text=="LOGISTIC"):
			print("LOGISTIC")
			self.MetodoActual = LOGISTICConfig()
			self.setVarButtons()
			self.varPredict()

		self.add_widget(self.MetodoActual)

class AprioriConfig(BoxLayout):
	def __init__(self, **kwargs):
		super(AprioriConfig, self).__init__(**kwargs)
		self.Support = 0.0045
		self.Confidence = 0.2
		self.Lift = 3
		self.utilVars = []

	def getSupport(self, text):
		try:
			self.Support = float(text)
			print('Soporte minimo: '+str(self.Support))
		except ValueError:
			print('Conversion no se pudo realizar.')

	def getConfidence(self, text):
		try:
			self.Confidence = float(text)
			print('Confianza minima: '+str(self.Confidence))
		except ValueError:
			print('Conversion no se pudo realizar.')

	def getLift(self, text):
		try:
			self.Lift = int(text)
			print('Elevacion minima:'+str(self.Lift))
		except ValueError:
			print('Conversion no se pudo realizar.')

class PearsonConfig(BoxLayout):
	def __init__(self,**kwargs):
		super(PearsonConfig, self).__init__(**kwargs)
		self.utilVars = []

class EuclideanConfig(BoxLayout):
	def __init__(self,**kwargs):
		super(EuclideanConfig, self).__init__(**kwargs)
		self.utilVars = []
		self.indices =[]

class KMeansConfig(BoxLayout):
	def __init__(self,**kwargs):
		super(KMeansConfig, self).__init__(**kwargs)
		self.utilVars = []
		self.n = 1 

	def getnClusters(self, text):
		try:
			self.n = int(text)
			print('Numero de clusters: '+str(self.n))
		except ValueError:
			print('Conversion no se pudo realizar.')

class LOGISTICConfig(BoxLayout):
	def __init__(self,**kwargs):
		super(LOGISTICConfig, self).__init__(**kwargs)
		self.Predictvar = None
		self.varL = set()
		self.utilVars = []
		self.Spin = Spinner(text="Variable Predictora",
			on_text=self.selectVarPredict, size_hint= (1, 0.1),
			values=self.varL)
		self.Spin.bind(on_press=self.selectVarPredict)
		self.add_widget(self.Spin)

	def selectVarPredict(self, instance):
		self.Predictvar = self.Spin.text
		print("Variable Predcitoria: {}".format(self.Predictvar))

class TG(ToggleButton):
	def __init__(self, contenido,downfunc,normalfunc,**kwargs):
		super(TG, self).__init__(**kwargs)
		self.Node = contenido
		self.downFunc =downfunc
		self.normalFunc = normalfunc


class Results(BoxLayout):
	def __init__(self, **kwargs):
		super(Results, self).__init__(**kwargs)
		self.orientation = 'vertical'
		self.Resultado = TextInput()
		self.add_widget(self.Resultado)
		self.SaveRes = Button(text="Guardar Resultados", size_hint=(1, .07))
		self.SaveRes.bind(on_press=self.saveres)
		self.add_widget(self.SaveRes)

	def saveres(self, instance):
		File = open("RESULTADO.txt", "w")
		File.write(self.Resultado.text)
		File.close()
		print("Resultado guardado.")



'''
class testApp(App):
	def build(self):
		root = BoxLayout(orientation = 'vertical')
		f = lambda : print("Test")
		root.add_widget(MainBar(frun=f))
		root.add_widget(ConfigMenu())
		root.add_widget(Button(text='Test'))
		return root
testApp().run()
'''

