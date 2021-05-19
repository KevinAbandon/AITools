import numpy as np
from apyori import apriori
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn import linear_model
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

def getApriori(variables, dataset, min_supp, min_conf, min_lif, min_len):
	data = []
	for d in dataset:
		row = []
		for v in variables:
			if(d[v.index] == 'true' or d[v.index] == 'T'):
				row.append(v.nombre)
			else:
				row.append('nan')
		data.append(row)
	Reglas = apriori(data, min_support=min_supp, min_confidence=min_conf, min_lift=min_lif, min_lenght=min_len)
	return list(Reglas)


def getCorrPearson(varl, data_frame):
	temp = dict()
	for v in varl:
		temp[v.nombre] = data_frame[v.nombre]
	Temp = pd.DataFrame(dict(temp))
	return Temp.corr(method='pearson')

def getEuclideanDistance(index, varl, data_frame):
	Matriz = []
	data = np.array(data_frame[[v.nombre for v in varl]])
	try:
		for i in index:
			temp =[]
			E1 = data[i]
			for j in index:
				E2 = data[j]
				temp.append(np.round(np.sqrt(np.sum((E1-E2)**2)), decimals=3))
			Matriz.append(temp)
		return np.array(Matriz)
	except:
		print('Valores no permitidos, ingresar valores numericos.')

def getKMeans(varl, data_frame, n):
	try:
		data = np.array(data_frame[[v.nombre for v in varl]])
		cluster = KMeans(n_clusters=n, random_state=0).fit(data)
		cluster.predict(data)
		data_frame['CLUSTER'] = cluster.labels_
		return cluster
	except:
		print('Valores no permitidos, ingresar valores numericos.')

def getLogisticRegresion(varPredic, varl, data_frame):
	try:
		Resultados = []
		Clasificacion = linear_model.LogisticRegression()
		X = np.array(data_frame[[v.nombre for v in varl]])
		Y = np.array(data_frame[[varPredic]])
		validation_size = 0.2
		seed = 1234
		X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed, shuffle = True)
		Clasificacion.fit(X_train, Y_train)
		PrediccionesNuevas = Clasificacion.predict(X_validation)
		confusion_matrix = pd.crosstab(Y_validation.ravel(), PrediccionesNuevas, rownames=['Real'], colnames=['Predicción'])
		Resultados.append("Intercept: {}\nCoeficientes: \n{}\n\n".format(Clasificacion.intercept_[0], Clasificacion.coef_[0]))
		Resultados.append("Exactitud: {}\n\nSummary:\n{}\n\n".format(Clasificacion.score(X_validation, Y_validation), classification_report(Y_validation, PrediccionesNuevas)))
		Resultados.append(str(confusion_matrix))
		return Resultados
	except:
		print('Valores no permitidos, ingresar valores numericos.')