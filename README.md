cve_scraper
python script to scrape tenable website for plugin data associated with a CVE. import data via excel workbook (xlsx). exports plugin data via csv
- create workbook with no field headers, just list the CVE numbers in the column A, starting with A1; ensure to save as workbook (xlsx);
- for example: (cell A1), type "CVE-2019-0708" (without quotes), (cell A2) "CVE-2021-34527" (without quotes), then save; add as many entries as you like;
- run the script, enter the name of the file in the pop up gui, and press enter;
- a csv will be created and if data was found, will be written to the csv;
