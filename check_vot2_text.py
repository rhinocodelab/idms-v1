import json

with open('app/upload_ghostlayer_docs/coordinates/20250930_115954_vot2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

full_text = data['full_text']
full_text_lower = full_text.lower()

print("Full text length:", len(full_text))
print("\nSearching for keywords:")
print("  'election commission of india':", 'election commission of india' in full_text_lower)
print("  'election commission':", 'election commission' in full_text_lower)
print("  'elector':", 'elector' in full_text_lower)
print("  'identity card':", 'identity card' in full_text_lower)

print("\nFirst 300 characters (cleaned):")
# Remove non-printable characters for display
clean_text = ''.join(c if c.isprintable() or c == '\n' else '?' for c in full_text[:300])
print(clean_text)
