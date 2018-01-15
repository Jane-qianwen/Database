######Jane(Zhuqianwen)'s hw1 for database
######object: parse the ebooks file to create four csv files
import csv
import sys
from sys import argv
import re

#read the input txt file
input_ebooks = open(argv[1],'r')
dict_for_tokens = {} #create a dictionary to store tokens and their counts

def create_ebook_csv(txtfile) :
	ebook_csvfile = file('ebook.csv','wb')#in write mode, create ebook.csv if there doesn't exixst
	tokens_csvfile = file('tokens.csv','wb')#in write mode, create tokens.csv if there doesn't exixst
	writer = csv.writer(ebook_csvfile,lineterminator='\r\n')
	writer.writerow(['title','author','release_date','ebook_id','language','body']) #the first row of the ebook.csv
	#writer = csv.writer(tokens_csvfile,lineterminator='\r\n')
	#writer.writerow(['ebook_id','token'])  #the first row of the tokens.csv
	writer_token = csv.writer(tokens_csvfile,lineterminator='\r\n')
	writer_token.writerow(['ebook_id','token'])  #the first row of the tokens.csv
	title=author=release_date=ebook_id=language=body = ''
	start_body = 0; # =1 means find the start of the book body, so that we can store the content of the whole body
	#strat to traverse the txtfile line by lline
	for line in txtfile.readlines() :
		if start_body == 0 and 'Title: ' in line:
			line = line.strip()#strip the default CRLF
			title = line.replace('Title: ','')
			title = title.strip()
		elif start_body == 0 and 'Author: ' in line:
			line = line.strip()#strip the default CRLF
			author = line.replace('Author: ','')
			author = author.strip()
		elif start_body == 0 and 'Release Date: ' in line:
			line = line.strip()#strip the default CRLF
			release_tmp = line.replace('Release Date: ','')
			release_date = release_tmp[0:release_tmp.find("[")]
			release_date = release_date.strip()
			#print (release_date)
			ebook_id = release_tmp[release_tmp.find("#")+1:release_tmp.find("]")]
			ebook_id = ebook_id.strip()
			#print (ebook_id)
		elif start_body == 0 and 'Language: ' in line:
			line = line.strip()#strip the default CRLF
			language = line.replace('Language: ','')
			language = language.strip()
		elif start_body == 0 and '*** START OF THE PROJECT GUTENBERG' in line : # find the start of the body
			start_body = 1 #now we can store the content of the body until we find the end
			ebook_body = ""#create a string to store the body of this ebook
		elif start_body == 1:
			if '*** END OF THE PROJECT GUTENBERG' in line:
				body = ebook_body
				if title == '':
					title = 'null'
				if author =='':
					author = 'null'
				if release_date =='' : 
					release_date = 'null'
				if ebook_id == '':
					ebook_id = 'null'
				if language == '':
					language = 'null'
				if body =='':
					body = 'null'
				#ebooks_information = [title,author,release_date,ebook_id,language,body] #to store the information of the eooks and finally write ebooks_information into the ebook.csv
				writer.writerow([title,author,release_date,ebook_id,language,body])########################
				create_tokens_csv(ebook_id,body,tokens_csvfile,dict_for_tokens)
				start_body = 0
				title=author=release_date=ebook_id=language=body = ''
			else :
				ebook_body = ebook_body + line
	ebook_csvfile.close()
	tokens_csvfile.close()

def create_tokens_csv(ebook_id,body,tokens_csvfile,dict_for_tokens):
	#split the input txt by the non-alphabetical characters
	body = body.strip()
	body = body.lower()
	tokens_of_body = re.split('[^a-zA-Z]',body)
	#tokens_of_body = split_body.lower() #lowercase of tokens
	#create a dictionary for all the tokens
	writer = csv.writer(tokens_csvfile,lineterminator='\r\n')
	#writer.writerow(['ebook_id','token'])  #the first row of the tokens.csv
	for token in tokens_of_body:
		if token=='':
			continue
		else:
			dict_for_tokens[token] = dict_for_tokens.get(token,0) + 1;#if the token exists in the dict , then it's value +1, or it's value=1
			writer.writerow([ebook_id,token])

def create_token_counts_csv(dict_for_tokens):
	token_counts_csvfile = file('token_counts.csv','wb')#in write mode, create token_counts.csv if there doesn't exixst
	writer = csv.writer(token_counts_csvfile,lineterminator='\r\n')
	writer.writerow(['token','count']) #the first row of the token_counts.csv
	for token in dict_for_tokens.keys():
		writer.writerow([token,dict_for_tokens[token]])
	token_counts_csvfile.close()

def create_name_counts_csv(popular_names,token_counts_csvfile):
	name_counts_csvfile = file('name_counts.csv','wb')#in write mode, create name_counts.csv if there doesn't exixst
	writer = csv.writer(name_counts_csvfile,lineterminator='\r\n')
	writer.writerow(['token','count'])
	#read the popular_names.txt
	names = open(popular_names,'r')
	#convert the names into a name list, split by non-alpha characters
	name_list = names.read()#read all the content of the namelist
	name_list = name_list.lower()#lower all the popular names
	name_list = re.split('[^a-z^A-Z]',name_list)
	#traverse the token_counts_csvfile
	token_counts = open(token_counts_csvfile)
	reader = csv.reader(token_counts)
	for line in reader:
		if line[0] in name_list:
			writer.writerow([line[0],line[1]])
	token_counts.close()
	name_counts_csvfile.close()
	names.close()
#the main function
create_ebook_csv(input_ebooks)
create_token_counts_csv(dict_for_tokens)
create_name_counts_csv('popular_names.txt','token_counts.csv')
input_ebooks.close()
exit(0)
