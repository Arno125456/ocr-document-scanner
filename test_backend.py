"""
Simple test script to verify backend functionality
Note: This is a basic test that checks if the modules can be imported
and basic functions work. For full testing, you would need sample images.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test if all modules can be imported without errors"""
    try:
        from document_processor import DocumentProcessor
        from ocr_handler import OCRHandler
        from text_categorizer import TextCategorizer
        print("[OK] All modules imported successfully")
        return True
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        return False

def test_basic_functions():
    """Test basic functionality of the components"""
    try:
        # Test TextCategorizer
        from text_categorizer import TextCategorizer
        categorizer = TextCategorizer()
        
        # Test with sample text
        sample_text = """
        John Doe
        john.doe@example.com
        123-456-7890
        Invoice Date: 2023-05-15
        Total Amount: $1,250.00
        """
        
        result = categorizer.categorize_text(sample_text)
        
        print("[OK] Text categorizer works")
        print(f"  Found {len(result['name'])} names, {len(result['email'])} emails, "
              f"{len(result['date'])} dates, {len(result['amount'])} amounts")
        return True
    except Exception as e:
        print(f"[ERROR] Function test error: {e}")
        return False

def main():
    print("Testing OCR Document Categorizer Backend...")
    print()
    
    success = True
    success &= test_imports()
    success &= test_basic_functions()
    
    print()
    if success:
        print("[OK] All basic tests passed!")
        print("Note: For complete testing, you need to run the API server and test with actual images.")
    else:
        print("[ERROR] Some tests failed!")
        
    return success

if __name__ == "__main__":
    main()