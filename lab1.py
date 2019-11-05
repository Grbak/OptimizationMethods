
class Simplex:
	def __init__ (self, c, A, b):
		self.c = c #Вектор коэффициентов целевой функции F
		self.A = A #Матрица системы ограничений
		self.b = b #Вектор правой части системы ограничений

		self.x = ["-", "x1", "x2", "x3", "x4", "x5", "x6", "b", "F"] #Список, элементы которого будут составлять элементы верхней строки симплекс-таблицы 
		#и первого столбца симплекс-таблицы, т.е. использоваться для визуализации 

		# Следующий блок кода инициализирует все строки симплекс-таблицы, которые позже будут добавлены в двумерный список, представляющий, собственно, 
		# всю симплекс-таблицу
		#
		# string - cписок, хранящий элементы самой верхней строки симплекс-таблицы. В вычислениях не участвует, используется для визуализации
		# firstBasicVariable - список, хранящий элементы строки первой базисной переменной. Нулевой элемент этого списка используется для визуализации
		# secondBasicVariable - -//- второй базисной переменной -//-
		# thirdBasicVariable - -//- третьей базисной переменной -//-
		# F - список, хранящий элементы последней строки симплек-таблицы

		self.string = [self.x[0], self.x[1], self.x[2], self.x[3], self.x[4], self.x[5], self.x[6], self.x[7]]
		self.firstBasicVariable = [self.x[3], self.A[0][0], self.A[0][1], self.A[0][2], 1.0, 0.0, 0.0, self.b[0]] 
		self.secondBasicVariable = [self.x[4], self.A[1][0], self.A[1][1], self.A[1][2], 0.0, 1.0, 0.0, self.b[1]] 
		self.thirdBasicVariable = [self.x[5], self.A[2][0], self.A[2][1], self.A[2][2], 0.0, 0.0, 1.0, self.b[2]] 
		self.F = [self.x[8], -self.c[0], -self.c[1], -self.c[2], 0.0, 0.0, 0.0, 0.0]	

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
		print("     Решим следующую задачу ЛП: \n")
		print("     F =", c[0], "* x1 +", c[1], "* x2 +", c[2], "* x3 -> max")
		print("    ", A[0][0], "* x1 +", A[0][1], "* x2 +", A[0][2], "* x3 <=", b[0])
		print("    ", A[1][0], "* x1 +", A[1][1], "* x2 +", A[1][2], "* x3 <=", b[1])
		print("    ", A[2][0], "* x1 +", A[2][1], "* x2 +", A[2][2], "* x3 <=", b[2])
		print("     x1, x2, x3 >= 0 \n")

		print("     Введением фиктивных переменных x4, x5 и x6 приведем исходную задачу к каноническому виду:\n")
		print("     F = - (", c[0], "* x1 +", c[1], "* x2 +", c[2], "* x3) -> min")
		print("     x4 =", b[0], "- (", A[0][0], "* x1 +", A[0][1], "* x2 +", A[0][2], "* x3)")
		print("     x5 =", b[1], "- (", A[1][0], "* x1 +", A[1][1], "* x2 +", A[1][2], "* x3)")
		print("     x6 =", b[2], "- (", A[2][0], "* x1 +", A[2][1], "* x2 +", A[2][2], "* x3)")
		print("     x1, x2, x3, x4, x5, x6 >= 0")



	# checking - функция, проверяющая, на каком этапе находится процесс решения задачи: найдено ли опорное решение, и если да, то является ли оно оптимальным 
	#
	# В случаях, когда оптимальное решение не найдено, функция возвращает единицу, в следствие чего программа перейдет к выполнению следующей итерации 
	# алгоритма симплекс-метода. В противном случае, функция вернет нуль, и программа закончит свое выполнение


	def checking (self):
		for element in range(1, len(self.SimplexTableau)):
			if(self.SimplexTableau[element][7] < 0):
				print("     В столбце свободных членов присутствуют отрицательные элементы, что говорит о недопустимости решения. \n")
				return 1

		for index in range(1, len(self.SimplexTableau[4])):
			if(self.SimplexTableau[4][index] < 0):
				print("     В строке функции присутствуют отрицательные элементы, что говорит о неоптимальности решения. \n")
				return 1

		print("     В нижней строке отсутствуют отрицательные элементы, что говорит о нахождении оптимального решения.\n")

		return 0



	#findResolvingColumn - функция нахождения разрешающего столбца

	def findResolvingColumn (self):

		#Проходимся по последней строке симплекс-таблицы и добавляем все отрицательные элементы в список listOfIndices

		listOfIndices = [] 
		for index in range(1, len(self.SimplexTableau[4])):
			if (self.SimplexTableau[4][index] < 0):
				listOfIndices.append(index);

		# Далее зададим начальное значение минимального элемента равное нулю. Это сработает, т.к. если программа дошла до этой строчки, значит, в строке 
		# F присутствуют отрицаельныне элементы, по определению меньшие нуля. Рассуждая таким же образом, начальный индекс минимального элемента также
		# зададим равным нулю

		minimalElement = 0
		indexOfResolvingColumn = 0 

		#Проходим по списку listOfIndices и находим минимальный элемент из отрицательных
			
		for index in listOfIndices: 
			if (self.SimplexTableau[4][index] < minimalElement):
				minimalElement = self.SimplexTableau[4][index]
				indexOfResolvingColumn = index

		#Затем выведем полученные результаты

		print("     max {", end = " ")
		for index in range(len(listOfIndices)):
			if(index == (len(listOfIndices) - 1)):
				print(abs(self.SimplexTableau[4][listOfIndices[index]]), "} =", abs(round(self.SimplexTableau[4][indexOfResolvingColumn], 2)))
				break
			print(abs(self.SimplexTableau[4][listOfIndices[index]]),",", end = " ")

		print("     Разрешающий столбец:", self.SimplexTableau[0][indexOfResolvingColumn], "\n")

		#Возвращаем индекс разрешающего столбца

		return indexOfResolvingColumn 
		


	#findResolvingString - функция нахождения разрешающей строки, использующая найденный ранее разрешающий столбец

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
				print(round((listOfValues[index]), 2), "} =", abs(round(self.SimplexTableau[4][indexOfResolvingColumn], 2)))
				break
			print(round(listOfValues[index], 2), ",", end = " ")
		print("     Разрешающая строка:", self.SimplexTableau[indexOfResolvingString][0], "\n")

		# Возвращаем индекс разрешающей строки

		return indexOfResolvingString



	# findResolvingElement - функция нахождения разрешающего элемента

	def findResolvingElement(self):
		resolvingColumn = self.findResolvingColumn()
		resolvingString = self.findResolvingString(resolvingColumn)

		return [resolvingString, resolvingColumn]



	# tableConversion - функция преобразования симплекс-таблицы

	def tableConversion(self, resolvingElement):
		indexOfResolvingString = resolvingElement[0]
		indexOfResolvingColumn = resolvingElement[1]
		
		#Преобразуем разрешающую строку, выводим результат

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

		# Выводим поставленную задачу

		self.printLinearProblem()

		# Выводим исходную симплекс-таблицу

		print("\n     Запишем исходную симплекс-таблицу: \n")
		self.printSimplexTableau()

		# Выполняем итерации алгоритма до тех пор, пока checking не вернет 0, то есть не будет найдено оптимальное решение

		while self.checking():
			resolvingElement = self.findResolvingElement()
			self.tableConversion(resolvingElement)

		# Выводим результат работы алгоритма

		print("     Оптимальное решение: \n")
		for index in range(1, len(self.SimplexTableau)):
			print("     ", self.SimplexTableau[index][0], " = ", round(self.SimplexTableau[index][7], 2), "\n")




c = [5.0, 6.0, 1.0]

A = [[2.0, 1.0, 1.0]
	,[1.0, 2.0, 0.0]
	,[0.0, 0.5, 1.0]]

b = [5.0, 3.0, 8.0]

myTask = Simplex(c, A, b)
myTask.simplexAlgorithm()

