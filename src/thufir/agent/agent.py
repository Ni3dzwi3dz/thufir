import os

from langchain_community.document_loaders import WebBaseLoader


class Agent:
    def init(self, document_loader: WebBaseLoader):
        self.document_loader = document_loader

    def load_documents(self, urls: list[str]):
        """Load documents from the given URLs using the document loader."""
        documents = []
        for url in urls:
            try:
                document = self.document_loader.load(url)
                documents.append(document)
            except Exception as e:
                print(f"Error loading document from {url}: {e}")
        return documents
