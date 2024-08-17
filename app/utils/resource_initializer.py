from langchain import hub

from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter


def initialize_resources():
    # 금융분야 마이데이터 기술 가이드라인 PDF 로더 초기화
    tech_guide_line_pdf = PyPDFLoader(
        'https://www.mydatacenter.or.kr:3441/cmmn/fileBrDownload?id=JHuKqjlWK0e%2FH9Yi7ed09GsZWL6TiRKp9yg4qGj%2FKFmV9RC6j8RJdh6I8JAqzoFv&type=2')

    # 금융분야 마이데이터 표준 API 규격 v1 PDF 로더 초기화
    my_data_api_standard_pdf = PyPDFLoader(
        'https://www.mydatacenter.or.kr:3441/cmmn/fileBrDownload?id=dKi%2B7cAM4PO8JA4z7jwm4AoM07vmQIbSKQ9EvM0DPRYokFCd%2BhLigsDUZ0hQopjD&type=2')

    # 텍스트 스플리터 초기화
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    # 두 문서의 텍스트 분할
    tech_guide_line = tech_guide_line_pdf.load_and_split(text_splitter)
    my_data_api_standard = my_data_api_standard_pdf.load_and_split(text_splitter)

    # 텍스트 결합
    all_texts = tech_guide_line + my_data_api_standard

    # 임베딩 및 검색기 초기화
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    hf_embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    docsearch = Chroma.from_documents(all_texts, hf_embeddings)
    # 유사도 기반 검색으로 0.8 이상인 결과만 조회하여 불필요한 토큰 전달 방지
    retriever = docsearch.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.8})

    # rag 프롬프트 초기화
    rag_prompt = hub.pull("hwchase17/openai-functions-agent")

    return retriever, rag_prompt
