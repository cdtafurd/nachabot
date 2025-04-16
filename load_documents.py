import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from data.urls import WEB_PATHS 

# Load and chunk documents (replace with your actual document loading logic)
def load_documents():
    """Load and chunk documents from the web."""
    # Define a custom BeautifulSoup strainer to filter the content
    bs4_strainer = bs4.SoupStrainer(
    class_=("frame frame-default frame-type-textmedia frame-layout-0", 
            "frame frame-default frame-type-header frame-layout-0",
            "breadcrumb-class clearfix col-sm-9"),)


# Load and chunk contents of the blog
    loader = WebBaseLoader(
        web_paths=WEB_PATHS,
        bs_kwargs={"parse_only": bs4_strainer},
        bs_get_text_kwargs={"separator": " ", "strip": True},
    )
    docs = loader.load()


    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=180)
    return text_splitter.split_documents(docs)