import unicodedata

from bs4 import BeautifulSoup, UnicodeDammit, NavigableString
from lxml import etree
from lxml.html import tostring as html_to_text

from .utils import *


def decode_html(html_string):
    converted = UnicodeDammit(html_string)
    if not converted.unicode_markup:
        raise UnicodeDecodeError(
            "Failed to detect encoding, tried [%s]",
            ', '.join(converted.tried_encodings))
    # print converted.original_encoding
    return converted.unicode_markup


def between(cur, end):
    while cur != end and cur is not None:
        if isinstance(cur, NavigableString):
            text = cur
            if len(text):
                yield text
        cur = cur.next_element


def clean_soup(soup):
    for el in soup.iter():
        if el.tag == "div" or el.tag == "p":
            el.tail = "\n" + el.tail if el.tail else "\n"
        if el.text:
            el.text = " ".join(el.text.splitlines())
        if el.tag == "table":
            if el.text:
                el.text = el.text.replace("\n", " ") + "\n\n"
    return soup


def section_selection(section_beg, section_end, directory_to_search, extraction_output):
    # Grab X words before and after the search terms
    begin_regex = section_beg
    end_regex = section_end
    # Speedup regex and allow multiline and any case matching
    begin_grab = re.compile(begin_regex, re.MULTILINE | re.IGNORECASE)
    end_grab = re.compile(end_regex, re.MULTILINE | re.IGNORECASE)

    in_section = False

    sections = list()

    for root, dirs, files in os.walk(directory_to_search):
        # Block to setup progress bar
        div = len(files) // 10

        if div <= 10:
            div = 1

        lgt = len(files) // div
        # End Block to setup progress bar

        for i, filename in enumerate(files):
            results = list()
            if filename.endswith('.pdf') or filename.endswith('.jpg') or filename.endswith('.DS_Store'):
                continue

            # print(filename)

            with open(directory_to_search + filename, "r", encoding='ASCII', errors='ignore', newline='') as filing_doc:
                soup = BeautifulSoup(filing_doc, "lxml")
                for script in soup.find_all(["script", "style"]):
                    script.extract()

                for match in soup.find_all("table"):
                    match.wrap(soup.new_tag("div"))

                for match in soup.find_all(["td", "tr", "tbody", "table", "i", "font", "b"]):
                    match.unwrap()
                soup.smooth()

                soup = soup.get_text(separator="\n ")
                maxOut = 0

                for paragraph in yield_paragraph(unicodedata.normalize("NFKD", soup.replace("Table of Contents", ""))):
                    temps = list()
                    if maxOut < 250:
                        maxOut += 1
                    if in_section:
                        if end_grab.findall(paragraph):
                            in_section = False
                        temps = paragraph
                    elif begin_grab.findall(paragraph):
                        in_section = True
                        temps = paragraph

                    # If itertools has something in it, we append the paragraph to results
                    if len(temps) > 0:
                        results.append(temps)
            if len(results) > 0:
                write_to_file(block_from_paragraphs(results), extraction_output, filename, "ASCII")
                sections.append([filename, results])

            # Update Progress Every 10 filings
            if i % div == 0:
                print_prog_bar(i / div, lgt, prefix='ReGex Section Grab:', suffix='Complete', length=50)

    return sections


def section_selection_lxml(section_beg, section_end, directory_to_search, extraction_output):
    # Regex to find where a section begins and ends
    begin_regex = section_beg
    end_regex = section_end
    # Speedup regex and allow multiline and any case matching
    begin_grab = re.compile(begin_regex, re.MULTILINE | re.IGNORECASE)
    end_grab = re.compile(end_regex, re.MULTILINE | re.IGNORECASE)

    in_section = False
    max_sections = 2
    sections = list()

    for filename in yield_filename(directory_to_search, "LXML Selection Grab"):
        results = list()

        # Skip over unreadable files that may be in directory
        if filename.endswith('.pdf') or filename.endswith('.jpg') or filename.endswith('.DS_Store'):
            continue

        with open(filename, "r", encoding='ASCII', errors='ignore', newline='') as filing_doc:
            # print(filename[filename.rfind("/") + 1:])
            soup = etree.HTML(decode_html(filing_doc.read()))

            for el in soup.iter("tr"):
                el.text = " ".join(el.itertext())
                for child in el.iterchildren():
                    if child.tag != "tr":
                        el.remove(child)
                el.tag = "div"
            # We remove tags that are for style creation. This will make it easier to parse documents
            etree.strip_tags(soup, ["script", "td", "tr", "font", "b", "a", "i", "text", "document", "filename",
                                    "sequence", "type", "description", "hr", "h1", "h2", "h3", "h4"])

            # Clean up text within tags to remove randomly placed newlines that cause output to be malformed.
            soup = clean_soup(soup)

            num_sections = 0
            o_n = 0
            for paragraph in yield_paragraph(
                    unicodedata.normalize("NFKD", html_to_text(soup, encoding="unicode", method="text"))):
                temps = list()

                # If we are in the section we want to be in, we start grabbing the paragraphs until we reach the end
                # of the section we want
                if in_section:
                    o_n += 1
                    if "item" in paragraph.lower():
                        if end_grab.search(paragraph):
                            num_sections += 1
                            in_section = False
                    temps = paragraph
                elif begin_grab.search(paragraph):
                    o_n = 1
                    in_section = True
                    temps = paragraph
                # If temps has something in it, we append the paragraph to results
                if len(temps) > 0:
                    results.append(temps)
                if num_sections >= max_sections:
                    break
        # print("searched")
        if len(results) > 0:
            sections.append([filename[filename.rfind("/") + 1:], results])
            write_to_file(block_from_paragraphs(results), extraction_output, filename[filename.rfind("/") + 1:],
                          "ASCII")

    return sections


def section_selection_atag_risk_factors(directory_to_search, extraction_output):
    sections = list()
    link_found = False
    risk_href = ''

    for filename in yield_filename(directory_to_search, "A Tag Selection Grab"):
        results = list()
        # Skip over unreadable files that may be in directory
        if filename.endswith('.pdf') or filename.endswith('.jpg') or filename.endswith('.DS_Store'):
            continue

        with open(filename, "r", encoding='ASCII', errors='ignore', newline='') as filing_doc:
            # print(filename[filename.rfind("/") + 1:])

            soup = etree.HTML(decode_html(filing_doc.read()))

            etree.strip_tags(soup, ["font", "u", "b", "i", "text"])

            for el in soup.iter("a"):
                # Search through a tag text for Risk Factors Section or variants of the section
                if el.text is not None and not link_found:
                    a_text = el.text.lower().replace('\n', ' ').strip()
                    if "risk factors" in a_text:
                        link_found = True
                        risk_href = el.attrib['href']
                        # print(risk_href)
                    elif "item 1a" in a_text:
                        link_found = True
                        risk_href = el.attrib['href']
                        # print(risk_href)
                # If we don't find text, go through a tag's name attribute for Risk Factors Section
                # or variants of the section
                if not link_found and el.attrib is not None and "name" in el.attrib.keys():
                    a_name = el.attrib['name'].lower()
                    if "risk" in a_name and "factors" in a_name:
                        link_found = True
                        risk_href = el.attrib['name']
                        # print(risk_href)
                    elif "item" in a_name and "1a" in a_name:
                        link_found = True
                        risk_href = el.attrib['name']
                        # print(risk_href)
            # Remove # from href if present to allow for searching for location of section
            if "#" in risk_href:
                risk_href = risk_href[1:]

            # We remove tags that are for style creation. This will make it easier to parse documents
            etree.strip_tags(soup, ["script", "td", "tr", "font", "u", "b", "i", "text", "document", "filename",
                                    "sequence", "type", "description", "hr", "h1", "h2", "h3", "h4"])

            # Create None variables to store beginning and end of risk section
            risk_elem = None
            end_of_risk_href = None

            # XPath to get all a tags with name attribute
            for el in soup.xpath(f".//a[@name]"):
                # We do lowercase comparison as href and name attributes do not always match case
                if risk_href.lower() == el.attrib["name"].lower() and risk_elem is None:
                    risk_elem = True
                    # print(el.attrib["name"])

                # If we have have found the beginning of the risk section, grab next non risk a tag
                elif risk_elem is not None and risk_href.lower() != el.attrib["name"].lower():
                    end_of_risk_href = el.attrib["name"]
                    # print(el.attrib["name"])
                    break

            # Clean up text within tags to remove randomly placed newlines that cause output to be malformed.
            soup = clean_soup(soup)

            # Convert our Soup object from LXML to BS4 to allow search between elements
            soup = BeautifulSoup(etree.tostring(soup, encoding='utf8'), features="lxml")

            # Do CSS Select for a tag with name = risk_href and end_of_risk_href to allow for case insensitive search
            risk_elem = soup.select(f'a[name="{risk_href}" i]')
            end_of_risk_elem = soup.select(f'a[name="{end_of_risk_href}" i]')

            risk_text = ''

            if len(risk_elem) and len(end_of_risk_elem):
                risk_text = ''.join(between(risk_elem[0], end_of_risk_elem[0]))

            for paragraph in yield_paragraph(unicodedata.normalize("NFKD", risk_text)):
                temps = paragraph
                # If temps has something in it, we append the paragraph to results
                if len(temps) > 0:
                    results.append(temps)

        link_found = False

        # print("searched")
        if len(results) > 0:
            sections.append([filename[filename.rfind("/") + 1:], results])
            write_to_file(block_from_paragraphs(results), extraction_output,
                          filename[filename.rfind("/") + 1:], "ASCII")

    return sections
