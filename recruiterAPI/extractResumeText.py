import langchain
from langchain_community.document_loaders import UnstructuredPDFLoader

def getResumeText(filepath):

    pdf_loader = UnstructuredPDFLoader(filepath)
    pdf_pages = pdf_loader.load_and_split()

    resumeText = ""
    for i in range(0,len(pdf_pages)):
        resumeText += pdf_pages[i].page_content
    
    resumeText = resumeText.replace("\\", " ").replace("\"", " ").replace("\n", " ").replace("\\n", " ").replace("    ", " ").replace("{", " ").replace("}", " ").replace("[", " ").replace("]", " ")

    return resumeText
