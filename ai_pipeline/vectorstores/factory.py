import os
from typing import Optional, Any
from langchain_openai import OpenAIEmbeddings

class VectorStoreFactory:
    """
    구성(Configuration)에 따라 적절한 Vector Store 인스턴스를 생성하는 팩토리 클래스.
    """
    
    @staticmethod
    def get_vector_store(
        provider: str, 
        collection_name: str, 
        embeddings: Optional[Any] = None,
        connection_string: Optional[str] = None,
        persist_directory: Optional[str] = None
    ):
        if embeddings is None:
            # 기본값으로 OpenAI Embeddings 사용 (환경변수 OPENAI_API_KEY 필요)
            embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            
        provider = provider.lower()
        
        if provider == "faiss":
            from langchain_community.vectorstores import FAISS
            if persist_directory and os.path.exists(os.path.join(persist_directory, "index.faiss")):
                return FAISS.load_local(persist_directory, embeddings, allow_dangerous_deserialization=True)
            return None # 신규 생성은 유즈케이스에 따라 다름
            
        elif provider == "chroma":
            from langchain_chroma import Chroma
            return Chroma(
                collection_name=collection_name,
                embedding_function=embeddings,
                persist_directory=persist_directory
            )
            
        elif provider == "pgvector":
            from langchain_postgres.vectorstores import PGVector
            conn = connection_string or os.getenv("VECTOR_DB_URL") or os.getenv("DATABASE_URL")
            if conn and conn.startswith("postgresql://"):
                conn = conn.replace("postgresql://", "postgresql+psycopg2://", 1)
            
            return PGVector(
                embeddings=embeddings,
                collection_name=collection_name,
                connection=conn,
                use_jsonb=True,
            )
            
        else:
            raise ValueError(f"지원하지 않는 Vector Store 프로바이더입니다: {provider}")
