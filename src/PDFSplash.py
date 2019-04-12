import os
import sys
import string
import re
import math
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import weasyprint #using Python3
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from xml.dom import minidom
import xml.etree.ElementTree as ET
import urllib.parse

# -*- coding: utf-8 -*-

class PDFSplash:
    def __init__():
        self.path_name_pdf = ""
        self.pdf_name_title = ""
        self.size_toc = []
        downloadStopWords()
        print("DOWNLOAD SUCESSFULLY")

    #use if get errors in text parser methods (nltk)
    def downloadStopWords(self):
        nltk.download('punkt')
        nltk.download('stopwords')
    #make an split of one pdf into two parts
    def PdfSplitToTwo(self, path, textToFind):
        file_name = os.path.splitext(os.path.basename(path))[0]
        pdf_reader = PdfFileReader(path)
        pdf_writer = PdfFileWriter()
        pdf_writer_second_part = PdfFileWriter()
        output_filename = output_filename_2 = " "
        part = 0

        #using the getPageNumberOfText() function to get the number of page where text appers
        first_part = getPageNumberOfText(path, textToFind)+1

        #RUN OUT THE LOOPS
        for page in range(0, first_part):
            pdf_writer.addPage(pdf_reader.getPage(page))
            output_filename = 'A_split_{}_{}.pdf'.format(file_name, part)

        part = 1

        for page in range(first_part-1, (pdf_reader.getNumPages()-first_part)+first_part):
            pdf_writer_second_part.addPage(pdf_reader.getPage(page))
            output_filename_2 = 'B_split_{}_{}.pdf'.format(file_name, part)

        part = part + 1

        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)
            print('Created: {} {}'.format(output_filename, part))

        with open(output_filename_2, 'wb') as out:
            pdf_writer_second_part.write(out)
            print('Created: {} {}'.format(output_filename_2, part))

        print("\n")

        return output_filename, output_filename_2

    #convert html file to pdf file into the path passed by
    def convertToPdf(self, path_html):
        pdf = weasyprint.HTML(path_html).write_pdf()
        pdf_file = open(''+path_html+'.pdf', 'wb')
        pdf_file.write(pdf)

        pdf_name = path_html+'.pdf'

        return pdf_name

    #returns the number of page where text_to_find appers
    def getPageNumberOfText(self, path, text_to_find):
        pdf = open(path, 'rb')
        pdfReader = PdfFileReader(pdf)

        #cleaning the text to find because causes discrepances

        translator = str.maketrans("", "", string.punctuation)

        search_word_clean = text_to_find

        page_apper = 0

        for pageNum in range(0, pdfReader.numPages):
            pageObj = pdfReader.getPage(pageNum)
            text = pageObj.extractText()
            search_text = text

            #cleaning up the text
            clean_text = search_text.translate(translator)
            clean_text.lower().split()
            clean_text = " ".join(search_text.split())

            ind = clean_text.find(search_word_clean)

            if(ind == -1):
                page_apper = -1
            else:
                page_apper = pageNum
                break

        if(page_apper == 0):
            page_apper = 1
            return page_apper
        else:
            return page_apper

    #get table is the same like "FIND_TEXT" function but return DICT(word, number)
    def getTableWordsbyNumbers(self,path, text_to_find):
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
    def getKeywordsOfPdf(self,path):
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

    #return the keys of the titles using regular expressions
    def FindKeys(self,text, regularExp):
        fileOp = open('text_result_extract_from_PDF.txt', 'w')
        fileOp.write(text)
        
        for match in re.finditer(r(regularExp), text):
            print (match.group())

    #specific print of the branchs of HTML file
    def branchsOfHTML(self,elem, func, level=0):
        func(elem, level)
        for child in elem.findall("./"):
            branchsOfHTML(child, func, level+1)

    def printLevelofHTML(self,elem, level):
        print('-'*level+elem.tag)

    def getHtml(self,text, number, path_name=""):
        if(number == -1):
            print("NOT FOUND", text)
        #bookmark number page
        html_part = '<p style="color: #4485b8;"><span style="background-color: #4485b8; color: #ffffff; padding: 0 5px;">'+text+'</span> &mdash; '+str(number)+'</p><hr/>'

        return html_part

    def generateTitleHTML(self,title, part):
        body_string = '<body onload="test()"> <hr /><h1 style="text-align: center;">'+title+'</h1><h3 style="text-align: center;">'+part+'</h3><p>&nbsp;</p> <h4 style="text-align: center;"><em>to find bookmarks PRESS CNTRL+F and paste the keyword. (or click on it and open the original file)</em></h4></body>'

        return body_string

    #generate HTML file with Table of Content
    def convertHTMLwithTOC(self,table, name_of_file, title_element, part_num):
        # generate the last file
        pdf_final_title = 'FINAL_DOCUMENT_WITH-TOC.pdf'
        f3 = open(pdf_final_title, 'w')
        self.path_name_pdf = os.path.abspath(pdf_final_title)
        print(self.path_name_pdf)
        f3.close()

        # generate dummy file to get the pages number
        f2 = open("html_count_pages.html", "w")
        f2.write(generateTitleHTML(title_element, 'PART '+str(part_num)))
        for name, number in table:
            f2.write(getHtml(name, 999, "none"))
        f2.close()

        pdf_filetest = convert_to_pdf("html_count_pages.html")

        pdf = open(pdf_filetest, 'rb')
        pdfReader = PdfFileReader(pdf)
        size = pdfReader.numPages
        self.size_toc.append(size-1)
        print("numbers of pages -> ", self.size_toc[part_num-1])

        #real_process to convert the HTML file
        f1 = open(name_of_file, 'w') #generate a HTML file with name_of_file name (ex, filename_proposed)
        f1.write(generateTitleHTML(title_element, 'PART '+str(part_num)))
        for name, number in table:
            if(number>=1):
                f1.write(getHtml(name, size_toc[part_num-1]+number, path_name_pdf))
        f1.close()

    def generateIndexListfromXML(self,path, pdf_path, elementToGet):
        doc_xml = minidom.parse(path)
        table_elements = []

        tree = ET.parse(path)
        root = tree.getroot()
        #branchsOfHTML(root, printLevelofHTML) an example of how use the print level

        doc_name = 'TOC_PREAM_.html'
        for child in root.iter(elementToGet):
            test = child.text
            number = getPageNumberOfText(pdf_path, test)
            table_elements.append((test, number))

        return table_elements, doc_name

    #append two pdf files into one, maybe we can recive a parameter called as "table_contenct" to make bookmarks"
    def pdfMerge(self,output_path, input_paths):
        pdf_merger = PdfFileMerger()
        for path in input_paths:
            pdf_merger.append(PdfFileReader(open(path, 'rb')))

        pdf_merger.write(output_path)
        pdf_merger.close()

    def splitXML(self,path, textToFind):
        tree = ET.parse(path)
        root = tree.getroot()

        lenght_text = len(textToFind)

        text_xml = ET.tostring(root).decode()

        #get the pos of the text in the XML file
        text_pos = text_xml.find(textToFind)

        #get the text from the XML file
        part_1 = text_xml[0:text_pos+lenght_text]
        part_2 = text_xml[text_pos+lenght_text+1:len(text_xml)]

        #create two separate files in XML
        with open('split_PART_1.xml', 'w') as f:
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            f.write("<root>\n")
            f.write(part_1)
            f.write("</SUPLINF>")
            f.write("</root>")

        with open('split_PART_2.xml', 'w') as f:
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            f.write("<root>\n")
            f.write(part_2)
            f.write("</SUPLINF>")
            f.write("</root>")
