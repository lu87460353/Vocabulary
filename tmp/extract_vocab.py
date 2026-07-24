import re, json, os

# Use absolute path
base = os.path.dirname(os.path.abspath(__file__))
vocab_path = os.path.join(base, 'vocab_full.txt')

with open(vocab_path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
words = []
skip_starts = ('说明：', '1. 本词汇表', '2. 本词汇表', '3. 本着', 
               '4. 本词汇表', '5. 本词汇表', '6. 本词汇表', '7. 部分',
               '附录2', '附录3', '普通高中', '\u2502', '\f')

letter_pattern = re.compile(r'^[A-Z]$')
number_pattern = re.compile(r'^\d+\s*$')

for line in lines:
    line = line.strip()
    if not line:
        continue
    if any(line.startswith(s) for s in skip_starts):
        continue
    if number_pattern.match(line):
        continue
    if letter_pattern.match(line):
        continue
    
    raw = line
    level = 0
    if raw.endswith('**'):
        level = 2
        word = raw[:-2].strip()
    elif raw.endswith('*'):
        level = 1
        word = raw[:-1].strip()
    else:
        word = raw.strip()
    
    if re.match(r'^[a-zA-Z]', word) and len(word) > 0:
        words.append({'word': word, 'level': level})

print(f"Total: {len(words)}")
print(f"Level 0: {sum(1 for w in words if w['level']==0)}")
print(f"Level 1: {sum(1 for w in words if w['level']==1)}")
print(f"Level 2: {sum(1 for w in words if w['level']==2)}")

for w in words[:20]:
    m = {0:'', 1:'*', 2:'**'}[w['level']]
    print(f"  {w['word']}{m}")

out_path = os.path.join(base, 'vocab_words.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(words, f, ensure_ascii=False, indent=2)
print(f"Saved to {out_path}")
