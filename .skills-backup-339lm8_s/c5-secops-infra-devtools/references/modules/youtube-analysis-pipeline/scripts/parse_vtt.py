import sys
import re

def clean_block_text(words):
    """
    Deduplicates repeated contiguous word sequences (n-grams) from YouTube rolling VTT subtitles.
    """
    res = []
    i = 0
    while i < len(words):
        matched_seq = False
        # Try matching repeated sequence lengths from 24 down to 1
        max_len = min(24, (len(words) - i) // 2)
        for seq_len in range(max_len, 0, -1):
            if i + 2 * seq_len <= len(words):
                seq1 = words[i:i + seq_len]
                seq2 = words[i + seq_len:i + 2 * seq_len]
                if seq1 == seq2:
                    res.extend(seq1)
                    i += 2 * seq_len
                    while i + seq_len <= len(words) and words[i:i + seq_len] == seq1:
                        i += seq_len
                    matched_seq = True
                    break
        if not matched_seq:
            res.append(words[i])
            i += 1
    return " ".join(res)

def parse_vtt(file_path, interval_sec=30):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Match cue start timestamp and inner content block
    cue_pattern = re.compile(
        r"(\d{2}:\d{2}:\d{2}\.\d{3}|\d{2}:\d{2}\.\d{3})\s+-->\s+[^\n]*\n(.*?)(?=\n(?:\d{2}:)?\d{2}:\d{2}|\Z)",
        re.DOTALL
    )
    matches = cue_pattern.findall(text)
    
    interval_blocks = {}
    for start_ts, content in matches:
        clean_lines = [re.sub(r'<[^>]+>', '', l).strip() for l in content.split('\n') if l.strip()]
        clean_str = " ".join(clean_lines)
        if not clean_str:
            continue
        
        parts = start_ts.split(':')
        if len(parts) == 3:
            secs = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(float(parts[2]))
        else:
            secs = int(parts[0]) * 60 + int(float(parts[1]))
            
        block_key = (secs // interval_sec) * interval_sec
        if block_key not in interval_blocks:
            interval_blocks[block_key] = []
        interval_blocks[block_key].append(clean_str)

    for block_key in sorted(interval_blocks.keys()):
        m, s = divmod(block_key, 60)
        h, m = divmod(m, 60)
        ts_str = f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"
        raw_text = " ".join(interval_blocks[block_key])
        cleaned = clean_block_text(raw_text.split())
        if cleaned.strip():
            print(f"[{ts_str}] {cleaned}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 parse_vtt.py <file.vtt> [interval_sec]")
        sys.exit(1)
    
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    parse_vtt(sys.argv[1], interval)
