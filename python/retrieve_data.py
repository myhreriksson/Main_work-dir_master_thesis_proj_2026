import os
import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source')
parser.add_argument('-p', '--path')
parser.add_argument('-n', '--name')
parser.add_argument('-e', '--extension')
arg = parser.parse_args()

def get_txt():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(response.text)
        print('Data successfully extracted.')

def get_pdf():
    with open(path, 'wb') as f:
        f.write(response.content)
        print('Data successfully extracted.')

response = requests.get(arg.source)
if response:
    print('Data retrieved.\n...')
else:
    print('Data could not be retrieved.')

path = os.path.join(arg.path, arg.name + arg.extension)

def main():
    if path.endswith('txt'):
        get_txt()
    elif path.endswith('pdf'):
        get_pdf()

if __name__=='__main__':
    main()