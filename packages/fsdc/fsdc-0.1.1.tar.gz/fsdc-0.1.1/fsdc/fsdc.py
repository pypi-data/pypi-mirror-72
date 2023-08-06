from filecmp import dircmp
import os
import argparse
import easygui
import pandas as pd
from pathlib import Path

def convert_bytes(num):
    #this function will convert bytes to MB.. GB.. etc
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return f'{num:.3f} {x}'
        num /= 1024.0

def file_size(file_path):
    #this function will return the file size
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)

def already_in_df(df, temp_df):

	length = len(df)
	for x in range (0, length):
		filename = df.at[x, 'Filename']
		size     = df.at[x, 'Size in Group A']
		path     = df.at[x, 'Path in Group A']

		if filename == temp_df.at[0, 'Filename'] and size == temp_df.at[0, 'Size in Group A'] and path == temp_df.at[0, 'Path in Group A']:
			return True

	return False

def not_unique(df, file):
	length = len(df)
	for x in range (0, length):
		filename = df.at[x, 'Filename']

		if filename == file:
			return True
	
	return False

def get_files(folder):

	df = pd.DataFrame(columns=['Filename', 'Path', 'Size'])
	for root, dirs, file in os.walk(folder):
		for x in file:
			size = file_size(os.path.join(root, x))
			temp_df = pd.DataFrame([[x, root, size]], columns=['Filename', 'Path', 'Size'])
			df = df.append(temp_df, ignore_index=True)

	return df

def get_unique_files(group_A, group_B):

	dfA = get_files(group_A)
	dfB = get_files(group_B)

	filesA = dfA['Filename']
	filesB = dfB['Filename']
	for x in filesA.values:
		for y in filesB.values:
			if x == y:
				dfA = dfA.drop(dfA[dfA.Filename == x].index)
				dfB = dfB.drop(dfB[dfB.Filename == y].index)

	return dfA, dfB






def main():

	df = pd.DataFrame(columns=['Filename', 'Identical', 'Path in Group A',
							   'Size in Group A','Path in Group B', 
							   'Size in Group B'])
	
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--no_gui", action="store_true", required=False,
					help="input from the terminal (default easygui)")
	ap.add_argument("-t", "--terminal_output", action="store_true", required=False,
					help="output in the terminal (default excel)")
	args = vars(ap.parse_args())
	
	no_gui = args['no_gui']
	t_output = args['terminal_output']
	
	if no_gui == False:
		group_A = easygui.diropenbox()
		print(group_A)
		group_B = easygui.diropenbox()
		print(group_B)
	
	else:
		group_A = input('Give the path of the first foldergroup: ')
		group_B = input('Give the path of the second foldergroup: ')
	
	for roota, dirsa, filesa in os.walk(group_A):
		for rootb, dirsb, filesb in os.walk(group_B):
			dc = dircmp(roota, rootb)
			if dc.same_files == []:
				pass
			else:
	
				if t_output == True:
					print('###################################')
					print('Same File found in : '+roota+' and '+rootb)
					print(dc.same_files)
				for f in dc.same_files:
					sizea = file_size(os.path.join(roota, f))
					sizeb = file_size(os.path.join(rootb, f))
					temp_df = pd.DataFrame([[f, 'yes', roota, sizea, rootb, sizeb]], columns=['Filename', 'Identical', 'Path in Group A', 
																					   'Size in Group A','Path in Group B', 
																					   'Size in Group B'])
					df = df.append(temp_df, ignore_index=True)

			if dc.common_files == []:
				pass
			else:

				if t_output == True:
					print('###################################')
					print('Same File found in : '+roota+' and '+rootb)
					print(dc.common_files)
				for f in dc.common_files:
					sizea = file_size(os.path.join(roota, f))
					sizeb = file_size(os.path.join(rootb, f))
					temp_df = pd.DataFrame([[f, 'no', roota, sizea, rootb, sizeb]], columns=['Filename', 'Identical', 'Path in Group A', 
																					   'Size in Group A','Path in Group B', 
																					   'Size in Group B'])
					if already_in_df(df, temp_df) == False:
						df = df.append(temp_df, ignore_index=True)

	


	#unique files
	a, b = get_unique_files(group_A, group_B)


	#output
	if no_gui == False:
			save_path = easygui.filesavebox(default="identical_files_from_")
	if no_gui == True:
			save_path = input('Enter the path where you want to save the file: ')
			save_name = input('How do you want to name that file: ')
			save path = save_path + save_name
			
	if t_output == False:

		with pd.ExcelWriter(save_path+'.xlsx') as writer:
			df.to_excel(writer, sheet_name='In both')
			a.to_excel(writer, sheet_name='Only in A')
			b.to_excel(writer, sheet_name='Only in B')