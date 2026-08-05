def extract_text_content(content) -> str:
    """
    Safely extracts clean string text from AIMessage content, supporting:
    - Plain strings
    - Lists of content block dicts (e.g., [{'type': 'text', 'text': '...', 'extras': ...}])
    - Lists containing strings
    """
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        text_parts = []
        for block in content:
            if isinstance(block, dict) and "text" in block:
                text_parts.append(block["text"])
            elif isinstance(block, str):
                text_parts.append(block)
        if text_parts:
            return "\n".join(text_parts)
    return str(content)
