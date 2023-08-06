# cheems.py

import re	# sub


def cheemsify_string(string):
	"""
	Returns a string as if Cheems said it.

	Given a string, returns a new string which is the result of taking the original,
	and replacing the first character in all sequences of repeated consonants with
	the letter 'm'.

	Parameters
	----------
	string: str
		The original string.

	Returns
	-------
	str
		The new string with the proper replacements.
	"""
	return re.sub(r'(.)\1+', lambda g:f'm{g.group(0)[1:]}', string)


def cheems_print(string):
	"""
	Prints a string as if Cheems said it.

	Given a string, "cheemsifies" it and then prints it.

	Parameters
	----------
	string: str
		The string that is to be printed in Cheems format.
	"""
	print(cheemsify_string(string))

