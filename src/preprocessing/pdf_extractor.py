"""
PDF Text Extraction Module
Extracts text from PDF medical reports
"""

import PyPDF2
import logging
from pathlib import Path
from typing import Optional, Dict

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFExtractor:
    """Extract text from PDF files"""
    
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    def extract_text(self, pdf_path: str) -> Optional[str]:
        """
        Extract text from a PDF file
        
        Args: 
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text or None if extraction fails
        """
        try: 
            pdf_path = Path(pdf_path)
            
            # Validate file exists
            if not pdf_path.exists():
                logger.error(f"File not found: {pdf_path}")
                return None
            
            # Validate file format
            if pdf_path.suffix. lower() not in self.supported_formats:
                logger.error(f"Unsupported file format: {pdf_path.suffix}")
                return None
            
            # Extract text
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                logger.info(f"Processing {num_pages} pages from {pdf_path. name}")
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
            
            if not text. strip():
                logger.warning(f"No text extracted from {pdf_path.name}")
                return None
            
            logger.info(f"Successfully extracted {len(text)} characters")
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF:  {str(e)}")
            return None
    
    def extract_with_metadata(self, pdf_path: str) -> Dict:
        """
        Extract text along with metadata
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns: 
            dict: Dictionary containing text and metadata
        """
        try:
            pdf_path = Path(pdf_path)
            text = self.extract_text(str(pdf_path))
            
            if text is None:
                return None
            
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata = pdf_reader.metadata
                
                return {
                    'text':  text,
                    'filename': pdf_path.name,
                    'num_pages': len(pdf_reader.pages),
                    'char_count': len(text),
                    'word_count': len(text.split()),
                    'metadata': {
                        'author': metadata.get('/Author', 'Unknown'),
                        'creator': metadata.get('/Creator', 'Unknown'),
                        'producer': metadata.get('/Producer', 'Unknown'),
                        'subject': metadata.get('/Subject', 'Unknown'),
                        'title': metadata.get('/Title', 'Unknown'),
                    } if metadata else {}
                }
                
        except Exception as e: 
            logger.error(f"Error extracting metadata:  {str(e)}")
            return None


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Convenience function to extract text from PDF
    
    Args:
        pdf_path (str): Path to PDF file
        
    Returns: 
        str: Extracted text
    """
    extractor = PDFExtractor()
    return extractor.extract_text(pdf_path)


# Example usage
if __name__ == "__main__":
    # Test the extractor
    extractor = PDFExtractor()
    
    # Example:  Extract from a sample PDF
    sample_pdf = "data/samples/sample_report.pdf"
    
    print("="*50)
    print("PDF Text Extractor - Test")
    print("="*50)
    
    result = extractor.extract_with_metadata(sample_pdf)
    
    if result:
        print(f"\n✅ Extraction Successful!")
        print(f"Filename: {result['filename']}")
        print(f"Pages: {result['num_pages']}")
        print(f"Characters: {result['char_count']}")
        print(f"Words: {result['word_count']}")
        print(f"\nFirst 500 characters:\n{result['text'][:500]}")
    else:
        print("\n❌ Extraction Failed!")
        print("Make sure to add a sample PDF to data/samples/")