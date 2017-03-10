import sys
import getopt
import os
import math
import operator
import re 

file_lines = [] 

def writeToDoc(location_array, name_array):
	
	f = open("location_test.txt","w+")
	for line in location_array: 
		f.write("Entry: %s, Word: %s, Type: %s \n" % (line[0], line[1], line[2]))
	f.close()

	f_n = open("name_test.txt", "w+")
	for line in name_array: 
		f_n.write("Entry: %s, Word: %s, ID: %s \n" % (line[0], line[1], line[2]))
	f_n.close()

def setCorrectID(name_array, file_lines): 
	id_reference = {} 
	temp_id_list = []
	for line in file_lines: 
		main_name_regex = '([A-Z]{3,}(,( [A-Z]+)+)?)'
		matches = re.findall(main_name_regex, line[1])
		if not matches:
			# print matches, line[0]
			continue

		if matches:
			# print matches[0]
			id_tup = (line[0], matches[0][0].lower()) # ID, followed by name
			temp_id_list.append(id_tup)
			#print id_tup

	for name in name_array:
		id_number = name[2]
		# access ID number, name 
		if id_number in id_reference:
			name[2] = id_reference[id_number][1]
		else:
			# look for name 
			# id_number = look_for_name(name, temp_id_list)
			#id_reference[id_number] = 
			# print look_for_name(name, temp_id_list)
			#id_reference[id_number] = look_for_name(name, temp_id_list)
			# print id_reference[id_number]
			# id_reference[name[2]] =
			#print name[1].lower()
			# find the appropriate name here 
			#print name

def look_for_name(name, temp_id_list): 
	main_index = int(name[0])
	# print temp_id_list[main_index][1], ", ", name[1].lower()
	if name[1].lower() in temp_id_list[main_index][1]:
		print temp_id_list[main_index][1], ", ", name[1].lower()
		return temp_id_list[main_index]

	
	#for id_value in temp_id_list:





def main(): 
	path = 'book-nlp-master/data/tokens/narratives.tokens'
	path2 = 'dataset.tsv'

	f_tokens = open(path)
	f_lines = open(path2)


	file_tokens = []
	#file_lines = []
	
	# convert file types to array
	for line in f_lines:
		line_array = line.split("\t")
		file_lines.append(line_array)

	for entry in f_tokens:
		file_tokens.append(entry.split())

	# begin sorting ++ appending here 

	## iterate through file lines, too! 
	current_narrative_index = -1 

	location_array = []
	name_array = []

	previously_seen_names_index = -1

	for i in xrange(3, len(file_tokens)):
		if previously_seen_names_index >= i: 
			continue


		line_array = file_tokens[i]
		# print line_array[7], line_array[11]

		if line_array[11] == 'LOCATION' or line_array[11] == 'PERSON':
			while current_narrative_index < len(file_lines) and line_array[7] not in file_lines[current_narrative_index][3]:
				#print file_lines[current_narrative_index][3], line_array[7]
				current_narrative_index = current_narrative_index + 1
				#print current_narrative_index, line_array[7]

		if line_array[11] == 'LOCATION' or line_array[10] == 'LOCATION':
			loc_tup = (current_narrative_index + 1, line_array[7], 'LOCATION')
			location_array.append(loc_tup)

		elif line_array[11] == 'PERSON' or line_array[10] == 'PERSON':
			full_name = line_array[7]
			characterID = line_array[len(line_array)-1] # last index is character ID, extract here
			while file_tokens[i + 1][11] == 'PERSON' or file_tokens[i + 1][10] == 'PERSON':
				full_name = full_name + ' ' + file_tokens[i + 1][7]
				i = i + 1
				previously_seen_names_index = i 

			name_tup = (file_lines[current_narrative_index][0], full_name, characterID)
			name_array.append(name_tup)


	setCorrectID(name_array, file_lines)	
	writeToDoc(location_array, name_array)






if __name__ == "__main__":
    main()