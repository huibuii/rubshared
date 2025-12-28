import chacha_template as chacha

compare_val_rot = 1756164132
compare_val_state = [1634760805, 857760878, 2036477234, 1797285236, 50463231, 117835012, 185207048, 252579084,
					 319951120, 387323156, 454695192, 522067228, 0, 2018915346, 4041129114, 2018915346]
compare_val_qr1 = [1742504000, 857760878, 2036477234, 1797285236, 1518405954, 1271407149, 3877912865, 137411679,
				   3678835995, 3584276975, 945816094, 3655229697, 72942896, 2018915346, 4041129114, 2018915346]
compare_val_qr2 = [1742504000, 857760878, 616232096, 1797285236, 1518405954, 1271407149, 3877912865, 2147249065,
				   4057461720, 3584276975, 945816094, 3655229697, 72942896, 957179129, 4041129114, 2018915346]
compare_val_ks = b';@\xb52\xd9\xc9p\x02\x93\x8ea\xc9NM\xe5\x89i\x16\x8aD\xc4\xa3\x00q\xd5\xd6\xea\xfb\xe3\x1c\xb1\x89' \
				 b'\xf1\x03\xabM\x04\xe5\xb52(?\xf6\xe2]\xfb\x87IE\nq\xa8H\x12\xb3i\xa1o\x9a\x90`\xf3\xdb\xbe'

try:
	if chacha.cyclic_shift(0x12345678, 9) != compare_val_rot:
		print(f'[-] Fehler in cyclic_shift.')
	else:
		print(f'[+] cyclic_shift OK.')

	chacha20_state = chacha.init_chacha_state(
		0xff0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f,
		0x123456789abcdef012345678)
	chacha20_state[12] = 0
	if chacha20_state != compare_val_state:
		print(f'[-] Fehler in init_chacha_state.')
	else:
		print(f'[+] init_chacha_state OK.')

	err = 0
	chacha20_state = [1634760805, 857760878, 2036477234, 1797285236, 2792911058, 1271407149, 3877912865, 137411679,
					  2132063910, 3584276975, 945816094, 3655229697, 3735928559, 2018915346, 4041129114, 2018915346]
	chacha.quarterround(chacha20_state, 0, 4, 8, 12)
	err |= not (chacha20_state == compare_val_qr1)
	chacha.quarterround(chacha20_state, 2, 7, 8, 13)
	err |= not (chacha20_state == compare_val_qr2)
	if err:
		print(f'[-] Fehler in quarterround.')
	else:
		print(f'[+] quarterround OK.')

	chacha20_state = chacha.init_chacha_state(
		0x8d0be299909c002c0daabd2fc08cf81a0c9bb9b66871347184ddf96a0a92d3ef,
		0x61910caba7c14f22038b3b11)
	keystream_block = chacha.generate_chacha_keystream(chacha20_state, block_count=0xabcdef12)
	if keystream_block != compare_val_ks:
		print(f'[-] Fehler in generate_chacha_keystream.')
	else:
		print(f'[+] generate_chacha_keystream OK.')
except Exception as e:
	print(f"[-] Fehler beim Ausführen des Codes! {e}")
	exit(-1)

print("Test end.")