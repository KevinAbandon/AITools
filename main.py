import kivy

from Metodos import *
from Reader import *
from UIclasses import * 

from kivy.core.window import Window
Window.size = (1000, 700)
Window.borderless = True
Window.left = 100
Window.top = 100

import matplotlib.pyplot as plt
import seaborn as sb    

class MetodosApp(App):

	Reader = FileReader()
	Result = None

	def build(self):
		root = BoxLayout(orientation='vertical')

		self.mainLayout = BoxLayout(orientation='horizontal')
		f = lambda : print("Test") #function test
		self.MB = MainBar(frun=self.RunMethod, fplot=self.graphicResults, fclose=self.closeW)

		self.MM = MetodosMenu(reader=self.Reader)
		self.R =Results()
		self.MM.getResultbox(self.R)
		self.mainLayout.add_widget(self.MM)
		self.mainLayout.add_widget(self.R)

		root.add_widget(self.MB)
		root.add_widget(self.mainLayout)

		return root

	def closeW(self):
		Window.close()

	def RunMethod(self):
		metodo = self.MM.MetodoName
		if(metodo == "APRIORI"):
			result = list(getApriori(self.MM.CU.MetodoActual.utilVars, self.Reader.dataset,
			self.MM.CU.MetodoActual.Support,
			self.MM.CU.MetodoActual.Confidence,
			self.MM.CU.MetodoActual.Lift, 2))
			s =''
			for item in result:
				  pair = item[0]
				  items = [x for x in pair]
				  s+="Regla: " + items[0]+"->"+items[1]+'\n'
				  s+="Soporte: "+str(items[1])+'\n'
				  s+="Confianza "+str(item[2][0][2])+'\n'
				  s+="Lift: "+str(item[2][0][3])+'\n'
				  s+="====================================="+'\n'
			self.R.Resultado.text = s

		elif(metodo =='PEARSON'):
			result = getCorrPearson(self.MM.CU.MetodoActual.utilVars, self.Reader.data_frame)
			self.R.Resultado.text = "Matriz de Correlacion:\n\n{}".format(result)
			self.Result = result

		elif(metodo =='EUCLIDEAN'):
			result = getEuclideanDistance(self.MM.CU.MetodoActual.indices, self.MM.CU.MetodoActual.utilVars, self.Reader.data_frame)
			try:	
				s = "Matriz de distancias: \n\n"
				for i in self.MM.CU.MetodoActual.indices:
					s += "\t\t\t\t"+str(self.MM.READER.data_frame.iloc[i][0])
				s += "\n"
				for i in range(len(result)):
					s += str(self.MM.READER.data_frame.iloc[self.MM.CU.MetodoActual.indices[i]][0])
					for r in result[i]:
						s += "\t\t\t\t"+str(r)
					s += "\n"
				self.Result = result
			except:
				s = "Variables no validas, variables numericas unicamente."

			self.R.Resultado.text = s

		elif(metodo == 'KMEANS'):
			try:
				result = getKMeans(self.MM.CU.MetodoActual.utilVars, self.Reader.data_frame, self.MM.CU.MetodoActual.n)
				centroides = pd.DataFrame(result.cluster_centers_.round(4))
				s = "Cuenta de Agrupaciones:\n{}\n\nLabels:\n{}\n\nCentroides:\n{}\n\nData Frame:\n{}\n\n".format(self.MM.READER.data_frame.groupby(['CLUSTER'])['CLUSTER'].count(),
					result.labels_, centroides, self.MM.READER.data_frame)
				 
				print('Termino KMEANS.')
			except:
				s = "Variables no validas, variables numericas unicamente."
			self.R.Resultado.text = s 
		elif(metodo == 'LOGISTIC'):
			try:
				result = getLogisticRegresion(self.MM.CU.MetodoActual.Predictvar, self.MM.CU.MetodoActual.utilVars, self.Reader.data_frame)
				s = result[0]+result[1]+result[2]
			except:
				s = "Variables no validas, variables numericas unicamente."
			self.R.Resultado.text = s 
		else:
			print("Configuracion invalida.")

	def graphicResults(self):
		metodo = self.MM.MetodoName
		if(metodo == "PEARSON"):
			try:
				plt.figure(figsize = (20,10))
				sb.heatmap(self.Result, annot = True)
				plt.show()
				print("Plot")
			except:
				print("Grafica no disponible")
		elif(metodo =='EUCLIDEAN'):
			try:
				plt.figure(figsize = (20,10))
				sb.heatmap(pd.DataFrame(self.Result), annot = True)
				plt.show()
				print("Plot")
			except:
				print("Grafica no disponible")
		else:
			print("Grafica no disponible")
			

if __name__ == '__main__':
	MetodosApp().run()