import urllib
import urllib2
import os
import sys
import subprocess
import netsnmp
import hashlib
import printconfig

params = {
	"id": os.getenv("TEAJOBID"),
	"user": os.getenv("TEAUSERNAME"),
	"printer": os.getenv("TEAPRINTERNAME"),
	"doc": os.getenv("TEATITLE")
	#"printedcount": 0
}

f = open("quota.log", "a")
f.write("printSetLog.py\n")

printStatus = os.getenv("TEASTATUS")
f.write("PrintStatus : " + printStatus + "\n")
if int(printStatus) == 0:
	printedcount = netsnmp.snmpget(".1.3.6.1.2.1.43.10.2.1.4.1.1", Version=1, DestHost=os.getenv("TEAPRINTERADDR"), Community="public")[0]
	f.write("Printedcount : " + printedcount + "\n")

	printedCountBefore = sys.stdin.read().strip()

	params["printedcount"] = int(printedcount) - int(printedCountBefore)

	chkSum = hashlib.md5()
	chkSum.update(params["id"])
	chkSum.update(params["user"])
	chkSum.update(str(params["printedcount"]))
	chkSum.update(printconfig.checksumSalt)
	params["chk"] = chkSum.hexdigest()[1:7]

	url = printconfig.setBaseUrl + "?" + urllib.urlencode(params)
	f.write(url + "\n")

	res = urllib2.urlopen(url)

f.write("\n")
f.close

sys.exit(0)