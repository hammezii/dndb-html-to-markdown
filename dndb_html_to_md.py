# import libraries
import html2text
import os
from bs4 import BeautifulSoup

# set directory for input_dir (drop files here to be converted) 
# and output_dir (where markdown files will be saved)
input_dir = "input" 
output_dir = "output"

# List of CSS elements to remove
elements_to_remove = [
    '.ddb-site-banner',
    '.b-noscript',
    '.ddb-footer',
    '.site-bar__container',
    '.page-header',
    '.p-article-byline',
    '#mega-menu-target',
    '#skip-to-content-link',
    'header',
    'footer'
]

# get list of html files in input_dir folder
files = []
for file in os.listdir(input_dir):
    if file.endswith(('.html','.htm')):
        files.append(file)

# uses Beautiful Soup to strip out elements in elements_to_remove
#open html_file and reads it
for file in files:  
    with open(os.path.join(input_dir, file), 'r', encoding='utf-8', errors='ignore') as fff:
        html_content = fff.read()

    # reads file with beautiful soup
    soup = BeautifulSoup(html_content, 'html.parser')
    soup.encode('UTF-8')

    # remove elements
    for element in elements_to_remove:
        for element in soup.select(element):
            element.decompose()

    # overwrite the file with the new cleaned version
    with open(os.path.join(input_dir, file), 'w', encoding='utf-8') as ffff: #overwrite the file
        ffff.write(str(soup))

    print(file+" is cleaned.")

# now html files are cleaned, runs them through html2text to convert them to markdown
# set html2text function and options: see config for all options
cleaner = html2text.HTML2Text()
cleaner.ignore_images = True
cleaner.ignore_links = True
cleaner.body_width = 0

# Conversion loop: performs conversion for each file in input_dir
# opens and reads each file from files
for file in files:
    with open(os.path.join(input_dir, file), "r", encoding='UTF-8', errors='ignore') as f:
        html = f.read()

    # change unicode characters to single or double quotation mark to be read by markdown
    tidy_html = html.replace("’", "'").replace("“", "\"").replace("”","\"")

    # convert html file to markdown
    text = cleaner.handle(tidy_html)

    # Open a file and write the conversion to it
    with open(os.path.join(output_dir, file), 'w') as ff:
        ff.write(text)   

    print(file+" is converted to markdown.")

# Rename converted files in output_dir folder
# get list of files in output_dir folder
converted = os.listdir(output_dir)

# rename each converted files
for convert in converted:
    newfiles = []
    newfiles.append(os.path.splitext(convert)[0]+'.md')
    for newfile in newfiles:
        os.replace(os.path.join(output_dir, convert), os.path.join(output_dir, newfile))

print("File conversion complete!")