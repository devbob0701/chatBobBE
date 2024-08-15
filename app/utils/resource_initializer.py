from langchain import hub
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter


def initialize_resources():
    # 금융분야 마이데이터 기술 가이드라인 PDF 로더 초기화
    loader1 = PyPDFLoader(
        'https://www.mydatacenter.or.kr:3441/cmmn/fileBrDownload?id=JHuKqjlWK0e%2FH9Yi7ed09GsZWL6TiRKp9yg4qGj%2FKFmV9RC6j8RJdh6I8JAqzoFv&type=2')
    document1 = loader1.load()

    # 금융분야 마이데이터 표준 API 규격 v1 PDF 로더 초기화
    loader2 = PyPDFLoader(
        'https://www.mydatacenter.or.kr:3441/cmmn/fileBrDownload?id=dKi%2B7cAM4PO8JA4z7jwm4AoM07vmQIbSKQ9EvM0DPRYokFCd%2BhLigsDUZ0hQopjD&type=2')
    document2 = loader2.load()

    # 텍스트 스플리터 초기화
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)

    # 두 문서의 텍스트 분할
    texts1 = text_splitter.split_documents(document1)
    texts2 = text_splitter.split_documents(document2)

    # 텍스트 결합
    all_texts = texts1 + texts2

    # 임베딩 및 검색기 초기화
    #embeddings = HuggingFaceBgeEmbeddings()
    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_documents(all_texts, embeddings)
    retriever = docsearch.as_retriever()

    # RAG 프롬프트 및 LLM 초기화
    rag_prompt = hub.pull("rlm/rag-prompt")
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    #llm = None

    return retriever, rag_prompt, llm