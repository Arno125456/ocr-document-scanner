import cv2
import numpy as np
from ocr_handler import OCRHandler
from text_categorizer import TextCategorizer

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

    def detect_document_type(self, image):
        """
        Detect document type based on visual features and OCR preview
        """
        # Get a quick OCR preview from the center region (where text usually is)
        h, w = image.shape[:2]
        center_crop = image[h//4:3*h//4, w//4:3*w//4]
        
        try:
            import pytesseract
            preview_text = pytesseract.image_to_string(
                cv2.cvtColor(center_crop, cv2.COLOR_BGR2GRAY),
                config='--psm 6',
                lang='eng+tha'
            ).lower()
            
            # Score each document type
            type_scores = {}
            for doc_type, keywords in self.doc_type_keywords.items():
                score = sum(1 for keyword in keywords if keyword in preview_text)
                type_scores[doc_type] = score
            
            # Return the type with highest score
            if max(type_scores.values()) > 0:
                doc_type = max(type_scores, key=type_scores.get)
                confidence = type_scores[doc_type] / len(self.doc_type_keywords[doc_type])
                return doc_type, confidence
            else:
                return 'general', 0.5
                
        except:
            return 'general', 0.5

    def enhance_image_for_detection(self, image):
        """
        Apply multiple enhancement techniques for better document detection
        """
        # Convert to LAB color space for better contrast handling
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to L channel
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced_l = clahe.apply(l)
        
        # Merge back and convert to BGR
        enhanced_lab = cv2.merge([enhanced_l, a, b])
        enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
        
        return enhanced

    def detect_document_contour_advanced(self, image):
        """
        Advanced document contour detection using multiple methods
        """
        contours_found = []
        
        # Method 1: Edge-based detection (original)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 75, 200)
        
        # Apply morphological operations to close gaps
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel, iterations=2)
        
        contours1, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_found.extend(contours1)
        
        # Method 2: Threshold-based detection (for documents with different background)
        # Otsu's thresholding
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Morphological operations to connect text regions
        kernel_large = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        dilated = cv2.dilate(thresh, kernel_large, iterations=3)
        eroded = cv2.erode(dilated, kernel_large, iterations=2)
        
        contours2, _ = cv2.findContours(eroded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_found.extend(contours2)
        
        # Method 3: Adaptive threshold (for varying lighting conditions)
        adaptive_thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        contours3, _ = cv2.findContours(adaptive_thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_found.extend(contours3)
        
        # Combine all contours and find the best document contour
        all_contours = []
        for cnt in contours_found:
            if cv2.contourArea(cnt) > 1000:  # Filter small noise
                all_contours.append(cnt)
        
        # Sort by area (largest first)
        all_contours = sorted(all_contours, key=cv2.contourArea, reverse=True)
        
        # Find the best rectangular contour
        best_contour = None
        best_score = 0
        
        for contour in all_contours[:10]:  # Check top 10 largest contours
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            
            # Score based on: number of points, area, rectangularity
            score = 0
            
            # Prefer 4-point contours
            if len(approx) == 4:
                score += 50
            
            # Check rectangularity (how close to a perfect rectangle)
            x, y, w, h = cv2.boundingRect(approx)
            rect_area = w * h
            contour_area = cv2.contourArea(contour)
            if rect_area > 0:
                rectangularity = contour_area / rect_area
                score += rectangularity * 30
            
            # Prefer larger contours (but not the entire image)
            img_area = image.shape[0] * image.shape[1]
            area_ratio = contour_area / img_area
            if 0.1 < area_ratio < 0.95:  # Not too small, not the whole image
                score += 20
            
            if score > best_score:
                best_score = score
                best_contour = approx
        
        # If no good contour found, use the largest contour
        if best_contour is None and all_contours:
            largest = max(all_contours, key=cv2.contourArea)
            peri = cv2.arcLength(largest, True)
            best_contour = cv2.approxPolyDP(largest, 0.04 * peri, True)
        
        # If still nothing, return image bounds
        if best_contour is None or len(best_contour) < 3:
            h, w = gray.shape[:2]
            best_contour = np.array([[[0, 0]], [[w, 0]], [[w, h]], [[0, h]]], dtype=np.int32)
        
        return best_contour, image

    def detect_document_contour(self, image_path):
        """
        Detect the document contour in the image using enhanced methods
        """
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image from {image_path}")
        
        # Enhance image for better detection
        enhanced = self.enhance_image_for_detection(image)
        
        # Use advanced detection
        contour, original_image = self.detect_document_contour_advanced(enhanced)
        
        return contour, original_image

    def order_points(self, pts):
        """
        Order points in clockwise order: top-left, top-right, bottom-right, bottom-left
        """
        rect = np.zeros((4, 2), dtype="float32")
        
        # Sort by x-coordinate
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]  # top-left (smallest sum)
        rect[2] = pts[np.argmax(s)]  # bottom-right (largest sum)
        
        # Compute the difference between points
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]  # top-right (smallest diff)
        rect[3] = pts[np.argmax(diff)]  # bottom-left (largest diff)
        
        return rect

    def perspective_transform(self, image, contour):
        """
        Apply perspective transformation to get a top-down view of the document
        """
        # Reshape contour to get points
        try:
            points = contour.reshape(len(contour), 2)
        except:
            return image
        
        # If we don't have 4 points, approximate to 4
        if len(points) != 4:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            if len(approx) >= 4:
                points = approx[:4].reshape(4, 2)
            else:
                # Use bounding box if approximation fails
                x, y, w, h = cv2.boundingRect(contour)
                points = np.array([[x, y], [x+w, y], [x+w, y+h], [x, y+h]], dtype=np.float32)
        
        # Order points correctly
        rect = self.order_points(points.astype(np.float32))
        
        # Calculate dimensions
        (tl, tr, br, bl) = rect
        
        # Calculate width of new image
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB), 100)
        
        # Calculate height of new image
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB), 100)
        
        # Define destination points
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")
        
        # Calculate perspective transform matrix
        M = cv2.getPerspectiveTransform(rect, dst)
        
        # Apply perspective transform
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        
        return warped

    def apply_document_enhancement(self, image):
        """
        Apply enhancements specifically for document images to improve OCR
        """
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Apply adaptive thresholding for better text contrast
        enhanced = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Remove small noise
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(enhanced, cv2.MORPH_OPEN, kernel, iterations=1)
        
        # Convert back to BGR for consistency
        return cv2.cvtColor(cleaned, cv2.COLOR_GRAY2BGR)

    def detect_and_crop(self, image_path):
        """
        Detect document in image and crop it with enhanced processing
        """
        try:
            # Detect document contour
            contour, image = self.detect_document_contour(image_path)
            
            # Apply perspective transformation
            cropped_image = self.perspective_transform(image, contour)
            
            # Apply document enhancement for better OCR
            enhanced_image = self.apply_document_enhancement(cropped_image)
            
            return enhanced_image
        except Exception as e:
            print(f"Document detection failed: {e}. Returning original image.")
            return cv2.imread(image_path)

    def extract_text(self, image, lang='eng', return_regions=False):
        """
        Extract text from the image using OCR

        Args:
            image: OpenCV image array
            lang: Language code for OCR (e.g., 'eng', 'tha', 'eng+tha')
            return_regions: If True, return text regions with bounding boxes
        """
        try:
            return self.ocr_handler.extract_text_with_tesseract(image, lang=lang, return_regions=return_regions)
        except Exception as e:
            print(f"OCR extraction failed: {e}")
            return "OCR extraction failed", {}, []

    def categorize_text(self, text):
        """
        Categorize the extracted text with document type awareness
        """
        try:
            # Get base categorization
            categories = self.text_categorizer.categorize_text(text)
            
            # Add document type information
            categories['document_type'] = 'general'
            
            # Simple document type detection based on keywords
            text_lower = text.lower()
            for doc_type, keywords in self.doc_type_keywords.items():
                if any(keyword in text_lower for keyword in keywords):
                    categories['document_type'] = doc_type
                    break
            
            return categories
        except Exception as e:
            print(f"Text categorization failed: {e}")
            return {
                'title': [],
                'date': [],
                'name': [],
                'email': [],
                'phone': [],
                'amount': [],
                'items': [],
                'other': [],
                'document_type': 'unknown'
            }
