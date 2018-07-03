import random
import math
from copy import deepcopy
from prime_utilities import find_prime_above
from finite_field_number import FiniteFieldNumber
from polynomials import evaluate, interpolate, divide
from matrix_utilities import rref
# Covered in Week 3 notes on error-correcting codes (http://www.eecs70.org/static/notes/n9.pdf)

# packets is list of ints, k is max number of erasures to correct for, m is modulus (for polynomials on finite fields)
def encode_for_erasure_errors(packets, k):
	m = find_prime_above(max(packets+[len(packets)+k]))
	packets = [FiniteFieldNumber(p, m) for p in packets]
	points = [(FiniteFieldNumber(i, m), packet) for i, packet in enumerate(packets)]
	p_coeffs = interpolate(points)
	for x in range(len(packets), len(packets)+k):
		packets.append(evaluate(p_coeffs, x))
	return packets, m

# packets is list if ints or FiniteFieldNumbers, n is message length
def decode_with_erasures(packets, n, m):
	packets = [None if p is None else FiniteFieldNumber(p, m) for p in packets]
	points = [(FiniteFieldNumber(i, m), packet) for i, packet in enumerate(packets) if packet is not None]
	p_coeffs = interpolate(points)
	return [evaluate(p_coeffs, i) for i in range(n)]


# packets is list of ints, k is max number of erasures to correct for, m is modulus (for polynomials on finite fields)
def encode_for_general_errors(packets, k):
	return encode_for_erasure_errors(packets, 2*k)

def decode_with_general_errors(r, n, m):
	k = (len(r)-n)/2
	# P(i)E(i) = r_i E(i)
	# Q(i) = r_i E(i)
	# P(i)E(i) = Q(i) has degree (n-1)+k (n+k coefficients)
	# E(i) has k+1 coefficients but the first is 1; therefore, we have a total of n+2k coefficients to determine

	# represent a linear equation as a list of coefficients for a1, a2..., b1, b2, ending with a constant (right hand side of equation)
	equations = [] # this becomes a matrix
	for x in range(len(r)):
		x = FiniteFieldNumber(x, m)
		equation = [pow(x, j) for j in range(n+k)]+[-pow(x, j)*r[x.value] for j in range(k)]+[pow(x, k)*r[x.value]]
		# first append coefficients for a_j, in increasing order
		# then append negative of coefficients for b_j, since we move them from right side to left
		# finally append the extended column of constants (since coefficient of E must be 1)
		equations.append(equation)

	reduced_equations = deepcopy(equations)
	rref(reduced_equations)
	q_coeffs = [reduced_equations[i][-1] for i in range(n+k)]
	e_coeffs = [reduced_equations[j][-1] for j in range(n+k, n+2*k)]+[FiniteFieldNumber(1, m)]
	p_coeffs, remainder = divide(q_coeffs, e_coeffs)
	return [evaluate(p_coeffs, i) for i in range(n)]


def test():
	# test correcting erasure errors
	message = [random.randrange(20) for _ in range(20)]
	max_erasures = 10
	encoded_packets, m = encode_for_erasure_errors(message, max_erasures)
	for i in range(max_erasures): # erase up to 4 packets from the encoding
		encoded_packets[random.randrange(len(encoded_packets))] = None
	assert decode_with_erasures(encoded_packets, len(message), m) == message

	# test correcting general errors
	message = [random.randrange(20) for _ in range(20)]
	max_general_errors = 7
	encoded_packets, m = encode_for_general_errors(message, max_general_errors)
	for i in range(max_general_errors): # alter up to k packets from the encoding
		encoded_packets[random.randrange(len(encoded_packets))] = FiniteFieldNumber(random.randrange(m), m)
	assert decode_with_general_errors(encoded_packets, len(message), m) == message




if __name__ == '__main__':
	test()