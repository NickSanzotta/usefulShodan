#!/usr/bin/env python3
# Version: usefulShodan.py v 2.04192021

import os
import sys
import getopt
import xlsxwriter
import time
from sys import argv
from netaddr import IPNetwork
timestr = time.strftime("%Y%m%d-%H%M")
curr_time = time.time()

class colors:
   white = "\033[1;37m"
   normal = "\033[0;00m"
   red = "\033[1;31m"
   blue = "\033[1;34m"
   green = "\033[1;32m"

banner = colors.green + r"""
                          ___          ___      
                        /'___\        /\_ \     
 __  __    ____     __ /\ \__/  __  __\//\ \    
/\ \/\ \  /',__\  /'__`\ \ ,__\/\ \/\ \ \ \ \   
\ \ \_\ \/\__, `\/\  __/\ \ \_/\ \ \_\ \ \_\ \_ 
 \ \____/\/\____/\ \____\\ \_\  \ \____/ /\____\
  \/___/  \/___/  \/____/ \/_/   \/___/  \/____/
 ____    __                  __                      
/\  _`\ /\ \                /\ \                     
\ \,\L\_\ \ \___     ___    \_\ \     __      ___    
 \/_\__ \\ \  _ `\  / __`\  /'_` \  /'__`\  /' _ `\  
   /\ \L\ \ \ \ \ \/\ \L\ \/\ \L\ \/\ \L\.\_/\ \/\ \ 
   \ `\____\ \_\ \_\ \____/\ \___,_\ \__/.\_\ \_\ \_\
    \/_____/\/_/\/_/\/___/  \/__,_ /\/__/\/_/\/_/\/_/

"""+'\n' \
+ colors.green + '\n usefulShodan.py v1.05162017' \
+ colors.normal + '\n Description: Parses Shodan data from a list of IP addresses and saves output to an XLSX file..'\
+ colors.normal + '\n Created by: Nick Sanzotta/@beamr' + '\n'\
+ colors.normal + ' ' + '*' * 95 +'\n' + colors.normal

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def usefulShodan(inputfile):
	savedTo = 'usefulShodan-data/shodan'+'_'+timestr+'.xlsx'
	# Create a workbook and add a worksheet.
	workbook = xlsxwriter.Workbook(savedTo)
	worksheet = workbook.add_worksheet()
	# Add a bold format to use to highlight cells.
	bold = workbook.add_format({'bold': True})
	# Write some data headers.
	worksheet.write('A1', 'Ports - SSL Versions:', bold)
	worksheet.write('B1', 'IP Addresses:', bold)
	# Start from the first cell. Rows and columns are zero indexed.
	row = 1
	col = 0
	#Import IP Addresses from file
	with open(inputfile, 'rb') as f1:
		scopeList = f1.read().splitlines()
		print("\n")
		for x in scopeList[::]:
			for ip in IPNetwork(x):
				# DEBUG print(ip)
				with open('scope.txt', 'ab+') as f2:
					f2.write(str(ip)+"\n")


	with open('scope.txt', 'rb') as f2:
		output1 = f2.read().splitlines()

	for host in output1:
		shodan = os.system('shodan host ' + host + '> /tmp/shodan.txt')
		time.sleep(1)
		with open('/tmp/shodan.txt', 'rb') as f3:
				output2 = f3.read()
		try:
			shodanList = output2.splitlines()
			ipaddress  = shodanList[0]
			servicesListening = shodanList[7::]
			servicesListening = [x.strip(' ') for x in servicesListening] #Removes white spaces for each item in list
			print(ipaddress)
			for item in servicesListening:
				item = item.replace('|-- ', '')
				print(item.strip())
				worksheet.write(row, col,     item.strip())
				worksheet.write(row, col + 1, ipaddress)
				row += 1
			print("\n")
		except IndexError:
			print("\n")
	workbook.close()
	print('Excel file saved to: ' + savedTo)



def help():
	cls()
	print(banner)
	print(" Usage: ./usefulShodan.py <OPTIONS> \n")
	print(" Example: ./usefulShodan.py -i /client/scope.txt\n")
	print(" Supports Single IP Address and CIDR format.\n")
	print(" Input file example:\n")
	print("\t root@beamr:~# more /scope.txt") 
	print("\t 210.11.101.0/25")
	print("\t 216.11.101.0/28")
	print("\t 10.10.10.10")
	print("\t 20.20.20.20\n")
	print(" Parsed data is saved in an XLSX format. (Filter and sort data for desired results.)")
	print(" Output path: shodan/shodan-data/shodan_timestamp.xlsx \n")
	print("\t -i <input>\t\tInputs file containing a list of IP addresses.")
	print("\t -h <help>\t\tPrints this help menu.")
	print(
		"""\nInstallation:
		usefulShodan.py requires the Shodan Command-Line Interface (CLI). 
		To install Shodan CLI execute: easy_install shodan
	
		To upgrade Shodan CLI: easy_install -U shodan
	
		Shodan CLI supports both free and paid API Keys.
		Initialize the environment with your API key using shodan init: shodan init YOUR_API_KEY""")
	sys.exit(2)
    
def main(argv):
    if len(argv) < 1:
        help()
    try:
        opts, args = getopt.getopt(argv, 'i:c:h',['input=','help'])
    except getopt.GetoptError:
        help()
        sys.exit(2)
    
    if not os.path.exists("usefulShodan-data/"):
        os.mkdir("usefulShodan-data/") 
    
    inputfile= ''

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            help()
            sys.exit(2)
        elif opt in ('-i', '--input'):
            inputfile = arg
        else:
            help()
            sys.exit(2)
    cls()
    usefulShodan(inputfile)

if __name__ == "__main__":
    main(argv[1:])
print("\nCompleted in: %.1fs\n" % (time.time() - curr_time))