import io
from docx import Document as DocxDocument

class ParserService:
    def parse_file(self, file_content: bytes, filename: str) -> str:
        ext = filename.split(".")[-1].lower()
        if ext == "txt":
            return file_content.decode("utf-8", errors="ignore")
        elif ext == "docx":
            return self._parse_docx(file_content)
        elif ext == "pdf":
            return self._parse_pdf(file_content)
        else:
            return file_content.decode("utf-8", errors="ignore")

    def _parse_docx(self, file_content: bytes) -> str:
        try:
            doc = DocxDocument(io.BytesIO(file_content))
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            return "\n".join(full_text)
        except Exception as e:
            return f"[Error parsing DOCX file: {str(e)}]"

    def _parse_pdf(self, file_content: bytes) -> str:
        # In a real environment, we'd use pypdf or pdfplumber:
        # reader = PdfReader(io.BytesIO(file_content))
        # return "\n".join([page.extract_text() for page in reader.pages])
        # Return a simulated extraction for regulatory compliance guidelines
        return (
            "Clinical Trial Study Protocol. Objective: Assess efficacy. "
            "Drug: ReguDraft-Compound. Adverse Events: headache, fatigue. "
            "Phase: Phase 3 clinical trial. Number of subjects: 150. "
            "Conclusion: Safe and effective."
        )

parser_service = ParserService()
