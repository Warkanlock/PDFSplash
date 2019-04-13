
<div align="center" style="text-align:center">
  <img src="https://raw.githubusercontent.com/Warkanlock/PDFSplash/master/logo.png?token=AMuOoIflLLGWKVYBWszV4LQQbH74FzL2ks5csSG8wA%3D%3D" height=30% width=30%/>
</div>

# PDFSplash
#### Tool for generate PDF´s in easy way (Table of Contents, Split them, etc)

*NOTE: Using Python 3.x for this tool*

## REQUIREMENTS

* OS
* RE
* SYS
* JSON
* REQUEST
* WEASYPRINT
* PyPDF2
* XML.DOM
* ElementTree
* URLLIB

## Tutorial for general purpose

## A guide step by step

1. Install all dependencies to ensure the correctly function of the software.
2. Instance the class and using it!.

## EXAMPLES OF USING

```python
#generate index from XML FILE using his PATH
tableOfContent, filenameOFfile = generateIndexListfromXML(document_path_name_XML, document_path_name_PDF, element_of_yourXML)


# You can generate TOC based in XML file and them you can merge with PDF file

#generate an HTML file with the INDEX of PDF
convertHTMLwithTOC(tableOfContent, filenameOFfile, title_of_document, 1)

#convert HTML to PDF
filename_PDF_withTOC = convertToPdf(filenameOFfile)
split_names_part1, split_names_part2 = PdfSplitToTwo(document_path_name_PDF, textToFindandSplit)

#merge PDFS using the TOC result and split one PDF
files = (filename_PDF_withTOC, split_names_part1)
pdfMerge('FINAL_DOCUMENT_WITH-TOC.pdf', files)
```
