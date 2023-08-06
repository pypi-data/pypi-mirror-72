import csv
import os
import re


# Print iterations progress
def print_prog_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s\n' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def csv_list_output(file_path):
    with open(file_path, "r", newline='', encoding='utf-8-sig') as infoFile:
        # Load CSV into dict
        csv_data = csv.DictReader(infoFile)
        # Get Keys from Fieldnames and initialize dict
        fields = csv_data.fieldnames
        temp = {str.lower(k): list() for k in fields}
        # Fill Dictionary out from list
        for row in csv_data:
            for k, v in row.items():
                temp[str.lower(k)].append(v)
        return temp


def find_info_for_year(full_info, year):
    temp = [list(full_info.keys())]
    for i, fyear in enumerate(full_info['fyear']):
        if fyear == year:
            temp.append([full_info[k][i] for k in full_info.keys()])
    return temp


def find_info(full_info, data):
    temp = [list(full_info.keys())]
    for cik in data['cik']:
        index_of_info = None
        if cik in full_info['cik']:
            index_of_info = full_info['cik'].index(cik)
            temp.append([full_info[k][index_of_info] for k in full_info.keys()])
    return temp


# When we need to split large files
def read_large_file(file, block_size=10000):
    space_after_tag = re.compile(r'>\s+', re.MULTILINE | re.IGNORECASE)
    newline_after_p_tag = re.compile(r'</p\s*>\s*', re.MULTILINE | re.IGNORECASE)
    newline_after_div_tag = re.compile(r'</div\s*>\s*', re.MULTILINE | re.IGNORECASE)
    newline_from_br = re.compile(r'<br\s*>\s*', re.MULTILINE | re.IGNORECASE)
    block = []
    for line in file:
        block.append(line)
        if len(block) == block_size:
            temp = space_after_tag.sub(u'>', ''.join(block))
            temp = newline_after_p_tag.sub(u'</p>\n', temp)
            temp = newline_after_div_tag.sub(u'</div>\n', temp)
            yield newline_from_br.sub(u'\n', temp)
            block = []

            # don't forget to yield the last block
    if block:
        temp = space_after_tag.sub(u'>', ''.join(block))
        temp = newline_after_p_tag.sub(u'</p>\n', temp)
        temp = newline_after_div_tag.sub(u'</div>\n', temp)
        yield newline_from_br.sub(u'\n', temp)


# Handles Filename generation
def yield_filename(directory_to_yield, yield_type):
    for root, dirs, files in os.walk(directory_to_yield):
        div = len(files) // 10
        if div <= 10:
            div = 1
        lgt = len(files) // div

        for i, filename in enumerate(files):
            # Update Progress Every 10 filings
            if i % div == 0:
                print_prog_bar(i / div, lgt, prefix=yield_type, suffix='Complete', length=50)
            yield directory_to_yield + filename


def yield_paragraph(text):
    # Paragraph Selector Regex
    many_space = re.compile(r'(?:\n {2,})|(?:\n+[ \t]?)+', re.MULTILINE | re.IGNORECASE)
    # Replace newline + many spaces with just newline. This allows paragraph select to work more accurately
    text = many_space.sub('\n', text)

    # paragraph_select = re.compile(r'(?:[^\n][\n]?)+(?:[^\n][\n]?)+', re.MULTILINE | re.IGNORECASE)
    paragraph_select = re.compile(r'(?:[^\n]*\t?[^ ]\n+)|(?:[^\n]*\t?[ ]+\n+)', re.MULTILINE | re.IGNORECASE)

    for match in paragraph_select.finditer(text):
        yield match.group()


def yield_sentence(text):
    sentence_select = re.compile(r'[^.!:;?\s][^.!:;?]*(?:[.!:;?](?![\'"]?\s|$)[^.!:;?]*)*[.!?:;]?[\'"]?(?=\s|$)',
                                 re.MULTILINE | re.IGNORECASE)

    for match in sentence_select.finditer(text):
        yield match.group()


def block_from_paragraphs(paragraphs):
    return '\n\t'.join(paragraph for paragraph in paragraphs)


def write_to_file(info, dir_out, filename, encoding_type):
    with open(dir_out + filename[:filename.rfind('.') + 1] + "rtf", "w") as output:
        output.write(str(info.encode(encoding_type, 'ignore'), encoding_type, 'ignore'))


def generate_word_dictionary(input_file, header_key):
    with open(input_file, "r", newline='', encoding='utf-8-sig') as dict_file:
        # Load CSV into dict
        csv_data = csv.DictReader(dict_file)

        # Listify CSV
        rows = list(csv_data)

        return [row[header_key] for row in rows]


def generate_dict_regex(word_dict):
    if not len(word_dict):
        return None

    return [r'\b' + word + r'\b' for word in word_dict]


def write_results_to_file(extraction_output, filename, snips):
    with open(extraction_output + filename[:filename.rfind('.') + 1] + "rtf", "w") as output:
        temp = '\n\t'.join(snip[1] for snip in snips)
        for char_code in range(144, 153):
            bad_char = chr(char_code)
            temp = temp.replace(bad_char, ' ')
        # temp = temp.replace(chr(776),' ')
        output.write(str(temp.encode("ASCII", 'ignore'), "ASCII", 'ignore'))


def move_filing(file_in, dir_out):
    filename = file_in.split("/")[-1]
    os.rename(file_in, dir_out + filename)
