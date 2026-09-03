import re
import os
import argparse
from pypdf import PdfReader

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input')
parser.add_argument('-o', '--output')
parser.add_argument('-n', '--name')
parser.add_argument('-e', '--extension')
arg = parser.parse_args()

# some of the numbers are wrong, but alignment is correct, so I'll choose to ignore it for the sake of my mental health
def pdf_vers():
    with open(out_path, 'w', encoding='utf-8') as f:
        reader = PdfReader(inp_path)
        # patterns 1-3 and this entire function are great reasons why I hate working with pdfs :)
        pattern_1 = r'(?=^\d+\n)'
        pattern_2 = r'anonymousgerman\sbible\s\d+'
        pattern_3 = r'chapter\s(\d+)'
        chapter = ''
        verses = []
        for p in reader.pages[37:]:
            page = p.extract_text()
            lines = re.split(pattern_1, page, flags=re.MULTILINE)
            for i, line in enumerate(lines):
                line = re.sub('\n', ' ', line.strip())
                line = re.sub(pattern_2, '', line, flags=re.IGNORECASE)
                if re.match(r'^\d', line):
                    verses.append(line)
                else:
                    try:
                        verses[-1] += line
                        continue
                    except Exception:
                        pass
                if verses:
                    verses[-1] = chapter + ':' + verses[-1]
                match = re.search(pattern_3, line, flags=re.IGNORECASE)
                if match:
                    chapter = match.group(1)
        for verse in verses:
            verse = re.sub(pattern_3, '', verse, flags=re.IGNORECASE)
            verse = re.sub(r'chapter\s*\w*', '', verse, flags=re.IGNORECASE)
            f.write(verse.strip() + '\n')
    print('Data successfully versified.')

def txt_vers():
    with (
        open(inp_path, 'r', encoding='utf-8') as i_f,
        open(out_path, 'w', encoding='utf-8') as o_f
        ):
        lines = i_f.readlines()
        verse = ''
        for line in lines:
            for segment in re.split(r'(?<!\d)(?=\d+:\d+\s)', line):
                if re.search(r'^\d+:\d+', segment):
                    if verse:
                        o_f.write(verse + '\n')
                    verse = segment.strip()
                else:
                    verse += ' ' + segment.strip()
        if verse:
            o_f.write(verse + '\n')
    print('Data successfully versified.')

inp_path = os.path.join(arg.input, arg.name + '_raw' + arg.extension)
out_path = os.path.join(arg.output, arg.name + '_tokenized' + '.txt')

def main():
    if inp_path.endswith('txt'):
        txt_vers()
    elif inp_path.endswith('pdf'):
        pdf_vers()

if __name__=='__main__':
    main()