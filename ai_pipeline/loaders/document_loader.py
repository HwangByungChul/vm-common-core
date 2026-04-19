import os
from typing import List
from langchain_core.documents import Document

def get_document_loader(file_path: str):
    """
    파일 확장자에 적합한 LangChain 로더 객체를 반환합니다.
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.pdf':
        from langchain_community.document_loaders import PyMuPDFLoader
        return PyMuPDFLoader(file_path)
    elif ext == '.docx':
        from langchain_community.document_loaders import Docx2txtLoader
        return Docx2txtLoader(file_path)
    elif ext == '.csv':
        from langchain_community.document_loaders import CSVLoader
        return CSVLoader(file_path)
    elif ext == '.xlsx' or ext == '.xls':
        from langchain_community.document_loaders import UnstructuredExcelLoader
        return UnstructuredExcelLoader(file_path)
    elif ext == '.md':
        try:
            from langchain_community.document_loaders import UnstructuredMarkdownLoader
            return UnstructuredMarkdownLoader(file_path)
        except ImportError:
            from langchain_community.document_loaders import TextLoader
            return TextLoader(file_path, encoding='utf-8')
    else: # fallback to TextLoader
        from langchain_community.document_loaders import TextLoader
        return TextLoader(file_path, encoding='utf-8')

def load_and_split_document(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 100) -> List[Document]:
    """
    문서를 로드하고 지정된 크기로 분할하여 반환합니다.
    """
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    
    loader = get_document_loader(file_path)
    raw_docs = loader.load()
    
    if not raw_docs:
        return []
        
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(raw_docs)
