import json
import sys
from pathlib import Path

def mojibake_tespiti(metin):
    mojibake_chars = ["Ã–", "Ä°", "Ã‡", "Å", "Ä", "Ã¼", "Ã¶", "Ä±", "Ã§", "Ãœ", "Ã", "â€", "â€˜", "Ã¢"]
    for char in mojibake_chars:
        if char in metin:
            return True
    return False

def fix_mojibake(metin):
    return metin.encode('cp1252', errors='replace').decode('utf-8', errors='replace')

def check_if_fully_fixed(metin):
    # Check if there are still replacement characters (\ufffd) left after fix
    if '\ufffd' in metin:
        return False
    return True

def main():
    input_file = "data/sentetik/evraklar.jsonl"
    output_file = "data/sentetik/evraklar_duzeltilmis.jsonl"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    mojibake_ids = []
    ascii_ids = []
    successful_fixes = 0
    unsuccessful_fixes = []
    
    fixed_lines = []
    
    for i, line in enumerate(lines):
        if not line.strip():
            continue
            
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            fixed_lines.append(line)
            continue
            
        record_id = record.get("id", f"unknown-{i}")
        
        # Check for SENT-0111 to SENT-0117 (ASCII issue)
        if "SENT-0111" <= record_id <= "SENT-0117":
            ascii_ids.append(record_id)
            fixed_lines.append(line) # Don't apply fix, keep original
            continue
            
        is_mojibake = False
        is_fully_fixed = True
        
        def process_node(node):
            nonlocal is_mojibake, is_fully_fixed
            if isinstance(node, str):
                if mojibake_tespiti(node):
                    is_mojibake = True
                    fixed_str = fix_mojibake(node)
                    if not check_if_fully_fixed(fixed_str):
                        is_fully_fixed = False
                    return fixed_str
                return node
            elif isinstance(node, dict):
                return {k: process_node(v) for k, v in node.items()}
            elif isinstance(node, list):
                return [process_node(item) for item in node]
            else:
                return node
                
        fixed_record = process_node(record)
        
        if is_mojibake:
            mojibake_ids.append(record_id)
            if is_fully_fixed:
                successful_fixes += 1
                fixed_lines.append(json.dumps(fixed_record, ensure_ascii=False) + "\n")
            else:
                unsuccessful_fixes.append(record_id)
                # Mark it as unfixable in the new file, writing the original or partially fixed? 
                # The instructions say: "düzeltilemeyenleri OLDUĞU GİBİ (işaretleyerek) bu yeni dosyaya yaz."
                record["_encoding_notu"] = "duzeltilemedi_kismi_mojibake"
                fixed_lines.append(json.dumps(record, ensure_ascii=False) + "\n")
        else:
            fixed_lines.append(line)
            
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
        
    print(f"Total mojibake affected: {len(mojibake_ids)}")
    print(f"Mojibake IDs: {mojibake_ids}")
    print(f"Successfully fixed: {successful_fixes}")
    print(f"Unsuccessful fixes: {len(unsuccessful_fixes)}")
    if unsuccessful_fixes:
        print(f"Unsuccessful IDs: {unsuccessful_fixes}")
    
    print(f"\nASCII issue IDs (SENT-0111 to SENT-0117): {len(ascii_ids)}")
    print(f"ASCII IDs: {ascii_ids}")

if __name__ == '__main__':
    main()
