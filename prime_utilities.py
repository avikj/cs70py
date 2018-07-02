from modular_arithmetic import mod_pow
import random
# Miller-Rabin primality test
def is_probably_prime(n, bases_to_check=[2,3,5,7,11,13,17]):
	if n in {2,3,5,7,11,13,17}:
		return True
	for a in bases_to_check:
		# rewrite n-1 as 2^s * d, where d is odd
		d = n-1
		s = 0
		while d % 2 == 0:
			s += 1
			d /= 2
		if mod_pow(a, d, n) == 1:
			continue
		passed = False
		for r in range(s):
			if mod_pow(a, d*(2**r), n) == n-1:
				passed = True
				break
		if passed:
			continue
		return False
	return True

# a generator which yields primes with b bits
def find_primes(b=256):
	while True:
		candidate = 2**(b-1) + random.randrange(2**(b-1))
		if is_probably_prime(candidate):
			yield candidate

def test():
	assert not is_probably_prime(121)
	assert is_probably_prime(191)

if __name__ == '__main__':
	test()