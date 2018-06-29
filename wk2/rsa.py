import random
import base64
BITS = 256
def encrypt_message(plaintext, public_key):
	while len(plaintext)*8 % BITS != 0:
		plaintext += chr(0) # null character
	result = ''
	for i in range(0, len(plaintext), BITS/8):
		chunk = str_to_int(plaintext[i:i+BITS/8])
		encrypted_chunk = mod_pow(chunk, public_key[0], public_key[1])
		result += int_to_str(encrypted_chunk)
	return base64.b64encode(result)

def str_to_int(s):
	r = 0
	for j, c in enumerate(s):
		r += ord(c)*(256**j)
	return r

def int_to_str(i):
	r = ''
	while i != 0:
		r += chr(i%256)
		i //= 256
	return r

def decrypt_message(ciphertext, private_key):
	ciphertext = base64.b64decode(ciphertext)
	assert len(ciphertext)*8 % BITS == 0
	result = ''
	# chunk length is twice as long for decryption since modulus has twice as many bits as plaintext chunk, and mod_pow(...) <= modulus
	for i in range(0, len(ciphertext), BITS/4): 
		chunk = str_to_int(ciphertext[i:i+BITS/4])
		encrypted_chunk = mod_pow(chunk, private_key[0], private_key[1])
		result += int_to_str(encrypted_chunk)
	return result

# given public key and factorization of N, returns private key
def create_private_key(public_key, p, q):
	return mod_inverse(public_key, (p-1)*(q-1))

# Miller-Rabin primality test
def is_probably_prime(n, bases_to_check=[2,3,5,7,11,13,17]):
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
def find_primes(b=BITS):
	while True:
		candidate = 2**(b-1) + random.randrange(2**(b-1))
		if is_probably_prime(candidate):
			yield candidate

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
	# assumes x >y
	# returns (gcd(x, y), a, b) such that ax + by = gcd(x, y)
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
	return egcd(m, n)[2]%m

def test_funcs():
	assert mod_inverse(3, 40) == 27
	assert mod_pow(52, 27, 55) == 13
	assert not is_probably_prime(121)
	assert is_probably_prime(191)
	pk, sk = create_key_pair()
	assert decrypt_message(encrypt_message('hello world', pk), sk) == 'hello world'
	assert decrypt_message(encrypt_message('hello world', sk), pk) == 'hello world'

# returns (public_key, private_key)
# each key consists of an exponent and modulus
def create_key_pair():
	fp = find_primes()
	p = next(fp)
	q = next(fp)
	N = p*q # N has more bits than e, d, and chunks of input to be encrypted, since if they were the same # of bits, the values might be higher than the modulus
	e = next(fp)
	d = mod_inverse(e, (p-1)*(q-1))
	return ((e, N), (d, N))

