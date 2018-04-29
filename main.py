# Imports
import csv
import sys
import psycopg2
import os
import sys

# Custom Classes
execfile( os.getcwd() + "/instagram.py"  )
# execfile( os.getcwd() + "/national_park.py"  )
# execfile( os.getcwd() + "/park_urls.py"  )
def check_parameters():
    for arg in sys.argv:
        if arg == "csv":
            csv = True
        elif "park" in arg:
            search_park = arg.split(":")[-1]
            if search_park[0] == ' ':
                search_park = search_park[1:]

if __name__ == "__main__":
    check_parameters()
    instagram = Instagram()
    instagram.login()
