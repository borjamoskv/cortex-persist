#!/usr/bin/env python3
"""
C5 Browser Forensics & Extension Triage Engine (v2.0)
Deterministic inspection, content-script collision audit, and atomic purge for Chromium on macOS.
"""

import argparse
import datetime
import glob
import json
import os
import shutil
import subprocess
import sys

CHROME_BASE = os.path.expanduser("~/Library/Application Support/Google/Chrome")

def webkit_time_to_iso(microseconds_val):
    try:
        val = int(microseconds_val)
        if val <= 0:
            return "N/A"
        dt = datetime.datetime(1601, 1, 1, tzinfo=datetime.timezone.utc) + datetime.timedelta(microseconds=val)
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        return "N/A"

def get_profile_paths():
    if not os.path.exists(CHROME_BASE):
        return []
    profiles = []
    for item in os.listdir(CHROME_BASE):
        full = os.path.join(CHROME_BASE, item)
        if os.path.isdir(full) and (item == "Default" or item.startswith("Profile ")):
            profiles.append(full)
    return sorted(profiles)

def load_extension_metadata(profile_path, ext_id, version_dir):
    mf_path = os.path.join(version_dir, "manifest.json")
    if not os.path.exists(mf_path):
        return None
    try:
        with open(mf_path, "r", encoding="utf-8", errors="ignore") as f:
            manifest = json.load(f)
    except Exception:
        return None

    name = manifest.get("name", "Unknown")
    if name.startswith("__MSG_"):
        key = name.replace("__MSG_", "").replace("__", "")
        def_loc = manifest.get("default_locale", "en")
        loc_path = os.path.join(version_dir, "_locales", def_loc, "messages.json")
        if os.path.exists(loc_path):
            try:
                with open(loc_path, "r", encoding="utf-8", errors="ignore") as lf:
                    loc_data = json.load(lf)
                    name = loc_data.get(key, {}).get("message", name)
            except Exception:
                pass

    content_scripts = manifest.get("content_scripts", [])
    matches = []
    for cs in content_scripts:
        matches.extend(cs.get("matches", []))

    permissions = manifest.get("permissions", []) + manifest.get("host_permissions", [])

    return {
        "id": ext_id,
        "name": name,
        "version": manifest.get("version", "Unknown"),
        "matches": matches,
        "permissions": permissions,
        "path": version_dir,
    }

def cmd_list(args):
    print("=== C5 CHROMIUM EXTENSIONS AUDIT ===")
    profiles = get_profile_paths()
    if not profiles:
        print("No Chrome profiles found at:", CHROME_BASE)
        return

    for prof in profiles:
        prof_name = os.path.basename(prof)
        ext_dir = os.path.join(prof, "Extensions")
        if not os.path.exists(ext_dir):
            continue

        sec_pref_path = os.path.join(prof, "Secure Preferences")
        sec_pref = {}
        if os.path.exists(sec_pref_path):
            try:
                with open(sec_pref_path, "r", encoding="utf-8", errors="ignore") as f:
                    sec_pref = json.load(f).get("extensions", {}).get("settings", {})
            except Exception:
                pass

        ext_ids = [d for d in os.listdir(ext_dir) if not d.startswith(".")]
        print(f"\nProfile: {prof_name} ({len(ext_ids)} extensions)")
        for eid in ext_ids:
            versions = glob.glob(os.path.join(ext_dir, eid, "*"))
            versions = [v for v in versions if os.path.isdir(v)]
            if not versions:
                continue
            meta = load_extension_metadata(prof, eid, versions[0])
            if not meta:
                continue
            
            p_info = sec_pref.get(eid, {})
            fit = p_info.get("first_install_time", 0)
            install_dt = webkit_time_to_iso(fit)
            active = p_info.get("active_bit", "Unknown")

            print(f"  - [{eid}] {meta["name"]} (v{meta["version"]}) | Active: {active} | Installed: {install_dt}")
            if meta["matches"]:
                sample = meta["matches"][:3]
                more = f" (+{len(meta["matches"])-3} more)" if len(meta["matches"]) > 3 else ""
                print(f"      Intercepts: {sample}{more}")

def cmd_scan(args):
    domain = args.domain.lower()
    print(f"=== SCANNING FOR INJECTIONS MATCHING DOMAIN: {domain} ===")
    profiles = get_profile_paths()
    found = 0

    for prof in profiles:
        prof_name = os.path.basename(prof)
        ext_dir = os.path.join(prof, "Extensions")
        if not os.path.exists(ext_dir):
            continue

        for eid in os.listdir(ext_dir):
            if eid.startswith("."):
                continue
            versions = [v for v in glob.glob(os.path.join(ext_dir, eid, "*")) if os.path.isdir(v)]
            if not versions:
                continue
            meta = load_extension_metadata(prof, eid, versions[0])
            if not meta:
                continue

            hit_matches = [m for m in meta["matches"] if domain in m]
            if hit_matches:
                found += 1
                print(f"\n[MATCH FOUND] Profile: {prof_name}")
                print(f"  Extension: {meta["name"]} (ID: {eid})")
                print(f"  Version:   {meta["version"]}")
                print(f"  Matching Patterns: {hit_matches}")
                print(f"  Directory: {meta["path"]}")

    if found == 0:
        print(f"\nNo extension in any profile intercepts domain: {domain}")
    else:
        print(f"\nTotal matching extensions found: {found}")

def cmd_purge(args):
    ext_id = args.id.strip()
    if not ext_id:
        print("Error: Extension ID required.")
        return

    print(f"=== ATOMIC PURGE OF EXTENSION: {ext_id} ===")
    profiles = get_profile_paths()
    purged_files = 0
    purged_prefs = 0

    for prof in profiles:
        prof_name = os.path.basename(prof)
        # 1. Delete Extension directory
        ext_path = os.path.join(prof, "Extensions", ext_id)
        if os.path.exists(ext_path):
            shutil.rmtree(ext_path, ignore_errors=True)
            print(f"  [{prof_name}] Deleted Extension directory: {ext_path}")
            purged_files += 1

        # 2. Delete Sync/Local Extension Settings
        for s_dir in ["Sync Extension Settings", "Local Extension Settings"]:
            sp = os.path.join(prof, s_dir, ext_id)
            if os.path.exists(sp):
                shutil.rmtree(sp, ignore_errors=True)
                print(f"  [{prof_name}] Deleted storage directory: {sp}")
                purged_files += 1

        # 3. Clean Secure Preferences
        sec_pref_path = os.path.join(prof, "Secure Preferences")
        if os.path.exists(sec_pref_path):
            try:
                with open(sec_pref_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                settings = data.get("extensions", {}).get("settings", {})
                if ext_id in settings:
                    del settings[ext_id]
                    # Backup before rewrite
                    shutil.copyfile(sec_pref_path, sec_pref_path + ".c5_bak")
                    with open(sec_pref_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2)
                    print(f"  [{prof_name}] Pruned from Secure Preferences (backup saved).")
                    purged_prefs += 1
            except Exception as e:
                print(f"  [{prof_name}] Error modifying Secure Preferences: {e}")

        # 4. Clean standard Preferences (install_signature.ids to prevent cloud re-sync)
        pref_path = os.path.join(prof, "Preferences")
        if os.path.exists(pref_path):
            try:
                with open(pref_path, "r", encoding="utf-8") as f:
                    pdata = json.load(f)
                sig = pdata.get("extensions", {}).get("install_signature", {})
                ids = sig.get("ids", [])
                if ext_id in ids:
                    ids.remove(ext_id)
                    with open(pref_path, "w", encoding="utf-8") as f:
                        json.dump(pdata, f)
                    print(f"  [{prof_name}] Pruned from Preferences install_signature.")
            except Exception as e:
                pass

    print(f"\nPurge complete. Files/dirs removed: {purged_files}, Preferences cleaned: {purged_prefs}")

def cmd_verify_network(args):
    print("=== C5 NETWORK & DNS INTEGRITY VERIFICATION ===")
    print("\n[1] Checking /etc/hosts:")
    with open("/etc/hosts", "r") as f:
        for line in f:
            if not line.startswith("#") and line.strip():
                print(" ", line.strip())

    print("\n[2] Checking DNS Resolvers:")
    try:
        out = subprocess.check_output(["scutil", "--dns"], text=True)
        for line in out.splitlines():
            if "nameserver[" in line:
                print(" ", line.strip())
    except Exception as e:
        print("  Error querying DNS:", e)

    print("\n[3] Checking Active Listening Ports:")
    try:
        out = subprocess.check_output(["lsof", "-i", "-P", "-n"], text=True)
        listeners = [l for l in out.splitlines() if "LISTEN" in l]
        for l in listeners[:15]:
            print(" ", l)
    except Exception as e:
        print("  Error querying listeners:", e)

def main():
    parser = argparse.ArgumentParser(description="C5 Browser Forensics & Triage Engine")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="List all extensions across all Chromium profiles")

    scan_parser = subparsers.add_parser("scan", help="Scan extensions matching a specific domain")
    scan_parser.add_argument("--domain", required=True, help="Domain to search for in content_scripts (e.g. instagram.com)")

    purge_parser = subparsers.add_parser("purge", help="Atomically remove an extension across all profiles")
    purge_parser.add_argument("--id", required=True, help="Extension ID to purge")

    subparsers.add_parser("verify-network", help="Check DNS, hosts, and listening sockets")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "list":
        cmd_list(args)
    elif args.command == "scan":
        cmd_scan(args)
    elif args.command == "purge":
        cmd_purge(args)
    elif args.command == "verify-network":
        cmd_verify_network(args)

if __name__ == "__main__":
    main()
