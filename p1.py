import os
import requests

def do_ping():
  os.system('fping -e -a -r 0 <hosts.txt >output.txt')

def load_hosts():
  global hosts
  hosts = set()
  f = open('hosts.txt')
  for line in f:
    hosts.add(line.strip())

load_hosts()

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
  do_ping()
  parse_output()
  global output
  print(output)
  for k in output:
    v = output[k]
    # requests.get(
    url = 'http://ping-store.herokuapp.com/pings-post?origin=A8&target=%s&success=%s&rtt=%s' % (k, 'false' if v is None else 'true', v)
    print(url)
    requests.get(url)


