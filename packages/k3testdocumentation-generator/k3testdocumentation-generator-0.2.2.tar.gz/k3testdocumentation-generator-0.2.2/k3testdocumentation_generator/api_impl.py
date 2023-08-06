"""
Module contains implementations for generating test documentation 
"""

import logging
import os
import json

#from fpdf import FPDF, HTMLMixin
from markdown import markdown
from jinja2 import Template
import pdfkit


logger = logging.getLogger(__name__)


# REQUIRED_TEST_KEYS = ["test_name", "test_descrition"]
# OPTIONAL_KEYS = ["requirements_fully_tested", "requirements_partially_tested", "required_equiptment", "precondition", "expected_results"]
# MARKDOWN_TEST_KEYS = ["precondition", "test_descrition", "expected_results"]

# def render_markdown_to_html(marddownContent):
#     return markdown(marddownContent)
#     """Render Markdown Syntax to final HTML."""
#     soup = BeautifulSoup(markdown(marddownContent))
#     _add_a_attrs(soup)
#     return soup.prettify()
# 
# def _add_a_attrs(soup):
#     """Add HTML attrs to our link elements"""
#     for tag in soup.find_all("a"):
#         tag['rel'] = "nofollow"
#         tag['target'] = "_blank"
    

def render_doc_template_with_dict(inputDict, templateString, templateType="jinja2"):
    if templateType != "jinja2":
        raise RuntimeError(f"Only jinja2 templates are supported atm. Given template type {templateType}")
    td = {}
    td["input_dict"] = inputDict
    td["markdown"] = markdown
    template = Template(templateString)
    return template.render(td)
    
def generate_pdf_document_from_html(htmlStr, outputPdfFilePath):
    pdfkit.from_string(htmlStr, outputPdfFilePath)
    

def _parse_test_dir(folderPath):
    testDict = {}
    logger.debug(f"Processing directory {folderPath}")
    tjPath = os.path.join(folderPath, "__test__.json")
    if os.path.isfile(tjPath):
        logger.debug(f"Processing __test__.json {tjPath}")
        with open(tjPath) as fh:
            try:
                testDict = json.load(fh)
            except:
                logger.warning(f"Error while parsing file {tjPath}")
                raise
    else:
        logger.debug("No __test__.json")
    
    for aFile in os.listdir(folderPath):
        if aFile == "__test__.json":
            continue
        filePath = os.path.join(folderPath, aFile)
        if os.path.isfile(filePath):
            nm, ext = os.path.splitext(aFile)
            with open(filePath) as fh:
                if ext == ".json":
                    logger.debug(f"Processing json file {aFile}")
                    try:
                        testDict[nm] = json.load(fh)
                    except:
                        logger.warning(f"Error while parsing json file {filePath}")
                        raise
                else:
                    logger.debug(f"Processing file {aFile}")
                    testDict[nm] = fh.read()
        elif os.path.isdir(filePath):
            testDict[nm] = _parse_test_dir(filePath)
    return testDict 

def get_dict_from_file_system(rootFolderPath):
    resultDict = {}
    for aDir in os.listdir(rootFolderPath):
        dirp = os.path.join(rootFolderPath, aDir)
        if os.path.isdir(dirp):
            resultDict[aDir] = _parse_test_dir(dirp)
    return resultDict

def generate_json_from_file_system(rootFolderPath, jsonOutputPath):
    with open(jsonOutputPath, "w") as fh:
        json.dump(get_dict_from_file_system(rootFolderPath), fh, indent=4, sort_keys=True)

def generate_coverage_evalution(requirementsList, testDocumentationDict, requirementComments={}):
    """
    Returns the following dict structure
    
   {"requirements" : [...],
    "tests" : [...],
    "requirement_comments" : requirementComments,
    "requirement_coverage" : {...}
   }
    
    where the value of requirement_coverage is a dict of a dict of lists. Keys
    of the first dict are the requirements, the keys of the second dict are
    'partially_tested_by' & 'fully_tested_by' and the lists contain the testIDs
    """
    res = {"requirements" : requirementsList,
           "tests" : [k for k in testDocumentationDict],
           "requirement_comments" : requirementComments,
           "requirement_coverage" : {}
           }
    
    for requirement in requirementsList:
        requirementCovDict = {}
        requirementCovDict["partially_tested_by"] = []
        requirementCovDict["fully_tested_by"] = []
        for test in testDocumentationDict:
            if requirement in testDocumentationDict[test]["requirements_fully_tested"]:
                requirementCovDict["fully_tested_by"].append(test)
            elif requirement in testDocumentationDict[test]["requirements_partially_tested"]:
                requirementCovDict["partially_tested_by"].append(test)
        res["requirement_coverage"][requirement] = requirementCovDict
    return res

