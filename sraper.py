import concurrent
import json
import sys

from requests_html import HTMLSession
import openpyxl
from tqdm import tqdm

cve_input_file = input("Enter CVE input file as <filename>.xlsx: ")
#print(cve_input_file)
cve_output_file = input("Enter CVE output file as <filename>.xlsx: ")

def scrape_data(_cve_code):
    global wsf
    session = HTMLSession()
    cve_url = f"https://www.tenable.com/cve/{_cve_code}"
    r = session.get(cve_url)
    data = r.html.xpath("//script[@id='__NEXT_DATA__']", first=True).text
    json_data = json.loads(data)['props']['pageProps']

    desciptions_list = json_data['cve']['cve']['description']['description_data']
    description = ''
    for desciptions in desciptions_list:
        if desciptions['lang'] == 'en':
            description = desciptions['value']

    plugins = json_data['plugins']
    for plugin in plugins:
        severity = plugin['_source']['risk_factor']
        plugin_name = plugin['_source']['script_name']
        add_row = [_cve_code, description, plugin['_id'], plugin_name, severity]
        wsf.append(add_row)

try:
    wb1 = openpyxl.load_workbook(cve_input_file)
    ws = wb1.active
except FileNotFoundError:
    print("The CVE input file was not found.")
    sys.exit()

wbf = openpyxl.Workbook()
wsf = wbf.active
wsf.append(['CVE Title', 'Description', 'Plugin ID', 'Plugin Name', 'Severity'])

cve_codes = []
for row in ws.rows:
    for cell in row:
        cve_codes.append(cell.value)

with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
    executor.map(scrape_data, cve_codes) # works!
#    list(tqdm(executor.map(scrape_data, cve_codes), total=len(cve_codes))) # og - no worky
#    list(executor.map(tqdm(scrape_data, cve_codes), total=len(cve_codes))) # new attempt - no worky

wbf.save(cve_output_file)
