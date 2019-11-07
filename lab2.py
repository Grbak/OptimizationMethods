

class Simplex:
	def __init__ (self, c, A, b):
		self.c = c # Вектор правой части системы ограничений
		self.A = A # Матрица системы ограничений
		self.b = b # Вектор коэффициентов целевой функции F

		self.x = ["-", "x1", "x2", "x3", "x4", "x5", "x6", "b", "F"] # Список, элементы которого будут использованы для вывода постановки ПЗ ЛП
		self.y = ["-", "y1", "y2", "y3", "y4", "y5", "y6", "b", "F"] # Список, элементы которого будут составлять элементы верхней строки симплекс-таблицы 
		#и первого столбца симплекс-таблицы, т.е. использоваться для визуализации 

		# Следующий блок кода инициализирует все строки симплекс-таблицы, которые позже будут добавлены в двумерный список, представляющий, собственно, 
		# всю симплекс-таблицу
		#
		# string - cписок, хранящий элементы самой верхней строки симплекс-таблицы. В вычислениях не участвует, используется для визуализации
		# firstBasicVariable - список, хранящий элементы строки первой базисной переменной. Нулевой элемент этого списка используется для визуализации
		# secondBasicVariable - -//- второй базисной переменной -//-
		# thirdBasicVariable - -//- третьей базисной переменной -//-
		# F - список, хранящий элементы последней строки симплек-таблицы

		self.string = [self.y[0], self.y[1], self.y[2], self.y[3], self.y[4], self.y[5], self.y[6], self.y[7]]
		self.firstBasicVariable = [self.y[4], -self.A[0][0], -self.A[1][0], -self.A[2][0], 1.0, 0.0, 0.0, -self.c[0]] 
		self.secondBasicVariable = [self.y[5], -self.A[0][1], -self.A[1][1], -self.A[2][1], 0.0, 1.0, 0.0, -self.c[1]] 
		self.thirdBasicVariable = [self.y[6], -self.A[0][2], -self.A[1][2], -self.A[2][2], 0.0, 0.0, 1.0, -self.c[2]] 
		self.F = [self.y[8], -self.b[0], -self.b[1], -self.b[2], 0.0, 0.0, 0.0, 0.0]	

		self.SimplexTableau = [self.string, self.firstBasicVariable, self.secondBasicVariable, self.thirdBasicVariable, self.F] #Двумерный список, хранящий
		# в себе всю симплекс-таблицу 


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

	# printLinearProblem - функция, выводящая решаему задачу

	def printLinearProblem (self):

		print("\n")
		print("     Исходная прямая задача ЛП: \n")
		print("     F =", c[0], "* x1 +", c[1], "* x2 +", c[2], "* x3 -> max")
		print("    ", A[0][0], "* x1 +", A[0][1], "* x2 +", A[0][2], "* x3 <=", b[0])
		print("    ", A[1][0], "* x1 +", A[1][1], "* x2 +", A[1][2], "* x3 <=", b[1])
		print("    ", A[2][0], "* x1 +", A[2][1], "* x2 +", A[2][2], "* x3 <=", b[2])
		print("     x1, x2, x3 >= 0 \n")

		print("     Сформулируем двойственную задачу ЛП: \n")
		print("     F =", b[0], "* y1 +", b[1], "* y2 +", b[2], "* y3 -> min")
		print("    ", A[0][0], "* y1 +", A[1][0], "* y2 +", A[2][0], "* y3 >=", c[0])
		print("    ", A[0][1], "* y1 +", A[1][1], "* y2 +", A[2][1], "* y3 >=", c[1])
		print("    ", A[0][2], "* y1 +", A[1][2], "* y2 +", A[2][2], "* y3 >=", c[2])
		print("     y1, y2, y3 >= 0 \n")

		print("     Введением фиктивных переменных y4, y5 и y6 приведем исходную задачу к каноническому виду:\n")
		print("     F = ", b[0], "* y1 +", b[1], "* y2 +", b[2], "* y3 -> min")
		print("     y4 =", -c[0], "- (-", A[0][0], "* y1 -", A[1][0], "* y2 -", A[2][0], "* y3)")
		print("     y5 =", -c[1], "- (-", A[0][1], "* y1 -", A[1][1], "* y2 -", A[2][1], "* y3)")
		print("     y6 =", -c[2], "- (-", A[0][2], "* y1 -", A[1][2], "* y2 -", A[2][2], "* y3)")
		print("     y1, y2, y3, y4, y5, y6 >= 0")



	# isBasic - функция, проверяющая, является ли решение, найденное на этом этапе, опорным. Если да - функция возвращает нуль, иначе - единицу

	def isBasic(self):
		for index in range(1, len(self.SimplexTableau) - 1):
			if(self.SimplexTableau[index][7] < 0):
				print("\n\n")
				print("     В столбце свободных членов присутствуют отрицательные элементы, что говорит о недопустимости решения.", end=" ")
				print("Преобразуем таблицу методом Жордановских преобразований: \n")
				return 0

		return 1

	# isOptimal - функция, проверяющая, является ли решение, найденное на этом этапе, оптимальны. Если да - функция возвращает нуль, иначе - единицу, после чего программа
	# закончит свое выполнения

	def isOptimal(self):
		for index in range(1, len(self.SimplexTableau[4]) - 1):
			if(self.SimplexTableau[4][index] > 0):
				print("\n\n")
				print("     В строке функции присутствуют положительные элементы, что говорит о неоптимальности решения. \n")
				return 0

		print("     В нижней строке отсутствуют отрицательные элементы, что говорит о нахождении оптимального решения.\n")

		return 1




	# findResolvingColumn - функция нахождения разрешающего столбца. flag - переменная, указывающая, для чего мы ищем разрешающий элемент - для нахождения опорного (в 
	# случае, когда функция была вызвана с аругментом, равным нулю) или оптимального решения ( --//--, равным единице). В зависимости от этого алгоритмы нахождения
	# разрешающего столбца будут разными

	def findResolvingColumn (self, flag):

		if(flag == 0):

			# Проходимся по столбцу свободных членов симплекс-таблицы и добавляем все отрицательные элементы в список listOfIndices

			listOfIndices = [] 
			for index in range(1, len(self.SimplexTableau) - 1):
				if (self.SimplexTableau[index][7] < 0):
					listOfIndices.append(index);

			# Далее зададим начальное значение минимального элемента равным нулю, а индекс - единице

			minimalElement = 0
			indexOfString = 1

			# Проходим по списку listOfIndices и находим минимальный элемент
			
			for index in listOfIndices: 
				if (self.SimplexTableau[index][7] < minimalElement):
					minimalElement = self.SimplexTableau[index][7]
					indexOfString = index

			print("     max {", end = " ")
			for index in range(len(listOfIndices)):
				if(index == (len(listOfIndices) - 1)):
					print(abs(self.SimplexTableau[listOfIndices[index]][7]), "} =", abs(round(minimalElement, 2)))
					break
				print(abs(self.SimplexTableau[listOfIndices[index]][7]),",", end = " ")

			print("     Найдем в строке", self.SimplexTableau[indexOfString][0], "первый отрицательный элемент.")

			# Проходим по строке с индексом indexOfString и ищем первый отрицательный элемент. Столбец, в котором находится этот элемент и будет разрешающим

			for index in range(1, len(self.SimplexTableau[indexOfString])):
				if(self.SimplexTableau[indexOfString][index] < 0):
					indexOfResolvingColumn = index
					break

			print("     Разрешающий столбец:", self.SimplexTableau[0][indexOfResolvingColumn], "\n")

			#Возвращаем индекс разрешающего столбца

			return indexOfResolvingColumn 

		if(flag == 1):

		# Проходимся по последней строке симплекс-таблицы и добавляем все положительные элементы в список listOfIndices

			listOfIndices = [] 
			for index in range(1, len(self.SimplexTableau[4]) - 1):
				if (self.SimplexTableau[4][index] > 0): 
					listOfIndices.append(index);

			# Далее зададим начальное значение максимального элемента равным нулю, а индекс - единице

			maximalElement = 0
			indexOfResolvingColumn = 1

			# Проходим по списку listOfIndices и находим максимальный элемент
			
			for index in listOfIndices: 
				if (self.SimplexTableau[4][index] > maximalElement):
					maximalElement = self.SimplexTableau[4][index]
					indexOfResolvingColumn = index

			# Затем выведем полученные результаты

			print("     max {", end = " ")
			for index in range(len(listOfIndices)):
				if(index == (len(listOfIndices) - 1)):
					print(abs(self.SimplexTableau[4][listOfIndices[index]]), "} =", abs(round(self.SimplexTableau[4][indexOfResolvingColumn], 2)))
					break
				print(abs(self.SimplexTableau[4][listOfIndices[index]]),",", end = " ")

			print("     Разрешающий столбец:", self.SimplexTableau[0][indexOfResolvingColumn], "\n")

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
			value = self.SimplexTableau[index][7] / self.SimplexTableau[index][indexOfResolvingColumn]
			if(value > 0):
				listOfValues.append(value)

		# В данном блоке найдем начальное минимальное значение частного b/a. Для этого пробежимся по всем строкам, и как только частное в какой-то строке 
		# будет положительным - запишем его в минимальное значение, а затем выйдем из цикла

		for index in listOfIndices:
			currentValue = self.SimplexTableau[index][7] / self.SimplexTableau[index][indexOfResolvingColumn]
			if (currentValue > 0):
				minimalValue = currentValue
				break

		# Находим минимальное положительное из всех частных, а также записываем его индекс - этот индекс и будет индексом разрешающей строки

		for index in listOfIndices: 
			currentValue = self.SimplexTableau[index][7] / self.SimplexTableau[index][indexOfResolvingColumn]
			if ( (currentValue <= minimalValue) & (currentValue > 0)):
				minimalValue = currentValue 
				indexOfResolvingString = index

		# Выводим полученные результаты

		print("     min {", end = " ")
		for index in range(len(listOfValues)):
			if(index == (len(listOfValues) - 1)):
				print(round((listOfValues[index]), 2), "} =", round(minimalValue, 2))
				break
			print(round(listOfValues[index], 2), ",", end = " ")
		print("     Разрешающая строка:", self.SimplexTableau[indexOfResolvingString][0], "\n")

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

		print("     Сперва изменим разрешающую строку, поделив каждый ее элемент на ", denominator, ": \n")
		self.printSimplexTableau()

		# Преобразуем оставшуюся часть таблицы, заменяем базис, выводим результат

		for index in range(1, len(self.SimplexTableau)):
			if(index == indexOfResolvingString):
				continue

			multiplier = self.SimplexTableau[index][indexOfResolvingColumn] / self.SimplexTableau[indexOfResolvingString][indexOfResolvingColumn]
			for element in range(1, len(self.SimplexTableau[index])):
				self.SimplexTableau[index][element] -= self.SimplexTableau[indexOfResolvingString][element] * multiplier 

		print("     А затем заменим базис, поменяв переменную ", self.SimplexTableau[indexOfResolvingString][0], "на переменную ", 
			self.SimplexTableau[0][indexOfResolvingColumn], ", и получим преобразованную таблицу: \n")

		self.SimplexTableau[indexOfResolvingString][0] = self.SimplexTableau[0][indexOfResolvingColumn]

		self.printSimplexTableau()



	# Функция simplexAlgorithm описывает весь алгоритм симплекс-метода

	def simplexAlgorithm(self):

		# Выводим поставленную задачу и исходную симплекс-таблицу

		self.printLinearProblem()

		print("\n     Запишем исходную симплекс-таблицу: \n")
		self.printSimplexTableau()

		# Преобразуем таблицу, пока isBasic не вернет единицу, т.е. не будет найдено опорное решение

		while not self.isBasic():
			resolvingElement = self.findResolvingElement(0)
			self.tableConversion(resolvingElement)

		# Преобразуем таблицу, пока isOptimal не вернет единицу, т.е. не будет найдено опорное решение

		while not self.isOptimal():
			resolvingElement = self.findResolvingElement(1)
			self.tableConversion(resolvingElement)

		# Выводим результат работы алгоритма

		print("     Оптимальное решение: \n")
		for index in range(1, len(self.SimplexTableau)):
			print("    ", self.SimplexTableau[index][0], " = ", round(self.SimplexTableau[index][7], 2), "\n")

		if(round(self.SimplexTableau[4][7], 2) == 13.67):
			print("     Таким образом, решения прямой и двойственной задач совпадают!")
		


c = [5.0, 6.0, 1.0]

A = [[2.0, 1.0, 1.0]
	,[1.0, 2.0, 0.0]
	,[0.0, 0.5, 1.0]]

b = [5.0, 3.0, 8.0]

myTask = Simplex(c, A, b)
myTask.simplexAlgorithm()


