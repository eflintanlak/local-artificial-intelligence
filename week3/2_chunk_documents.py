import os

documents_folder = "documents"

def load_and_chunk_documents():
    all_chunks = []
    
    files = os.listdir(documents_folder)
    
    for filename in files:
        filepath = os.path.join(documents_folder, filename)
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        paragraphs = content.split("\n\n")
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            
            if len(paragraph) < 40:
                continue
            
            all_chunks.append({
                "source": filename,
                "text": paragraph
            })
    
    return all_chunks

chunks = load_and_chunk_documents()

print(f"Total chunks created: {len(chunks)}\n")

for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1} (from {chunk['source']}):")
    print(f"  {chunk['text'][:80]}...")
    print()