

import PyPDF2
import docx
import tiktoken

class DocumentProcessor:
    """
    A class to process various document types (PDF, DOCX, TXT),
    extract text, clean it, and prepare it for analysis.
    """

    def __init__(self, max_tokens=3000):
        """
        Initializes the DocumentProcessor.

        Args:
            max_tokens (int): The maximum number of tokens to allow.
        """
        self.max_tokens = max_tokens
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def _get_text_from_pdf(self, file_path):
        """Extracts text from a PDF file."""
        text = ""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text

    def _get_text_from_docx(self, file_path):
        """Extracts text from a DOCX file."""
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    def _get_text_from_txt(self, file_path):
        """Extracts text from a TXT file."""
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        return text

    def _clean_text(self, text):
        """Cleans the extracted text."""
        return " ".join(text.split())

    def process(self, file_path):
        """
        Processes a document, extracts and cleans text, and returns metadata.

        Args:
            file_path (str): The path to the document.

        Returns:
            dict: A dictionary containing the document's content and metadata.
        """
        file_type = file_path.split(".")[-1].lower()
        text = ""

        if file_type == "pdf":
            text = self._get_text_from_pdf(file_path)
        elif file_type == "docx":
            text = self._get_text_from_docx(file_path)
        elif file_type == "txt":
            text = self._get_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        cleaned_text = self._clean_text(text)
        tokens = self.tokenizer.encode(cleaned_text)
        token_count = len(tokens)

        if token_count > self.max_tokens:
            cleaned_text = self.tokenizer.decode(tokens[:self.max_tokens])
            token_count = self.max_tokens

        return {
            "file_type": file_type,
            "content": cleaned_text,
            "token_count": token_count,
            "size_bytes": len(cleaned_text.encode('utf-8'))
        }

