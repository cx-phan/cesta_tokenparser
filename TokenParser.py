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
		f.write("Entry: %s \t Word: %s\t Type: %s \n" % (line[0], line[1], line[2]))
	f.close()

	f_n = open("name_test.tsv", "w+")
	f_n.write("Entry \t Word \t ID \n")
	for line in name_array: 
		f_n.write("%s \t %s \t %s \n" % (line[0], line[1], line[2]))
	f_n.close()

def setCorrectID(name_array, file_lines): 
	# same data in these two arrays, but formatted differently
	temp_id_list = {}
	name_list = {}

	f_n = open("debug_two.txt", "w+")
	for line in file_lines: 
		main_name_regex = '([A-Z]{3,}(,( [A-Z]+)+)?)'
		matches = re.findall(main_name_regex, line[1])
		if not matches:
			continue

		 #if this match exists 
		raw_name = matches[0][0].lower()
		first_last_name = raw_name.split(", ")
		name = raw_name # create the name 

		if len(first_last_name) > 1: 
			name = first_last_name[1] + " " + first_last_name[0]

		id_tup = (line[0], name) # ID, followed by name
		temp_id_list[int(line[0])] = id_tup
		name_list[name] = line[0]
		f_n.write("%s \t %s \t %s \n" % (raw_name, name, line[0]))


	# id reference lookup is the table of direct names IDs to their paragraph usages 
	id_reference_lookup = define_main_names(name_array, temp_id_list)
	name_array, temp_id_list = remove_names (name_array, temp_id_list)
	name_array = look_for_name(name_array, temp_id_list, id_reference_lookup)

	return look_for_name_2(name_array, name_list)

def define_main_names (name_array, temp_id_list): 
	id_reference = {}
	copy_of_temp_id_list = temp_id_list
	
	f_n = open("debug.txt", "w+")
	previous_index = int(name_array[0][0])

	for i, name in enumerate(name_array): 
		main_index = int(name[0])


		if name[1].lower() in copy_of_temp_id_list[main_index][1]: 
			if name[2] == '-1' or id_reference.has_key(name[2]):
				continue
			id_reference[name[2]] = (name[1], copy_of_temp_id_list[main_index][0])
			f_n.write("%s \t %s \t %s \n" % (name[2], name[1], copy_of_temp_id_list[main_index][0]))



	return id_reference

def remove_names (name_array, temp_id_list): 
	j = 0

	for i in xrange(0, len(temp_id_list)):
		paragraph_index = int(name_array[j][0])
		
		while (paragraph_index == i): 
			name = name_array[j] # easier declaration 

			# here, iterate through name list 
			if name[1].lower() in temp_id_list[paragraph_index][1]: 
				del name_array[j]
			else: 
				j = j + 1

			paragraph_index = int(name_array[j][0])

	return name_array, temp_id_list

# first iteration of looking through names based on ID 
def look_for_name(name_array, temp_id_list, id_reference_lookup): 
	updated_name_array = []

	for i, name in enumerate(name_array): 
		main_ID = name[2]

		if not id_reference_lookup.has_key(main_ID):
			updated_name_array.append((name[0], name[1], '-1'))
			continue

		tup2 = (name[0], name[1], id_reference_lookup[main_ID][1])
		updated_name_array.append(tup2)
	
	return updated_name_array

def look_for_name_2(name_array, name_list): 

	# test case
	array = {'hugh leycester':1, 'oswald leycester': 2948} 
	string = 'hugh leycester'
	
	print 'oswald leycester' in name_list

	print string in array
	updated_name_array = []
	for i, name in enumerate(name_array): 
		if name[2] != '-1': 
			updated_name_array.append(name)
			continue

		list_of_names = createNames(name)

		for name_i in list_of_names:
			if name_i.lower() in name_list:
				print name_i
				updated_name_array.append((name[0], name[1], name_list[name_i.lower()]))
				continue

	return updated_name_array
		

def createNames (name): 
	if len(name) == 1:
		return name[1]
	list_of_names = [name[1]]
	return list_of_names


def main(): 
	path = 'book-nlp-master/data/tokens/narratives.tokens'
	path2 = 'dataset.tsv'

	f_tokens = open(path)
	f_lines = open(path2)


	file_tokens = []
	file_lines = []
	
	# convert file types to array
	for line in f_lines:
		line_array = line.split("\t")
		file_lines.append(line_array)

	for entry in f_tokens:
		file_tokens.append(entry.split())


	## iterate through file lines, too! 
	current_narrative_index = -1 

	location_array = []
	name_array = []

	previously_seen_names_index = -1

	for i in xrange(3, len(file_tokens)):
		if previously_seen_names_index >= i: 
			continue


		line_array = file_tokens[i]

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


	updated_name_array = setCorrectID(name_array, file_lines)	
	writeToDoc(location_array, updated_name_array)


if __name__ == "__main__":
    main()