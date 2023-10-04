# Disclaimer
This script is provided with no guarantees, warantees, or herbal teas. It was written in a hurry by someone with no professional Python coding experience. It worked in my very limited testing, but it might require tweaks or updates to work for you.

**Note**: The script currently only supports uploading machine assets. User asset upload may come in the future.

# Overview
Graylog 5.2 includes a new Asset Database plugin which allows you to define machine and user assets and correlate those assets with your incoming log data. At release, it supports entering assets manually or importing from either LDAP or Active Directory. However, many people who don't have an LDAP or AD server do have way more machines than they care to enter manually. So I built this script to import machine assets in bulk from a .csv file.

# Instructions
The most important thing to mention is that the script expects your .csv file to be organized exactly like the provided `sample_machine_upload.csv` file. The first column must be the machine name. The second column must be the description. And so on out to the 15th column for time zone.

I highly recommend you use `sample_machine_upload.csv` as a starting point. Load it up in your favorite spreadsheet program, delete rows 2-6, and fill in with your own data.

## python3 upload-assets.py -h
```
usage: upload-assets.py [-h] [--https] [-s SERVER] [-p PORT] -k APIKEY -f FILE [--noheader]

Bulk import assets from a .csv file to Graylog Security

optional arguments:
  -h, --help            show this help message and exit
  --https               Use https (as opposed to http)
  -s SERVER, --server SERVER
                        The host where Graylog is running (default to localhost)
  -p PORT, --port PORT  The port Graylog is listening on (default to 9000)
  -k APIKEY, --apikey APIKEY
                        The API key for accessing the Graylog API
  -f FILE, --file FILE  The .csv file to read data from
  --noheader            The .csv file has column headers per the documentation
```


