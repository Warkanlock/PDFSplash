import os
import sys
import re
import json
import requests
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import weasyprint
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from xml.dom import minidom
import xml.etree.ElementTree as ET
import urllib.parse

#nltk.download('punkt')
#nltk.download('stopwords')
#

#make an split of one pdf
def pdf_split(path):

    file_name = os.path.splitext(os.path.basename(path))[0]

    #VARIABLES
    pdf_reader = PdfFileReader(path)
    pdf_writer = PdfFileWriter()
    pdf_writer_second_part = PdfFileWriter()
    output_filename = output_filename_2 = "testing"
    part = 0

    #HARDCODED, CHANGE FOR THE POSITION APPERS OF "PART 1 INCOME TAXES"
    #parte_primera = 102

    parte_primera = find_text(path, "PART 1")+1
    #parte_primera = find_text(path, "Accordingly, 26 CFR part 1 is proposed to be amended as follows")+1


    #RUN OUT THE LOOPS
    for page in range(0, parte_primera):
        pdf_writer.addPage(pdf_reader.getPage(page))
        output_filename = 'preamble_split_{}_{}.pdf'.format(file_name, part)

    part = 1

    for page in range(parte_primera-1, (pdf_reader.getNumPages()-parte_primera)+parte_primera):
        pdf_writer_second_part.addPage(pdf_reader.getPage(page))
        output_filename_2 = 'proposed_split_{}_{}.pdf'.format(file_name, part)

    part = part + 1

    with open(output_filename, 'wb') as out:
        pdf_writer.write(out)
        print('Created: {} {}'.format(output_filename, part))

    with open(output_filename_2, 'wb') as out:
        pdf_writer_second_part.write(out)
        print('Created: {} {}'.format(output_filename_2, part))

    print("\n")

    return output_filename, output_filename_2

#convert html file to pdf file
def convert_to_pdf(path_html):
    pdf = weasyprint.HTML(path_html).write_pdf()
    pdf_file = open(''+path_html+'.pdf', 'wb')
    pdf_file.write(pdf)

    pdf_name = path_html+'.pdf'

    return pdf_name
    #pdfkit.from_file(path_html, 'book_mark.pdf')

#returns the number of page where text_to_find appers
def find_text(path, text_to_find):
    pdf = open(path, 'rb')
    pdfReader = PdfFileReader(pdf)

    search_word = text_to_find
    page_apper = 0

    for pageNum in range(1, pdfReader.numPages):
        pageObj = pdfReader.getPage(pageNum)
        text = pageObj.extractText().encode('utf-8')
        search_text = text
        if search_word in search_text.decode("utf-8"):
            page_apper = pageNum

    return page_apper

#get table is the same like "FIND_TEXT" function but return DICT(word, number)
def get_table(path, text_to_find):
    pdf = open(path, 'rb')
    pdfReader = PdfFileReader(pdf)

    search_word = text_to_find
    page_apper = 0

    for pageNum in range(1, pdfReader.numPages):
        pageObj = pdfReader.getPage(pageNum)
        text = pageObj.extractText().encode('utf-8')
        search_text = text
        if search_word in search_text.decode("utf-8"):
            page_apper = pageNum

    return (page_apper, text_to_find)

#get keywords and txt of the pdf file
def get_text(path):
    pdf = open(path, 'rb')
    pdf_reader = PdfFileReader(pdf)
    num_pages = pdf_reader.numPages
    count = 0
    text = ""

    while count < num_pages:
        page = pdf_reader.getPage(count)
        count += 1
        text += page.extractText()

    tokens = word_tokenize(text)

    punctuations = ['(', ')', '.', '-', ':', '[', ']',',']

    stop_words = stopwords.words('english')

    keywords = [word for word in tokens if not word in stop_words and not word in punctuations]

    #find_key(text)
    return text
    #print(keywords)

#return the keys of the titles
def find_key(text):
    #matchObjects = re.findall(r"(?![XIV].[A-Z])[XIV§]+\.(.*)", text)
    #print(matchObjects)

    archivo = open('text_result_extract_from_PDF.txt', 'w')
    archivo.write(text)

    print("-----------------------")

    for match in re.finditer(r"(?![XIV]\.[A-Z])[XIV§]+\.(.*)", text):
        print (match.group())

    print("-----------------------")

    for match in re.finditer(r"\([a-z]*\)(.*)\.", text.strip()):
        print (match.group())

    print("-----------------------")

    for match in re.finditer(r"\([0-9]*\)(.*)\.", text.strip()):
        print (match.group())

    ##FUNCTION TOOLS

#specific print of the branchs
def perf_func(elem, func, level=0):
    func(elem, level)
    for child in elem.findall("./"):
        perf_func(child, func, level+1)
def print_level(elem, level):
    print('-'*level+elem.tag)

        ##FUNCTION TOOLS

#get HTML file from a text string
def get_html(text, number):
    #html_part = "<a href=#"++">"+text+"</a>"
    html_part = "<h4>"+text+"</h4>"+"........"+"Keyword N°"+str(number)
    return html_part

def get_page_number(text, root, header):

    number_pages = 0
    i = 0
    tc = 0
    flag_total = 0

    for child in root.iter(header):
        #print(child.text)
        #print(text)
        if not (child.text == text):
            i += 1
            #print(i)
        else:
            break

    for pages in root.iter('PRTPAGE'):
        tc += 1
        flag_total = (int(float(pages.attrib['P'])) - tc) - (int(float(pages.attrib['P'])))

    number_pages = ((number_pages + i) * flag_total)/flag_total
    return number_pages

def generate_title_html(title, part):
    body_string = '<hr /><h1 style="text-align: center;">'+title+'</h1><h3 style="text-align: center;">'+part+'</h3><p>&nbsp;</p> <h4 style="text-align: center;"><em>to use the keywords index, PRESS CNTRL+F and paste the keyword.</em></h4>'
    return body_string

def generate_index_list_xml(path):
    doc_xml = minidom.parse(path)
    headers = doc_xml.getElementsByTagName('HD')
    subjects = doc_xml.getElementsByTagName('SUBJECT')
    subelementos = doc_xml.getElementsByTagName('E')
    title_element = " "
    table_elements = []
    table_elements_2 = []


    tree = ET.parse(path)
    root = tree.getroot()
    #perf_func(root, print_level)

    for child in root.iter('PREAMB'):
        title = child.find('SUBJECT').text
        title_element = title

    pream_doc_name = 'TOC_PREAM_' + title_element + '.html'
    propo_doc_name = 'TOC_PROPOSED_' + title_element + '.html'

    f1 = open(pream_doc_name, 'w')
    f2 = open(propo_doc_name, 'w')


    #print("-------------- FIRST TOC ------------------")

    f1.write(generate_title_html(title_element, 'PART ONE'))

    for child in root.iter('HD'):
         test = child.text
         #number = find_text('preamble_split_test_0.pdf', test)
         number=get_page_number(test, root, 'HD')
         if "PART 1" not in test and "Authority" not in test:
             table_elements.append(test)
             f1.write(get_html(test,number))

    # print("-------------- SECTION NUMBER ------------------")
    #
    # for child in root.iter('SECTNO'):
    #     print(child.text)

    f1.close()

    #print("-------------- SECOND TOC ------------------")

    f2.write(generate_title_html(title_element, 'PART TWO'))

    for childA in root.iter('SUPLINF'):
        for child in childA.iter('SUBJECT'):
            #number = find_text('proposed_split_test_1.pdf', child.text)
            number=get_page_number(child.text, root, 'SUBJECT')
            if "Amended" not in child.text:
                table_elements_2.append(child.text)
                f2.write(get_html(child.text, number))

    #print("-------------- TERCER TOC ------------------")

    #for match in re.finditer('\w(?!(http:)(https:)(Link:)(www.)$(.gov))\d*[a-zA-Z0-9 ]{10,}(?!(.*gov)|(.htm))(?=\:|\.)', text):
    #    print(match.group())
    #for child in root.iter('E'):
    #    print(child.text)

    f2.close()

    return table_elements, table_elements_2, pream_doc_name, propo_doc_name, title_element

def get_document_xml(document_number):
    document_name = -1
    url = 'http://www.federalregister.gov/api/v1/documents/'+document_number+'.json'
    get_document = requests.get(url)
    get_document_json = json.loads(get_document.content)
    if not(get_document_json['title'] == ""):
        get_xml = requests.get(get_document_json['full_text_xml_url'])
        open('document_'+document_number+'XMLFORMAT.xml', 'wb').write(get_xml.content)
        document_name = 'document_'+document_number+'XMLFORMAT.xml'
    else:
        print("\t ------------------- \t          RESULTS NOT FOUND             \t ------------------- ")
        document_name = ""

    return document_name

def get_document_name(document_number):
    document_name = ""
    url = 'http://www.federalregister.gov/api/v1/documents/'+document_number+'.json'
    get_document = requests.get(url)
    if(get_document.status_code == requests.codes.ok):
        get_document_json = json.loads(get_document.content)
        document_name = get_document_json['title']
        return document_name
    else:
        print("\t ------------------- \t          RESULTS NOT FOUND             \t ------------------- ")
        document_name = ""
        return document_name


#append two pdf files into one, maybe we can recive a parameter called as "table_contenct" to make bookmarks"
def pdf_merge(output_path, input_paths, table=0):
    pdf_merger = PdfFileMerger()
    in_order = ""

    for path in input_paths:
        pdf_merger.append(PdfFileReader(open(path, 'rb')))

    #pdf_merger.addBookmark("TESTING", 50)
    pdf_merger.write(output_path)

    pdf_merger.close()

    #with open(output_path, 'wb') as fileobj:
    #    pdf_merger.write(fileobj)

def split_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()

    lenght_text = len('<P>Accordingly, 26 CFR part 1 is proposed to be amended as follows:</P>')

    text_xml = ET.tostring(root).decode()

    #get the pos of the text in the XML file
    text_pos = text_xml.find('Accordingly, 26 CFR part 1 is proposed to be amended as follows:')

    #get the text from the XML file
    part_1 = text_xml[0:text_pos+lenght_text]
    part_2 = text_xml[text_pos+lenght_text+1:len(text_xml)]

    #create two separate files in XML
    with open('PREAMBLE_split_PART_1.xml', 'w') as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        f.write("<root>\n")
        f.write(part_1)
        f.write("</SUPLINF>")
        f.write("</root>")

    with open('PROPOSED_split_PART_2.xml', 'w') as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        f.write("<root>\n")
        f.write(part_2)
        f.write("</SUPLINF>")
        f.write("</root>")

def get_document_number(search):

    document_number = 0
    document_title = "not found"

    url =  'http://www.federalregister.gov/api/v1/documents.json'
    params = { "per_page" : "20", "order" : "relevance", "conditions[term]" : search, "conditions[agencies][]" : "treasury-department" }
    query = urllib.parse.urlencode(params)
    final_URL = url + '?' + query
    get_document = requests.get(final_URL)
    get_document_json = json.loads(get_document.content)
    if(get_document_json['count'] == 0):
        print("\t ------------------- \t          RESULTS NOT FOUND              \t ------------------- ")
        document_number = -1
        document_title = ""
    else:
        document_number = get_document_json['results'][0]['document_number']
        document_title = get_document_json['results'][0]['title']


    return document_number, document_title

def clean():
    print("\t ------------------- \t --------------------------------------  \t -------------------")
    print("\t ------------------- \t --------------------------------------  \t -------------------")
    print("\t ------------------- \t --------------------------------------  \t -------------------")
    print("\t ------------------- \t --------------------------------------  \t -------------------\n")
    #os.system('cls' if os.name == 'nt' else 'clear')

############################################

#INITIAL PROGRAM
path = '/home/ignacio/PycharmProjects/PDFtest/pdfs_irs/test.pdf'
path_html = 'TOC_part_one.html'
path_html2 = 'TOC_part_two.html'
path_xml = 'document_2018-27391XMLFORMAT.xml'
path_document = '2018-27391'
document_path_name = " "

##HTML METHODS
#txt = get_text(path)

##XML METHODS
#split_xml(path_xml)

while True:
    print("\t ------------------- \t GET DOCUMENT FROM THE FEDERAL REGISTER \t ------------------- \n")
    print("(1) Insert the name of the document (loose, because make a search by name)")
    print("(2) Insert the document year and serial number (exact copy of the document)\n")
    option = input("Enter an option: ")

    if(option == "1"):
        document_name = input("Enter the exact document name to search it: ")
        document_number, document_title = get_document_number(document_name)
        if not document_number == -1:
            print("[DOCUMENT NUMBER]", document_number)
            print("[DOCUMENT TITLE]", document_title)
            opt = input("IS THIS YOUR DOCUMENT? Press [Y/n] -> ")
            if(opt == "Y" or opt == "y"):
                print("DOWNLOADING THE DOCUMENT.")
                # get the XML document to the path, returns the name of the XML file
                document_path_name = get_document_xml(document_number)

                input("DOCUMENT DOWNLOAD, PRESS ENTER TO CONTINUE.")
                break

            elif(opt == "N" or opt=="n"):
                clean()
                continue
        else:
            clean()
            continue

    if(option== "2"):
        year = input("Enter a YEAR of a document (1990-2020) (FOUR DIGITS): ")
        while(len(year)<4 or len(year)>4 or int(float(year))<1990 or int(float(year))>2020):
            year = input("REINSERT a YEAR of a document (1990-2020) (FOUR DIGITS): ")

        document = input("Enter a DOCUMENT serial number: ")
        name = get_document_name(year + '-' + document)
        if not(name==""):
            print("[DOCUMENT TITLE] "+name)
            opt = input("IS THIS YOUR DOCUMENT? Press [Y/n] -> ")
            if (opt == "Y" or opt == "y"):
                print("DOWNLOADING THE DOCUMENT.")
                # get the XML document to the path, returns the name of the XML file
                document_path_name = get_document_xml(year + '-' + document)

                input("DOCUMENT DOWNLOAD, PRESS ENTER TO CONTINUE.")
                break

            elif (opt == "N" or opt == "n"):
                clean()
                continue
        else:
            clean()
            continue

        break

    else:
        clean()
        print(" ")

while True:
    path = input("Enter the path (/home/user/...) of the PDF what you want to merge and create a TOC:") #PATH OF PDF (SE PODRIA BAJAR DEL JSON PERO EL IRS USA OTROS)
    opt = input("Is this, "+path+" a correct path? (Y/n)")
    if (opt == "Y" or opt == "y"):
        break

    elif (opt == "N" or opt == "n"):
        path = input("Reinsert the path: ")


##GENERAL FUNCTIONS

# for a in range(0, 100):
#     time.sleep(0.1)
#     hash = count * a
#     space = '-' * (100 - len(hash))
#     sys.stdout.write("\r WAITING: [{0}]".format(hash + space))

print("\t ------------------- \t GET THE TABLE OF CONTENT OF THE DOCUMENTS DOWNLOADED RECENTLY \t ------------------- \n")
# generate index from PATH XML
toc_1, toc_2, filename_pream, filename_proposed, title_of_document = generate_index_list_xml(document_path_name)

print("\t ------------------- \t CONVERT TO PDF THE HTML \t ------------------- \n")

# #convert HTML to PDF
filename_pream_PDF = convert_to_pdf(filename_pream)
filename_proposed_PDF = convert_to_pdf(filename_proposed)

print("\t ------------------- \t SPLIT AND MERGE THE DOCUMENTS INTO ONE \t ------------------- \n")
split_names_part1, split_names_part2 = pdf_split(path)

files = (filename_pream_PDF, split_names_part1)
files_2 = (filename_proposed_PDF, split_names_part2)

#files = ('TOC_part_one.html.pdf', 'preamble_split_test_0.pdf')
#files_2 = ('TOC_part_two.html.pdf', 'proposed_split_test_1.pdf')

#merge PDFS
pdf_merge('FINAL_PREAM_'+title_of_document+'_WITH-TOC.pdf',files)
pdf_merge('FINAL_PROPOSED_'+title_of_document+'_WITH-TOC.pdf',files_2)


print("\t ------------------- \t CREATE TOC AND MERGE COMPLETE "+title_of_document+" \t ------------------- \n")