from PIL import Image
import numpy as np
import io
import os

class OCRHandler:
    def __init__(self):
        self.vision_available = False
        try:
            from google.cloud import vision
            self.client = vision.ImageAnnotatorClient()
            self.vision_available = True
            print("✅ Google Cloud Vision initialized")
        except Exception as e:
            print(f"⚠️ Google Cloud Vision not available: {e}")
            self.client = None
            self.vision_available = False

    def extract_text_with_tesseract(self, image, lang='eng', return_regions=False):
        """Extract text using Google Cloud Vision API"""
        import time
        start_time = time.time()
        
        try:
            print(f"🔍 Starting Google Cloud Vision OCR...")
            
            # Convert image to bytes
            if isinstance(image, np.ndarray):
                pil_image = Image.fromarray(image)
            else:
                pil_image = image
            
            img_byte_arr = io.BytesIO()
            pil_image.save(img_byte_arr, format='PNG')
            img_bytes = img_byte_arr.getvalue()
            
            print(f"📊 Image size: {len(img_bytes)} bytes")
            
            # Create Vision image
            from google.cloud import vision
            vision_image = vision.Image(content=img_bytes)
            
            # Detect text
            print("📝 Detecting text...")
            text_response = self.client.text_detection(image=vision_image)
            texts = text_response.text_annotations
            
            if texts:
                full_text = texts[0].description
                print(f"✅ OCR completed in {time.time() - start_time:.2f}s")
                print(f"📄 Extracted {len(full_text)} characters")
            else:
                full_text = "No text detected"
                print(f"⚠️ No text found in {time.time() - start_time:.2f}s")
            
            # Extract regions if requested
            regions = []
            if return_regions and len(texts) > 1:
                print("📍 Extracting text regions...")
                for text_obj in texts[1:]:  # Skip first (full text)
                    vertices = text_obj.bounding_poly.vertices
                    if vertices:
                        x_coords = [v.x for v in vertices]
                        y_coords = [v.y for v in vertices]
                        x = min(x_coords)
                        y = min(y_coords)
                        w = max(x_coords) - x
                        h = max(y_coords) - y
                        
                        # Get image dimensions for percentage calculation
                        img_width = pil_image.width
                        img_height = pil_image.height
                        
                        regions.append({
                            'text': text_obj.description,
                            'confidence': 95,  # Google doesn't provide confidence for text detection
                            'bbox': {
                                'x': x,
                                'y': y,
                                'width': w,
                                'height': h,
                                'x_percent': (x / img_width) * 100 if img_width > 0 else 0,
                                'y_percent': (y / img_height) * 100 if img_height > 0 else 0,
                                'width_percent': (w / img_width) * 100 if img_width > 0 else 0,
                                'height_percent': (h / img_height) * 100 if img_height > 0 else 0,
                            }
                        })
                print(f"📍 Extracted {len(regions)} regions")
            
            # Clean up
            text_response = None
            
            return full_text.strip() if full_text else "No text detected", {}, regions
            
        except Exception as e:
            print(f"❌ Google Cloud Vision error after {time.time() - start_time:.2f}s: {e}")
            import traceback
            traceback.print_exc()
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
