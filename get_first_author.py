# show how to use Python to fetch author data from webpage 
# fetch all of the first author of professors, from google scholar page 
# the first author list only contains unique author (duplicates get removed, and sorted)
# run with Python 3
# dependency: BeautifulSoup, requests 

from bs4 import BeautifulSoup

import requests

def get_first_authors_list(url):

	soup = BeautifulSoup(requests.get(url).text, 'html.parser')

	#print(soup.prettify())

	all_author = []
	index = 0 

	for hit in soup.findAll(attrs={'class' : 'gs_gray'}):
		if index%2==0:
			all_author.append(str(hit.contents))
		index=index+1

	first_author = []

	for entry in all_author:
		cut_pos = entry.find(",")
		entry = entry[2:cut_pos];
		if entry != '' and entry[-1]!="'":
			first_author.append(entry)

	first_author = list(set(first_author))

	first_author.sort();

	title = str(soup.title)

	prof = title[7:title.find("- Google")]

	write_file_helper("Professor: " + prof)
	write_file_helper("Found "+ str(len(first_author)) + " first author students")

	for author in first_author:
		write_file_helper(author)

	write_file_helper("--------------------")


def get_prof_url_list_on_one_page(url):

	soup = BeautifulSoup(requests.get(url).text, 'html.parser')

	prof_url_list = []

	for a in soup.find_all('a', href=True):
		entry = str(a['href'])
		if entry.find("/citations?user=")!=-1:
			prof_url_list.append("https://scholar.google.ca"+entry)

	return list(set(prof_url_list))


def get_first_authors_from_all_prof_on_one_page(url):
	prof_list = get_prof_url_list_on_one_page(url)
	for prof in prof_list:
		get_first_authors_list(prof)

def write_file_helper(s):
	file = open('author_list.txt', 'a')
	file.write(s+"\n")
	file.close()


## unit test:  get_first_authors_list

# url=[]
# url.append("http://scholar.google.ca/citations?user=nelvBCQAAAAJ&hl=en&oi=ao")
# url.append("https://scholar.google.ca/citations?user=5HX--AYAAAAJ&hl=en")
# url.append("https://scholar.google.ca/citations?user=P4nfoKYAAAAJ&hl=en")

# for entry in url:
# 	get_first_authors_list(entry)


## unit test:  get_prof_url_list_on_one_page

url = "https://scholar.google.ca/citations?view_op=search_authors&hl=en&mauthors=label:neuroscience&before_author=_evs_zMhAQAJ&astart=0"

# result = get_prof_url_list_on_one_page(url)

# for entry in result:
# 	print(entry)

get_first_authors_from_all_prof_on_one_page(url)
