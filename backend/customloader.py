from neo4j_graphrag.experimental.components.pdf_loader import DataLoader
from neo4j_graphrag.experimental.components.types import DocumentInfo, PdfDocument
from neo4j_graphrag.exceptions import PdfLoaderError
from fsspec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem
from pathlib import Path
from typing import Dict, Optional, Union
import fitz  # This is pymupdf
import io
import fsspec


def is_default_fs(fs: fsspec.AbstractFileSystem) -> bool:
	return isinstance(fs, LocalFileSystem) and not fs.auto_mkdir


class PyMuPdfLoader(DataLoader):
	@staticmethod
	def load_file(
		file: str,
		fs: AbstractFileSystem,
	) -> str:
		"""Parse PDF file using pymupdf and return text."""
		try:
			with fs.open(file, "rb") as fp:
				stream = fp if is_default_fs(fs) else io.BytesIO(fp.read())
				doc = fitz.open(stream=stream.read())
				text = ""
				for page in doc:
					text += page.get_text()
				return text
		except Exception as e:
			raise PdfLoaderError(e)

	async def run(
		self,
		filepath: Union[str, Path],
		metadata: Optional[Dict[str, str]] = None,
		fs: Optional[Union[AbstractFileSystem, str]] = None,
	) -> PdfDocument:
		if not isinstance(filepath, str):
			filepath = str(filepath)
		if isinstance(fs, str):
			fs = fsspec.filesystem(fs)
		elif fs is None:
			fs = LocalFileSystem()
		text = self.load_file(filepath, fs)
		return PdfDocument(
			text=text,
			document_info=DocumentInfo(
				path=filepath,
				metadata=self.get_document_metadata(text, metadata),
			),
		)
