from langchain.agents import create_agent
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.docstore import InMemoryDocstore
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_ollama import ChatOllama
import faiss
import os
from langfuse import observe, get_client, propagate_attributes
from langfuse.langchain import CallbackHandler

# add the keys
os.environ["LANGFUSE_PUBLIC_KEY"] = ""
os.environ["LANGFUSE_SECRET_KEY"] = ""
os.environ["LANGFUSE_BASE_URL"] = "http://localhost:3001"

class BookChat:
    vectorstore = None
    def __init__(self):
        self.ollama = ChatOllama(
            model = "llama3.2",
            temperature = 0
        )
        self.llm = ChatOpenAI(
            model = "gpt-3.5-turbo",
            temperature = 0.4
        )
        loader = PyPDFLoader("javaguide.pdf")
        pages = loader.load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 50
        )
        self.documents = splitter.split_documents(pages)
        self.ollamaEmbedding = OllamaEmbeddings(
            model = "llama3.2",
        )
        self.embedding = OpenAIEmbeddings()
        self.docstore = InMemoryDocstore({})
        self.index = faiss.IndexFlatL2(len(self.embedding.embed_query("hello world")))
        BookChat.vectorstore = FAISS.from_documents(self.documents, self.embedding)
        self.inmemory = FAISS(
            embedding_function = self.embedding,
            index = self.index,
            docstore = self.docstore,
            index_to_docstore_id = {}
        )
        self.tools = [BookChat.retrieve_context]
        self.prompt = (
            "You have access to a tool that retrieves context from a document."
            "Use the tool to help answer user queries."
        )

        self.agent = create_agent(
            model = self.llm,
            tools = self.tools,
            system_prompt = self.prompt
        )

    @tool(response_format="content_and_artifact")
    def retrieve_context(query):
        """Retrieve information to help answer a query."""
        retrieved_docs = BookChat.vectorstore.similarity_search(query, k=2)
        serialized = "\n\n".join(
            f"Source: {doc.metadata}\nContent: {doc.page_content}"
            for doc in retrieved_docs
        )
        return serialized, retrieved_docs

    def get_agent(self):
        return self.agent


@observe
def process_user_prompt(query: str):
    agent = BookChat().get_agent()
    langfuse = get_client()
    with propagate_attributes(
            trace_name="bookchat-traces",
            session_id="session-1",
            user_id="user-1",
    ):
        langfuse_handler = CallbackHandler()
        for step in agent.stream(
                {
                        "messages": [{
                            "role": "user",
                            "content": query
                        }]
                    },
                    config = {
                        "callbacks": [langfuse_handler]
                    },
                    stream_mode="values",
        ):
            if not isinstance(step["messages"][-1], ToolMessage):
                step["messages"][-1].pretty_print()


if __name__ == "__main__":
    query = "As per the document, list some 8 annotations?"
    process_user_prompt(query)
