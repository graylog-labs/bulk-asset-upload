import argparse
import csv
import json
import logging
import requests
from datetime import datetime, timezone
from logging.handlers import TimedRotatingFileHandler

handlers = set()
handlers.add(TimedRotatingFileHandler('asset-upload.log', when='W0', backupCount=4))
logging.basicConfig(level=logging.DEBUG, handlers=handlers, 
                    format='%(asctime)s %(levelname)s %(module)s:%(funcName)s %(message)s')
logging.Formatter.formatTime = (lambda self, record, datefmt=None: 
    datetime.fromtimestamp(record.created, timezone.utc).astimezone().isoformat(sep='T',timespec='milliseconds'))

def split_and_strip(input: str) -> list:
    return [x.strip() for x in input.split(',')]

def do_post(request_url: str, api_key: str, record: dict, request_headers: dict={}) -> dict:
    logging.debug(f'Invoking the API with API key {api_key}')
    endpoint = '/api/plugins/org.graylog.plugins.securityapp.asset/assets'
    try:
        result = requests.post(
            request_url + endpoint,
            headers = request_headers,
            auth = (api_key, 'token'),
            json = record
            )
    except requests.exceptions.RequestException as e:
        logging.critical('Error %s submitting API call', e)
        return

    if result.status_code != 200:
        logging.critical(
            'Unable to perform API call - error code %s',
            result.status_code
            )
        return

    logging.debug('API call successful')
    return result.json()

def build_record(csv_row:dict) -> dict:
    logging.debug(f'Building record for {csv_row[0]} with IPs [{csv_row[6]}] owned by {csv_row[2]}')
    record = {}
    record['name'] = csv_row[0]
    record['description'] = csv_row[1]
    record['category'] = split_and_strip(csv_row[7])
    record['priority'] = csv_row[3]
    record['details'] = {}
    record['details']['type'] = 'machine'
    record['details']['owner'] = csv_row[2]
    record['details']['hostnames'] = split_and_strip(csv_row[4])
    record['details']['mac_addresses'] = split_and_strip(csv_row[5])
    record['details']['ip_addresses'] = split_and_strip(csv_row[6])
    record['geo_info'] = {}
    record['geo_info']['city_name'] = csv_row[8]
    record['geo_info']['region'] = csv_row[9]
    record['geo_info']['country_name'] = csv_row[10]
    record['geo_info']['latitude'] = csv_row[11]
    record['geo_info']['longitude'] = csv_row[12]
    record['geo_info']['country_iso_code'] = csv_row[13]
    record['geo_info']['time_zone'] = csv_row[14]

    logging.debug(f'Generated record:\n {json.dumps(record, indent=2)}')

    return record

def main():
    logging.info('Starting machine asset upload')
    parser = argparse.ArgumentParser(description='Bulk import assets from a .csv file to Graylog Security')
    parser.add_argument('--https', action='store_true', help='Use https (as opposed to http)')
    parser.add_argument('-s', '--server', default='localhost', help='The host where Graylog is running (default to localhost)')
    parser.add_argument('-p', '--port', default='9000', help='The port Graylog is listening on (default to 9000)')
    parser.add_argument('-k', '--apikey', required=True, help='The API key for accessing the Graylog API')
    parser.add_argument('-f', '--file', required=True, help='The .csv file to read data from')
    parser.add_argument('--noheader', action='store_false', help='The .csv file has column headers per the documentation')

    logging.debug('Parsing command line args')
    parsed_args = parser.parse_args()

    request_url = ''
    if parsed_args.https:
        request_url = 'https://'
    else:
        request_url = 'http://'
    request_url += f'{parsed_args.server}:{parsed_args.port}'
    logging.debug(f'Request URL: {request_url}')

    logging.debug(f'Opening input file: {parsed_args.file}')
    with open(parsed_args.file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header_skipped = False
        records_read = 0

        for record in csv_reader:
            if not header_skipped and parsed_args.noheader:
                logging.debug('Skipping header row')
                header_skipped = True
                continue
            
            # Parse a row of data
            asset_record = build_record(record)
            
            # PUT the record to the API
            do_post(request_url=request_url, api_key=parsed_args.apikey, record=asset_record, request_headers={})

            records_read += 1

        logging.info(f'Handled {records_read} records -- DONE')

if __name__ == '__main__':
    main()