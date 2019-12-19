class Simplex:
	def __init__ (self, c, A, b, signsOfInequality):
		self.c = c # Вектор правой части системы ограничений
		self.A = A # Матрица системы ограничений
		self.b = b # Вектор коэффициентов целевой функции F

		self.x = ["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9"] # Список, элементы которого будут использованы для вывода постановки ПЗ ЛП
		self.other = ["-", "F", "b"]
		self.basicVariables = ["x4", "x5", "x6", "x7", "x8", "x9"] 
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
			self.basicVariable.append(self.basicVariables[i])
			for j in range(self.numberOfFreeVariables):
				self.basicVariable.append(A[i][j])
			for element in range(self.numberOfBasicVariables):
				if(element == i):
					self.basicVariable.append(1.0)
				else:
					self.basicVariable.append(0.0)
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
		print(") -> max")

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
			if(self.SimplexTableau[self.numberOfBasicVariables + 1][index] < 0):
				return 0
		return 1



	# findResolvingColumn - функция нахождения разрешающего столбца. flag - переменная, указывающая, для чего мы ищем разрешающий элемент - для нахождения опорного (в 
	# случае, когда функция была вызвана с аругментом, равным нулю) или оптимального решения ( --//--, равным единице). В зависимости от этого алгоритмы нахождения
	# разрешающего столбца будут разными

	def findResolvingColumn (self, flag):

		if(flag == 0):

			# Проходимся по столбцу свободных членов симплекс-таблицы и добавляем все отрицательные элементы в список listOfIndices

			listOfIndices = [] 
			for index in range(1, len(self.SimplexTableau) - 1):
				if (self.SimplexTableau[index][self.numberOfVariables + 1] < 0):
					listOfIndices.append(index);

			# Далее зададим начальное значение минимального элемента равным нулю, а индекс - единице

			minimalElement = 0
			indexOfString = 1

			# Проходим по списку listOfIndices и находим минимальный элемент
			
			for index in listOfIndices: 
				if (self.SimplexTableau[index][self.numberOfVariables + 1] < minimalElement):
					minimalElement = self.SimplexTableau[index][self.numberOfVariables + 1]
					indexOfString = index

			indexOfResolvingColumn = 0

			# Проходим по строке с индексом indexOfString и ищем первый отрицательный элемент. Столбец, в котором находится этот элемент и будет разрешающим

			for index in range(1, len(self.SimplexTableau[indexOfString]) - 1):
				if(self.SimplexTableau[indexOfString][index] < 0):
					indexOfResolvingColumn = index
					break
			#Возвращаем индекс разрешающего столбца

			return indexOfResolvingColumn 

		if(flag == 1):

		# Проходимся по последней строке симплекс-таблицы и добавляем все отрицательные элементы в список listOfIndices

			listOfIndices = [] 
			for index in range(1, len(self.SimplexTableau[self.numberOfBasicVariables]) - 1):
				if (self.SimplexTableau[self.numberOfBasicVariables + 1][index] < 0): 
					listOfIndices.append(index);

			# Далее зададим начальное значение минимального элемента равным нулю, а индекс - единице

			minimalElement = 0
			indexOfResolvingColumn = 1

			# Проходим по списку listOfIndices и находим максимальный элемент
			
			for index in listOfIndices: 
				if (self.SimplexTableau[self.numberOfBasicVariables + 1][index] < minimalElement):
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
		resolvingColumn = self.findResolvingColumn(flag)
		resolvingString = self.findResolvingString(resolvingColumn)

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

		# self.printSimplexTableau()
		# print("\n")



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
			resolvingElement = self.findResolvingElement(0)
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
			print("    ", self.SimplexTableau[index][0], " = ", round(self.SimplexTableau[index][self.numberOfVariables + 1], 2), "\n")

		return 1





class IntegerLinearProgramming:
	def __init__(self, c, A, b, signsOfInequality):
		self.c = c 
		self.A = A 
		self.b = b 
		self.signsOfInequality = signsOfInequality
		self.task = Simplex(c, A, b, signsOfInequality)



	def getFractions(self):
		fractions = []

		for i in range(3):
			for j in range(1, self.task.numberOfBasicVariables + 1):
					if(self.task.SimplexTableau[j][0] == self.task.x[i]):
						# print(self.task.x[i])
						fractions.append(round(self.task.SimplexTableau[j][self.task.numberOfVariables + 1] % 1, 2))

		return fractions



	def getMinimalFraction(self, fractions):
		minimalFraction = 0.99

		for index in range(len(fractions)):
			if(fractions[index] < minimalFraction) & (fractions[index] != 0):
				minimalFraction = fractions[index]

		return minimalFraction



	def getIndexOfVariableForAddingNewLimitation(self, minimalFraction):
		indexOfVariableForAddingNewLimitation = 0
		for index in range(1, self.task.numberOfBasicVariables + 1):
			# print(round(self.task.SimplexTableau[index][self.task.numberOfVariables + 1] % 1, 2))
			if((round(self.task.SimplexTableau[index][self.task.numberOfVariables + 1] % 1, 2) == minimalFraction)):
				indexOfVariableForAddingNewLimitation = index
				break

		return indexOfVariableForAddingNewLimitation



	def printFractions(self, stringOfFractions):
		print("     Остатки элементов этой строки:\n")
		for i in range(len(stringOfFractions) - 1):
			print("     {", self.task.x[i], "} =", round(stringOfFractions[i], 2),"\n")
		print("     {", self.task.other[2], "} =", round(stringOfFractions[len(stringOfFractions) - 1], 2), "\n")



	def findVariableForAddingNewLimitation(self):
		fractions = self.getFractions()
		minimalFraction = self.getMinimalFraction(fractions)
		indexOfVariableForAddingNewLimitation = self.getIndexOfVariableForAddingNewLimitation(minimalFraction)

		if not(indexOfVariableForAddingNewLimitation == 0):
			print("\n\n     Минимальный остаток в столбце свободных членов равен", minimalFraction, "и находится в строке",
				self.task.SimplexTableau[indexOfVariableForAddingNewLimitation][0],".\n")

		return indexOfVariableForAddingNewLimitation



	def getStringOfFractions(self, indexOfVariableForAddingNewLimitation):
		stringOfFractions = []
		for index in range(1, self.task.numberOfVariables + 2):
			stringOfFractions.append(self.task.SimplexTableau[indexOfVariableForAddingNewLimitation][index] % 1)

		return stringOfFractions



	def newLimitationCalculation(self, stringOfFractions):
		valuesOfNewLimitation = []
		for i in range(self.task.numberOfFreeVariables):
			valuesOfNewLimitation.append(- stringOfFractions[i])
		valuesOfNewLimitation.append(- stringOfFractions[len(stringOfFractions) - 1])

		for i in range(self.task.numberOfVariables - self.task.numberOfFreeVariables):
			# print("_______________________________________________________________")
			for j in range(3):
				valuesOfNewLimitation[j] += stringOfFractions[i + self.task.numberOfFreeVariables] * self.task.A[i][j]
				# print(valuesOfNewLimitation)
			valuesOfNewLimitation[len(valuesOfNewLimitation) - 1] += stringOfFractions[i + self.task.numberOfFreeVariables] * self.task.b[i]

		return valuesOfNewLimitation



	def makingNewSimplex(self):
		self.task = Simplex(self.c, self.A, self.b, self.signsOfInequality)



	def addingNewLimitation(self, valuesOfNewLimitation):
		listOfLastString = []
		for i in range(self.task.numberOfFreeVariables):
			listOfLastString.append(round(valuesOfNewLimitation[i], 2))
		self.A.append(listOfLastString)

		self.b.append(valuesOfNewLimitation[len(valuesOfNewLimitation) - 1])

		self.signsOfInequality.append("<=")
 


	def printCalculations(self, stringOfFractions):
		print("     Проводим вычисления:\n\n     ", end="")
		for index in range(len(stringOfFractions) - 2):
			if(stringOfFractions[index] == 0):
				continue
			print(round(stringOfFractions[index], 2), "*", self.task.x[index], "+", end=" ")
		print(round(stringOfFractions[len(stringOfFractions) - 2], 2), "*", self.task.x[len(stringOfFractions) - 2], "<=", round(stringOfFractions[len(stringOfFractions) - 1], 2), "\n     ")

		# for index in range(self.task.numberOfFreeVariables):
		# 	if(stringOfFractions[index] == 0):
		# 		continue
		# 	print(round(stringOfFractions[index], 2), "*", self.task.x[index], "+", end=" ")

		# for i in range(self.task.numberOfFreeVariables, self.task.numberOfVariables):
		# 	if(stringOfFractions[i] == 0):
		# 		continue
		# 	print(round(stringOfFractions[i]), "* (", end= "")
		# 	print(self.b[i - self.task.numberOfFreeVariables], end="")
		# 	for j in range(self.task.numberOfFreeVariables):
		# 		print(" - ", A[i - self.task.numberOfFreeVariables][j], "*", self.task.x[j], end="")
		# 	print(") +")

	

	def printNewLimitation(self, valuesOfNewLimitation):
		print("     Добавляем новое ограничение:\n\n     ", end="")
		for j in range (len(valuesOfNewLimitation) - 2):
				print(valuesOfNewLimitation[j], "*", self.task.x[j], "+", end=" ")
		print(valuesOfNewLimitation[len(valuesOfNewLimitation) - 2], "*", self.task.x[len(valuesOfNewLimitation) - 2], "<=", self.b[len(self.b) - 1])



	def iterationOfCuttingPlaneMethod(self):

		# Находим строку, по которой будем добавлять новое ограничение, выводим остатки элементов этой строки

		indexOfVariableForAddingNewLimitation = self.findVariableForAddingNewLimitation()
		if(indexOfVariableForAddingNewLimitation == 0):
			print("     Целочисленное решение найдено!")
			return 1
		stringOfFractions = self.getStringOfFractions(indexOfVariableForAddingNewLimitation)
		self.printFractions(stringOfFractions)

		# Вычисляем коэффциенты для нового ограничения, добавляем их в начальные условия, выводим новое ограничение

		valuesOfNewLimitation = self.newLimitationCalculation(stringOfFractions)
		self.addingNewLimitation(valuesOfNewLimitation)
		self.printCalculations(stringOfFractions)
		self.printNewLimitation(valuesOfNewLimitation)

		# Создаем новую симплекс-таблицу

		self.makingNewSimplex()

		self.task.printLinearProblem()
		self.task.simplexAlgorithm()



	def cuttingPlaneMethod(self):

		# Выводим исходную задачу и решаем ее с помощью симплекс-метода

		self.task.printLinearProblem()
		self.task.simplexAlgorithm()

		# Проводим итерации метода секущих плоскостей
		
		while True:
			if(self.iterationOfCuttingPlaneMethod() == 1):
				break



signsOfInequality = ["<=", "<=", "<="]

c = [3.0, 1.0, 4.0]

A = [[2.0, 1.0, 1.0]
	,[1.0, 4.0, 0.0]
	,[0.0, 0.5, 1.0]]

b = [6.0, 4.0, 1.0]


myTask = IntegerLinearProgramming(c, A, b, signsOfInequality)
myTask.cuttingPlaneMethod()
`

