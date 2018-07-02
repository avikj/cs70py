from copy import copy
from finite_field_number import FiniteFieldNumber

# Covered in Week 3 notes on polynomials (http://www.eecs70.org/static/notes/n8.html)

# A polynomial is represented as a list of coefficients of the polynomial
# the degree of the polynomial is len(p_coeffs)-1
# the coefficient at index i corresponds to the x^i term
# i.e. [c, b, a] represents ax^2+bx+c
def evaluate(p_coeffs, x):
	return sum((pow(x, i)*p_coeffs[i] for i in range(len(p_coeffs))))

def multiply(p_coeffs, q_coeffs, do_trim=True):
	r_coeffs = [0]*((len(p_coeffs)-1)+(len(q_coeffs)-1)+1) # degree is sum of degrees of factors; len(coeffs) = degree + 1
	for i in range(len(p_coeffs)):
		for j in range(len(q_coeffs)):
			r_coeffs[i+j] += p_coeffs[i]*q_coeffs[j]
	return trim(r_coeffs) if do_trim else r_coeffs

def add(p_coeffs, q_coeffs, do_trim=True):
	r_coeffs = [0]*max(len(p_coeffs), len(q_coeffs))
	for i in range(len(r_coeffs)):
		if i < len(p_coeffs):
			r_coeffs[i] += p_coeffs[i]
		if i < len(q_coeffs):
			r_coeffs[i] += q_coeffs[i]
	return trim(r_coeffs) if do_trim else r_coeffs
# returns coeffs representing p multiplied by x^n
def increase_degree(p_coeffs, n):
	for i in range(n):
		p_coeffs = [0]+p_coeffs
	return p_coeffs

# returns (quotient, remainder) of division of p by q (long division algorithm)
def divide(p_coeffs, q_coeffs):
	p_degree = len(p_coeffs)-1
	p_coeffs = [float(c) for c in p_coeffs]
	r_coeffs = []
	for i in range(len(p_coeffs)-len(q_coeffs)+1):
		print p_coeffs
		r_coeff = p_coeffs[-1]/q_coeffs[-1]
		print 'got coefficient ', r_coeff
		r_coeffs = [r_coeff] + r_coeffs # we get higher degree coefficients first, so we need to prepend to get them sorted with increasing degree
		p_coeffs = add(p_coeffs, increase_degree(multiply(q_coeffs, [-r_coeff], False), len(p_coeffs)-len(q_coeffs)), False)
		p_coeffs = p_coeffs[:-1]
	return trim(r_coeffs), trim(p_coeffs)
def trim(p_coeffs):
	while len(p_coeffs) > 0 and p_coeffs[-1] == 0:
		p_coeffs = p_coeffs[:-1]
	return p_coeffs

# Lagrangian interpolation
def interpolate(points):
	# get polynomials that evaluate to 1 at the a given x and 0 at the others
	def delta(x0, xs):
		result = [1]
		for root in xs:
			result = multiply(result, [-root, 1]) # multiply by (x-r)
		result = multiply(result, [evaluate(result, x0)**(-1)])
		return result
	xs, ys = [x for x, y in points], [y for x, y in points]
	deltas = [delta(x, xs[:i]+xs[i+1:]) for i, x in enumerate(xs)]
	result_coeffs = []
	for i in range(len(points)):
		result_coeffs = add(result_coeffs, multiply(deltas[i], [ys[i]]))
	return trim(result_coeffs)

def equal(p_coeffs, q_coeffs, tolerance=0):
	p_coeffs, q_coeffs = trim(p_coeffs), trim(q_coeffs)
	if len(p_coeffs) != len(q_coeffs):
		return False
	for i in range(len(p_coeffs)):
		if abs(p_coeffs[i]-q_coeffs[i]) > tolerance:
			return False
	return True

def test():
	assert evaluate([1, 2, 3], 5) == 1 + 2*5**1 + 3*5**2 # p(x) = 3x^2+2x+1
	assert evaluate([1, 0, 0], 100) == 1 # p(x) = 1
	assert add([1, 1], [1, 1]) == [2, 2] # (1+x)+(1+x) = (2+2x)
	assert add([1, 1], [1, -1, 4]) == [2, 0, 4] # (1+x)+(1-x+4x^2) = (2+4x^2)
	assert multiply([1, 1], [1, 1]) == [1, 2, 1] # (1+x)*(1+x) = (1+2x+x^2)
	assert multiply([2], [3, 2, 10, 1]) == [6, 4, 20, 2] # 2*(3+2x+10x^2+x^3) = 6+4x+20x^2+2x^3
	p = [1, 2, 3]
	assert equal(interpolate([(1, evaluate(p, 1)), (10, evaluate(p, 10)), (7, evaluate(p, 7))]), [1, 2, 3], 1e-5)
	quotient, remainder = divide([-1, 0, 1, 1], [-1, 1])
	assert equal(quotient, [2, 2, 1], 1e-5) and equal(remainder, [1], 1e-5)

	# Test on FiniteFieldNumbers
	p = [3, 2] # 2x + 3
	assert isinstance(evaluate(p, FiniteFieldNumber(2, 5)), FiniteFieldNumber)
	assert evaluate(p, FiniteFieldNumber(2, 5)) == 2
	p = [FiniteFieldNumber(3, 5), FiniteFieldNumber(2, 5)]
	assert isinstance(evaluate(p, 2), FiniteFieldNumber)
	assert evaluate(p, 2) == 2


test()