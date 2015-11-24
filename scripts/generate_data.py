#!/usr/bin/python

import csv
import sys
from tools import companies, replacement

""" use this to write an array as a csv compatible with gephi """
def writearray(a, filename):
	with open(filename,'w+') as f:
		w = csv.writer(f, dialect='excel-tab')
		w.writerows(a)

def construct_nodes(csv_object):
	count = dict_count_author_mail(csv_object)
	a = [['Id', 'Author', 'Company', 'Weight']]
	authors_done = []
	index = 1
	nr = len(count)
	for author in count:
		print(str(index*100/nr)+"%("+str(index)+"/"+str(nr)+")", end="\r")
		index += 1
		company = ""
		try:
			new_author = replacement[author]
		except KeyError:
			new_author = author
		try:
			company = companies[new_author]
		except KeyError:
			pass

		if new_author not in authors_done:
			a.append([index, new_author, company, count[new_author]])
			authors_done.append(new_author)

	print("")
	return a

def construct_edges(csv_object, ids):
	print("Constructing exchanges dictionnary")
	d = dict_exchanges(csv_object)
	a = [['Source', 'Target', 'Weight']]

	print("Formatting exchanges array")
	index = 1
	nr = len(d)
	for exchange in d:
		print(str(index*100/nr)+"%("+str(index)+"/"+str(nr)+")", end="\r")
		index += 1
		new_exchange = exchange
		try:
			new_exchange[0] = replacement[new_exchange[0]]
		except KeyError:
			pass
		try:
			new_exchange[1] = replacement[new_exchange[1]]
		except KeyError:
			pass
		author1 = ids[new_exchange[0]]
		author2 = ids[new_exchange[1]]
		count = d[new_exchange]
		a.append([author1, author2, count])
	print("")
	return a

""" construct dict of author => id from nodes """
def dict_authors_id(nodes):
	d = {}
	index = 1
	nr = len(nodes)
	for n in nodes:
		print(str(index*100/nr)+"%("+str(index)+"/"+str(nr)+")", end="\r")
		index += 1
		d[n[1]] = n[0]
	print("")
	return d

""" use this to count the number of mail per author """
def dict_count_author_mail(csv_object):
	d = {}
	for row in csv_object:
		author = row['Author']
		try:
			author = replacement[author]
		except KeyError:
			pass
		if author not in d.keys():
			d[author] = 0
		d[author] += 1
	return d

""" constructs dict subject => list of authors """
def dict_author_per_subject(csv_object):
	d = {}
	index = 1
	nr = len(csv_object)
	for row in csv_object:
		print(str(index*100/nr)+"%("+str(index)+"/"+str(nr)+")", end="\r")
		index += 1
		subject = row['Subject']
		author = row['Author']
		try:
			author = replacement[author]
		except KeyError:
			pass
		if subject not in d.keys():
			d[subject] = []
		if author not in d[subject]:
			d[subject].append(author)
	print("")
	return d

""" constructs dict (author1, author2) => nbr_of_mails """
def dict_exchanges(csv_object):
	print("Constructing authors per subject dictionnary")
	d = dict_author_per_subject(csv_object)
	exchanges = {}
	index = 1
	nr = len(d)
	print("Constructing exchanges dictionnary")
	for authors in d.values():
		print(str(index*100/nr)+"%("+str(index)+"/"+str(nr)+")", end="\r")
		index += 1
		authors.sort()
		for i in range(0, len(authors)):
			author1 = authors[i]
			for j in range(i+1, len(authors)):
				author2 = authors[j]
				couple = (author1, author2)
				if couple not in exchanges.keys():
					exchanges[couple] = 0
				exchanges[couple] += 1
	print("")
	return exchanges

def get_csv_raw(inputfilename):
	fieldnames = ['Date', 'New', 'Subject', 'Author']
	return get_csv(inputfilename, fieldnames)

""" opens a csv """
def get_csv(inputfilename, fieldnames):
	csv.register_dialect('inputcsvdialect', delimiter=',', quoting=csv.QUOTE_ALL, quotechar="'")
	inputfile = open(inputfilename, 'r', newline='')
	reader = csv.DictReader(inputfile, fieldnames=fieldnames, dialect='inputcsvdialect')
	l = []
	for row in reader:
		l.append(dict(row))
	return l

if __name__ == '__main__':
	inputfilename = None
	outputfilename = None
	data = None
	e = n = None
	if len(sys.argv) <= 1:
		print("Utilisation : ")
		print(sys.argv[0]+" mails.csv output_filename")

	if len(sys.argv) >= 2:
		inputfilename = sys.argv[1]
		print("Parsing CSV")
		data = get_csv_raw(inputfilename)
		print("Constructing nodes")
		n = construct_nodes(data)
		print("Constructing ID dictonnary")
		ids = dict_authors_id(n)
		print("Constructing edges")
		e = construct_edges(data, ids)

	if len(sys.argv) >= 3:
		outputfilename = sys.argv[2]
		writearray(n, outputfilename+'-nodes.csv')
		writearray(e, outputfilename+'-edges.csv')
	
