from __future__ import division
from copy import copy
from finite_fields import FiniteFieldNumber, FiniteField

# Covered in Week 3 notes on polynomials (http://www.eecs70.org/static/notes/n8.html)

def trim(p_coeffs):
	while len(p_coeffs) > 0 and p_coeffs[-1] == 0:
		p_coeffs = p_coeffs[:-1]
	return p_coeffs

# Lagrangian interpolation
def interpolate(points, field=None):
	if field is None:
		field = type(points[0][1])
	# get polynomials that evaluate to 1 at the a given x and 0 at the others
	def delta(x0, xs):
		result = Polynomial([1], field)
		for root in xs:
			result *= Polynomial([-root, 1], field) # multiply by (x-r)
		result *= result.evaluate(x0)**(-1)
		return result
	xs, ys = [x for x, y in points], [y for x, y in points]
	deltas = [delta(x, xs[:i]+xs[i+1:]) for i, x in enumerate(xs)]
	result = []
	for i in range(len(points)):
		result += deltas[i] * Polynomial(ys[i], field=field)
	return result

def equal(p_coeffs, q_coeffs, tolerance=0):
	p_coeffs, q_coeffs = trim(p_coeffs), trim(q_coeffs)
	if len(p_coeffs) != len(q_coeffs):
		return False
	for i in range(len(p_coeffs)):
		if abs(p_coeffs[i]-q_coeffs[i]) > tolerance:
			return False
	return True

def test():
	p = Polynomial([1, 2, 3])
	assert p == Polynomial([1, 2, 3])
	assert p == Polynomial([1, 2, 3, 0])
	assert p != Polynomial([0, 1, 2, 3])
	assert p.evaluate(5) == 1 + 2*5**1 + 3*5**2 # p(x) = 3x^2+2x+1
	assert Polynomial([1, 0, 0]).evaluate(100) == 1 # p(x) = 1
	assert Polynomial([1, 1])+Polynomial([1, 1]) == Polynomial([2, 2]) # (1+x)+(1+x) = (2+2x)
	assert Polynomial([1, 1]) + Polynomial([1, -1, 4]) == Polynomial([2, 0, 4]) # (1+x)+(1-x+4x^2) = (2+4x^2)
	assert Polynomial([1, 1])*Polynomial([1, 1]) == Polynomial([1, 2, 1]) # (1+x)*(1+x) = (1+2x+x^2)
	assert Polynomial([2])*Polynomial([3, 2, 10, 1]) == Polynomial([6, 4, 20, 2]) # 2*(3+2x+10x^2+x^3) = 6+4x+20x^2+2x^3
	assert interpolate([(1, p.evaluate(1)), (10, p.evaluate(10)), (7, p.evaluate(7))]).__eq__(Polynomial([1, 2, 3]), 1e-5)
	quotient, remainder = Polynomial([-1, 0, 1, 1]) / Polynomial([-1, 1])
	assert quotient.__eq__(Polynomial([2, 2, 1]), 1e-5) and remainder.__eq__(Polynomial([1]), 1e-5)

	# Test on FiniteFieldNumbers
	p = Polynomial([3, 2], FiniteField(5)) # 2x + 3
	assert isinstance(p.evaluate(2), FiniteFieldNumber)
	assert p.evaluate(2) == 2
	p = Polynomial([3, 2], FiniteField(5))
	q = Polynomial([3, 2], FiniteField(5))
	r = p*q
	quotient, remainder = r/p
	assert quotient == q

class Polynomial(object):
	def __init__(self, arg, field=None):
		self.field = float
		if isinstance(arg, Polynomial):
			self.coeffs = copy(arg.coeffs)
			self.field = arg.field
		elif isinstance(arg, list):
			self.coeffs = trim(arg)
		else: # polynomial is a constant
			self.coeffs = [arg]
			if field is None:
				self.field = type(arg)
		if field is not None:
			self.field = field
		self.coeffs = [self.field(c) for c in self.coeffs]
		self.degree = max(len(self.coeffs)-1, 0)

	def evaluate(self, x):
		return sum([pow(x, i)*self.coeffs[i] for i in range(len(self.coeffs))])

	def __add__(self, other):
		other = self.typecast(other)
		r_coeffs = [0]*max(len(self.coeffs), len(other.coeffs))
		for i in range(len(r_coeffs)):
			if i < len(self.coeffs):
				r_coeffs[i] += self.coeffs[i]
			if i < len(other.coeffs):
				r_coeffs[i] += other.coeffs[i]
		return Polynomial(r_coeffs, self.field)
	def __radd__(self, other):
		return self + other
	def __mul__(self, other):
		other = self.typecast(other)
		r_coeffs = [0]*((len(self.coeffs)-1)+(len(other.coeffs)-1)+1) # degree is sum of degrees of factors; len(coeffs) = degree + 1
		for i in range(len(self.coeffs)):
			for j in range(len(other.coeffs)):
				r_coeffs[i+j] += self.coeffs[i]*other.coeffs[j]
		return Polynomial(trim(r_coeffs), self.field)

	def __rmul__(self, other):
		return self * other
	def __sub__(self, other):
		other = self.typecast(other)
		return self + other * (-1)
	def __rsub__(self, other):
		return (-1)*(self-other)
	def __pow__(self, power):
		result = Polynomial([1], self.field)
		for i in range(power):
			result = result * self
		return result
	def __div__(self, other):
		p = Polynomial(self, self.field) # impelment copy constructor
		r = Polynomial(0, self.field)
		i = 0
		while len(p.coeffs) > 0:
			r_coeff = p.coeffs[-1]/other.coeffs[-1]
			r += r_coeff*Polynomial.power(p.degree-other.degree, field=self.field)
			prev_p_degree = p.degree
			p = p - r_coeff*other*Polynomial.power(p.degree-other.degree, field=self.field)
			if p.degree == prev_p_degree:
				p = p-Polynomial.power(p.degree, field=self.field)*p.coeffs[-1]
			i += 1
		return r, p
	def __truediv__(self, other):
		return self.__div__(other)
	def typecast(self, other):
		if not isinstance(other, Polynomial):
			other = Polynomial(other, self.field)
		return other

	def __str__(self):
		self.coeffs = trim(self.coeffs)
		if len(self.coeffs) == 0:
			return '0'
		result = '+'+str(self.coeffs[0])
		if len(self.coeffs) > 1:
			result = '+%sx'%self.coeffs[1] + result 
		for i in range(2, len(self.coeffs)):
			result = '+%sx^%d'%(self.coeffs[i], i) + result 
		return result[1:]
	def __repr__(self):
		return self.__str__()
	def __eq__(self, other, tolerance=0):
		if len(self.coeffs) != len(other.coeffs):
			return False
		if issubclass(self.field, float):
			return all([abs(self.coeffs[i]-other.coeffs[i]) <= tolerance for i in range(len(self.coeffs))]) 
		return self.coeffs == other.coeffs
	def __ne__(self, other):
		return not (self == other)

	@staticmethod
	def power(n, field=float):
		return Polynomial([0]*n+[1], field=field)
if __name__ == '__main__':
	test()