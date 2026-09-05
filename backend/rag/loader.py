from pathlib import Path

from pypdf import PdfReader


def load_text_file(file_path: str) -> str:
    """
    Load a plain text or Markdown file.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    return path.read_text(
        encoding="utf-8",
        errors="ignore",
    )


def load_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    reader = PdfReader(str(path))

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n\n".join(pages)


def load_document(file_path: str) -> str:
    """
    Automatically load a supported document.
    """

    path = Path(file_path)

    extension = path.suffix.lower()

    if extension in [".txt", ".md"]:
        return load_text_file(file_path)

    if extension == ".pdf":
        return load_pdf(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}. "
        "Supported types: .txt, .md, .pdf"
    )