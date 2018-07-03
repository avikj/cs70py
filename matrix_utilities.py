
# finds rref of matrix in place
def rref(matrix):
	# returns a-b
	def subtract(a, b):
		return [a[i]-b[i] for i in range(len(a))]
	# returns a multiplied by scalar s
	def multiply(a, s):
		return [a[i]*s for i in range(len(a))]
	# returns len(row) if there is no pivot column
	def get_pivot(row):
		pivot = 0
		while pivot < len(row) and row[pivot] == 0:
			pivot += 1
		return pivot
	pivot = 0
	for i in range(len(matrix)):
		pivot = get_pivot(matrix[i])
		if pivot >= len(matrix[i]):
			continue
		matrix[i] = multiply(matrix[i], 1/matrix[i][pivot])
		# we zero out column i in every row other than i
		for j in range(len(matrix)):
			if j == i: continue
			matrix[j] = subtract(matrix[j], multiply(matrix[i], matrix[j][pivot]))
	matrix.sort(key=get_pivot)