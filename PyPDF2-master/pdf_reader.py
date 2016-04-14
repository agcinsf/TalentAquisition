from PyPDF2 import PdfFileReader
from os import listdir
from os.path import isfile, join
import re
import sys

REGEX_EMAIL = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
REGEX_TEL = r"^(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?$"

"""
Converts all resume in pdf files into txt files.
"""
def pdf_to_text(src_dir="../Resumes/", dst_dir="../resume_txt/"):

	files = [f for f in listdir(src_dir) if isfile(join(src_dir, f))][1:]
	for i in range(len(files)):
		pdfFileObj = open(src_dir+files[i], 'rb')
		pdfReader = PdfFileReader(pdfFileObj)
		num_pages = pdfReader.numPages
		f1 = open(dst_dir+"{0}.txt".format(files[i]), 'w+')
		for page in range(num_pages):
			pageObj = pdfReader.getPage(page)
			f1.write(pageObj.extractText().encode('utf-8'))
		f1.close()

"""
Receives txt files and strips off the lines that contain personal information.
"""
def txt_to_no_personal(src_dir="../resume_txt/", dst_dir="../resume_txt_edited/"):

	files = [f for f in listdir(src_dir) if isfile(join(src_dir, f))]
	for i in range(len(files)):
		resume_to_write = strip_personal_info(src_dir+files[i])
		f1 = open(dst_dir+files[i], 'w+')
		f1.write(resume_to_write)
		f1.close()


"""
Aggregates most popular names into a set 'names'.
"""
def form_name_set(src_dir="../names/"):
	names = set()
	files = [f for f in listdir(src_dir) if isfile(join(src_dir, f))][1:]
	for i in range(len(files)):
		f = open(src_dir+files[i], 'r')
		for line in f:
			words = line.split(',')
			names.add(words[0])

"""
From txt files of resume, strip off the lines that contain 
"name", "address", "phone number", "email" information.
"""
def strip_personal_info(file_dir, lines_considered=7):
	txt_file = open(file_dir, 'r+')
	txt_to_return = ""
	line_num = 0
	personal_line = 0
	for line in txt_file:
		if line_num >= lines_considered:
			break
		line_num += 1
		words = line.split(' ')
		for word in words:		
			if re.match(REGEX_TEL, word, re.M|re.I) or \
			   re.match(REGEX_EMAIL, word, re.M|re.I):
				personal_line = line_num
				break
	txt_file.close()

	txt_file = open(file_dir, 'r+')
	line_num = 0
	for line in txt_file:
		line_num += 1
		if line_num <= personal_line:
			continue
		txt_to_return += line

	txt_file.close()
	return txt_to_return

def main(argv):
	print "This program receives 3 parameters:"
	print "1. PDF Resume source directory path"
	print "2. A path where a user want to store Resumes in .txt files"
	print "3. A path where a user want to store Resumes in .txt files without personal information."
	if len(argv) != 3:
		form_name_set()
		pdf_to_text()
		txt_to_no_personal()
	else:
		form_name_set()
		pdf_to_text(argv[0], argv[1])
		txt_to_no_personal(argv[1], argv[2])

if __name__ == "__main__":
	main(sys.argv[1:])