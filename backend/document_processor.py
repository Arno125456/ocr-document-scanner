import pytesseract
from PIL import Image
import numpy as np

class DocumentProcessor:
    def __init__(self):
        self.ocr_handler = OCRHandler()
        self.text_categorizer = TextCategorizer()
        
        # Document type indicators
        self.doc_type_keywords = {
            'invoice': ['invoice', 'bill', 'payment', 'total', 'amount due', 'tax', 'vat', 'ใบแจ้งหนี้', 'ใบเสร็จ'],
            'receipt': ['receipt', 'purchase', 'transaction', 'cash', 'credit', 'ใบเสร็จรับเงิน'],
            'contract': ['agreement', 'contract', 'party', 'terms', 'conditions', 'signature', 'สัญญา', 'ข้อตกลง'],
            'letter': ['dear', 'sincerely', 'regards', 'subject', 'reference', 'เรียน', 'ขอแสดงความนับถือ'],
            'report': ['report', 'summary', 'conclusion', 'findings', 'analysis', 'รายงาน', 'สรุป'],
            'form': ['form', 'application', 'name', 'address', 'phone', 'email', 'แบบฟอร์ม', 'สมัคร'],
            'id_card': ['identification', 'id no', 'card no', 'national id', 'บัตรประชาชน', 'เลขที่'],
            'bank_statement': ['statement', 'account no', 'balance', 'transaction', 'bank', 'ยอดเงิน', 'บัญชี'],
        }

    def detect_document_type(self, image, text):
        """Detect document type based on text content"""
        text_lower = text.lower()
        type_scores = {}
        
        for doc_type, keywords in self.doc_type_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            type_scores[doc_type] = score
        
        if max(type_scores.values(), default=0) > 0:
            return max(type_scores, key=type_scores.get)
        return 'general'

    def detect_and_crop(self, image_path):
        """
        For simplicity, just return the image without cropping.
        In production, you'd want to add proper document detection.
        """
        from PIL import Image
        return np.array(Image.open(image_path))

    def extract_text(self, image, lang='eng', return_regions=False):
        """Extract text using pytesseract"""
        try:
            if isinstance(image, str):
                from PIL import Image
                image = np.array(Image.open(image))
            
            return self.ocr_handler.extract_text_with_tesseract(image, lang=lang, return_regions=return_regions)
        except Exception as e:
            print(f"OCR extraction failed: {e}")
            return "OCR extraction failed", {}, []

    def categorize_text(self, text):
        """Categorize extracted text"""
        try:
            return self.text_categorizer.categorize_text(text)
        except Exception as e:
            print(f"Text categorization failed: {e}")
            return {
                'title': [],
                'date': [],
                'name': [],
                'email': [],
                'phone': [],
                'amount': [],
                'address': [],
                'tax_id': [],
                'invoice_number': [],
                'items': [],
                'other': [],
                'document_type': 'unknown'
            }
