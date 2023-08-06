from collections import Counter

from .utils import *


def does_word_exist(section, word_patterns, debug=False):
    """Converts section to dict of words and then does regex on keys to find if word exists in section
        This is done to reduce number of sections to ones we know might fit criteria

       Keyword arguments:
       section -- read out of section file
       imag -- list of regex patterns for word to check against
    """

    words_in_section = Counter(section.split())

    if debug:
        print(words_in_section)

    regex_matches = [re.compile(pattern, re.IGNORECASE).match for pattern in word_patterns]

    words_matched = {k: v for k, v in words_in_section.items()
                     if any(regex_match(k) for regex_match in regex_matches)}

    if debug:
        print(words_matched)

    if len(words_matched):
        return True

    return False


def paragraph_search(section, word_patterns, debug=False):
    if not len(word_patterns):
        return []
    regex_searches = [re.compile(pattern, re.MULTILINE | re.IGNORECASE).search for pattern in word_patterns]
    matched_paragraphs = []
    # Primary Keyword is the first in the regex patterns
    matched_primary_keyword = False
    matched_secondary = False

    for paragraph in yield_paragraph(section):
        # if debug: print(paragraph)

        # If each word pattern matches, matched_all will return True after loop is done for paragraph.
        # This means we save it on our list
        for i, regex_search in enumerate(regex_searches):
            if i == 0:
                matched_primary_keyword = True if regex_search(paragraph) else False
            else:
                matched_secondary = True if regex_search(paragraph) else False
                if matched_secondary:
                    break
        if matched_primary_keyword and (len(regex_searches) == 1 or (len(regex_searches) > 1 and matched_secondary)):
            matched_paragraphs.append(paragraph)

    if debug:
        print(matched_paragraphs)

    return matched_paragraphs


def sentence_search(section, word_patterns, debug=False):
    if not len(word_patterns):
        return []
    regex_searches = [re.compile(pattern, re.MULTILINE | re.IGNORECASE).search for pattern in word_patterns]
    matched_paragraphs = []
    # Primary Keyword is the first in the regex patterns
    matched_primary_keyword = False
    matched_secondary = False

    for paragraph in yield_paragraph(section):
        # if debug: print(paragraph)
        for sentence in yield_sentence(paragraph):
            # If each word pattern matches, matched_all will return True after loop is done for paragraph.
            # This means we save it on our list
            for i, regex_search in enumerate(regex_searches):
                if i == 0:
                    matched_primary_keyword = True if regex_search(sentence) else False
                else:
                    matched_secondary = True if regex_search(sentence) else False
                    if matched_secondary:
                        break
            if matched_secondary:
                break
        if matched_primary_keyword and (
                len(regex_searches) == 1 or (len(regex_searches) > 1 and matched_secondary)):
            matched_paragraphs.append(paragraph)

    if debug:
        print(matched_paragraphs)

    return matched_paragraphs


def paragraph_keyword_search(section, search_patterns, dir_out, filename, debug=False):
    inventory_risk_paragraphs = paragraph_search(section, search_patterns, debug)

    if len(inventory_risk_paragraphs):
        write_to_file(block_from_paragraphs(inventory_risk_paragraphs), dir_out,
                      filename, "ASCII")
        if debug:
            (len(inventory_risk_paragraphs))
        return True
    return False


def sentence_keyword_search(section, search_patterns, dir_out, filename, debug=False):
    inventory_risk_paragraphs = sentence_search(section, search_patterns, debug)

    if len(inventory_risk_paragraphs):
        write_to_file(block_from_paragraphs(inventory_risk_paragraphs), dir_out,
                      filename, "ASCII")
        if debug:
            (len(inventory_risk_paragraphs))
        return True
    return False