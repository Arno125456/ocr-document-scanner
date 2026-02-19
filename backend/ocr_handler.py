from PIL import Image
import numpy as np

class OCRHandler:
    def __init__(self):
        self.tesseract_available = False
        try:
            import pytesseract
            self.pytesseract = pytesseract
            self.tesseract_available = True
            print("Tesseract found")
        except:
            print("Tesseract not available - OCR will use fallback")
            self.tesseract_available = False

    def extract_text_with_tesseract(self, image, lang='eng', return_regions=False):
        """Extract text from image"""
        import time
        start_time = time.time()
        
        if not self.tesseract_available:
            # Fallback: return image info only
            if isinstance(image, np.ndarray):
                h, w = image.shape[:2]
                return f"Image {w}x{h} - Tesseract not available", {}, []
            return "Tesseract not available", {}, []
        
        try:
            print(f"Starting OCR on image shape: {image.shape if isinstance(image, np.ndarray) else 'PIL'}, lang: {lang}")
            
            # Convert to PIL Image
            if isinstance(image, np.ndarray):
                pil_image = Image.fromarray(image)
            else:
                pil_image = image
            
            # Extract text - limit processing time
            config = '--oem 3 --psm 6'
            print("Running image_to_string...")
            text = self.pytesseract.image_to_string(pil_image, lang=lang, config=config, timeout=30)
            print(f"OCR completed in {time.time() - start_time:.2f}s, text length: {len(text)}")
            
            # Extract regions if requested (with timeout)
            regions = []
            if return_regions:
                print("Extracting text regions...")
                data = self.pytesseract.image_to_data(pil_image, output_type=self.pytesseract.Output.DICT, config=config, lang=lang, timeout=30)
                regions = self._extract_regions(data, image.shape if isinstance(image, np.ndarray) else (pil_image.height, pil_image.width))
                print(f"Extracted {len(regions)} regions")
            
            return text.strip() if text else "No text detected", {}, regions
        except Exception as e:
            print(f"OCR error after {time.time() - start_time:.2f}s: {e}")
            return f"OCR error: {str(e)}", {}, []

    def _extract_regions(self, ocr_data, image_shape):
        """Extract text regions with bounding boxes"""
        regions = []
        img_h, img_w = image_shape[:2]
        n_boxes = len(ocr_data.get('level', []))
        
        for i in range(n_boxes):
            text = ocr_data.get('text', [''])[i].strip()
            conf = int(ocr_data.get('conf', [0])[i])
            
            if text and conf > 30:
                x = ocr_data.get('left', [0])[i]
                y = ocr_data.get('top', [0])[i]
                w = ocr_data.get('width', [0])[i]
                h = ocr_data.get('height', [0])[i]
                
                regions.append({
                    'text': text,
                    'confidence': conf,
                    'bbox': {
                        'x': x, 'y': y, 'width': w, 'height': h,
                        'x_percent': (x / img_w) * 100 if img_w > 0 else 0,
                        'y_percent': (y / img_h) * 100 if img_h > 0 else 0,
                        'width_percent': (w / img_w) * 100 if img_w > 0 else 0,
                        'height_percent': (h / img_h) * 100 if img_h > 0 else 0,
                    }
                })
        
        # Merge into lines
        return self._merge_to_lines(regions, img_w, img_h)

    def _merge_to_lines(self, regions, img_w, img_h):
        """Merge word regions into lines"""
        if not regions:
            return []
        
        sorted_regions = sorted(regions, key=lambda r: r['bbox']['y'])
        lines = []
        current_line = [sorted_regions[0]]
        threshold = 10
        
        for i in range(1, len(sorted_regions)):
            region = sorted_regions[i]
            prev = current_line[-1]
            y_diff = abs(region['bbox']['y'] - prev['bbox']['y'])
            
            if y_diff <= threshold:
                current_line.append(region)
            else:
                if current_line:
                    lines.append(current_line)
                current_line = [region]
        
        if current_line:
            lines.append(current_line)
        
        # Merge each line
        merged = []
        for line in lines:
            line_sorted = sorted(line, key=lambda r: r['bbox']['x'])
            min_x = min(r['bbox']['x'] for r in line_sorted)
            min_y = min(r['bbox']['y'] for r in line_sorted)
            max_x = max(r['bbox']['x'] + r['bbox']['width'] for r in line_sorted)
            max_y = max(r['bbox']['y'] + r['bbox']['height'] for r in line_sorted)
            
            merged.append({
                'text': ' '.join(r['text'] for r in line_sorted),
                'confidence': sum(r['confidence'] for r in line_sorted) / len(line_sorted),
                'bbox': {
                    'x': min_x, 'y': min_y, 'width': max_x - min_x, 'height': max_y - min_y,
                    'x_percent': (min_x / img_w) * 100,
                    'y_percent': (min_y / img_h) * 100,
                    'width_percent': ((max_x - min_x) / img_w) * 100,
                    'height_percent': ((max_y - min_y) / img_h) * 100,
                }
            })
        
        return merged
