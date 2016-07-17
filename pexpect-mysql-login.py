import pexpect
import sys
from pprint import pprint
username = ''
password = ''
finallist = []
iplistfile = ''
with open(iplistfile) as f:
  iplist = f.read().splitlines()

for ip in iplist:
    print 'trying ' + ip
    try: 
      child = pexpect.spawn("mysql -u {} -p -h {}".format(username,ip))
      child.expect('Enter password: ')
      child.sendline(password)
      i = child.expect(['mysql> ', '\n\nERROR'])
      if i==0:
        finallist.append(ip)
    except:
      pass
print "[!] list of IP's w/ successful login"
pprint(finallist)
