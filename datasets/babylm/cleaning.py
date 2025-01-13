""" Cleaning functions for BabyLM datasets. Based on:
https://github.com/timinar/BabyLlama/blob/main/mrclean.py
https://huggingface.co/datasets/cambridge-climb/BabyLM/blob/main/clean_data.py
"""

import re

def cleanup_simple_wikipedia(text):
    text = re.sub(r'\n\n', '', text)
    return text

def cleanup_wikipedia(text):
    text = re.sub(r'= = = (.+?) = = =\n', r'\1', text)
    lines = [line.strip() for line in text.splitlines()]
    text =  re.sub(r'\n\n', '', '\n'.join(lines)[1:])
    return text

def cleanup_qed(text):
    punctuation_ex = re.compile(r'([.!?]\s*)')
    unimportant_chars_ex = re.compile(r'\(.*?\)|[.!?]')
    lines = []
    for line in text.splitlines():
        nchars = len(line)
        if nchars > 0:
            line_body = unimportant_chars_ex.sub('', line)
            f_upper = sum(c.isupper() for c in line_body) / len(line_body) if len(line_body) > 0 else 0
            if f_upper >= 0.5: # Mostly uppercase characters
                split_on_punctuation = punctuation_ex.split(line.replace('l', 'I'))
                line = ''.join([sentence.capitalize() for sentence in split_on_punctuation])
        lines.append(line.strip())
    return '\n'.join(lines)

def cleanup_extra_spaces(text):
    multiple_spaces_ex = re.compile(r'[ \t\u00A0]+')
    space_before_punctuation_ex = re.compile(r'[ \t\u00A0]([.,;!?])')
    text = multiple_spaces_ex.sub(' ', text)
    text = space_before_punctuation_ex.sub(r'\1', text)
    return text

def cleanup_bnc_spoken(text):
    text = cleanup_extra_spaces(text)
    text =  re.sub(r'\n\n', '', text)
    return text

def cleanup_aochildes(text):
    text = cleanup_extra_spaces(text)
    text = text[text.find('\t')+1:]
    return text

def cleanup_cbt(text):
    text = cleanup_extra_spaces(text)
    space_before_apostroph = re.compile(r"([\w\d])[ \t\u00A0](['’]\w)")
    #space_before_quote = re.compile(r"[ \t\u00A0](['’])")
    #space_after_quote = re.compile(r"([`])[ \t\u00A0]")
    #text = space_before_quote.sub(r'\1', text)
    #text = space_after_quote.sub(r'\1', text)
    text = space_before_apostroph.sub(r'\1\2', text)
    return text

def cleanup_children_stories(text):
    return text

def cleanup_gutenberg(text):
    # Overall, the text is clean, however some entries don’t seem
    # very useful, e.g. figure captions preceded by a number.
    # Not sure if we should remove them, because that would also
    # remove bullet lists which are otherwise consistent with the
    # surrounding text.
    # No start or end tokens because the text seems to be cut.
    return text

def cleanup_open_subtitles(text,):
    # The text is mostly clean, apart from some subtitle credits
    # such as "Subtitles by ...".
    subtitle_credit_ex = re.compile(r'^.*subtitle.*$\n', re.MULTILINE | re.IGNORECASE)
    text = subtitle_credit_ex.sub('', text)
    return text

def cleanup_switchboard(text):
    # No start or end tokens because the text seems to be cut.
    text = text[text.find('\t')+1:]
    return text
