from dual import Dual

class Simplex:
	def __init__ (self, c, A, b, signsOfInequality):
		self.c = c # Вектор правой части системы ограничений
		self.A = A # Матрица системы ограничений
		self.b = b # Вектор коэффициентов целевой функции F

		self.x = ["u1", "u2", "u3", "u4", "u5", "u6", "u7", "u8", "u9"] # Список, элементы которого будут использованы для вывода постановки ПЗ ЛП
		self.other = ["-", "W", "b"]
		self.basicVariables = ["u4", "u5", "u6", "u7", "u8", "u9"] 
		self.signsOfInequality = signsOfInequality # Список знаков неравенст

		self.numberOfFreeVariables = len(self.c) # Количество свободных переменных
		self.numberOfBasicVariables = len(self.A) # Количеество базисных переменных
		self.numberOfVariables = self.numberOfFreeVariables + self.numberOfBasicVariables # Количество всех переменных

		# Следующий блок кода инициализирует все строки симплекс-таблицы, которые позже будут добавлены в двумерный список, представляющий, собственно, 
		# всю симплекс-таблицу
		#
		# string - cписок, хранящий элементы самой верхней строки симплекс-таблицы. В вычислениях не участвует, используется для визуализации
		# firstBasicVariable - список, хранящий элементы строки первой базисной переменной. Нулевой элемент этого списка используется для визуализации
		# secondBasicVariable - -//- второй базисной переменной -//-
		# thirdBasicVariable - -//- третьей базисной переменной -//-
		# F - список, хранящий элементы последней строки симплек-таблицы

		self.SimplexTableau = []

		self.string = []
		self.string.append(self.other[0])
		for index in range (self.numberOfVariables):
			self.string.append(self.x[index])
		self.string.append(self.other[2])
		self.SimplexTableau.append(self.string)

		for i in range(self.numberOfBasicVariables):
			self.basicVariable = []
			self.basicVariable.append(self.basicVariables[i + 1])
			for j in range(self.numberOfFreeVariables):
				self.basicVariable.append(A[i][j])
			for element in range(self.numberOfBasicVariables):
				if(element == i):
					self.basicVariable.append(1)
				else:
					self.basicVariable.append(0)
			self.basicVariable.append(self.b[i])
			self.SimplexTableau.append(self.basicVariable)


		self.F = []
		self.F.append(self.other[1])
		for index in self.c:
			self.F.append(-index)
		for index in range(self.numberOfBasicVariables + 1):
		 	self.F.append(0)
		self.SimplexTableau.append(self.F)


	# printSimplexTableau - функция, выводящая симплекс таблицу 
	#
	# Поскольку строки и числа выводятся по разным правилам, в обоих циклах мы проверяем, чему равен итератор  цикла. Если в родительском цикле итератор 
	# цикла равен нулю, это значит, что выводится первая строка симплекс-таблицы. Тип данных всех ее элементов - string, поэтому мы выводим их, как string, 
	# а затем переходим к следующей итерации родительского цикла 
	#
	# Далее, если во вложенном цикле итератор равен нулю, это значит, что выводится первый элементы строки. Поскольку для всех строк первый элемент 
	# используется для визуализации и имеет тип данных string, мы выводим его, как string. Затем программа переходит к следующей итерации вложенного цикла, 
	# выводит все следующие элементы данной строки как числа, при этом округляя, а затем переходит к следующей итерации родительского цикла. И так далее,
	# пока не будет выведена вся симплекс-таблица


	def printSimplexTableau (self): 
		for index in range(len(self.SimplexTableau)):
			if(index == 0): 
				for string in range(len(self.SimplexTableau[index])):
					print(("%7s" % (self.SimplexTableau[index][string])), end ="")
				print("\n")
				continue

			for element in range(len(self.SimplexTableau[index])):
				if(element == 0):
					print(("%7s" % (self.SimplexTableau[index][element])), end ="")
					continue
				print(( "%7s" % round(self.SimplexTableau[index][element], 2)), end ="")
			print("\n")



	# printLinearProblem - функция, выводящая решаемую задачу

	def printLinearProblem (self):

		# Вывод постановки задачи

		print("\n     F = ", end="")
		for j in range (self.numberOfFreeVariables):
			if(j == self.numberOfFreeVariables - 1):
				print(self.c[j], "*", self.x[j], end="")
				break
			print(self.c[j], "*", self.x[j], end=" + ")
		print(" -> max")

		# Вывод системы ограничений

		for i in range (self.numberOfBasicVariables):
			print("     ", end="")
			for j in range (self.numberOfFreeVariables - 1):
				print(self.A[i][j], "*", self.x[j], "+", end=" ")
			print(self.A[i][self.numberOfFreeVariables - 1], "*", self.x[self.numberOfFreeVariables - 1], self.signsOfInequality[i],self.b[i])
		
		# Вывод системы ограничений с веденными фиктивными переменными

		print("     ", end="")
		for i in range(self.numberOfFreeVariables - 1):
			print(self.x[i], end=", ")
		print (self.x[self.numberOfFreeVariables - 1],">= 0 \n")

		print("     Введем фиктивные переменные ", end="")
		for index in range(self.numberOfBasicVariables - 1):
			print(self.basicVariables[index], ",", end=" ")
		print(self. basicVariables[self.numberOfBasicVariables - 1], ":\n")


		print("     F = - ( - ", end="")
		for j in range (self.numberOfFreeVariables):
			if(j == self.numberOfFreeVariables - 1):
				print(self.c[j], "*", self.x[j], end="")
				break
			print(self.c[j], "*", self.x[j], end=" - ")
		print(") -> min")

		for i in range (self.numberOfBasicVariables):
			print("     ", end="")
			for j in range (self.numberOfFreeVariables - 1):
				print(self.A[i][j], "*", self.x[j], "+", end=" ")
			if(self.signsOfInequality[i] == ">="):
				print(self.A[i][self.numberOfFreeVariables - 1], "*", self.x[self.numberOfFreeVariables - 1], "- 1.0 *", self.basicVariables[i], "=", self.b[i])
			else:
				print(self.A[i][self.numberOfFreeVariables - 1], "*", self.x[self.numberOfFreeVariables - 1], "+ 1.0 *", self.basicVariables[i], "=", self.b[i])


		print("     ", end="")
		for i in range(self.numberOfVariables - 1):
			print(self.x[i], end=", ")
		print (self.x[self.numberOfVariables - 1], ">= 0 \n")


		for i in range(1, self.numberOfBasicVariables + 1):
			if(self.signsOfInequality[i - 1] == ">="):
				for j in range(1, self.numberOfVariables + 2):
					if not (j == self.numberOfFreeVariables + i):
						self.SimplexTableau[i][j] *= -1



	# isBasic - функция, проверяющая, является ли решение, найденное на этом этапе, опорным. Если нет - функция возвращает нуль, иначе - единицу

	def isBasic(self):
		for index in range(1, len(self.SimplexTableau) - 1):
			if(self.SimplexTableau[index][self.numberOfVariables + 1] < 0):
				return 0
		return 1



	# isOptimal - функция, проверяющая, является ли решение, найденное на этом этапе, оптимальным. Если нет - функция возвращает нуль, иначе - единицу, после чего программа
	# закончит свое выполнения

	def isOptimal(self):
		for index in range(1, len(self.SimplexTableau[4]) - 1):
			if(self.SimplexTableau[self.numberOfBasicVariables + 1][index] > 0):
				return 0
		return 1



	# findResolvingColumn - функция нахождения разрешающего столбца. flag - переменная, указывающая, для чего мы ищем разрешающий элемент - для нахождения опорного (в 
	# случае, когда функция была вызвана с аругментом, равным нулю) или оптимального решения ( --//--, равным единице). В зависимости от этого алгоритмы нахождения
	# разрешающего столбца будут разными

	def findResolvingColumn (self, flag):

		# if(flag == 0):

		# 	# Проходимся по столбцу свободных членов симплекс-таблицы и добавляем все отрицательные элементы в список listOfIndices

		# 	listOfIndices = [] 
		# 	for index in range(1, len(self.SimplexTableau) - 1):
		# 		if (self.SimplexTableau[index][self.numberOfVariables + 1] < 0):
		# 			listOfIndices.append(index);

		# 	# Далее зададим начальное значение минимального элемента равным нулю, а индекс - единице

		# 	minimalElement = 0
		# 	indexOfString = 1

		# 	# Проходим по списку listOfIndices и находим минимальный элемент
			
		# 	for index in listOfIndices: 
		# 		if (self.SimplexTableau[index][self.numberOfVariables + 1] < minimalElement):
		# 			minimalElement = self.SimplexTableau[index][self.numberOfVariables + 1]
		# 			indexOfString = index

		# 	indexOfResolvingString = 0

		# 	print("------------------------",indexOfString)

		# 	# Проходим по строке с индексом indexOfString и ищем первый отрицательный элемент. Столбец, в котором находится этот элемент и будет разрешающим

		# 	for index in range(1, len(self.SimplexTableau[indexOfString]) - 1):
		# 		if(self.SimplexTableau[indexOfString][index] < 0):
		# 			indexOfResolvingString = index
		# 			break
		# 	#Возвращаем индекс разрешающего столбца


		# 	min = 0
		# 	indexOfResolvingColumn = 0
		# 	for index in range(1, len(self.SimplexTableau[indexOfResolvingString])):
		# 		if(self.SimplexTableau[indexOfResolvingString][index] < min):
		# 			indexOfResolvingColumn = index

		# 	return [indexOfResolvingString, indexOfResolvingColumn]

		if(flag == 1):

		# Проходимся по последней строке симплекс-таблицы и добавляем все отрицательные элементы в список listOfIndices

			listOfIndices = [] 
			for index in range(1, len(self.SimplexTableau[self.numberOfBasicVariables]) - 1):
				if (self.SimplexTableau[self.numberOfBasicVariables + 1][index] > 0): 
					listOfIndices.append(index);

			# Далее зададим начальное значение минимального элемента равным нулю, а индекс - единице

			maximalElement = 0
			indexOfResolvingColumn = 1

			# Проходим по списку listOfIndices и находим максимальный элемент
			
			for index in listOfIndices: 
				if (self.SimplexTableau[self.numberOfBasicVariables + 1][index] > maximalElement):
					minimalElement = self.SimplexTableau[self.numberOfBasicVariables + 1][index]
					indexOfResolvingColumn = index

			# Возвращаем индекс разрешающего столбца

			return indexOfResolvingColumn 
		


	# findResolvingString - функция нахождения разрешающей строки, использующая найденный ранее разрешающий столбец

	def findResolvingString (self, indexOfResolvingColumn):

		# listOfIndices - список, в который мы положим индексы тех строк, значения элементов разрешающего столбца которых не равны нулю. Это нужно для того, 
		# чтобы избежать деления на ноль 
		#
		# listOfValues - список,в который мы положим значения b/a для каждой строки, где a - элемент разрешающего столбца, а b - элемент столбца свободных 
		# членов

		listOfIndices = []
		listOfValues = []

		# Заполняем списки listOfIndices и listOfValues 

		for index in range(1, len(self.SimplexTableau) - 1):
			if (self.SimplexTableau[index][indexOfResolvingColumn] != 0): 
				listOfIndices.append(index)

		for index in listOfIndices:
			value = self.SimplexTableau[index][self.numberOfVariables + 1] / self.SimplexTableau[index][indexOfResolvingColumn]
			if(value >= 0):
				listOfValues.append(value)

		# В данном блоке найдем начальное минимальное значение частного b/a. Для этого пробежимся по всем строкам, и как только частное в какой-то строке 
		# будет положительным - запишем его в минимальное значение, а затем выйдем из цикла

		for index in listOfIndices:
			currentValue = self.SimplexTableau[index][self.numberOfVariables + 1] / self.SimplexTableau[index][indexOfResolvingColumn]
			if (currentValue >= 0):
				minimalValue = currentValue
				break

		# Находим минимальное положительное из всех частных, а также записываем его индекс - этот индекс и будет индексом разрешающей строки

		for index in listOfIndices: 
			currentValue = self.SimplexTableau[index][self.numberOfVariables + 1] / self.SimplexTableau[index][indexOfResolvingColumn]
			if ( (currentValue <= minimalValue) & (currentValue >= 0)):
				minimalValue = currentValue 
				indexOfResolvingString = index

		# Возвращаем индекс разрешающей строки

		return indexOfResolvingString



	# findResolvingElement - функция нахождения разрешающего элемента. flag - переменная, указывающая, для чего мы ищем разрешающий элемент - для нахождения опорного или 
	# оптимального решения. Поскольку от этого зависит только нахождение разрешающего столбца, с аргументом flag вызывается только функция findResolvingColumn

	def findResolvingElement(self, flag):
		if(flag == 0):
			return self.findResolvingColumn(flag)

		resolvingColumn = self.findResolvingColumn(flag)
		print("     Разрешающий столбец:", resolvingColumn, "\n")
		resolvingString = self.findResolvingString(resolvingColumn)
		print("     Разрешающая строка:", resolvingString, "\n\n")

		return [resolvingString, resolvingColumn]



	# tableConversion - функция преобразования симплекс-таблицы

	def tableConversion(self, resolvingElement):
		indexOfResolvingString = resolvingElement[0]
		indexOfResolvingColumn = resolvingElement[1]
		
		# Преобразуем разрешающую строку, выводим результат

		denominator = self.SimplexTableau[indexOfResolvingString][indexOfResolvingColumn]
		for index in range(1, len(self.SimplexTableau[indexOfResolvingString])):
			self.SimplexTableau[indexOfResolvingString][index] /= denominator

		# Преобразуем оставшуюся часть таблицы, заменяем базис, выводим результат

		for index in range(1, len(self.SimplexTableau)):
			if(index == indexOfResolvingString):
				continue

			multiplier = self.SimplexTableau[index][indexOfResolvingColumn] / self.SimplexTableau[indexOfResolvingString][indexOfResolvingColumn]
			for element in range(1, len(self.SimplexTableau[index])):
				self.SimplexTableau[index][element] -= self.SimplexTableau[indexOfResolvingString][element] * multiplier 

		self.SimplexTableau[indexOfResolvingString][0] = self.SimplexTableau[0][indexOfResolvingColumn]

		self.printSimplexTableau()


	def gavno(self):
		listOfIndices = [] 
		for index in range(1, len(self.SimplexTableau) - 1):
			if (self.SimplexTableau[index][self.numberOfVariables + 1] < 0):
				listOfIndices.append(index);

		# print(listOfIndices)

		# Далее зададим начальное значение минимального элемента равным нулю, а индекс - единице

		minimalElement = 0
		indexOfString = 1

		# Проходим по списку listOfIndices и находим минимальный элемент
			
		for index in listOfIndices: 
			if (self.SimplexTableau[index][self.numberOfVariables + 1] < minimalElement):
				minimalElement = self.SimplexTableau[index][self.numberOfVariables + 1]
				indexOfString = index

		print("     Разрешающая строка:", indexOfString,"\n")

		min = 0
		ind = 0

		for i in range(1, len(self.SimplexTableau[indexOfString]) - 1):
			if(self.SimplexTableau[indexOfString][i] < min):
				min = self.SimplexTableau[indexOfString][i]
				ind = i

		
		print("     Разрешающий столбец:", ind,"\n")

		return [indexOfString, ind]


	# simplexAlgorithm - функция, описывающая весь алгоритм симплекс-метода

	def simplexAlgorithm(self):

		# Выводим исходную симплекс-таблицу

		print("\n     Решим задачу с помощью симплекс-метода. Запишем исходную симплекс-таблицу:\n")
		self.printSimplexTableau()

		# Преобразуем таблицу, пока isBasic не вернет единицу, т.е. не будет найдено опорное решение

		while not self.isBasic():
			if(self.findResolvingColumn(0) == 0):
				print("\n     На одном из этапов решения симплекс-таблица имеет следующий вид, что говорит об отсутствии решения задачи:\n")
				self.printSimplexTableau()
				return 0
			resolvingElement = self.gavno()
			self.tableConversion(resolvingElement)

		# Преобразуем таблицу, пока isOptimal не вернет единицу, т.е. не будет найдено опорное решение

		while not self.isOptimal():
			resolvingElement = self.findResolvingElement(1)
			self.tableConversion(resolvingElement)

		# Если решения нет - функция выведет 0

		for index in range(1, len(self.SimplexTableau) - 1):
		 	if(self.SimplexTableau[index][self.numberOfVariables + 1] < 0):
		 		print("     В столбце свободных членов присутствуют отрицательные значения. Следовательно, решения не существует.\n")
		 		return 0

		# Выводим результат работы алгоритма

		print("\n     Конечная симплекс-таблица имеет вид:\n")
		self.printSimplexTableau()

		print("\n     Оптимальное решение:\n")
		for index in range(1, self.numberOfBasicVariables + 2):
			print("    ", self.SimplexTableau[index][0], " = ", round(self.SimplexTableau[index][self.numberOfVariables + 1], 3), "\n")

		return 1




class matrixGames:
	def __init__(self, C):
		self.C = C

		self.strategyMatrix = []

		self.a = ["a1", "a2", "a3", "a4", "a5"]
		self.b = ["b1", "b2", "b3", "b4"]
		self.x = ["x1", "x2", "x3", "x4", "x5"]
		self.u = ["u1", "u2", "u3", "u4", "u5"]
		self.other = ["-", "g", "h"]

		string = []
		string.append(self.other[0])
		for i in range(len(C[0])):
			string.append(self.a[i])
		self.strategyMatrix.append(string)


		for i in range(len(self.C)):
			string = []
			string.append(self.b[i])

			for j in range(len(C[i])):
				string.append(C[i][j])

			self.strategyMatrix.append(string)


	def printStrategyMatrix(self):
		for index in range(len(self.strategyMatrix)):
			if(index == 0): 
				for string in range(len(self.strategyMatrix[index])):
					print(("%7s" % (self.strategyMatrix[index][string])), end ="")
				print("\n")
				continue

			for element in range(len(self.strategyMatrix[index])):
				if(element == 0):
					print(("%7s" % (self.strategyMatrix[index][element])), end ="")
					continue
				print(("%7s" % (self.strategyMatrix[index][element])), end ="")
			print("\n")


	def printSystemOfEquations(self):
		for i in range (len(self.C)):
			print("     ", end="")
			for j in range (len(self.C[i]) - 1):
				print(self.C[i][j], "*", self.x[j], "+", end=" ")
			print(self.C[i][len(self.C)], "*", self.x[len(self.C)], ">=", self.other[1])

		print("     ", end="")
		for index in range(len(self.C[0]) - 2):
			print(self.x[index], "+", end=" ")
		print(self.x[len(self.C[0]) - 2], "= 1\n")


		print("     Разделим систему на функцию g:\n")

		for i in range (len(self.C)):
			print("     ", end="")
			for j in range (len(self.C[i]) - 1):
				print(self.C[i][j], "*", self.u[j], "+", end=" ")
			print(self.C[i][len(self.C)], "*", self.u[len(self.C)], ">= 1")

		print("     ", end="")
		for index in range(len(self.C[0]) - 2):
			print(self.u[index], "+", end=" ")
		print(self.u[len(self.C[0]) - 2], "= 1\n")


	def makingSimplex(self):

			A = []

			for i in range(len(self.C[0])):
		 		string = []
		 		for j in range(len(self.C)):
		 			string.append(C[j][i])
		 		A.append(string)

			b = []
			for i in range(len(self.C[0])):
				b.append(1.0)

			c = []
			for i in range(len(self.C)):
				c.append(1.0)

			self.task = Simplex(c, A, b, [">=",">=",">=",">=",">="])


			# A = self.C

			# b = []
			# for i in range(len(self.C[0])):
			# 	b.append(1.0)

			# c = []
			# for i in range(len(self.C)):
			# 	c.append(1.0)

			# self.task = Dual(c, A, b)





	def algorithm(self):

		print("     Дана матрица стратегий:\n")
		self.printStrategyMatrix()
		print("     Составим систему уравнений:\n")
		self.printSystemOfEquations()
		self.makingSimplex()

		print("     Сформулируем задачу для решения симплекс-методом:")

		self.task.printLinearProblem()

		# print("     Исходная симплекс-таблица имеет вид:\n")
		# self.task.printSimplexTableau()

		self.task.simplexAlgorithm()





C = [[19, 6, 8, 2, 7]
	,[7, 9, 2, 0, 12]
	,[3, 18, 11, 9, 10]
	,[19, 10, 6, 19, 4]]



myTask = matrixGames(C)
myTask.algorithm()
