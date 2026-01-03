import struct
import matplotlib.pyplot as plt
import time
from pathlib import Path



def plot_results(x_data, y_data, x_label='xlabel', y_label='ylabel', filename='plot.png'):
	""" 2D plot of y_data against x_data, stored as PNG """
	fig, ax = plt.subplots(nrows=1, ncols=1)
	ax.plot(x_data, y_data, marker='o')
	ax.set_xlabel(x_label)
	ax.set_ylabel(y_label)
	plt.savefig(Path(filename), format="png", dpi=300)
	fig.show()

def plot_results_log(x_data, y_data, x_label='xlabel', y_label='ylabel', filename='plot_log.png'):
	""" 2D plot of y_data against x_data with logarithmic y axis, stored as PNG """
	fig, ax = plt.subplots(nrows=1, ncols=1)
	ax.plot(x_data, y_data, marker='o')
	ax.set_xlabel(x_label)
	ax.set_ylabel(y_label)
	ax.set_yscale('log')
	plt.savefig(Path(filename), format="png", dpi=300)
	fig.show()

def print_chacha_keystream(keystream):
	""" Print a keystream block of 64 bytes as a block of 16 32-bit words """
	for i in range(64):
		print(f'{keystream[i]:02x}', end='')
		if (i+1) % 16 == 0:
			print()
		elif (i+1) % 4 == 0:
			print(' ', end='')
	print()

def print_chacha_state(state):
	""" Print the ChaCha state as 16 single 32-bit words """
	for i in range(16):
		print(f'{state[i]:08x} ', end='')
		if (i+1) % 4 == 0:
			print()
	print()

"""
ChaCha specific functions. Look out for 'TODOs'. Here you need to add code.
"""

def cyclic_shift(v, s):
	"""
	Returns rotation of v (32-bit integer) by s (integer from 0 to 32) positions to the left (cyclic)
	:param v: 32-bit integer to be rotated
	:param s: number of positions to rotate
	:return: rotated version of v
	"""
	# TODO: implement cyclic shift
	if not (0 <= v <= 0xFFFFFFFF):
		raise TypeError("v ist nicht in der range")

	digits = str(bin(v))[2:]

	while (len(digits) < 32):
		digits = "0" + digits

	s %= len(digits) # in case s is larger than v we need to modular reduce
	digits =  digits[s:] + digits[:s] # The return value takes the bits from the s' position to LSB and concatenates the bits from MSB to s' position.
	return int(digits, 2) #convert list to int and return

def init_chacha_state(key, nonce):
	"""
	Initialize the ChaCha state with key and nonce and return state
	:param key: 256-bit key
	:param nonce: 96-bit nonce
	:return: initial ChaCha state, a list of 16 32-bit integers.
	"""
	# converts the key to a list of eight 32-bit integers
	key_as_ints = struct.unpack('<8L', (key.to_bytes(32, "big")))
	# converts the nonce to a list of three 32-bit integers
	nonce_as_bytes = struct.unpack('<3L', (nonce.to_bytes(12, "big")))
	# Dummy initialization. Fills the state with zeros.
	state = [0] * 16

	# TODO: implement state initialization.
	blockcounter = 0x1
	constants = (0x61707865, 0x3320646e, 0x79622d32, 0x6b206574)

	state[0:4] = constants
	state[4:12] = key_as_ints
	state[12] = blockcounter
	state[13:16] = nonce_as_bytes

	return state


def mod32addition(x,y):
	x = (x + y) & 0xFFFFFFFF
	return x


def quarterround(state_array,a,b,c,d):

	""" Execute ChaCha quarterround on state at positions a,b,c,d of state_array.
	:param state_array: the ChaCha state, a list of 16 32-bit integers.
	:param a: Value between 0 and 15. Index for the the state array.
	:param b: Value between 0 and 15. Index for the the state array.
	:param c: Value between 0 and 15. Index for the the state array.
	:param d: Value between 0 and 15. Index for the the state array.
	:return: no return value (changes are directly applied to the array due to 'call by reference').
	"""
	pass
	# TODO: implement quarterround


	at = a
	bt = b
	ct = c
	dt = d

	a = int(state_array[at])
	b = int(state_array[bt])
	c = int(state_array[ct])
	d = int(state_array[dt])

	a = mod32addition(a,b)
	d ^= a
	d = cyclic_shift(d, 16)

	c = mod32addition(c,d)
	b ^= c
	b = cyclic_shift(b, 12)

	a = mod32addition(a,b)
	d ^= a
	d = cyclic_shift(d, 8)

	c = mod32addition(c,d)
	b ^= c
	b = cyclic_shift(b, 7)

	state_array[at] = a
	state_array[bt] = b
	state_array[ct] = c
	state_array[dt] = d


def generate_chacha_keystream(state, block_count):
	"""
	ChaCha inner block function, for given state matrix and block number.
	:param state:  is the ChaCha state of 16 single 32-bit integers.
	:param block_count: is a 32-bit integer, denoting the keystream block number to be generated (to be updated in state)
	:return: 64 bytes (current key stream block)
	"""
	# TODO: implement ChaCha inner block and adjust block_count

	initial_state = state.copy()
	state_out = state.copy()
	state_out[12] = block_count

	# converts the ChaCha state (a list of 16 32-bit integers) to a list of bytes
	def inner_block(state):
		quarterround(state, 1, 5, 9, 13)
		quarterround(state, 0, 4, 8, 12)
		quarterround(state, 2, 6, 10, 14)
		quarterround(state, 3, 7, 11, 15)
		quarterround(state, 0, 5, 10, 15)
		quarterround(state, 1, 6, 11, 12)
		quarterround(state, 2, 7, 8, 13)
		quarterround(state, 3, 4, 9, 14)

	for i in range(0,10):
		inner_block(state_out)

	for x in range (0,16):
		state_out[x] = mod32addition(state_out[x],initial_state[x])

	return struct.pack('<16L', *(state_out))


def process_file(source_file='encrypted.zip', target_file='decrypted.zip'):
	"""
	apply ChaCha20 keystream to source file to either encrypt or decrypt
	:param source_file: name of source file (string)
	:param target_file: name of target file (string)
	:return:
	"""
	print(f'******************\n'
		  f'Encrypt / decrypt: {source_file}...\n'
		  '******************')

	# TODO: implement keystream. Hard-code the key, nonce and block count here.

	if not Path(source_file).exists():
		print(f'... {source_file} not found.')
		return
	f_out = open(target_file, "wb")

	with open(source_file, "rb") as f_in:
		in_block = f_in.read(64) # read file input
		while in_block:
			for i in range(len(in_block)):
				f_out.write(bytes([0])) # TODO: implement en/decryption
			in_block = f_in.read(64)

	f_out.close()

def bruteforce(max_key_length=18):
	"""
	Bruteforce key search with files in directory bruteforce_files/
	This function shall print the found keys for at least 20 files in bruteforce_files/
	:param max_key_length: is the maximum key space size to be searched during the brute-force attacks.
	:return:
	"""
	knownplaintext = str.encode("knownplaintext")
	for bits in range(1,max_key_length,1):
		f_in = open(f'bruteforce_files/{bits}.txt', "rb")
		cipher_text = f_in.read(len(knownplaintext))
		f_in.close()
		# TODO: implement brute force

	# TODO: for task h), use plot_results and plot_results_log to show runtime length over key length


if __name__ == '__main__':
	chacha20_state = init_chacha_state(
		0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f,
		0x000000090000004a00000000) # example from RFC8439 2.3.2.
	print_chacha_state(chacha20_state)
	print_chacha_keystream(generate_chacha_keystream(chacha20_state, block_count=1))

	chacha20_state = init_chacha_state(
		0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f,
		0x000000000000004a00000000) # example from RFC8439 2.4.2.
	print_chacha_state(chacha20_state)
	print_chacha_keystream(generate_chacha_keystream(chacha20_state, block_count=1))
	print_chacha_keystream(generate_chacha_keystream(chacha20_state, block_count=2))

	""" Task f) """

	process_file(source_file='template_and_files/encrypted.zip', target_file='decrypted.zip') # decrypt

	""" Task g) +  h) """

	bruteforce(max_key_length=20)
