# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import threading
import time, string
import sys, random

alphabet = string.ascii_lowercase										# Lower case alphabet.
punctuation = string.punctuation										# All punctuation cases.
encrypted_file = sys.argv[1]										# Encrypted file to be checked caesar.
random_cases = [" ", "\t", "\r","\n","0","1","2","3","4","5","6","7","8","9","á","é","í","ó","ú","Á","É","Í","Ó","Ú"]	# Random cases where might not be in alphabet.
plaintxt_file = "plaintext.txt"											# Plain text file to see answer.

def longest_word(line):													# Function to get the longest string in a list.
	word = max(line, key=len)											# Getting the max in the list, length wise.
	for i in range(len(word)):											# now going through each character in the word
		if word[i] in punctuation:										# if word contains a punctuation, for example (general-purpose).
			return word[:i]												# return the half of the word (general).
	return word															# Returning the longest word in the list.

def location(letter):													# Function to get the position of the letter in the alphabet.
	try:																# For cases where fada letters come up, ex. á é í ó ú.
		position = alphabet.index(letter)								# Getting the position index of the letter in the alphabet list
		return position													# Returns the position
	except ValueError:													# If you get a ValueError on a letter (fada letters) just return as normal a.
		return 0

def encrypt(file):														# Function to encrypt text using ord.
	encrypted_text = ""													# empty string to add the encrypted message into.
	key = random.randrange(1, 26)										# Random key to encrypt text in.

	with open(file, encoding="utf8") as f:
		line = f.readlines()

	for sentence in line:
		for letter in sentence:
			if letter.isupper():										# Case where the letter is uppercase,
				letter = letter.lower()									# Temporarily turn it into lowercase.
				position = location(letter)								# then get the index/position of that letter in the alphabet.
				i = (position + key) % 26								# and add the correct key to the index/position of the letter.
				letter = alphabet[i]									# Then simply change the letter to the correct position.
				encrypted_text += letter.upper()						# Turn the letter back into uppercase and add it back into the sentence.
			elif (letter in punctuation) or (letter in random_cases):	# Case where if the character is a punctuation or a space,
				encrypted_text += letter								# We just leave it as it is and move on to next letter/character.
			else:														# Case where letter is a normal lowercase letter
				position = location(letter)								# get index/position of letter.
				i = (position + key) % 26								# change into correct key.
				letter = alphabet[i]									# make the encrypted letter into correct letter
				encrypted_text += letter								# add letter into encrypted_text.

	print("\nThe encrypted message is:\n\n{}".format(encrypted_text))

def decrypt(file, key):													# Function to decrypt a file
	decrypted_word = ""													# empty string to add the decrypted word into
	decrypted_text = ""													# empty string to add the full decrypted text into
	decrypted_text_and_key = []											# placing key and decrypted text into list to return
	all_keys = {}														# Dictionary of keys for key file

	with open(file, encoding="utf8") as f:												# Opening the file as f.
		line = f.readlines()											# Turning the whole file content into a list.

	for sentence in line:												# Now getting the whole list as a string.
		sentence = sentence.split()									# Then splitting by a space which gives you only the words without the spaces in list form.

	word = longest_word(sentence)										# Now getting the longest word in a sentence.
	word = word.translate(str.maketrans('', '', string.punctuation))	# Removing punctuation from the longest word

	for letter in word:													# For each letter in the longest word.
		position = location(letter)										# Search for the index/position of the letter in the alphabet.
		index = (position + key) % 26									# Now to change that key we add the index/position with the key and save it as the new position it will take, modulus 26 so that it will restart back to "a" when it passes "z".
		letter = alphabet[index]										# Now simply change the letter with the new letter, we do this with every letter we get in the longest word.
		decrypted_word += letter										# Add each letter one by one into the decrypted_word until you get the full decrypted word

	if decrypted_word in open("dictionary").read():						# It will check every for every key, so we only want to print when we find that the word is actually in the dictionary, we have the key.
		for each_word in line:											# Now i get the full with all the spaces and punctuation,
			for letter in each_word:									# And then get the letter/character in the sentence, including the spaces and punctuations.
				if letter.isupper():									# Case where the letter is uppercase,
					letter = letter.lower()								# Temporarily turn it into lowercase.
					position = location(letter)							# then get the index/position of that letter in the alphabet.
					i = (position + key) % 26							# and add the correct key to the index/position of the letter.
					if (letter in punctuation) or (letter in random_cases) or (letter in all_keys):		# If key is already in the dictionary or the key is a punctuation or one of the random cases, pass.
						pass
					else:
						all_keys[letter.upper()] = alphabet[i].upper()	# If key is not in the dictionary and it is a letter then put it into the dictionary
					letter = alphabet[i]								# Then simply change the letter to the correct position.
					decrypted_text += letter.upper()					# Turn the letter back into uppercase and add it back into the sentence.
				elif (letter in punctuation) or (letter in random_cases):	# Case where if the character is a punctuation or a space,
					decrypted_text += letter							# We just leave it as it is and move on to next letter/character.
				else:													# Case where letter is a normal lowercase letter
					position = location(letter)							# get index/position of letter.
					i = (position + key) % 26							# change into correct key.
					if(letter in punctuation) or (letter in random_cases) or (letter in all_keys):
						pass
					else:
						all_keys[letter.upper()] = alphabet[i].upper()
					letter = alphabet[i]								# make the encrypted letter into correct letter
					decrypted_text += letter							# add letter into decrypted text.

		count = 0														# Settomg variable count as 0
		fullproof_check = decrypted_text.strip().split()						# a full_proof case, sometimes when checking the key of a single word, sometimes, in rare cases there can be multiple words but the code will still be encrypted this would check multiple words just to make sure.
		if len(fullproof_check) > 70:									# if the decrypted text is greater than length 3
			for i in range(10):											# we want to check 9 other random words just to make sure we get ONLY the correct file.
				j = random.randrange(0, len(fullproof_check))			# getting 3 random words in the file
				fullproof_check[j] = fullproof_check[j].translate(str.maketrans('', '', string.punctuation))
				if fullproof_check[j] in open("dictionary").read():	# checking if all 3 are in the dictionary
					count += 1											# if it is in the dictionary count we add 1 to the count
			if count >= 6:												# if 3 or more words are in the dictionary, we can be sure that the key is correct.
				print("\nAnswer outputted into caesar-decrypt.txt and caesar-key.txt")
				print("\nThe decrypted message is:\n\n{}".format(decrypted_text))	# Printing decrypted text out.
				decrypted_textfile = open("caesar-decrypted.txt","w")				#Writing the decrypted_text to the caesar-decrypted.txt file 
				decrypted_textfile.write("\nThe decrypted message is:\n\n{}".format(decrypted_text))
				decrypted_textfile.close()
				key_textfile = open("caesar-key.txt","w")				# Writing the key into caesar-key.txt file
				for key in sorted(all_keys.keys()):
					if key.lower() in alphabet:							# just want the letters
						key_textfile.write("{} : {}\n".format(key, all_keys[key]))
				key_textfile.close()

		elif len(fullproof_check) <= 30:									# now if the length of the text file is not greater than 3, then we can be pretty sure that it is correct with checking the one word.
			print("\nThe decrypted message is:\n\n{}".format(decrypted_text))	# Printing decrypted text out.


def main():
	start = time.perf_counter()											# Testing how long program takes.

	keys = []															# list of keys
	cipher_threads = []													# list of threads

#--------------------------Creating Threads--------------------------#

	for i in range(1, 27):
		keys.append(i)													# Appending all possible keys into list

	for key in keys:													# Creating thread for every key
		start_thread = threading.Thread(target=decrypt, args=(encrypted_file, key,))	# creating threads
		cipher_threads.append(start_thread)								# Append those threads into cipher_threads
		start_thread.setDaemon = True									# By setting them as daemon threads, we can let them run and forget about them, and when our program quits, any daemon threads are killed automatically.

#--------------------------Starting Threads--------------------------#

	for thread in cipher_threads:										# Getting every thread in cipher_threads
		thread.start()													# Starting those threads

#--------------------------Joining Threads--------------------------#

	for thread in cipher_threads:										# Getting every thread in cipher threads
		thread.join()													# Joining those threads

	finish = time.perf_counter()										# Stop Time
	print()
	print(f"Finished in {round(finish-start, 2)} second(s)")			# Print out how long program took to run

if __name__ == '__main__':
	main()
