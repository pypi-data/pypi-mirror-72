import argparse
import os
import sys
import yaml

parser = argparse.ArgumentParser(description='Scrape R&D competitions and push the results to the SuiteCRM API.',
                                 prog='opportunity_scraper')
parser.add_argument('-c', '--config', dest='config',
                    default=f'{os.environ["HOME"]}/.config/opportunity_scraper/settings.yaml',
                    help='Location of config file')

try:
    file = open(parser.parse_args().config, 'r')
except Exception:
    print(f"Couldn't open config file {parser.parse_args().config}")
    sys.exit(1)

settings = yaml.load(file, Loader=yaml.FullLoader)
