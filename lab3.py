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



	# bruteForce - реализация метода перебора
	# Первый цикл итерирутся трижды, второй - дважды, а третий - шесть раз. Это было сделано из тех соображений, что исходя из системы ограничений первая переменная не 
	# может быть больше двух, вторая - не больше единицы а третья не больше пяти. Можно было бы создать метод, который бы это высчитывал, но мне показалось это
	# пустой тратой времени, поэтому я просто вручную подставил значения для своего варианта

	def bruteForce(self):
		print("     Решим задачу методом перебора: \n")

		self.solutions = []
		self.valuesOfFunction = []

		for i in range(3):
			for j in range(2):
				for k in range(6):
					x = [i, j, k]

					F = self.checking(x)
					if(F):
						self.solutions.append(x)

						value = 0
						for index in range(self.numberOfFreeVariables):
							value += self.c[index] * x[index]
						self.valuesOfFunction.append(value)

						print("     ", end="")
						for index in range(self.numberOfFreeVariables - 1):
							print(x[index], "*", self.c[index], "+", end=" ")
						print(x[self.numberOfFreeVariables - 1], "*", self.c[self.numberOfFreeVariables - 1], "=", value)

		print("\n     Количество целочисленных решений:", len(self.solutions))

		maximalValue = 0
		indexOfMaximalValue = 0
		for index in range(self.numberOfFreeVariables):
			maximalValue += self.c[index] * self.solutions[0][index]

		for index in range(len(self.solutions)):
			if(self.valuesOfFunction[index] > maximalValue):
				maximalValue = self.valuesOfFunction[index]
				indexOfMaximalValue = index

		print("\n     Найденное методом перебора решение:\n")
		for index in range(self.numberOfFreeVariables):
			print("    ", self.x[index], "=", self.solutions[indexOfMaximalValue][index],"\n")
		print("    ",self.other[1], "=", maximalValue, "\n")



	# checking - функция, возвращающая один, если вектор корней x удовлетворяет всем ограничениям, и ноль - если не удовлетворяет. Используется при проверке в методе 
	# перебором

	def checking(self, x):
		for i in range(self.numberOfBasicVariables):
			value = 0
			for j in range(self.numberOfFreeVariables):
				value += self.A[i][j] * x[j]

			if(self.signsOfInequality[i] == "<="):
				if not (value <= self.b[i]):
					return 0

			if(self.signsOfInequality[i] == ">="):
				if not (value >= self.b[i]):
					return 0
		return 1



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

	






# IntegerLinearProgramming - класс задачи ЦЛП

class IntegerLinearProgramming:
	def __init__(self, c, A, b, signsOfInequality):
		self.c = c 
		self.A = A 
		self.b = b 
		self.signsOfInequality = signsOfInequality
		task = Simplex(c, A, b, signsOfInequality)
		self.indexOfBranchVariable = 0 # Индекс переменной ветвления


	# checking - функция, проверяющая, является ли найденное на данном этапе решение целочисленным. Если да - вернет ноль, в противном случае вернет индекс строки 
	# переменной, ветвление которой надо осуществить

	def checking(self, task):
		listOfFreeVariablesIndices = []
		for index in range(1, task.numberOfBasicVariables + 1):
			if((task.SimplexTableau[index][0] == task.x[index - 1])):
				listOfFreeVariablesIndices.append(index)

		self.indexOfBranchVariableString = 0

		for index in listOfFreeVariablesIndices:
			fraction = task.SimplexTableau[index][task.numberOfVariables + 1] - int(task.SimplexTableau[index][task.numberOfVariables + 1])
			if(fraction != 0):
				print("     Произведем ветвление по переменной", task.SimplexTableau[index][0], ". Для этого добавим новое ограничение: \n")
				self.indexOfBranchVariableString = index

				if(task.SimplexTableau[index][0] == "x1"):
					self.indexOfBranchVariable = 1
					break
				if(task.SimplexTableau[index][0] == "x2"):
					self.indexOfBranchVariable = 2
					break
				if(task.SimplexTableau[index][0] == "x3"):
					self.indexOfBranchVariable = 3
					break

		return self.indexOfBranchVariableString

	# addingListToA - функция, добавляющая новую строки в матрицу ограничений при добавлении нового ограничения в задачу

	def addingListToA(self, indexOfBranchVariable):
		listOfLastString = []
		for index in range(len(self.c)):
			if(index == self.indexOfBranchVariable - 1):
				listOfLastString.append(1)
			else:
				listOfLastString.append(0)
		self.A.append(listOfLastString)

	# addingElementToB - функция, добавляющая новый элемент в вектор правой части системы ограничений, а также в вектор знаков неравенств
	# Параметр i указывает, какой именно знак у нового ограничения

	def addingElementToB(self, i, task):
		if(i == 0):
			self.b.append(int(task.SimplexTableau[self.indexOfBranchVariableString][task.numberOfVariables + 1]))
			self.signsOfInequality.append("<=")
			print("     ", task.SimplexTableau[self.indexOfBranchVariableString][0], "<=", self.b[len(self.b) - 1], "\n")
		else:
			self.b.append(int(task.SimplexTableau[self.indexOfBranchVariableString][task.numberOfVariables + 1]) + 1)
			self.signsOfInequality.append(">=")
			print("     ", task.SimplexTableau[self.indexOfBranchVariableString][0], ">=", self.b[len(self.b) - 1], "\n")


	# delete - функция, удаляющая последнюю строку матрицы A, а также последние элементы вектора правой части системы ограничений и вектора знаков неравенств. Это 
	# используется в алгоритме метода ветвей и границ, когда необходимо в процессе ветвления удалить последнее добавленное ограничение и добавить новое 

	def delete(self):
		A.pop()
		b.pop()
		signsOfInequality.pop()

	# findAndPrintOptimalSolution - функция, принимающая в качестве аргумента список со всеми целочисленными решениями, находит из них оптимальное, и выводит результат

	def findAndPrintOptimalSolution(self, integerSolutions):
		maximalValueOfFunction = 0
		indexOfOptimalSolution = 0
		for index in range(len(integerSolutions)):
			if( integerSolutions[index][3] > maximalValueOfFunction):
				indexOfOptimalSolution = index

		x = ["x1", "x2", "x3", "F"]

		for index in range(4):
			print("\n    ", x[index], "=", integerSolutions[indexOfOptimalSolution][index])
			
	# getIntegerSolution - функция, получающая из симплекс-таблицы целочисленное решение. Возвращает список, первым значением которого является коэффициент при x1,
	# вторым - коэффициент при x2, третьим - коэффициент при x3, а последним - значение функции при данных корнях. Необходима, когда нужно будет из всех решений найти
	# оптимальное, а также при удобном выводе этого оптимального решения

	def getIntegerSolution(self, task):
		integerSolution = []
		for i in range(3):
			for j in range(1, task.numberOfBasicVariables + 1):
					if(task.SimplexTableau[j][0] == task.x[i]):
						integerSolution.append(task.SimplexTableau[j][task.numberOfVariables + 1])
						break
		integerSolution.append(task.SimplexTableau[task.numberOfBasicVariables + 1][task.numberOfVariables + 1])

		return integerSolution


	def branchAndBoundAlgorithm(self):

		# integerSolutions - список, в который будут добавляться в течение работы алгоритма все целочисленные решения, а в конце алгоритма с помощью этого списка из всех
		# решений будет найдено оптимальное

		integerSolutions = [] 

		# Решение исходной задачи методом перебора, а также с помощью симплекс-метода

		initialTask = Simplex(self.c, self.A, self.b, self.signsOfInequality)
		initialTask.printLinearProblem()
		initialTask.bruteForce()
		initialTask.simplexAlgorithm()


		for i in range(2):

			# Проверяем, является ли решение задачи не данном этапе целочисленным. Если да - выходим из цикла - то есть заканчиваем ветвление, а также добавляем данное
			# целочисленное решение в список всех целочисленных решений. Если нет - получаем индекс строки переменной, ветвление которой нужно осуществить

			indexOfBranchVariableString = self.checking(initialTask)
			if not(indexOfBranchVariableString):
				print("\n     Целочисленное решение найдено!\n")
				integerSolution = self.getIntegerSolution(initialTask)
				integerSolutions.append(integerSolution)
				break

			# Добавляем новые ограничения в начальные условия

			self.addingListToA(self.indexOfBranchVariable)
			self.addingElementToB(i, initialTask)

			# Решаем новую задачу с помощью симплекс-метода. Если решения нет - удаляем все добавленные на данном этапе новые ограничения и переходим к следующей итерации 
			# ветвления 

			print("     Тогда задача будет иметь вид:")

			firstStepTask = Simplex(c, A, b, signsOfInequality)
			firstStepTask.printLinearProblem()
			if not(firstStepTask.simplexAlgorithm()):
				self.delete()
				continue

			# Далее алгоритм производит ветвление и работает так же, как и на этом этапе. Всего алгоритм имеет три цикла, каждый следующий цикл вложен в предыдущий. Это
			# связано с тем, что в исходной функции всего три переменных - таким образом максимальная высота дерева в решении данной задачи будет равна трем

			for j in range(2):
				indexOfBranchVariableStringFirstStep = self.checking(firstStepTask)

				if not(indexOfBranchVariableStringFirstStep):
					print("\n     Целочисленное решение найдено!\n")
					integerSolution = self.getIntegerSolution(firstStepTask)
					integerSolutions.append(integerSolution)
					break

				self.addingListToA(self.indexOfBranchVariable)
				self.addingElementToB(j, firstStepTask)

				print("     Тогда задача будет иметь вид:")

				secondStepTask = Simplex(c, A, b, signsOfInequality)
				secondStepTask.printLinearProblem()
				if not(secondStepTask.simplexAlgorithm()):
					self.delete()
					continue

				for k in range(2):
					indexOfBranchVariableStringSecondStep = self.checking(secondStepTask)

					if not(indexOfBranchVariableStringSecondStep):
						print("\n     Целочисленное решение найдено!\n")
						integerSolution = self.getIntegerSolution(secondStepTask)
						integerSolutions.append(integerSolution)
						break

					self.addingListToA(self.indexOfBranchVariable)
					self.addingElementToB(j, secondStepTask)

					print("     Тогда задача будет иметь вид:")

					thirdStepTask = Simplex(c, A, b, signsOfInequality)
					thirdStepTask.printLinearProblem()
					if not(task3.simplexAlgorithm()):
						self.delete()
						continue

					self.delete()

				self.delete()

			self.delete()

		# Из всех целочисленных решений находим оптимальное 

		print("\n     Методом ветвей и границ найдено следующее целочисленное решение:")
		self.findAndPrintOptimalSolution(integerSolutions)





signsOfInequality = ["<=", "<=", "<="]

c = [5, 6, 1]

A = [[2, 1, 1]
	,[1, 2, 0]
	,[0, 0.5, 1]]

b = [5, 3, 8]

myTask = IntegerLinearProgramming(c, A, b, signsOfInequality)
myTask.branchAndBoundAlgorithm()








