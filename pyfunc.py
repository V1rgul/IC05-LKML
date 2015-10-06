#!/usr/bin/python -i

import csv
import sys

""" use this to write an array as a csv compatible with gephi """
def writearray(a, filename):
	with open(filename,'w+') as f:
		w = csv.writer(f, dialect='excel-tab')
		w.writerows(a)

def construct_nodes(csv_object):
	count = dict_count_author_mail(csv_object)
	a = []
	index = 1
	for author in count:
		a.append([index, author, count[author]])
		index +=1
	return [['Id', 'Author', 'Count']]+a

""" construct dict of author => id from nodes """
def dict_authors_id(nodes):
	d = {}
	for n in nodes:
		d[n[1]] = n[0]

def construct_edges(csv_object):
	d = dict_exchanges(csv_object)
	a = ['Source', 'Target', 'Count']

""" use this to count the number of mail per author """
def dict_count_author_mail(csv_object):
	d = {}
	for row in csv_object:
		author = row['Author']
		if author not in d.keys():
			d[author] = 0
		d[author] += 1
	return d

""" constructs dict subject => list of authors """
def dict_author_per_subject(csv_object):
	d = {}
	for row in csv_object:
		subject = row['Subject']
		author = row['Author']
		if subject not in d.keys():
			d[subject] = []
		if author not in d[subject]:
			d[subject].append(author)
	return d

""" constructs dict (author1, author2) => nbr_of_mails """
def dict_exchanges(csv_object):
	d = dict_author_per_subject(csv_object)
	exchanges = {}
	for authors in d.values():
		authors.sort()
		for i in range(0, len(authors)):
			author1 = authors[i]
			for j in range(i+1, len(authors)):
				author2 = authors[j]
				couple = (author1, author2)
				if couple not in exchanges.keys():
					exchanges[couple] = 0
				exchanges[couple] += 1
	return exchanges

def get_csv_raw(inputfilename):
	fieldnames = ['Id', 'New', 'Subject', 'Author']
	return get_csv(inputfilename, fieldnames)

""" opens a csv """
def get_csv(inputfilename, fieldnames):
	csv.register_dialect('inputcsvdialect', delimiter=',', quoting=csv.QUOTE_ALL, quotechar="'")
	inputfile = open(inputfilename, 'r', newline='')
	reader = csv.DictReader(inputfile, fieldnames=fieldnames, dialect='inputcsvdialect')
	return reader

if __name__ == '__main__':
	inputfilename = None
	outputfilename = None
	data = None
	e = n = None
	if len(sys.argv) >= 2:
		inputfilename = sys.argv[1]
		data = get_csv_raw(inputfilename)
		n = construct_nodes(data)
		e = construct_edges(data)


	if len(sys.argv) >= 3:
		outputfilename = sys.argv[2]
		writearray(n, outputfilename+'-nodes.csv')
		writearray(e, outputfilename+'-edges.csv')
	
