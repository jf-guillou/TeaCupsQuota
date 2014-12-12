import urllib
import urllib2
import os
import sys
import subprocess
import netsnmp
import json
import printconfig
returncode = 0

params = {
	"user": os.getenv("TEAUSERNAME"),
	#"pagecount": 0
}
f = open("quota.log", "a")
f.write("printCheckQuota.py\n")

pageCounter = subprocess.Popen(["/usr/local/bin/pkpgcounter", os.getenv("TEADATAFILE")], stdout=subprocess.PIPE)
params["pagecount"] = int(pageCounter.stdout.read().strip()) * int(os.getenv("TEACOPIES"))

f.write("Build url\n")
url = printconfig.checkBaseUrl + "?" + urllib.urlencode(params)

res = json.loads(urllib2.urlopen(url).read())

if res['status'] == "error" or (res['status'] == "success" and not res['data']['can_print']) :
	returncode = -1

f.write(url + "\n")
f.write(json.dumps(res) + "\n")

if returncode == 0 :
	printedcount = netsnmp.snmpget(".1.3.6.1.2.1.43.10.2.1.4.1.1", Version=1, DestHost=os.getenv("TEAPRINTERADDR"), Community="public")[0]
	f.write("Printedcount : " + printedcount + "\n")
	print printedcount

f.write("\n")
f.close()

sys.exit(returncode)