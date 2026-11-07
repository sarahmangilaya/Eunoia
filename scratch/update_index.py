import json, re

# Read current index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Load new exhibits
with open('scratch/full_catalog.json', 'r', encoding='utf-8') as f:
    full_catalog = json.load(f)

print(f'Full catalog items: {len(full_catalog)}')

# 1. Replace exhibits array in EUNOIA_CONFIG
exhibits_json = json.dumps(full_catalog, indent=4)
# Find start of exhibits: [ and end of ];
start_idx = content.find('  exhibits: [')
if start_idx == -1:
    raise ValueError("Could not find '  exhibits: [' in index.html")

end_needle = '  ]\n};\n\n/* ==========================================================================\n   §4  ENGINE'
end_idx = content.find(end_needle)
if end_idx == -1:
    # Try alternative matching
    end_needle = '];\n\n/* ==========================================================================\n   §4  ENGINE'
    end_idx = content.find(end_needle)
    if end_idx == -1:
        raise ValueError("Could not find exhibits end needle in index.html")

print(f"Replacing exhibits from char {start_idx} to {end_idx}")
new_exhibits_code = f"  exhibits: {exhibits_json}\n}};"
content = content[:start_idx] + new_exhibits_code + content[end_idx + len(end_needle) - len('\n\n/* ==========================================================================\n   §4  ENGINE'):]

print("Exhibits array replaced successfully!")

# Write to scratch/index_test.html to verify
with open('scratch/index_test.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved scratch/index_test.html")

