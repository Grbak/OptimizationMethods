class Dual:
	def __init__ (self, c, A, b):
		self.c = c # Вектор правой части системы ограничений
		self.A = A # Матрица системы ограничений
		self.b = b # Вектор коэффициентов целевой функции F

		self.other = ["-", "Z", "b"]
		self.basicVariables = ["v6", "v7", "v8", "v9"] 
		self.u = ["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9"]

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
			self.string.append(self.u[index])
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
			self.F.append(index)
		for index in range(self.numberOfBasicVariables + 1):
		 	self.F.append(0.0)
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

		print("\n     W = ", end="")
		for j in range (self.numberOfFreeVariables):
			if(j == self.numberOfFreeVariables - 1):
				print(self.c[j], "*", self.u[j], end="")
				break
			print(self.c[j], "*", self.u[j], end=" + ")
		print(" -> min")

		# Вывод системы ограничений

		for i in range (self.numberOfBasicVariables):
			print("     ", end="")
			for j in range (self.numberOfFreeVariables - 1):
				print(self.A[i][j], "*", self.u[j], "+", end=" ")
			print(self.A[i][self.numberOfFreeVariables - 1], "*", self.u[self.numberOfFreeVariables - 1]," self.signsOfInequality[i]",self.b[i])
		
		# Вывод системы ограничений с веденными фиктивными переменными

		print("     ", end="")
		for i in range(self.numberOfFreeVariables - 1):
			print(self.u[i], end=", ")
		print (self.u[self.numberOfFreeVariables - 1],">= 0 \n")

		print("     Введем фиктивные переменные ", end="")
		for index in range(self.numberOfBasicVariables - 1):
			print(self.basicVariables[index], ",", end=" ")
		print(self. basicVariables[self.numberOfBasicVariables - 1], ":\n")


		print("     W = - ( - ", end="")
		for j in range (self.numberOfFreeVariables):
			if(j == self.numberOfFreeVariables - 1):
				print(self.c[j], "*", self.u[j], end="")
				break
			print(self.c[j], "*", self.u[j], end=" - ")
		print(") -> min")

		for i in range (self.numberOfBasicVariables):
			print("     ", end="")
			for j in range (self.numberOfFreeVariables - 1):
				print(self.A[i][j], "*", self.u[j], "+", end=" ")
			print(self.A[i][self.numberOfFreeVariables - 1], "*", self.u[self.numberOfFreeVariables - 1], "+ 1.0 *", self.basicVariables[i], "=", self.b[i])


		print("     ", end="")
		for i in range(self.numberOfVariables - 1):
			print(self.u[i], end=", ")
		print (self.u[self.numberOfVariables - 1], ">= 0 \n")






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

		if(flag == 0):

			# Проходимся по столбцу свободных членов симплекс-таблицы и добавляем все отрицательные элементы в список listOfIndices

			listOfIndices = [] 
			for index in range(1, len(self.SimplexTableau) - 1):
				if (self.SimplexTableau[index][self.numberOfVariables + 1] < 0):
					listOfIndices.append(index);

			print(listOfIndices)

			# Далее зададим начальное значение минимального элемента равным нулю, а индекс - единице

			minimalElement = 0
			indexOfString = 1

			# Проходим по списку listOfIndices и находим минимальный элемент
			
			for index in listOfIndices: 
				if (self.SimplexTableau[index][self.numberOfVariables + 1] <= minimalElement):
					minimalElement = self.SimplexTableau[index][self.numberOfVariables + 1]
					indexOfString = index

			print(indexOfString)

			indexOfResolvingColumn = 0

			# Проходим по строке с индексом indexOfString и ищем первый отрицательный элемент. Столбец, в котором находится этот элемент и будет разрешающим

			for index in range(1, len(self.SimplexTableau[indexOfString]) - 1):
				if(self.SimplexTableau[indexOfString][len(self.SimplexTableau[indexOfString]) - 1 - index] < 0):
					indexOfResolvingColumn = len(self.SimplexTableau[indexOfString]) - 1 -index
					break
			#Возвращаем индекс разрешающего столбца

			return indexOfResolvingColumn 

		if(flag == 1):

		# Проходимся по последней строке симплекс-таблицы и добавляем все положительные элементы в список listOfIndices

			listOfIndices = [] 
			for index in range(1, len(self.SimplexTableau[self.numberOfBasicVariables]) - 1):
				if (self.SimplexTableau[self.numberOfBasicVariables + 1][index] > 0): 
					listOfIndices.append(index);

			# Далее зададим начальное значение максимального элемента равным нулю, а индекс - единице

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
			print(currentValue)
			if ((currentValue <= minimalValue) & (currentValue >= 0)):
				minimalValue = currentValue 
				indexOfResolvingString = index

		print(indexOfResolvingString)

		# Возвращаем индекс разрешающей строки

		return indexOfResolvingString



	# findResolvingElement - функция нахождения разрешающего элемента. flag - переменная, указывающая, для чего мы ищем разрешающий элемент - для нахождения опорного или 
	# оптимального решения. Поскольку от этого зависит только нахождение разрешающего столбца, с аргументом flag вызывается только функция findResolvingColumn

	def findResolvingElement(self, flag):
		resolvingColumn = self.findResolvingColumn(flag)
		resolvingString = self.findResolvingString(resolvingColumn)

		print("     Разрешающий элемент находится в", resolvingString, "строке и",resolvingColumn, "столбце")

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
		print("\n")



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
			print("    ", self.SimplexTableau[index][0], " = ", round(self.SimplexTableau[index][self.numberOfVariables + 1], 4), "\n")

		return 1

