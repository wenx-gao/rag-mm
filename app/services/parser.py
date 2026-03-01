# app/services/parser.py
import logging
from pathlib import Path
import pandas as pd

# NEW IMPORT PATHS FOR DOCLING v2.x
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentParser:
    def __init__(self):
        # 1. Setup the Pipeline Options (High-level config)
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_table_structure = True
        pipeline_options.table_structure_options.do_cell_matching = True
        
        # 2. NEW v2 WAY: Wrap pipeline options in a FormatOption object
        self.converter = DocumentConverter(
            allowed_formats=[
                InputFormat.PDF, 
                InputFormat.DOCX, 
                InputFormat.XLSX, 
                InputFormat.IMAGE
            ],
            # This is the change: format_options instead of pipeline_options
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

    def parse(self, file_path: str) -> list[dict]:
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix in ['.xlsx', '.csv']:
            return self._parse_tabular(path)

        return self._parse_multimodal(path)

    def _parse_tabular(self, path: Path) -> list[dict]:
        df = pd.read_excel(path) if path.suffix == '.xlsx' else pd.read_csv(path)
        markdown_content = df.to_markdown(index=False)
        return [{
            "text": markdown_content, 
            "metadata": {"source": path.name, "type": "table"}
        }]

    def _parse_multimodal(self, path: Path) -> list[dict]:
        result = self.converter.convert(path)
        doc = result.document
        chunks = []
        
        for element, _level in doc.iterate_items():
            # In Docling v2, we can export elements to markdown directly
            content = ""
            if hasattr(element, 'export_to_markdown'):
                content = element.export_to_markdown()
            elif hasattr(element, 'text'):
                content = element.text

            if content.strip():
                chunks.append({
                    "text": content,
                    "metadata": {
                        "source": path.name,
                        "page_no": getattr(element, 'page_no', None),
                        "type": element.__class__.__name__
                    }
                })
        return chunks
