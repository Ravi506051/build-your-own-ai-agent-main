"""Minimal RAG document Q&A agent with OpenAI or Ollama backends."""

import os
import uuid
from pathlib import Path

import chromadb
import requests
from chromadb.config import Settings
from colorama import Fore, Style, init
from openai import OpenAI
from sentence_transformers import SentenceTransformer

init(autoreset=True)

BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR / "docs"
DB_DIR = BASE_DIR / "chroma_db"
COLLECTION = "rag_docs"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 3


class RAGAgent:
    """RAG document Q&A agent using sentence-transformers and ChromaDB."""

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "ollama").lower()
        self.model_name = "all-MiniLM-L6-v2"
        self.embedder = SentenceTransformer(self.model_name)
        self.collection = self._setup_vector_db()
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if self.provider == "openai" else None
        self._ensure_docs_exist()
        self._index_documents()

    def _setup_vector_db(self):
        """Create or load persistent ChromaDB collection."""
        client = chromadb.PersistentClient(path=str(DB_DIR), settings=Settings(anonymized_telemetry=False))
        return client.get_or_create_collection(name=COLLECTION)

    def _ensure_docs_exist(self):
        """Create sample docs when docs directory is empty."""
        DOCS_DIR.mkdir(exist_ok=True)
        if any(DOCS_DIR.glob("*.txt")):
            return
        samples = {
            "rag_intro.txt": """Retrieval-Augmented Generation (RAG) combines retrieval and generation.
The system retrieves relevant document snippets and injects them into prompts.
This helps language models answer with grounded, source-based context.
RAG is useful when model weights do not contain private or fresh information.""",
            "embeddings.txt": """Embeddings are dense vector representations of text.
Similar meanings produce vectors that are close in vector space.
A vector database can quickly find nearest chunks for a user query.
This enables semantic search beyond exact keyword matching.""",
            "chunking.txt": """Chunking splits long documents into smaller pieces.
Good chunk sizes preserve meaning while fitting model context windows.
Overlapping chunks reduce the chance of losing boundary information.
Simple character-based chunking is easy to implement and often sufficient.""",
        }
        for name, text in samples.items():
            (DOCS_DIR / name).write_text(text, encoding="utf-8")

    def _chunk_text(self, text: str):
        """Split text into overlapping character chunks."""
        chunks, start = [], 0
        while start < len(text):
            end = start + CHUNK_SIZE
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start += CHUNK_SIZE - CHUNK_OVERLAP
        return chunks

    def _index_documents(self):
        """Embed and index docs into ChromaDB if not already indexed."""
        if self.collection.count() > 0:
            return
        all_chunks, ids, metas = [], [], []
        for file_path in DOCS_DIR.glob("*.txt"):
            text = file_path.read_text(encoding="utf-8").strip()
            for i, chunk in enumerate(self._chunk_text(text)):
                all_chunks.append(chunk)
                ids.append(str(uuid.uuid4()))
                metas.append({"source": file_path.name, "chunk": i})
        if not all_chunks:
            return
        embeddings = self.embedder.encode(all_chunks).tolist()
        self.collection.add(ids=ids, documents=all_chunks, metadatas=metas, embeddings=embeddings)

    def retrieve(self, query: str):
        """Retrieve top-k relevant chunks for a query."""
        q_emb = self.embedder.encode([query]).tolist()[0]
        result = self.collection.query(query_embeddings=[q_emb], n_results=TOP_K)
        docs = result.get("documents", [[]])[0]
        metas = result.get("metadatas", [[]])[0]
        return [f"[{m.get('source')}#{m.get('chunk')}] {d}" for d, m in zip(docs, metas)]

    def _build_prompt(self, query: str, contexts):
        """Create grounded prompt with retrieved context."""
        context_block = "\n\n".join(contexts) if contexts else "No relevant context found."
        return (
            "You are a helpful document QA assistant. "
            "Answer using only the context below. If the answer is unknown, say so.\n\n"
            f"Context:\n{context_block}\n\n"
            f"Question: {query}\n"
            "Answer:"
        )

    def _call_openai(self, prompt: str):
        """Generate answer using OpenAI Chat Completions API."""
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        resp = self.openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You answer questions from provided context."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        return resp.choices[0].message.content.strip()

    def _call_ollama(self, prompt: str):
        """Generate answer using local Ollama HTTP API."""
        model = os.getenv("OLLAMA_MODEL", "llama3.2")
        base_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        resp = requests.post(
            f"{base_url}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json().get("response", "").strip()

    def answer(self, query: str):
        """Retrieve context and ask selected LLM provider to answer."""
        contexts = self.retrieve(query)
        prompt = self._build_prompt(query, contexts)
        if self.provider == "openai":
            answer = self._call_openai(prompt)
        else:
            answer = self._call_ollama(prompt)
        return contexts, answer


def repl():
    """Run interactive Q&A loop for the RAG agent."""
    agent = RAGAgent()
    print("RAG agent ready. Type /quit to exit.")
    print(f"Provider: {agent.provider}")
    while True:
        query = input(f"{Fore.WHITE}You> {Style.RESET_ALL}").strip()
        if not query:
            continue
        if query.lower() == "/quit":
            print("Goodbye.")
            break
        try:
            contexts, answer = agent.answer(query)
            print(f"{Style.DIM}Context:")
            for c in contexts:
                print(f"{Style.DIM}- {c}")
            print(f"{Fore.GREEN}\nAnswer: {answer}\n")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    repl()
