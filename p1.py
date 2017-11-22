import os
import requests
import datetime

def do_ping():
  os.system('fping -e -a -r 0 <hosts.txt >output.txt')

def load_hosts():
  global hosts
  hosts = set()
  f = open('hosts.txt')
  for line in f:
    hosts.add(line.strip())

def parse_output():
  global output
  output = {}
  global hosts
  output = { k:None for k in hosts }
  f = open('output.txt')
  for line in f:
    terms = line.strip().split()
    host = terms[0]
    time = terms[1][1:]
    output[host] = time

def full():
  time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
  do_ping()
  parse_output()
  global output
  print(output)
  for k in output:
    v = output[k]
    url = os.getenv('STORE_URL')
    print('url:', url)
    success = 'false' if v is None else 'true'
    payload = '{"origin":"raspi2a", "target":"%s", "success":"%s", "rtt":"%s", "time":"%s"}' % (k, success, v, time)
    # print('payload:', payload)
    h = {'Content-type': 'application/json'}
    r = requests.post(url, data=payload, headers=h)
    print(r, r.text)


load_hosts()
full()
print('done!')

