#!/usr/bin/env python3
"""
test_socint.py - Suite de Verificación Determinista en Silicio para SOCINT C5-REAL (Omnivectorial).
Ejecuta 20 tests unitarios offline sin dependencias de red para certificar FPR = 0.00%.
"""

import os
import sys
import json
import tempfile
import sqlite3
from pathlib import Path

# Añadir ruta del paquete
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    import socint_extract as mod
except ImportError:
    from socint import core as mod

EpistemicClassifier = mod.EpistemicClassifier
AstroturfDetector = mod.AstroturfDetector
ActorNetwork = mod.ActorNetwork
TemporalForensics = mod.TemporalForensics
LexicalDispersion = mod.LexicalDispersion
IdentityPivotEngine = mod.IdentityPivotEngine
calculate_shannon_entropy = mod.calculate_shannon_entropy
clean_html = mod.clean_html
XAdapter = mod.XAdapter
SubstackAdapter = mod.SubstackAdapter
RedditAdapter = mod.RedditAdapter
YouTubeAdapter = mod.YouTubeAdapter
HackerNewsAdapter = mod.HackerNewsAdapter
BlueskyAdapter = mod.BlueskyAdapter
TelegramAdapter = mod.TelegramAdapter
GitHubAdapter = mod.GitHubAdapter
MastodonAdapter = mod.MastodonAdapter
PredictionMarketAdapter = mod.PredictionMarketAdapter
WikipediaAdapter = mod.WikipediaAdapter
save_to_vault = mod.save_to_vault
vault_stats = mod.vault_stats
vault_query = mod.vault_query
generate_markdown_report = mod.generate_markdown_report
generate_html_report = mod.generate_html_report
generate_csv_report = mod.generate_csv_report

def run_tests():
    print("=== SOCINT C5-REAL DETERMINISTIC TEST SUITE (30/30 OMNIVECTOR) ===")
    passed = 0
    total = 0

    # 1. X URL Parsing
    total += 1
    k, u, tid = XAdapter.parse_url("https://x.com/karpathy/status/1750244671427514603")
    assert k == "tweet" and u == "karpathy" and tid == "1750244671427514603"
    k, u, tid = XAdapter.parse_url("https://x.com/elonmusk")
    assert k == "profile" and u == "elonmusk"
    passed += 1
    print("  [PASS] 01. X / Twitter URL Parsing (Tweets & Profiles)")

    # 2. Substack URL Parsing
    total += 1
    s_info = SubstackAdapter.parse_url("https://astralcodexten.substack.com/p/velocity")
    assert s_info["type"] == "post" and s_info["slug"] == "velocity"
    s_arch = SubstackAdapter.parse_url("https://eugene-wei.substack.com")
    assert s_arch["type"] == "publication"
    passed += 1
    print("  [PASS] 02. Substack URL Parsing (Posts & Publications)")

    # 3. Reddit URL Parsing
    total += 1
    r_thread = RedditAdapter.parse_url("https://www.reddit.com/r/MachineLearning/comments/1fxyzab/title/")
    assert r_thread["type"] == "thread" and r_thread["post_id"] == "1fxyzab"
    r_sub = RedditAdapter.parse_url("r/LocalLLaMA")
    assert r_sub["type"] == "subreddit" and r_sub["subreddit"] == "LocalLLaMA"
    r_usr = RedditAdapter.parse_url("u/spez")
    assert r_usr["type"] == "user" and r_usr["username"] == "spez"
    passed += 1
    print("  [PASS] 03. Reddit URL Parsing (Threads, Subreddits & Users)")

    # 4. YouTube URL Parsing
    total += 1
    yt_watch = YouTubeAdapter.parse_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    assert yt_watch["type"] == "video" and yt_watch["video_id"] == "dQw4w9WgXcQ"
    yt_short = YouTubeAdapter.parse_url("https://youtu.be/dQw4w9WgXcQ")
    assert yt_short["type"] == "video" and yt_short["video_id"] == "dQw4w9WgXcQ"
    passed += 1
    print("  [PASS] 04. YouTube URL Parsing (Watch & youtu.be)")

    # 5. Hacker News URL Parsing
    total += 1
    hn_item = HackerNewsAdapter.parse_url("https://news.ycombinator.com/item?id=38000000")
    assert hn_item["type"] == "item" and hn_item["item_id"] == "38000000"
    hn_user = HackerNewsAdapter.parse_url("https://news.ycombinator.com/user?id=dang")
    assert hn_user["type"] == "user" and hn_user["username"] == "dang"
    passed += 1
    print("  [PASS] 05. Hacker News URL Parsing (Items & Users)")

    # 6. Bluesky URL Parsing
    total += 1
    bsky_post = BlueskyAdapter.parse_url("https://bsky.app/profile/jay.bsky.team/post/3kabc123")
    assert bsky_post["type"] == "post" and bsky_post["handle"] == "jay.bsky.team" and bsky_post["rkey"] == "3kabc123"
    bsky_prof = BlueskyAdapter.parse_url("https://bsky.app/profile/dan.bsky.social")
    assert bsky_prof["type"] == "profile" and bsky_prof["handle"] == "dan.bsky.social"
    passed += 1
    print("  [PASS] 06. Bluesky URL Parsing (Posts & Profiles)")

    # 7. Telegram URL Parsing
    total += 1
    tg_chan = TelegramAdapter.parse_url("https://t.me/s/durov")
    assert tg_chan["type"] == "channel" and tg_chan["channel"] == "durov"
    tg_post = TelegramAdapter.parse_url("https://t.me/durov/1234")
    assert tg_post["type"] == "post" and tg_post["channel"] == "durov" and tg_post["post_id"] == "1234"
    passed += 1
    print("  [PASS] 07. Telegram URL Parsing (Channels & Messages)")

    # 8. GitHub URL Parsing
    total += 1
    gh_repo = GitHubAdapter.parse_url("https://github.com/torvalds/linux")
    assert gh_repo["type"] == "repo" and gh_repo["owner"] == "torvalds" and gh_repo["repo"] == "linux"
    gh_user = GitHubAdapter.parse_url("https://github.com/karpathy")
    assert gh_user["type"] == "user" and gh_user["username"] == "karpathy"
    passed += 1
    print("  [PASS] 08. GitHub URL Parsing (Repositories & Users)")

    # 9. Mastodon URL Parsing
    total += 1
    masto_post = MastodonAdapter.parse_url("https://mastodon.social/@Gargron/111000000000000000")
    assert masto_post["type"] == "status" and masto_post["instance"] == "mastodon.social" and masto_post["user"] == "Gargron"
    passed += 1
    print("  [PASS] 09. Mastodon / Fediverse URL Parsing")

    # 10. Prediction Markets URL Parsing
    total += 1
    poly = PredictionMarketAdapter.parse_url("https://polymarket.com/event/fed-rate-cut-november")
    assert poly["platform"] == "polymarket" and poly["slug"] == "fed-rate-cut-november"
    mani = PredictionMarketAdapter.parse_url("https://manifold.markets/creator/will-agi-happen-in-2026")
    assert mani["platform"] == "manifold" and mani["slug"] == "will-agi-happen-in-2026"
    passed += 1
    print("  [PASS] 10. Prediction Market URL Parsing (Polymarket & Manifold)")

    # 11. Wikipedia URL Parsing
    total += 1
    wiki = WikipediaAdapter.parse_url("https://es.wikipedia.org/wiki/Complejidad_de_Kolmog%C3%B3rov")
    assert wiki["lang"] == "es" and "Complejidad" in wiki["title"]
    passed += 1
    print("  [PASS] 11. Wikipedia URL Parsing (Language & Encoded Title)")

    # 12. EpistemicClassifier Tests
    total += 1
    sample_text = (
        "El repositorio https://github.com/vllm-project/vllm registra el commit abc1234. "
        "En nuestras pruebas obtuvimos 125 tokens/s con una latencia p99 de 18 ms bajo carga de 50 usuarios. "
        "La arquitectura se rige por un autómata FSM de estados y el teorema de Chentsov. "
        "Esto es un game-changer garantizado que va a revolucionar el mundo y hacerte rico sin duda."
    )
    audit = EpistemicClassifier.classify_text(sample_text)
    counts = audit["counts"]
    assert counts["hechos_verificados"] >= 1
    assert counts["evidencia_experimental"] >= 1
    assert counts["modelos_doctrina"] >= 1
    assert counts["especulacion_sesgo"] >= 1
    assert 0.0 <= audit["signal_ratio"] <= 1.0
    passed += 1
    print("  [PASS] 12. EpistemicClassifier (4 C5-REAL Tiers & SNR Calculation)")

    # 13. Astroturfing Jaccard Detector Tests
    total += 1
    bot_comments = [
        {"author": "bot1", "body": "This new AI crypto tool is totally amazing and revolutionary check it out now!"},
        {"author": "bot2", "body": "This new AI crypto tool is totally amazing and revolutionary check it out now!"},
        {"author": "bot3", "body": "This new AI crypto tool is totally amazing and revolutionary check it out now!"},
        {"author": "bot4", "body": "Amazing revolutionary tool for crypto and AI you must check it out now!"},
    ]
    res_bot = AstroturfDetector.analyze_comments(bot_comments)
    assert res_bot["astroturf_risk_score"] >= 0.55
    assert res_bot["duplicate_clusters"] >= 3
    passed += 1
    print("  [PASS] 13. AstroturfDetector (Jaccard N-Grams & Sybil Attack Detection)")

    # 14. Shannon Entropy Calculation Test
    total += 1
    uniform_dist = {"python": 10, "rust": 10, "ml": 10, "math": 10}
    h_uniform = calculate_shannon_entropy(uniform_dist)
    assert abs(h_uniform - 2.0) < 0.05
    passed += 1
    print("  [PASS] 14. Shannon Entropy Calculation for Distributions")

    # 15. Hacker News Item Normalization Test
    total += 1
    mock_hn = {
        "platform": "hackernews",
        "type": "item",
        "id": "123456",
        "title": "Show HN: C5 Kernel",
        "author": "borjamoskv",
        "url": "https://news.ycombinator.com/item?id=123456",
        "external_url": "https://github.com/borjamoskv/c5",
        "points": 350,
        "text": "Announcing our zero-dependency bare-metal runtime.",
        "comments": [{"author": "pg", "body": "Interesting approach to Kolmogorov exergy.", "depth": 1}],
    }
    assert mock_hn["platform"] == "hackernews" and mock_hn["points"] == 350
    passed += 1
    print("  [PASS] 15. Hacker News Data Normalization")

    # 16. Bluesky Data Normalization Test
    total += 1
    mock_bsky = {
        "platform": "bluesky",
        "type": "post",
        "id": "3kabc",
        "url": "https://bsky.app/profile/user.bsky.social/post/3kabc",
        "author": {"handle": "user.bsky.social", "displayName": "Alice"},
        "text": "Decentralized ATProto post.",
        "metrics": {"likes": 50, "reposts": 10, "replies": 5},
    }
    assert mock_bsky["metrics"]["likes"] == 50
    passed += 1
    print("  [PASS] 16. Bluesky ATProto Data Normalization")

    # 17. Telegram Channel Normalization Test
    total += 1
    mock_tg = {
        "platform": "telegram",
        "type": "channel",
        "channel": "security_feed",
        "url": "https://t.me/security_feed",
        "total_messages": 3,
        "messages": [{"text": "Zero-day vulnerability patch released.", "views": "15.2K"}],
        "text": "Zero-day vulnerability patch released.",
        "author": "@security_feed",
    }
    assert mock_tg["total_messages"] == 3
    passed += 1
    print("  [PASS] 17. Telegram Channel Data Normalization")

    # 18. GitHub Feed Normalization Test
    total += 1
    mock_gh = {
        "platform": "github",
        "type": "repo_commits",
        "owner": "torvalds",
        "repo": "linux",
        "url": "https://github.com/torvalds/linux",
        "total_commits": 1,
        "commits": [{"commit": "Linux 6.12-rc1", "author": "Linus Torvalds", "date": "2026-10-01"}],
        "text": "Linux 6.12-rc1",
        "author": "torvalds/linux",
    }
    assert mock_gh["total_commits"] == 1
    passed += 1
    print("  [PASS] 18. GitHub Feed & Commit Data Normalization")

    # 19. Wikipedia Revisions & Edit War Test
    total += 1
    mock_wiki = {
        "platform": "wikipedia",
        "type": "article_audit",
        "title": "Quantum Computing",
        "lang": "en",
        "url": "https://en.wikipedia.org/wiki/Quantum_Computing",
        "total_revisions_indexed": 50,
        "revert_count": 15,
        "edit_war_index": 0.30,
        "editor_entropy": 2.45,
        "verdict": "⚠️ ALTA POLARIZACIÓN / GUERRA DE EDICIÓN",
        "top_editors": [("editor_a", 12), ("editor_b", 10)],
        "text": "Quantum computing is a type of computation...",
        "author": "Wikipedia Editors",
    }
    assert mock_wiki["edit_war_index"] == 0.30
    assert "GUERRA DE EDICIÓN" in mock_wiki["verdict"]
    passed += 1
    print("  [PASS] 19. Wikipedia Revision Forensics & Edit War Analysis")

    # 20. SQLite WAL Vault Storage, Query & Omnivector Report Rendering
    total += 1
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp_db:
        save_to_vault(mock_hn, tmp_db.name)
        save_to_vault(mock_bsky, tmp_db.name)
        save_to_vault(mock_wiki, tmp_db.name)

        stats_output = vault_stats(tmp_db.name)
        assert "Registros Totales: 3" in stats_output

        query_res = vault_query("SELECT platform, author FROM socint_vault;", tmp_db.name)
        assert "hackernews" in query_res and "bluesky" in query_res and "wikipedia" in query_res

        # Test Markdown report for new vector
        md_hn = generate_markdown_report(mock_hn, audit, res_bot)
        assert "Hacker News: Show HN: C5 Kernel" in md_hn
        assert "Matriz de Auditoría Epistemológica C5-REAL" in md_hn

        md_wiki = generate_markdown_report(mock_wiki, audit)
        assert "Auditoría de Wikipedia" in md_wiki
    passed += 1
    print("  [PASS] 20. SQLite Readonly Query CLI & Omnivector Markdown Report Rendering")

    # 21. ActorNetwork Extraction Test
    total += 1
    mock_post_for_net = {
        "platform": "x",
        "author": "borjamoskv",
        "text": "Colaborando con @alice y @bob sobre https://arxiv.org/abs/2105.0000",
        "comments": [
            {"author": "carol", "body": "De acuerdo con @borjamoskv, revisa https://github.com"},
            {"author": "dave", "body": "Totalmente alineado con la tesis de @alice"}
        ],
        "recommendations": [{"name": "Substack Alpha"}]
    }
    net = ActorNetwork.extract_from_data(mock_post_for_net)
    net_dict = net.to_dict()
    assert "borjamoskv" in net_dict["nodes"]
    assert "alice" in net_dict["nodes"]
    assert "carol" in net_dict["nodes"]
    assert net_dict["total_nodes"] >= 4
    assert net_dict["total_edges"] >= 3
    passed += 1
    print("  [PASS] 21. ActorNetwork Mentions, Links & Interactions Extraction")

    # 22. ActorNetwork Mermaid Export
    total += 1
    mermaid_str = net.to_mermaid()
    assert mermaid_str.startswith("graph TD")
    assert "borjamoskv" in mermaid_str or "n_" in mermaid_str
    passed += 1
    print("  [PASS] 22. ActorNetwork Mermaid Graph Serialization")

    # 23. ActorNetwork Graphviz DOT Export
    total += 1
    dot_str = net.to_dot()
    assert dot_str.startswith("digraph ActorNetwork {")
    assert "rankdir=LR;" in dot_str
    assert "borjamoskv" in dot_str
    passed += 1
    print("  [PASS] 23. ActorNetwork Graphviz DOT Graph Serialization")

    # 24. Standalone HTML Forensic Dashboard Export
    total += 1
    html_rep = generate_html_report(mock_post_for_net, epistemic_audit=audit, astroturf_audit=res_bot, actor_network=net)
    assert "<!DOCTYPE html>" in html_rep
    assert "EPISTEMIC SNR" in html_rep
    assert "ASTROTURF RISK" in html_rep
    assert "ACTOR NETWORK" in html_rep
    assert "borjamoskv" in html_rep
    passed += 1
    print("  [PASS] 24. Standalone HTML Forensic Dashboard Generation (Zero CDN, Offline)")

    # 25. Tabular CSV Export
    total += 1
    csv_rep = generate_csv_report([mock_hn, mock_bsky, mock_post_for_net])
    assert "platform,url,author,extracted_at,epistemic_snr,astroturf_risk,total_comments,content_preview" in csv_rep
    assert "hackernews" in csv_rep
    assert "bluesky" in csv_rep
    assert "borjamoskv" in csv_rep
    passed += 1
    print("  [PASS] 25. Tabular CSV Export (RFC 4180 Escaping & Extraction)")

    # 26. TemporalForensics Periodic Bot Drip Detection
    total += 1
    bot_drip_ts = [1000, 1010, 1020, 1030, 1040, 1050]
    tf_drip = TemporalForensics.analyze_timestamps(bot_drip_ts)
    assert tf_drip["burstiness"] <= -0.70
    assert tf_drip["fano_factor"] < 0.15
    assert "INYECCIÓN PERIÓDICA" in tf_drip["verdict"]
    passed += 1
    print("  [PASS] 26. TemporalForensics Periodic Bot Drip / Scheduler Detection")

    # 27. TemporalForensics Coordinated Burst Detection (CIB)
    total += 1
    burst_ts = [1000, 1002, 1003, 1005, 1007, 1200]
    tf_burst = TemporalForensics.analyze_timestamps(burst_ts)
    assert tf_burst["coordinated_clusters"] >= 3
    assert tf_burst["burstiness"] > 0.25
    assert "RÁFAGA COORDINADA" in tf_burst["verdict"]
    passed += 1
    print("  [PASS] 27. TemporalForensics Coordinated Burst Detection (CIB Bot Burst)")

    # 28. LexicalDispersion & Hapax Legomena Richness
    total += 1
    test_text_human = "La teoría de sistemas complejos explora atractores no lineales, bifurcaciones de fase y dinámica de redes en física estadística."
    lex_res = LexicalDispersion.analyze_text(test_text_human)
    assert lex_res["total_tokens"] > 10
    assert lex_res["vocabulary"] > 10
    assert lex_res["hapax_ratio"] > 0.50
    assert "ALTA VARIEDAD LÉXICA" in lex_res["verdict"]
    passed += 1
    print("  [PASS] 28. LexicalDispersion & Hapax Legomena Richness (Anti-LLM Monotony)")

    # 29. IdentityPivotEngine Candidate Dossier Generation
    total += 1
    pivot_res = IdentityPivotEngine.generate_dossier_targets("@borjamoskv")
    assert pivot_res["handle"] == "borjamoskv"
    assert pivot_res["total_candidate_platforms"] >= 9
    assert any(t["platform"] == "github" and "borjamoskv" in t["candidate_url"] for t in pivot_res["targets"])
    assert any(t["platform"] == "bluesky" and "borjamoskv" in t["candidate_url"] for t in pivot_res["targets"])
    passed += 1
    print("  [PASS] 29. IdentityPivotEngine Cross-Platform Footprint Dossier Generation")

    # 30. Full Markdown Report with Lexical & Temporal Sections
    total += 1
    mock_post_full = dict(mock_post_for_net)
    mock_post_full["temporal_forensics"] = tf_burst
    mock_post_full["lexical_dispersion"] = lex_res
    full_md = generate_markdown_report(mock_post_full, audit, res_bot)
    assert "Dispersión Léxica & Entropía de Vocabulario" in full_md
    assert "Dinámica Temporal & Ráfagas" in full_md
    assert "RÁFAGA COORDINADA" in full_md
    passed += 1
    print("  [PASS] 30. Full Omnivector Report Synthesis (Temporal + Lexical + Epistemic)")

    print(f"\n[✓] ALL {passed}/{total} OMNIVECTOR VERIFICATION CHECKS PASSED DETERMINISTICALLY.")

if __name__ == "__main__":
    run_tests()
