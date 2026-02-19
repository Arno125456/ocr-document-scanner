import re
from datetime import datetime

class TextCategorizer:
    def __init__(self):
        self.patterns = {
            'date': [
                r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
                r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',
                r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b',
                r'\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b',
                # Thai date patterns (e.g., 1 มกราคม 2567)
                r'\b\d{1,2}\s+(?:ม\.?ค\.?|ก\.?พ\.?|มี\.?ค\.?|เม\.?ย\.?|พ\.?ค\.?|มิ\.?ย\.?|ก\.?ค\.?|ส\.?ค\.?|ก\.?ย\.?|ต\.?ค\.?|พ\.?ย\.?|ธ\.?ค\.?|[a-zA-Zก-ฮ]+)\s+\d{4}\b',
                # Thai Buddhist year dates
                r'\b\d{1,2}\s+[ก-ฮ]+\s+พ\.?ศ\.?\s*\d{4}\b',
            ],
            'email': [
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[ก-ฮ]{2,}\b',
            ],
            'phone': [
                r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
                r'\+\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b',
                # Thai phone numbers (e.g., 081-234-5678, 02-123-4567)
                r'\b\d{2,3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
                r'\b0\d{1}[-.\s]?\d{3}[-.\s]?\d{4}\b',
            ],
            'amount': [
                r'\$\s*\d+(?:[,\.]\d{2,})?',
                r'\b\d+(?:[,\.]\d{2,})?\s*\$',
                # Thai Baht patterns (e.g., 1,234.56 บาท, ฿1,234.56)
                r'\b\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*บาท\b',
                r'฿\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?',
                # Numbers with currency words
                r'\b\d{1,3}(?:,\d{3})*\s*(?:USD|EUR|GBP|THB|Baht)\b',
            ],
            'name': [
                r'(?:Name|Customer|Client|ชื่อ|ลูกค้า|ผู้ซื้อ|ผู้ขาย):\s*([A-Za-z][a-z]+\s*[A-Za-z][a-z]*)',
                r'^([A-Z][a-z]+\s+[A-Z][a-z]+)$',
                # Thai names (Thai script characters)
                r'(?:ชื่อ|นามสกุล|ลูกค้า|นาย|นาง|นางสาว):\s*([\u0E00-\u0E7F]{2,})',
                # Thai title prefixes
                r'^(นาย|นาง|นางสาว|ดร\.|ผศ\.|รศ\.|ศ\.)\s+([\u0E00-\u0E7F]+)',
            ],
            'address': [
                r'\b\d{1,5}\s+[A-Za-z]+\s+(?:Street|St|Road|Rd|Avenue|Ave|Boulevard|Blvd|Lane|Ln|Drive|Dr)\b',
                r'(?:Address|ที่อยู่|ที่อยู่จัดส่ง):\s*(.+)',
                # Thai address patterns
                r'\b(?:หมู่|ซอย|ถนน|แขวง|เขต|อำเภอ|จังหวัด)\s+[\u0E00-\u0E7F0-9]+',
            ],
            'tax_id': [
                # US EIN
                r'\b\d{2}-\d{7}\b',
                # Thai Tax ID
                r'\b\d{13}\b',
                # VAT number
                r'\b(?:VAT|Tax ID|ภาษี)\s*[:.-]?\s*\d{9,13}\b',
            ],
            'invoice_number': [
                r'(?:Invoice|Bill|Receipt|Order|Invoice No|Bill No|เลขที่)\s*[:.-]?\s*[A-Za-z0-9-]+',
                r'\b(?:INV|INV-\d|2\d{3})[A-Za-z0-9-]{4,}\b',
            ],
        }

        # Thai keywords for categorization
        self.thai_keywords = {
            'items': ['สินค้า', 'รายการ', 'ปริมาณ', 'จำนวน', 'หน่วย', 'ราคา/หน่วย', 'รวม'],
            'title_indicators': ['ใบเสร็จ', 'ใบแจ้งหนี้', 'ใบกำกับภาษี', 'รายงาน', 'เอกสาร', 'หัวข้อ', 'เรื่อง', 'ใบสำคัญ'],
            'section_headers': ['หมวด', 'ส่วนที่', 'หัวข้อ', 'มาตรา', 'ข้อ'],
        }

        # Document type specific patterns
        self.doc_type_patterns = {
            'invoice': {
                'headers': ['invoice', 'tax invoice', 'ใบกำกับภาษี', 'ใบแจ้งหนี้'],
                'fields': ['invoice no', 'invoice date', 'due date', 'amount due', 'total']
            },
            'receipt': {
                'headers': ['receipt', 'payment receipt', 'ใบเสร็จรับเงิน'],
                'fields': ['receipt no', 'payment date', 'amount received', 'payment method']
            },
            'contract': {
                'headers': ['agreement', 'contract', 'สัญญา', 'ข้อตกลง'],
                'fields': ['party', 'effective date', 'term', 'termination']
            },
            'letter': {
                'headers': ['dear', 'learn', 'เรียน'],
                'fields': ['subject', 'reference', 'เรื่อง', 'อ้างถึง']
            },
            'report': {
                'headers': ['report', 'รายงาน', 'สรุปผล'],
                'fields': ['executive summary', 'findings', 'conclusion', 'recommendations']
            },
            'id_card': {
                'headers': ['identification card', 'บัตรประชาชน', 'national id'],
                'fields': ['id no', 'name', 'surname', 'date of birth', 'address']
            },
            'bank_statement': {
                'headers': ['statement', 'bank statement', 'ยอดบัญชี'],
                'fields': ['account no', 'account name', 'balance', 'transaction date']
            },
        }

    def detect_document_type(self, text):
        """
        Detect the type of document based on content
        """
        text_lower = text.lower()
        type_scores = {}
        
        for doc_type, patterns in self.doc_type_patterns.items():
            score = 0
            # Check for headers
            for header in patterns['headers']:
                if header in text_lower:
                    score += 3
            # Check for fields
            for field in patterns['fields']:
                if field in text_lower:
                    score += 1
            type_scores[doc_type] = score
        
        # Return the type with highest score
        if max(type_scores.values()) > 0:
            return max(type_scores, key=type_scores.get)
        return 'general'

    def detect_section_headers(self, lines):
        """
        Detect section/heading lines in the document
        """
        sections = []
        section_patterns = [
            r'^\d+\.\s+[A-Z]',  # "1. Introduction"
            r'^[A-Z][A-Z\s]+$',  # "INTRODUCTION" (all caps)
            r'^[IVX]+\.',  # Roman numerals "I.", "II."
            r'^section\s+\d+',  # "Section 1"
            r'^article\s+\d+',  # "Article 1"
            r'^หมวด\s+\d+',  # Thai "หมวด 1"
            r'^ส่วนที่\s+\d+',  # Thai "ส่วนที่ 1"
            r'^ข้อ\s+\d+',  # Thai "ข้อ 1"
            r'^มาตรา\s+\d+',  # Thai "มาตรา 1"
        ]
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            for pattern in section_patterns:
                if re.match(pattern, line_stripped, re.IGNORECASE):
                    sections.append((i, line_stripped))
                    break
        
        return sections

    def categorize_by_sections(self, text, lines):
        """
        Categorize text based on detected sections/headings
        """
        sections = self.detect_section_headers(lines)
        categorized_sections = {}
        
        if len(sections) >= 2:
            # Group content between section headers
            for i in range(len(sections)):
                start_idx = sections[i][0]
                end_idx = sections[i + 1][0] if i + 1 < len(sections) else len(lines)
                
                section_title = sections[i][1]
                section_content = lines[start_idx + 1:end_idx]
                
                # Categorize content within this section
                section_data = {
                    'title': section_title,
                    'content': [line.strip() for line in section_content if line.strip()],
                    'category': self._infer_section_category(section_title)
                }
                categorized_sections[section_title] = section_data
        
        return categorized_sections

    def _infer_section_category(self, section_title):
        """
        Infer the category of a section based on its title
        """
        title_lower = section_title.lower()
        
        category_keywords = {
            'introduction': ['introduction', 'overview', 'background', 'preface', 'บทนำ', 'บทคัดย่อ'],
            'terms_conditions': ['terms', 'conditions', 'agreement', 'clause', 'ข้อกำหนด', 'เงื่อนไข'],
            'financial': ['payment', 'price', 'cost', 'fee', 'amount', 'financial', 'การเงิน', 'ราคา'],
            'contact': ['contact', 'address', 'phone', 'email', 'ติดต่อ', 'ที่อยู่'],
            'dates': ['date', 'deadline', 'effective', 'duration', 'วันที่', 'ระยะเวลา'],
            'parties': ['party', 'party a', 'party b', 'between', 'คู่สัญญา', 'ระหว่าง'],
            'signatures': ['signature', 'signed', 'witness', 'ลงนาม', 'ลายเซ็น', 'พยาน'],
            'items': ['item', 'product', 'description', 'quantity', 'สินค้า', 'รายการ'],
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in title_lower for keyword in keywords):
                return category
        
        return 'general'

    def categorize_text(self, text):
        lines = text.split('\n')
        categories = {
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
            'document_type': 'unknown',
            'sections': {}
        }

        # Detect document type
        categories['document_type'] = self.detect_document_type(text)

        # Extract title (usually first significant line)
        for line in lines[:5]:
            line = line.strip()
            if len(line) > 3:
                is_not_title = any(keyword in line.lower() for keyword in ['total', 'amount', 'date', 'email', 'page'])
                is_thai_title = any(keyword in line for keyword in self.thai_keywords['title_indicators'])
                if not is_not_title and (is_thai_title or len(line) > 5):
                    categories['title'].append(line)
                    break

        # Process each line for categorization
        for line in lines:
            line = line.strip()
            if not line or len(line) < 3:
                continue

            categorized = False

            # Check against patterns
            for category, patterns in self.patterns.items():
                if category in ['title', 'items', 'other', 'document_type', 'sections']:
                    continue
                    
                for pattern in patterns:
                    try:
                        matches = re.findall(pattern, line, re.IGNORECASE)
                        if matches:
                            categories[category].extend([str(m) for m in matches])
                            categorized = True
                            break
                    except:
                        continue
                if categorized:
                    break

            # If not categorized by patterns, classify as item or other
            if not categorized:
                # Check for English and Thai item keywords
                is_item = any(word in line.lower() for word in ['item', 'product', 'service', 'qty', 'quantity', 'description'])
                is_thai_item = any(word in line for word in self.thai_keywords['items'])
                is_section_header = any(word in line for word in self.thai_keywords['section_headers'])
                
                if is_item or is_thai_item:
                    categories['items'].append(line)
                elif is_section_header or (len(line) > 5 and line.isupper()):
                    # Potential section header
                    categories['other'].append(line)
                else:
                    categories['other'].append(line)

        # Detect sections for structured documents
        categories['sections'] = self.categorize_by_sections(text, lines)

        # Remove duplicates while preserving order
        for category in categories:
            if category == 'sections':
                continue
            unique_items = []
            for item in categories[category]:
                if item not in unique_items:
                    unique_items.append(item)
            categories[category] = unique_items

        return categories
