from typing import Dict, List, Any, Union
from fastapi import HTTPException

def get_nested_value(obj: Union[Dict, List], path: str) -> Any:
    """Get value from nested dictionary or list using dot notation.
    Handles array indices and nested objects."""
    if not path:
        return None

    keys = path.split('.')
    current = obj

    for key in keys:
        # Handle array index if key is numeric
        if isinstance(current, list) and key.isdigit():
            index = int(key)
            if 0 <= index < len(current):
                current = current[index]
            else:
                return None
        # Handle dictionary access
        elif isinstance(current, dict):
            current = current.get(key)
            if current is None:
                return None
        else:
            return None

    return current

def transform_data(data: Dict[str, Any], mapping: Dict[str, str], array_path: str = None, preserve_null: bool = False) -> Dict[str, Any]:
    """Transform data based on mapping configuration."""
    try:
        # If we're transforming array items
        if array_path:
            source_array = get_nested_value(data, array_path)
            
            if not isinstance(source_array, list):
                raise HTTPException(
                    status_code=400,
                    detail=f"Array path '{array_path}' does not point to a list"
                )
            
            transformed_array = []
            for item in source_array:
                transformed_item = {}
                for new_key, source_path in mapping.items():
                    value = get_nested_value(item, source_path)
                    if value is not None or preserve_null:
                        transformed_item[new_key] = value
                if transformed_item:  # Only add non-empty items
                    transformed_array.append(transformed_item)
            
            return {
                "transformed_data": transformed_array,
                "items_processed": len(source_array),
                "items_transformed": len(transformed_array)
            }
        
        # Regular transformation for single object
        result = {}
        for new_key, source_path in mapping.items():
            value = get_nested_value(data, source_path)
            if value is not None or preserve_null:
                result[new_key] = value
        
        return {
            "transformed_data": result,
            "fields_mapped": len(result)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Transformation failed: {str(e)}"
        ) 