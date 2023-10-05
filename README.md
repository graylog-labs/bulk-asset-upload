# Disclaimer
This script is provided with no guarantees, warranties, or herbal teas. It was written in a hurry by someone with no professional Python coding experience. It worked in my very limited testing, but it might require tweaks or updates to work for you.

# Overview
Graylog 5.2 includes a new Asset Database plugin which allows you to define machine and user assets and correlate those assets with your incoming log data. At release, it supports entering assets manually or importing from either LDAP or Active Directory. However, many people who don't have an LDAP or AD server do have way more machines than they care to enter manually. So I built this script to import machine assets in bulk from a .csv file.

# Instructions
The most important thing to mention is that the script expects your .csv file to be organized exactly like the provided `sample_machine_upload.csv` and `sample_user_upload.csv` files. If the data is not in the expected columns, the script will not work.

I highly recommend you use `sample_machine_upload.csv` or `sample_user_upload.csv` as a starting point. Load it up in your favorite spreadsheet program, delete the non-header rows, and fill in with your own data.

## python3 upload-assets.py -h
```
usage: upload-assets.py [-h] (--user | --machine) [--https] [-s SERVER] [-p PORT] -k APIKEY -f FILE [--noheader]

Bulk import assets from a .csv file to Graylog Security

optional arguments:
  -h, --help            show this help message and exit
  --user                Upload user assets
  --machine             Upload machine assets
  --https               Use https (as opposed to http)
  -s SERVER, --server SERVER
                        The host where Graylog is running (default to localhost)
  -p PORT, --port PORT  The port Graylog is listening on (default to 9000 for HTTP, not used for HTTPS)
  -k APIKEY, --apikey APIKEY
                        The API key for accessing the Graylog API
  -f FILE, --file FILE  The .csv file to read data from
  --noheader            The .csv file has no column headers, there is data in the first row
```