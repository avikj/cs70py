import random
import base64
from modular_arithmetic import mod_inverse, mod_pow, is_probably_prime

# Covered in Week 2 notes on bijections and RSA (http://www.eecs70.org/static/notes/n7.pdf)

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

# a generator which yields primes with b bits
def find_primes(b=BITS):
	while True:
		candidate = 2**(b-1) + random.randrange(2**(b-1))
		if is_probably_prime(candidate):
			yield candidate

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

def test_funcs():
	assert mod_inverse(3, 40) == 27
	assert mod_pow(52, 27, 55) == 13
	assert not is_probably_prime(121)
	assert is_probably_prime(191)
	pk, sk = create_key_pair()
	assert decrypt_message(encrypt_message('hello world', pk), sk) == 'hello world'
	assert decrypt_message(encrypt_message('hello world', sk), pk) == 'hello world'