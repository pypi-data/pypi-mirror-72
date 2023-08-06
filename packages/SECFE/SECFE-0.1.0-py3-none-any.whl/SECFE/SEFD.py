import random
from datetime import datetime, timedelta

import requests
from lxml import etree, html

from .utils import *


# Rework to make use of utils functions
def EDGAR_Query(file_path, filing_type):
    # Dictionary to hold all company data
    sec_data = dict()

    # URL to EDGAR
    url = "https://www.sec.gov/cgi-bin/browse-edgar"

    with open(file_path, "r", newline='', encoding='utf-8-sig') as info_file:
        # Load CSV into dict
        csv_data = csv.DictReader(info_file)

        # Listify CSV and Setup ProgBar
        rows = list(csv_data)
        div = len(rows) // 10

        if div <= 10:
            div = 1

        lgt = len(rows) // div

        # Generate data for each MnA
        for i, row in enumerate(rows):
            CIK = str(row['cik'])
            # tgCIK = str(row['tgcik'])
            start_date = row['strdate']
            end_date = str(int(datetime.strftime(datetime.strptime(str(row['filedate']), "%Y%m%d")
                                                 + timedelta(weeks=+40), "%Y%m%d"))) \
                if row['filedate'] != '' \
                else str(int(datetime.strftime(datetime.strptime(str(row['strdate']), "%Y%m%d")
                                               + timedelta(weeks=+40), "%Y%m%d")))

            fiscal_end = datetime.strftime(datetime.strptime(str(row['strdate']), "%Y%m%d"), "%m-%d-%Y")
            if "conm" in row.keys():
                name = str(row['conm']).strip()
            else:
                name = CIK

            params = {
                'CIK': CIK,
                'owner': 'exclude',
                'action': 'getcompany',
                # 'Find':'Search',
                # Return XML
                'output': 'xml',
                # Specify that we only want certain filings
                'type': filing_type,
                # Specify Last Year We Want
                'dateb': end_date,
                # Specify First Year We Want
                'datea': start_date
            }
            headers = {
                'Cache-Control': 'no-cache',
                'Accept-Encoding': 'gzip, deflate, br'
            }

            response = requests.get(url, headers=headers, params=params)
            if "no matching cik" in response.text.lower():
                continue
            site = etree.fromstring(response.content)

            cur_filing = name + " -> " + fiscal_end

            sec_data[cur_filing] = dict()
            sec_data[cur_filing]["fiscalEnd"] = str(row['strdate'])
            sec_data[cur_filing]["filerInfo"] = dict()
            sec_data[cur_filing]["filerInfo"]["CIK"] = CIK

            # Show Company Info ************************************
            for elem in site.find("companyInfo"):
                if elem.tag == "CIK":
                    sec_data[cur_filing]["filerInfo"]["SEC CIK"] = elem.text.strip()  # .lstrip('0')
                if elem.tag == "name":
                    sec_data[cur_filing]["filerInfo"]["SEC Name"] = elem.text.strip()

            #                    print("%s - %s" % (elem.tag, elem.text))

            # Get Filings ************************************
            sec_data[cur_filing]["filings"] = list()
            results = site.find("results")
            filing = {}
            if results is not None:
                for filings in results:
                    for file in filings:
                        # Add type of filing
                        if file.tag == "type":
                            filing["type"] = file.text
                        # Add date of filing
                        if file.tag == "dateFiled":
                            filing["date"] = file.text  # print(elem.text[0:4])
                        # Add link to filing
                        if file.tag == "filingHREF":
                            filing["link"] = file.text

                    # Append to Filings if not empty
                    if len(filing) > 0:
                        sec_data[cur_filing]["filings"].append(filing.copy())

                    # Clear to reset for next pass
                    filing.clear()
                    # time.sleep(.3)
            # Update Progress Every 10 filings
            if i % div == 0:
                print_prog_bar(i / div, lgt, prefix='EDGAR Search:', suffix='Complete', length=50)

    return sec_data


def filter_empty(sec_data, path_out):
    print(len(sec_data))
    no_filings = list()
    for cur_filing in sec_data:
        if len(sec_data[cur_filing]['filings']) == 0:
            temp = cur_filing.split('->')

            no_filings.append({'CIK': sec_data[cur_filing]["filerInfo"]['CIK'],
                               'name': temp[0].strip(),
                               'fiscalEnd': sec_data[cur_filing]["fiscalEnd"]
                               })

            # Set LIFO to none for filtering later
            sec_data[cur_filing] = None

    # Filter out any items that are None
    filtered = {k: v for k, v in sec_data.items() if v is not None}
    sec_data.clear()
    sec_data.update(filtered)

    if len(no_filings) > 0:
        # Rewrite json to not include empty listings
        # with open(pathIn, "w") as jsonOut:
        #    jFormatted = json.dumps(secInfo)
        #    jsonOut.write(jFormatted)
        #    jsonOut.close()

        # Write out No Listings to a CSV
        with open(path_out, "w", newline='') as output:
            if len(no_filings) > 0:
                dict_to_csv = csv.DictWriter(output, no_filings[0].keys())
                dict_to_csv.writeheader()
                dict_to_csv.writerows(no_filings)

    print(len(sec_data))

    return sec_data


def follow_links(sec_data):
    div = len(sec_data) // 10
    if div <= 10:
        div = 1
    lgt = len(sec_data) // div

    for i, cur_filing in enumerate(sec_data):
        for filing in sec_data[cur_filing]['filings']:
            doc_link = dict()
            # Get HTML ************************
            url = filing['link']

            headers = {
                'Cache-Control': 'no-cache',
                'Accept-Encoding': 'gzip, deflate, br'
            }

            response = requests.get(url, headers=headers)
            # ***********************************

            site = html.fromstring(response.content).body
            site.make_links_absolute("https://www.sec.gov/")

            # load table
            table = site.find_class('tableFile')[0]

            # Grab 10-K Filing (First Item In the List)
            aTag = table[1][2][0]
            # Grab Type of File (For 10-K thi si the first item in the list)
            file_type = str.upper(table[1][3].text_content().strip().replace(".", "_"))

            # Add link to file to list for filing. We add each file as file_type:link; ex: 10-K:http://www.sec.gov
            if file_type not in doc_link.keys():
                doc_link[file_type] = aTag.attrib['href']
            else:
                doc_link[f'{file_type} {random.randint(0, 25)}'] = aTag.attrib['href']

            del filing['link']
            filing['docLink'] = doc_link

        # Update Progress Every 2 filings
        if i % div == 0:
            print_prog_bar(i / div, lgt, prefix='Doc Linking:', suffix='Complete', length=50)

    return sec_data


# Unified = True results in all files from the same filing being output the same way
def filing_downloader(sec_data, save_folder, unified=False):
    div = len(sec_data) // 10
    if div <= 10:
        div = 1
    lgt = len(sec_data) // div

    for i, cur_filing in enumerate(sec_data):
        if len(sec_data[cur_filing]['filings']) > 0:
            for filing in sec_data[cur_filing]['filings']:
                for filing_type, doc in filing['docLink'].items():
                    exib = ""

                    # 'wb' Overwrites to create new filing
                    write_type = 'wb'
                    if unified:
                        exib = filing_type
                        # 'ab' Appends to the end of a filing to create one unified document
                        write_type = 'ab'
                    # Get DOC ************************
                    url = doc

                    headers = {
                        'Cache-Control': 'no-cache',
                        'Accept-Encoding': 'gzip, deflate, br'
                    }

                    response = requests.get(url, headers=headers)
                    # ***********************************
                    # filename = cur_filing.replace("->","-")+" "+ exib +filing['date']
                    filename = f'{sec_data[cur_filing]["filerInfo"]["CIK"]} {exib} {filing["date"]}'
                    # Sanitize String to valid filename
                    keep_characters = (' ', '.', '_', '-')
                    filename = "".join(c for c in filename if c.isalnum() or c in keep_characters).rstrip()
                    # Add file extension
                    filename += url[-4:]

                    with open(save_folder + filename, write_type) as f:
                        f.write(str(response.content))

                # time.sleep(.4)
        if i % div == 0:
            print_prog_bar(i / div, lgt, prefix='Downloading Filings:', suffix='Complete', length=50)
