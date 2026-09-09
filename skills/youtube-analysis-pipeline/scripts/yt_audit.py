#!/usr/bin/env python3
import sys
import os
import subprocess
import json

def run_cmd(cmd):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"ERROR: {e.stderr}"

def fetch_youtube_audit(url, output_dir="scratch"):
    os.makedirs(output_dir, exist_ok=True)
    print(f"[+] Extrayendo metadatos para: {url}")
    meta_json = run_cmd(f'yt-dlp --dump-json "{url}" 2>/dev/null')
    
    metadata = {}
    if meta_json and not meta_json.startswith("ERROR"):
        try:
            raw = json.loads(meta_json)
            metadata = {
                "title": raw.get("title"),
                "channel": raw.get("uploader"),
                "duration": raw.get("duration"),
                "description": raw.get("description"),
                "tags": raw.get("tags", [])
            }
            with open(os.path.join(output_dir, "metadata.json"), "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[-] Error parseando metadatos: {e}")
            
    print("[+] Intentando descarga de subtítulos (es, en, ko, ja, de)...")
    sub_cmd = f'yt-dlp --ignore-errors --no-check-certificate --write-auto-subs --write-subs --sub-langs "es,en,ko,ko-orig,ja,de,fr" --skip-download "{url}" -o "{output_dir}/transcript.%(ext)s" 2>&1'
    sub_out = run_cmd(sub_cmd)
    
    vtt_files = [f for f in os.listdir(output_dir) if f.endswith(".vtt")]
    if not vtt_files:
        print("[-] Subtítulos predeterminados bloqueados o no encontrados. Consultando list-subs...")
        list_subs = run_cmd(f'yt-dlp --list-subs "{url}" 2>/dev/null')
        print(f"[i] Subtítulos disponibles:\n{list_subs[:500]}")
        
    print(f"[+] VTTs encontrados en {output_dir}: {vtt_files}")
    return metadata, vtt_files

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 yt_audit.py <YOUTUBE_URL> [OUTPUT_DIR]")
        sys.exit(1)
    
    target_url = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    fetch_youtube_audit(target_url, out_dir)
