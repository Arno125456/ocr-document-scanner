import pytesseract
from PIL import Image
import cv2
import numpy as np
import os

class OCRHandler:
    def __init__(self):
        # Set Tesseract path for Windows
        tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        import os
        if os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            self.tesseract_available = True
            print(f"Tesseract found at: {tesseract_path}")
        else:
            # Try other common paths
            possible_paths = [
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                r'C:\Users\Public\tesseract.exe',
                r'C:\tesseract\tesseract.exe'
            ]

            for path in possible_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    self.tesseract_available = True
                    print(f"Tesseract found at: {path}")
                    break
            else:
                # Try to find in PATH
                try:
                    pytesseract.get_tesseract_version()
                    self.tesseract_available = True
                    print("Tesseract found in PATH")
                except:
                    print("Warning: Tesseract is not installed or not found in common locations.")
                    print("Please install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki")
                    self.tesseract_available = False

    def preprocess_for_ocr(self, image):
        """
        Preprocess the image to improve OCR accuracy
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # Apply threshold to get image with only black and white
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Apply median blur to remove noise
        denoised = cv2.medianBlur(thresh, 3)

        # Convert to PIL Image for pytesseract
        pil_image = Image.fromarray(denoised)

        return pil_image

    def extract_text_with_tesseract(self, image, lang='eng', return_regions=False):
        """
        Extract text from image using Tesseract OCR

        Args:
            image: OpenCV image array
            lang: Language code for OCR (e.g., 'eng', 'tha', 'eng+tha')
            return_regions: If True, return text regions with bounding boxes
        """
        if not self.tesseract_available:
            # Return a mock response when Tesseract is not available
            return "Tesseract OCR not available. Please install Tesseract.", {}, []

        # Store original image shape for region calculation
        original_shape = image.shape
        
        # Preprocess image
        processed_img = self.preprocess_for_ocr(image)

        # Configure tesseract options for better accuracy
        # psm 6: Assume a single uniform block of text
        # psm 3: Fully automatic page segmentation, but no OSD
        config = '--oem 3 --psm 6'

        try:
            # Extract text with specified language
            # For Thai, use 'tha' or 'eng+tha' for mixed languages
            text = pytesseract.image_to_string(processed_img, lang=lang, config=config)

            # Extract detailed data for potential highlighting
            data = pytesseract.image_to_data(processed_img, output_type=pytesseract.Output.DICT, config=config, lang=lang)

            # Extract text regions with bounding boxes if requested
            regions = []
            if return_regions:
                regions = self._extract_text_regions(data, original_shape)
                print(f"Extracted {len(regions)} text regions from image of shape {original_shape}")

            return text.strip(), data, regions
        except Exception as e:
            print(f"Error during OCR: {e}")
            return "", {}, []

    def _extract_text_regions(self, ocr_data, image_shape, merge_blocks=True):
        """
        Extract text regions with bounding boxes from OCR data
        
        Args:
            ocr_data: Dictionary from pytesseract.image_to_data
            image_shape: Tuple of (height, width) from the original image
            merge_blocks: If True, merge nearby words into lines/blocks
            
        Returns:
            List of dictionaries with text, confidence, and bounding box coordinates
        """
        img_h, img_w = image_shape[:2]
        
        # First pass: collect all word-level regions
        word_regions = []
        n_boxes = len(ocr_data.get('level', []))
        
        for i in range(n_boxes):
            text = ocr_data.get('text', [''])[i].strip()
            conf = int(ocr_data.get('conf', [0])[i])
            
            if text and conf > 30:
                x = ocr_data.get('left', [0])[i]
                y = ocr_data.get('top', [0])[i]
                w = ocr_data.get('width', [0])[i]
                h = ocr_data.get('height', [0])[i]
                
                word_regions.append({
                    'text': text,
                    'confidence': conf,
                    'bbox': {'x': x, 'y': y, 'width': w, 'height': h},
                    'center_y': y + h/2  # For line detection
                })
        
        if not merge_blocks:
            # Return word-level regions
            return self._convert_to_percentages(word_regions, img_w, img_h)
        
        # Merge words into lines and blocks
        merged_regions = self._merge_word_regions(word_regions, img_w, img_h)
        return merged_regions

    def _merge_word_regions(self, word_regions, img_w, img_h):
        """
        Merge nearby word regions into lines and text blocks
        
        Strategy:
        1. Group words by line (similar y-coordinate)
        2. Merge words in same line into line-level regions
        3. Optionally merge nearby lines into paragraph blocks
        """
        if not word_regions:
            return []
        
        # Sort by y-coordinate (top to bottom)
        sorted_regions = sorted(word_regions, key=lambda r: r['center_y'])
        
        # Group into lines
        lines = []
        current_line = [sorted_regions[0]]
        line_threshold = 10  # Pixels tolerance for same line
        
        for i in range(1, len(sorted_regions)):
            region = sorted_regions[i]
            prev_region = current_line[-1]
            
            # Check if this word is on the same line
            y_diff = abs(region['center_y'] - prev_region['center_y'])
            
            if y_diff <= line_threshold:
                current_line.append(region)
            else:
                # Save current line and start new one
                if current_line:
                    lines.append(current_line)
                current_line = [region]
        
        # Don't forget the last line
        if current_line:
            lines.append(current_line)
        
        # Merge each line into a single region
        line_regions = []
        for line in lines:
            if not line:
                continue
            
            # Sort line by x-coordinate (left to right)
            line_sorted = sorted(line, key=lambda r: r['bbox']['x'])
            
            # Calculate merged bounding box
            min_x = min(r['bbox']['x'] for r in line_sorted)
            min_y = min(r['bbox']['y'] for r in line_sorted)
            max_x = max(r['bbox']['x'] + r['bbox']['width'] for r in line_sorted)
            max_y = max(r['bbox']['y'] + r['bbox']['height'] for r in line_sorted)
            
            # Merge text
            merged_text = ' '.join(r['text'] for r in line_sorted)
            
            # Average confidence
            avg_conf = sum(r['confidence'] for r in line_sorted) / len(line_sorted)
            
            line_regions.append({
                'text': merged_text,
                'confidence': avg_conf,
                'bbox': {
                    'x': min_x,
                    'y': min_y,
                    'width': max_x - min_x,
                    'height': max_y - min_y,
                }
            })
        
        # Convert to percentages
        return self._convert_to_percentages(line_regions, img_w, img_h)

    def _convert_to_percentages(self, regions, img_w, img_h):
        """Convert pixel coordinates to percentages for responsive display"""
        converted = []
        for region in regions:
            converted.append({
                'text': region['text'],
                'confidence': region['confidence'],
                'bbox': {
                    'x': region['bbox']['x'],
                    'y': region['bbox']['y'],
                    'width': region['bbox']['width'],
                    'height': region['bbox']['height'],
                    'x_percent': (region['bbox']['x'] / img_w) * 100 if img_w > 0 else 0,
                    'y_percent': (region['bbox']['y'] / img_h) * 100 if img_h > 0 else 0,
                    'width_percent': (region['bbox']['width'] / img_w) * 100 if img_w > 0 else 0,
                    'height_percent': (region['bbox']['height'] / img_h) * 100 if img_h > 0 else 0,
                }
            })
        return converted