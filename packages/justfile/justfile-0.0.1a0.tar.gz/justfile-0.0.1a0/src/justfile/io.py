import os
from justfile.exception import JustFileException

def read(path, mode="r", complain=False, default_content=None):
	"""Read contents from a file.
	
	:param path: Full path of the file
	
	:param mode: How to open the file
	
	:param complain: If true, all exceptions will be swallowed and
		`default_content` will be returned.
	
	:param default_content: What to return in case we can't read.
	
	"""
	try:
		if not os.path.exists(path):
			raise JustFileException(f"{path} does not exist.")
		if not os.path.exists(path):
			return None
		with open(path, mode) as f:
			return f.read()
	except Exception as e:
		if not complain:
			return default_content
		raise e

def write(path, content, mode="w+", create_dirs=True, complain=False):
	"""Write contents to a file.
	
	:param path: Full path of the file
	
	:param content: Content to write to the file.
	
	:param mode: How to open the file
	
	:param create_dirs: Whether to create directories to the file.
	
	:param complain: If False, will swallow all exceptions.
	
	:return: True on success, False otherwise.
	"""
	try:
		d = os.path.dirname(path)
		if not os.path.exists(d) and len(d) and create_dirs:
			os.makedirs(d)
		with open(path, mode) as f:
			f.write(content)
			return True
	except Exception as e:
		if complain:
			raise e
		return False

def append(path, content, mode="a+", create_dirs=True, complain=False):
	"""Append contents to a file.
	
	:param path: Full path of the file
	
	:param content: Content to write to the file.
	
	:param mode: How to open the file
	
	:param create_dirs: Whether to create directories to the file.
	
	:param complain: If False, will swallow all exceptions.
	
	:return: True on success, False otherwise.
	
	"""
	return write(path, content, mode, create_dirs, complain)
