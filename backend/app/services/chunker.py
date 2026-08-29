import re


def semantic_chunk(text: str, max_chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    paragraphs = re.split(r'\n\s*\n', text)
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        if len(current_chunk) + len(para) < max_chunk_size:
            current_chunk += "\n\n" + para if current_chunk else para
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = para

    if current_chunk:
        chunks.append(current_chunk)

    final_chunks = []
    for chunk in chunks:
        if len(chunk) > max_chunk_size:
            words = chunk.split()
            temp = ""
            for word in words:
                if len(temp) + len(word) < max_chunk_size:
                    temp += " " + word if temp else word
                else:
                    final_chunks.append(temp)
                    temp = word
            if temp:
                final_chunks.append(temp)
        else:
            final_chunks.append(chunk)

    return final_chunks if final_chunks else [text]
