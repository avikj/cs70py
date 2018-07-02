# Covered in Week 2 notes on modular arithmetic (http://www.eecs70.org/static/notes/n6.pdf)

def mod_pow(base, exp, m):
	if exp == 0:
		return 1
	z = mod_pow(base, exp//2, m)
	if exp % 2 == 0:
		return z*z % m
	return z*z*base % m


# find d = gcd(m, n) = 1 and a, b such that am + bn = d
# then b*n == 1 mod m -> b and n are inverses
def mod_inverse(n, m):
	# assumes x > y
	# returns (gcd(x, y), a, b) such that ax + by = gcd(x, y)
	if n == 0:
		raise ValueError('0 has no modular inverse.')
	def egcd(x, y):
		if y == 0:
			return (x, 1, 0)
		d, a0, b0 = egcd(y, x%y)
		#    a0y + b0(x%y) = d
		# -> a0y + b0(x-(x//y)y) = d
		# -> a0y + b0x - b0(x//y)y = d
		# -> b0x + (a0-b0(x//y))y = d
		# -> a1 = b0, b1 = a0-b0(x//y)
		# -> a1x + b1y = d
		return (d, b0, a0-b0*(x//y))
	r = egcd(m, n)
	if r[0] != 1:
		raise ValueError('Argument must be coprime to modulus.')
	return r[2]%m


def test():
	assert mod_inverse(3, 40) == 27
	assert mod_pow(52, 27, 55) == 13

if __name__ == '__main__':
	test()