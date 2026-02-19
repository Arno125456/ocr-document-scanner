import json
from datetime import datetime
from typing import Dict, Any

def export_results_to_json(result: Dict[str, Any], filename: str = None) -> str:
    """
    Export the categorized results to a JSON file
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ocr_results_{timestamp}.json"
    
    # Prepare the data to be exported
    export_data = {
        "timestamp": datetime.now().isoformat(),
        "results": result,
        "summary": {
            "total_categories": len(result),
            "total_items": sum(len(items) for items in result.values())
        }
    }
    
    # Write to file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    return filename