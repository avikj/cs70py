from modular_arithmetic import mod_inverse, mod_pow, is_probably_prime

# Covered in Week 3 notes on polynomials (http://www.eecs70.org/static/notes/n8.html)

# Implementation of Z/pZ with overloaded number operations
class FiniteFieldNumber(object):
	def __init__(self, value, m):
		if not is_probably_prime(m):
			raise ValueError('Modulus must be prime.')
		self.value = value%m
		self.m = m

	def inverse(self):
		return FiniteFieldNumber(mod_inverse(self.value, self.m), self.m)

	def __add__(self, other):
		other = self.typecast(other)
		return FiniteFieldNumber(self.value+other.value, self.m)

	def __sub__(self, other):
		other = self.typecast(other)
		return FiniteFieldNumber(self.value-other.value, self.m)

	def __mul__(self, other):
		other = self.typecast(other)
		return FiniteFieldNumber(self.value*other.value, self.m)

	def __radd__(self, other):
		return self.__add__(other)

	def __rmul__(self, other):
		return self.__mul__(other)

	def __rsub__(self, other):
		other = self.typecast(other)
		return FiniteFieldNumber(other.value-self.value, self.m)

	def __div__(self, other):
		other = self.typecast(other)
		return self.__mul__(other.inverse())

	def __rdiv__(self, other):
		other = self.typecast(other)
		return other.__mul__(self.inverse())

	def __pow__(self, power):
		if isinstance(power, FiniteFieldNumber):
			power = power.value
		if not isinstance(power, int):
			raise ValueError('Cannot raise to non-integer power.')
		if power < 0:
			return self.__pow__(-power).inverse()
		return FiniteFieldNumber(mod_pow(self.value, power, self.m), self.m)

	def __neg__(self):
		return FiniteFieldNumber(-self.value, self.m)

	def __eq__(self, other):
		if not isinstance(other, FiniteFieldNumber):
			if isinstance(other, int):
				other = FiniteFieldNumber(other, self.m)
			else:
				raise ValueError('Cannot operate on non-integer values.')
		return self.value == other.value and self.m == other.m

	def __str__(self):
		return str(self.value)

	def typecast(self, other):
		if not isinstance(other, FiniteFieldNumber):
			if isinstance(other, int):
				other = FiniteFieldNumber(other, self.m)
			else:
				raise ValueError('Cannot operate on non-integer values.')
		if self.m != other.m:
			raise ValueError('Cannot operate on numbers from different fields')
		return other

def test():
	# test __eq__ and __init__
	assert FiniteFieldNumber(7, 11) == FiniteFieldNumber(7, 11)
	assert FiniteFieldNumber(7, 11) == 7
	assert FiniteFieldNumber(7, 11) != FiniteFieldNumber(8, 11)
	assert FiniteFieldNumber(7, 11) != 8
	assert 8 != FiniteFieldNumber(7, 11)
	assert FiniteFieldNumber(7, 11) == FiniteFieldNumber(18, 11)
	assert FiniteFieldNumber(7, 11) == 18
	assert FiniteFieldNumber(7, 11) == -4
	assert 18 == FiniteFieldNumber(7, 11)
	# test inverse
	assert FiniteFieldNumber(7, 11).inverse() == 8
	# test __add__
	assert FiniteFieldNumber(7, 11) + FiniteFieldNumber(6, 11) == FiniteFieldNumber(2, 11)
	assert FiniteFieldNumber(7, 11) + 6 == FiniteFieldNumber(2, 11)
	assert FiniteFieldNumber(7, 11) + 4 == 0
	# test __radd__
	assert 10+FiniteFieldNumber(7, 11) == 6
	# test __sub__
	assert FiniteFieldNumber(7, 11) - FiniteFieldNumber(8, 11) == 10
	assert FiniteFieldNumber(7, 11) - 8 == 10
	# test __rsub__
	assert 7-FiniteFieldNumber(10, 11) == 8
	# test __mul__
	assert FiniteFieldNumber(7, 11)*8 == 1
	# test __rmul__
	assert 8*FiniteFieldNumber(7, 11) == 1
	# test __div__
	assert FiniteFieldNumber(1, 11)/7 == 8
	# test __rdiv__
	assert 1/FiniteFieldNumber(7, 11) == 8
	# test __pow__
	assert FiniteFieldNumber(7, 11)**2 == 5
	assert pow(FiniteFieldNumber(7, 11), 2) == 5
	assert pow(FiniteFieldNumber(7, 11), -1) == FiniteFieldNumber(7, 11).inverse()
	assert pow(FiniteFieldNumber(7, 11), -2) == FiniteFieldNumber(7, 11).inverse()**2
	# test __neg__
	assert -FiniteFieldNumber(7, 11) == 4

test()
