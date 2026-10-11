#!/usr/bin/env python3
"""
socint_extract.py - Suite Soberana de Inteligencia Social (SOCINT C5-REAL)
Motor omnivectorial de extracción, normalización, detección de astroturfing y auditoría
epistemológica de telemetría discursiva en 11 plataformas públicas (stdlib pura):
1. X (Twitter)
2. Substack
3. Reddit
4. YouTube
5. Hacker News
6. Bluesky (ATProto)
7. Telegram (Canales públicos)
8. GitHub (Actividad pública y Atom feeds)
9. Mastodon (Fediverse abierto)
10. Mercados de Predicción (Polymarket & Manifold)
11. Wikipedia (Historial de revisiones y disputas)
"""

import sys
import os
import re
import math
import json
import time
import html
import sqlite3
import argparse
from datetime import datetime, timezone
import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
DEFAULT_DB_PATH = os.path.expanduser("~/.gemini/antigravity/socint_vault.db")

# -----------------------------------------------------------------------------
# HTTP Helpers & Resilient Fetcher
# -----------------------------------------------------------------------------

def http_get(url, headers=None, timeout=12, max_retries=2):
    req_headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/html, application/xml, */*",
        "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
    }
    if headers:
        req_headers.update(headers)

    req = urllib.request.Request(url, headers=req_headers)
    last_err = None

    for attempt in range(max_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = resp.status
                content_type = resp.headers.get("Content-Type", "")
                charset = "utf-8"
                if "charset=" in content_type.lower():
                    charset = content_type.lower().split("charset=")[-1].split(";")[0].strip()
                data = resp.read()
                try:
                    text = data.decode(charset)
                except Exception:
                    text = data.decode("utf-8", errors="replace")
                return status, text, resp.headers
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code in (429, 500, 502, 503, 504) and attempt < max_retries:
                time.sleep(1.5 * (attempt + 1))
                continue
            break
        except Exception as e:
            last_err = e
            if attempt < max_retries:
                time.sleep(1.0 * (attempt + 1))
                continue
            break

    raise RuntimeError(f"Error HTTP al conectar con {url}: {last_err}")


def calculate_shannon_entropy(counter_dict):
    """Calcula la entropía de Shannon H = -sum(p_i * log2(p_i)) sobre una distribución de frecuencias."""
    total = sum(counter_dict.values())
    if total <= 0:
        return 0.0
    entropy = 0.0
    for count in counter_dict.values():
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)
    return round(entropy, 3)


def clean_html(raw_html):
    """Sanea HTML eliminando scripts, tags y decodificando entidades a texto plano."""
    text = re.sub(r'<script.*?</script>', '', raw_html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</p>', '\n\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<h[1-6].*?>(.*?)</h[1-6]>', r'\n\n### \1\n\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '', text)
    return html.unescape(text).strip()


# -----------------------------------------------------------------------------
# Epistemic Classifier & Astroturf Detection Engine (C5-REAL Standard)
# -----------------------------------------------------------------------------

class EpistemicClassifier:
    """Clasifica afirmaciones discursivas en las 4 categorías epistemológicas de C5-REAL."""

    FACT_PATTERNS = [
        r"\b(?:github\.com/[a-zA-Z0-9_\-\.]+/[a-zA-Z0-9_\-\.]+)\b",
        r"\b(?:0x[a-fA-F0-9]{40,64})\b",
        r"\b(?:sha256|[a-f0-9]{64})\b",
        r"\b(?:doi:\s*10\.\d{4,9}/[-._;()/:A-Z0-9]+)\b",
        r"\b(?:rfc\s*\d+|iso\s*\d+|ieee\s*\d+)\b",
        r"\b(?:sentencia|ley\s*\d+/\d+|borme|boe|decreto)\b",
        r"\b(?:v\d+\.\d+\.\d+|commit\s+[0-9a-f]{7,40})\b",
    ]

    EXPERIMENTAL_PATTERNS = [
        r"\b(?:\d+(?:\.\d+)?\s*(?:ms|us|ns|fps|tokens?/s|gb/s|mb/s|kb/s|hz|khz|mhz|ghz))\b",
        r"\b(?:\d+(?:\.\d+)?%\s*(?:latencia|throughput|acierto|accuracy|p99|p95|error rate|cpu|ram))\b",
        r"\b(?:benchmark|telemetr[ií]a|ab test|a/b testing|p99|p95|latency|sample size|n\s*=\s*\d+)\b",
        r"\b(?:\$\d+(?:\.\d+)?(?:k|m|b)?\s*(?:arr|mrr|coste|cost|gasto|ahorro))\b",
    ]

    MODEL_PATTERNS = [
        r"\b(?:arquitectura|paradigma|heur[ií]stica|teorema|axioma|morfismo|isomorfismo)\b",
        r"\b(?:markov|fisher|chentsov|landauer|shannon|bayes|fsm|invariante|atractor)\b",
        r"\b(?:pipeline|framework|metodolog[ií]a|diseño|topolog[ií]a|patr[oó]n|abstracci[oó]n)\b",
    ]

    SPECULATION_PATTERNS = [
        r"\b(?:garantizado|100x|revolucionar[aá]|cambiar[aá] el mundo|game[- ]changer)\b",
        r"\b(?:sin duda|todo el mundo sabe|f[aá]cilmente|secreto de|hacerte rico)\b",
        r"\b(?:alucina con|no te lo vas a creer|hilo imprescindible|el futuro de)\b",
        r"\b(?:seg[uú]n mi intuici[oó]n|creo firmemente|predicci[oó]n para \d{4})\b",
    ]

    @classmethod
    def classify_text(cls, text):
        sentences = [s.strip() for s in re.split(r'[\.\n\r]+', text) if len(s.strip()) > 15]

        facts = []
        experimental = []
        models = []
        speculation = []

        for s in sentences:
            s_lower = s.lower()
            if any(re.search(p, s_lower, re.IGNORECASE) for p in cls.FACT_PATTERNS):
                facts.append(s)
            elif any(re.search(p, s_lower, re.IGNORECASE) for p in cls.EXPERIMENTAL_PATTERNS):
                experimental.append(s)
            elif any(re.search(p, s_lower, re.IGNORECASE) for p in cls.MODEL_PATTERNS):
                models.append(s)
            elif any(re.search(p, s_lower, re.IGNORECASE) for p in cls.SPECULATION_PATTERNS):
                speculation.append(s)

        total_classified = len(facts) + len(experimental) + len(models) + len(speculation)
        grounded = len(facts) + len(experimental) + len(models)

        if total_classified == 0:
            signal_ratio = 0.50
        else:
            signal_ratio = round(grounded / (grounded + (len(speculation) * 1.5)), 3)

        return {
            "counts": {
                "hechos_verificados": len(facts),
                "evidencia_experimental": len(experimental),
                "modelos_doctrina": len(models),
                "especulacion_sesgo": len(speculation),
            },
            "signal_ratio": min(1.0, max(0.0, signal_ratio)),
            "samples": {
                "hechos": facts[:3],
                "experimental": experimental[:3],
                "modelos": models[:3],
                "especulacion": speculation[:3],
            }
        }


class AstroturfDetector:
    """Detecta campañas de astroturfing y bots analizando similitud léxica Jaccard y ratios de autor."""

    @staticmethod
    def _get_ngrams(text, n=3):
        tokens = re.findall(r"\w+", text.lower())
        if len(tokens) < n:
            return set(tokens)
        return set(" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1))

    @classmethod
    def analyze_comments(cls, comments):
        if not comments or len(comments) < 4:
            return {
                "astroturf_risk_score": 0.0,
                "duplicate_clusters": 0,
                "author_concentration": 0.0,
                "verdict": "DATOS INSUFICIENTES (Muestra reducida)",
            }

        authors = [c.get("author") for c in comments if c.get("author") not in (None, "[deleted]", "[removed]")]
        unique_authors = set(authors)
        author_concentration = round(1.0 - (len(unique_authors) / max(1, len(authors))), 2)

        ngrams_list = [cls._get_ngrams(c.get("body", "")) for c in comments]
        duplicate_pairs = 0
        pair_matches = []

        for i in range(len(comments)):
            if len(ngrams_list[i]) < 3:
                continue
            for j in range(i + 1, len(comments)):
                if len(ngrams_list[j]) < 3:
                    continue
                intersection = len(ngrams_list[i].intersection(ngrams_list[j]))
                union = len(ngrams_list[i].union(ngrams_list[j]))
                if union > 0:
                    sim = intersection / union
                    if sim > 0.60:
                        duplicate_pairs += 1
                        pair_matches.append({
                            "author_a": comments[i].get("author"),
                            "author_b": comments[j].get("author"),
                            "similarity": round(sim, 2),
                            "sample": comments[i].get("body", "")[:80]
                        })

        total_pairs = max(1, (len(comments) * (len(comments) - 1)) // 2)
        pair_ratio = duplicate_pairs / total_pairs

        risk_score = round(min(1.0, (author_concentration * 0.35) + (pair_ratio * 0.65 * 2.0)), 2)

        if risk_score >= 0.55:
            verdict = "⚠️ ALTO RIESGO DE ASTROTURFING (Campaña artificial detectada)"
        elif risk_score >= 0.25:
            verdict = "⚠️ RIESGO MODERADO (Repetición léxica o saturación de autor)"
        else:
            verdict = "✅ DISCUSIÓN ORGÁNICA (Baja correlación sintética)"

        return {
            "astroturf_risk_score": risk_score,
            "duplicate_clusters": duplicate_pairs,
            "author_concentration": author_concentration,
            "verdict": verdict,
            "suspicious_pairs": pair_matches[:5],
        }


# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# ACTOR NETWORK & ENTITY GRAPH ANALYZER (Pure Stdlib)
# -----------------------------------------------------------------------------

class ActorNetwork:
    """Extrae y modela el grafo de interacción (menciones @handle, enlaces externos y pares autor-réplica)."""

    def __init__(self):
        self.nodes = set()
        self.edges = []

    def add_interaction(self, source, target, rel_type="interacts", weight=1):
        if not source or not target or source == target:
            return
        source_clean = str(source).strip()
        target_clean = str(target).strip()
        if not source_clean or not target_clean or source_clean == target_clean:
            return
        self.nodes.add(source_clean)
        self.nodes.add(target_clean)
        for edge in self.edges:
            if edge["source"] == source_clean and edge["target"] == target_clean and edge["type"] == rel_type:
                edge["weight"] += weight
                return
        self.edges.append({
            "source": source_clean,
            "target": target_clean,
            "type": rel_type,
            "weight": weight
        })

    @classmethod
    def extract_from_data(cls, data):
        net = cls()
        author = data.get("author") or data.get("username") or data.get("channel") or "source_author"

        text = data.get("text") or data.get("content") or data.get("selftext") or data.get("description") or ""
        mentions = re.findall(r'(?:@|u/)([a-zA-Z0-9_\.\-]+)', text)
        for m in mentions:
            net.add_interaction(author, m, rel_type="mentions")

        urls = re.findall(r'https?://([a-zA-Z0-9_\.\-]+)', text)
        for u in urls:
            if not any(skip in u for skip in ["twitter.com", "x.com", "t.co", "fxtwitter.com"]):
                net.add_interaction(author, f"domain:{u}", rel_type="references_domain")

        comments = data.get("comments", [])
        for c in comments:
            c_author = c.get("author") or "anon"
            if c_author and c_author not in ("[deleted]", "[removed]"):
                net.add_interaction(c_author, author, rel_type="replies_to")
            c_body = c.get("body") or c.get("text") or ""
            c_mentions = re.findall(r'(?:@|u/)([a-zA-Z0-9_\.\-]+)', c_body)
            for cm in c_mentions:
                net.add_interaction(c_author, cm, rel_type="mentions")

        for rec in data.get("recommendations", []):
            rec_name = rec.get("name") or rec.get("domain") or rec.get("title")
            if rec_name:
                net.add_interaction(author, rec_name, rel_type="recommends")

        return net

    def to_dict(self):
        return {
            "nodes": sorted(list(self.nodes)),
            "edges": self.edges,
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges)
        }

    def to_mermaid(self):
        lines = ["graph TD"]
        if not self.edges:
            for n in sorted(list(self.nodes))[:15]:
                safe_n = re.sub(r'["\(\)\[\]]', '', str(n))
                lines.append(f'    node_{abs(hash(n)) % 65536}["{safe_n}"]')
            return "\n".join(lines)

        for edge in self.edges[:30]:
            s = re.sub(r'["\(\)\[\]]', '', str(edge["source"]))
            t = re.sub(r'["\(\)\[\]]', '', str(edge["target"]))
            w = edge["weight"]
            lbl = f"{edge['type']}" + (f" ({w})" if w > 1 else "")
            lines.append(f'    n_{abs(hash(s)) % 65536}["{s}"] -->|"{lbl}"| n_{abs(hash(t)) % 65536}["{t}"]')
        return "\n".join(lines)

    def to_dot(self):
        lines = ["digraph ActorNetwork {", "    rankdir=LR;", "    node [shape=box];"]
        for edge in self.edges:
            s = str(edge["source"]).replace('"', '\\"')
            t = str(edge["target"]).replace('"', '\\"')
            lines.append(f'    "{s}" -> "{t}" [label="{edge["type"]}", weight={edge["weight"]}];')
        lines.append("}")
        return "\n".join(lines)

    def to_gexf(self):
        """Exporta la red al formato GEXF 1.2 (Graph Exchange XML) para Gephi."""
        sorted_nodes = sorted(list(self.nodes))
        node_map = {n: idx for idx, n in enumerate(sorted_nodes)}
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">',
            '  <graph mode="static" defaultedgetype="directed">',
            '    <nodes>'
        ]
        for idx, n in enumerate(sorted_nodes):
            safe_lbl = html.escape(str(n))
            lines.append(f'      <node id="{idx}" label="{safe_lbl}" />')
        lines.append('    </nodes>')
        lines.append('    <edges>')
        for idx, e in enumerate(self.edges):
            s_id = node_map.get(e["source"], 0)
            t_id = node_map.get(e["target"], 0)
            w = e.get("weight", 1)
            rel = html.escape(str(e.get("type", "interacts")))
            lines.append(f'      <edge id="{idx}" source="{s_id}" target="{t_id}" weight="{w}" label="{rel}" />')
        lines.append('    </edges>')
        lines.append('  </graph>')
        lines.append('</gexf>')
        return "\n".join(lines)

    def compute_centrality(self, damping=0.85, max_iter=40, tol=1e-5):
        """Calcula métricas de centralidad en silicio (Grado y PageRank / Power Iteration) sin dependencias."""
        nodes = sorted(list(self.nodes))
        N = len(nodes)
        if N == 0:
            return {"in_degree": {}, "out_degree": {}, "pagerank": {}, "top_influencers": []}

        in_degree = {n: 0 for n in nodes}
        out_degree = {n: 0 for n in nodes}
        out_links = {n: [] for n in nodes}

        for e in self.edges:
            s = e["source"]
            t = e["target"]
            w = e.get("weight", 1)
            if s in out_degree:
                out_degree[s] += w
                out_links[s].append((t, w))
            if t in in_degree:
                in_degree[t] += w

        # Power Iteration PageRank
        pr = {n: 1.0 / N for n in nodes}
        for _ in range(max_iter):
            next_pr = {n: (1.0 - damping) / N for n in nodes}
            for u in nodes:
                total_w = sum(w for _, w in out_links[u])
                if total_w > 0:
                    for v, w in out_links[u]:
                        if v in next_pr:
                            next_pr[v] += damping * pr[u] * (w / total_w)
                else:
                    for v in nodes:
                        next_pr[v] += damping * pr[u] / N

            err = sum(abs(next_pr[n] - pr[n]) for n in nodes)
            pr = next_pr
            if err < tol:
                break

        total_pr = sum(pr.values())
        if total_pr > 0:
            pr = {n: round(score / total_pr, 5) for n, score in pr.items()}

        sorted_pr = sorted(pr.items(), key=lambda x: x[1], reverse=True)

        return {
            "in_degree": in_degree,
            "out_degree": out_degree,
            "pagerank": pr,
            "top_influencers": [{"node": n, "score": s, "in_degree": in_degree.get(n, 0)} for n, s in sorted_pr[:10]]
        }


# -----------------------------------------------------------------------------
# TEMPORAL FORENSICS & BURSTINESS ENGINE (Poisson vs Coordinated Drip)
# -----------------------------------------------------------------------------

class TemporalForensics:
    """Analiza la dinámica temporal de comentarios para detectar campañas coordinadas y bots periódicos."""

    @staticmethod
    def analyze_timestamps(timestamps):
        if not timestamps or len(timestamps) < 3:
            return {
                "burstiness": 0.0,
                "fano_factor": 1.0,
                "coordinated_clusters": 0,
                "mean_delta_sec": 0.0,
                "verdict": "DATOS INSUFICIENTES (Muestra temporal reducida)"
            }

        sorted_ts = sorted([float(t) for t in timestamps])
        deltas = [sorted_ts[i+1] - sorted_ts[i] for i in range(len(sorted_ts) - 1)]
        mu = sum(deltas) / len(deltas)
        if mu <= 0:
            return {
                "burstiness": -1.0,
                "fano_factor": 0.0,
                "coordinated_clusters": len(deltas),
                "mean_delta_sec": 0.0,
                "verdict": "⚠️ ALERTA: Envío simultáneo masivo (Delta 0s)"
            }

        var = sum((d - mu)**2 for d in deltas) / len(deltas)
        sigma = math.sqrt(var)
        burstiness = round((sigma - mu) / (sigma + mu) if (sigma + mu) > 0 else 0.0, 3)
        fano = round(var / mu, 3)
        coordinated_clusters = sum(1 for d in deltas if d <= 15)

        if burstiness <= -0.70 and fano < 0.15:
            verdict = "⚠️ INYECCIÓN PERIÓDICA DETECTADA (Bot scheduler / Cron determinista)"
        elif coordinated_clusters >= 3 and burstiness > 0.25:
            verdict = "⚠️ RÁFAGA COORDINADA DETECTADA (Coordinated Inauthentic Behavior / Bot Burst)"
        elif burstiness > 0.40:
            verdict = "ℹ️ ACTIVIDAD POR RÁFAGAS (Picos orgánicos de atención o viralidad)"
        else:
            verdict = "✅ LLEGADA POISSONIANA (Interacción orgánica aleatoria)"

        return {
            "burstiness": burstiness,
            "fano_factor": fano,
            "coordinated_clusters": coordinated_clusters,
            "mean_delta_sec": round(mu, 2),
            "verdict": verdict
        }


# -----------------------------------------------------------------------------
# COORDINATED ACTION MATRIX & CIB CO-OCCURRENCE ENGINE
# -----------------------------------------------------------------------------

class CoordinatedActionMatrix:
    """Detecta co-amplificación y sincronización de actores sobre objetivos comunes en ventanas breves."""

    @staticmethod
    def analyze_co_actions(comments, time_window_sec=60):
        """Identifica parejas de actores que intervienen en proximidad temporal estrecha (<= time_window_sec)."""
        if not comments or len(comments) < 2:
            return {
                "co_actions": [],
                "total_synchronized_pairs": 0,
                "max_co_occurrences": 0,
                "cib_synchronization_score": 0.0,
                "verdict": "DATOS INSUFICIENTES"
            }

        pairs = {}
        sorted_comments = sorted(
            [c for c in comments if (c.get("timestamp") or c.get("created_utc")) and c.get("author") not in (None, "[deleted]", "[removed]")],
            key=lambda x: float(x.get("timestamp") or x.get("created_utc") or 0)
        )

        for i in range(len(sorted_comments)):
            a1 = sorted_comments[i]["author"]
            t1 = float(sorted_comments[i].get("timestamp") or sorted_comments[i].get("created_utc") or 0)
            for j in range(i + 1, len(sorted_comments)):
                a2 = sorted_comments[j]["author"]
                t2 = float(sorted_comments[j].get("timestamp") or sorted_comments[j].get("created_utc") or 0)
                delta = t2 - t1
                if delta > time_window_sec:
                    break
                if a1 != a2:
                    pair_key = tuple(sorted([a1, a2]))
                    pairs[pair_key] = pairs.get(pair_key, 0) + 1

        sorted_pairs = sorted(
            [{"actor_a": k[0], "actor_b": k[1], "co_occurrences": v} for k, v in pairs.items()],
            key=lambda x: x["co_occurrences"],
            reverse=True
        )

        total_interactions = len(sorted_comments)
        max_co = sorted_pairs[0]["co_occurrences"] if sorted_pairs else 0
        cib_score = round(min(1.0, (max_co * 2.0) / max(1, total_interactions)), 3)

        if cib_score >= 0.50:
            verdict = "⚠️ ALTA CO-SINCRONIZACIÓN (Posible campaña de astroturfing orquestada)"
        elif cib_score >= 0.20:
            verdict = "⚠️ CO-OCURRENCIA MODERADA (Pares de cuentas recurrentes en ráfagas)"
        else:
            verdict = "✅ COORDINACIÓN BAJA O NULA (Distribución de actores asíncrona)"

        return {
            "co_actions": sorted_pairs[:10],
            "total_synchronized_pairs": len(pairs),
            "max_co_occurrences": max_co,
            "cib_synchronization_score": cib_score,
            "verdict": verdict
        }


# -----------------------------------------------------------------------------
# LEXICAL DISPERSION & HAPAX ENTROPY ANALYZER
# -----------------------------------------------------------------------------

class LexicalDispersion:
    """Mide la riqueza del vocabulario y la tasa de Hapax Legomena para detectar texto sintético LLM."""

    @staticmethod
    def analyze_text(text):
        tokens = re.findall(r"\w+", text.lower())
        if not tokens:
            return {"total_tokens": 0, "vocabulary": 0, "hapax_ratio": 0.0, "lexical_density": 0.0, "verdict": "TEXTO VACÍO"}

        counts = {}
        for t in tokens:
            counts[t] = counts.get(t, 0) + 1

        hapax = sum(1 for c in counts.values() if c == 1)
        hapax_ratio = round(hapax / len(counts), 3) if counts else 0.0
        density = round(len(counts) / len(tokens), 3)

        if density < 0.25 and len(tokens) > 50:
            verdict = "⚠️ VOCABULARIO HIPER-REPETITIVO (Posible spam o texto prefabricado)"
        elif hapax_ratio > 0.45:
            verdict = "✅ ALTA VARIEDAD LÉXICA (Patrón natural de habla humana)"
        else:
            verdict = "ℹ️ DISPERSIÓN LÉXICA ESTÁNDAR"

        return {
            "total_tokens": len(tokens),
            "vocabulary": len(counts),
            "hapax_ratio": hapax_ratio,
            "lexical_density": density,
            "verdict": verdict
        }


# -----------------------------------------------------------------------------
# CROSS-PLATFORM IDENTITY PIVOT ENGINE (Unified Footprint Dossier)
# -----------------------------------------------------------------------------

class IdentityPivotEngine:
    """Genera un dossier de investigación unificada expandiendo un handle hacia las 11 plataformas."""

    PLATFORM_TEMPLATES = {
        "x": "https://x.com/{handle}",
        "bluesky": "https://bsky.app/profile/{handle}.bsky.social",
        "github": "https://github.com/{handle}",
        "telegram": "https://t.me/{handle}",
        "reddit": "https://reddit.com/user/{handle}",
        "substack": "https://{handle}.substack.com",
        "youtube": "https://www.youtube.com/@{handle}",
        "hackernews": "https://news.ycombinator.com/user?id={handle}",
        "mastodon": "https://mastodon.social/@{handle}",
    }

    @classmethod
    def generate_dossier_targets(cls, handle):
        clean_handle = re.sub(r'^[@/]|(?:u/)', '', str(handle).strip())
        targets = []
        for plat, tmpl in cls.PLATFORM_TEMPLATES.items():
            targets.append({
                "platform": plat,
                "handle": clean_handle,
                "candidate_url": tmpl.format(handle=clean_handle)
            })
        return {
            "handle": clean_handle,
            "total_candidate_platforms": len(targets),
            "targets": targets
        }


# -----------------------------------------------------------------------------
# SENTIMENT & EMOTIONAL VOLATILITY ENGINE (Zero external dependencies)
# -----------------------------------------------------------------------------

class SentimentAffectEngine:
    """Motor léxico ligero de polaridad y volatilidad emocional (Zero-deps)."""

    POSITIVE_WORDS = {
        "excelente", "increible", "brillante", "exito", "positivo", "genial",
        "avance", "innovacion", "solucion", "solido", "gran", "mejor", "victoria",
        "acierto", "valioso", "great", "excellent", "amazing", "breakthrough",
        "success", "positive", "good", "best", "solution", "innovative", "solid", "win"
    }

    NEGATIVE_WORDS = {
        "estafa", "fraude", "fracaso", "falso", "terrible", "desastre", "odio",
        "basura", "humo", "scam", "troll", "trampa", "horrible", "peor",
        "crisis", "fraud", "fail", "disaster", "hate", "trash", "worst", "broken"
    }

    @classmethod
    def score_text(cls, text):
        tokens = set(re.findall(r'\w+', text.lower()))
        if not tokens:
            return 0.0
        pos_count = len(tokens.intersection(cls.POSITIVE_WORDS))
        neg_count = len(tokens.intersection(cls.NEGATIVE_WORDS))
        diff = pos_count - neg_count
        total = pos_count + neg_count
        return round(diff / max(1, total), 3) if total > 0 else 0.0

    @classmethod
    def analyze_thread(cls, comments):
        if not comments:
            return {
                "mean_polarity": 0.0,
                "emotional_volatility": 0.0,
                "outrage_flag": False,
                "verdict": "SIN COMENTARIOS"
            }
        scores = [cls.score_text(c.get("body") or c.get("text") or "") for c in comments]
        mean_pol = round(sum(scores) / len(scores), 3)
        var = sum((s - mean_pol)**2 for s in scores) / len(scores)
        volatility = round(math.sqrt(var), 3)
        outrage_flag = (mean_pol < -0.30 and volatility > 0.35)

        if outrage_flag:
            verdict = "⚠️ INDIGNACIÓN POLARIZADA DETECTADA (Manufactured Outrage / Hostile Swarm)"
        elif mean_pol > 0.25:
            verdict = "✅ TONO PREDOMINANTEMENTE FAVORABLE / ALINEADO"
        elif mean_pol < -0.25:
            verdict = "⚠️ TONO CRÍTICO O HOSTIL GENERALIZADO"
        else:
            verdict = "ℹ️ TONO NEUTRO O EQUILIBRADO"

        return {
            "mean_polarity": mean_pol,
            "emotional_volatility": volatility,
            "outrage_flag": outrage_flag,
            "verdict": verdict
        }


# -----------------------------------------------------------------------------
# MERKLE ATTESTATION & CRYPTOGRAPHIC PROOF (Tamper-Evident Evidence Seal)
# -----------------------------------------------------------------------------

def compute_merkle_root(fields_dict):
    """Calcula la raíz de Merkle SHA-256 sobre los campos de evidencia indexados."""
    import hashlib
    leaves = []
    for k in sorted(fields_dict.keys()):
        val = fields_dict[k]
        if isinstance(val, (dict, list)):
            val_bytes = json.dumps(val, sort_keys=True, ensure_ascii=False).encode("utf-8")
        else:
            val_bytes = str(val).encode("utf-8")
        leaves.append(hashlib.sha256(val_bytes).hexdigest())

    current = sorted(leaves)
    if not current:
        return hashlib.sha256(b"").hexdigest()

    while len(current) > 1:
        next_level = []
        for i in range(0, len(current), 2):
            if i + 1 < len(current):
                combined = (current[i] + current[i+1]).encode("utf-8")
            else:
                combined = (current[i] + current[i]).encode("utf-8")
            next_level.append(hashlib.sha256(combined).hexdigest())
        current = next_level

    return current[0]


# -----------------------------------------------------------------------------
# STIX 2.1 THREAT INTELLIGENCE SERIALIZER (OASIS Open CTI Standard)
# -----------------------------------------------------------------------------

class StixThreatIntel:
    """Serializa la evidencia y deducciones forenses a STIX 2.1 para OpenCTI, MISP y Splunk."""

    @staticmethod
    def generate_bundle(post_data, astroturf_audit=None, temporal_audit=None, sentiment_audit=None):
        import uuid
        from datetime import datetime, timezone

        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        bundle_id = f"bundle--{uuid.uuid4()}"
        objects = []

        author = post_data.get("author") or post_data.get("username") or post_data.get("channel") or "unknown-target"
        platform = post_data.get("platform") or "web"
        url = post_data.get("url") or ""
        target_uuid = uuid.uuid5(uuid.NAMESPACE_URL, url or author)
        target_id = f"identity--{target_uuid}"

        target_identity = {
            "type": "identity",
            "spec_version": "2.1",
            "id": target_id,
            "created": now_iso,
            "modified": now_iso,
            "name": f"{author} ({platform})",
            "identity_class": "individual",
            "description": f"Actor investigated via SOCINT C5-REAL on {platform}",
            "contact_information": url
        }
        objects.append(target_identity)

        obs_id = f"observed-data--{uuid.uuid4()}"
        observed_obj = {
            "type": "observed-data",
            "spec_version": "2.1",
            "id": obs_id,
            "created": now_iso,
            "modified": now_iso,
            "first_observed": now_iso,
            "last_observed": now_iso,
            "number_observed": 1,
            "objects": {
                "0": {
                    "type": "url",
                    "value": url or "https://unknown.local"
                },
                "1": {
                    "type": "user-account",
                    "account_login": author,
                    "account_type": platform
                }
            }
        }
        objects.append(observed_obj)

        if astroturf_audit and astroturf_audit.get("astroturf_risk_score", 0) >= 0.25:
            ind_id = f"indicator--{uuid.uuid4()}"
            risk = astroturf_audit.get("astroturf_risk_score")
            ind_obj = {
                "type": "indicator",
                "spec_version": "2.1",
                "id": ind_id,
                "created": now_iso,
                "modified": now_iso,
                "name": f"SOCINT Astroturf Detection ({int(risk*100)}% risk)",
                "description": astroturf_audit.get("verdict"),
                "indicator_types": ["anomalous-activity"],
                "pattern": f"[user-account:account_type = '{platform}']",
                "pattern_type": "stix",
                "valid_from": now_iso
            }
            objects.append(ind_obj)

            rel_id = f"relationship--{uuid.uuid4()}"
            objects.append({
                "type": "relationship",
                "spec_version": "2.1",
                "id": rel_id,
                "created": now_iso,
                "modified": now_iso,
                "relationship_type": "indicates",
                "source_ref": ind_id,
                "target_ref": target_id
            })

        if temporal_audit and "RÁFAGA" in temporal_audit.get("verdict", ""):
            ind_t_id = f"indicator--{uuid.uuid4()}"
            objects.append({
                "type": "indicator",
                "spec_version": "2.1",
                "id": ind_t_id,
                "created": now_iso,
                "modified": now_iso,
                "name": "Coordinated Inauthentic Behavior Burst",
                "description": temporal_audit.get("verdict"),
                "indicator_types": ["anomalous-activity"],
                "pattern": f"[user-account:account_type = '{platform}']",
                "pattern_type": "stix",
                "valid_from": now_iso
            })

        return {
            "type": "bundle",
            "id": bundle_id,
            "objects": objects
        }


# -----------------------------------------------------------------------------
# ADAPTER 1: X (Twitter) Engine
# -----------------------------------------------------------------------------

class XAdapter:
    FX_API = "https://api.fxtwitter.com"
    SYNDICATION_API = "https://cdn.syndication.twimg.com/tweet-result"

    @staticmethod
    def parse_url(url_or_id):
        m = re.search(r"(?:twitter|x|fxtwitter|vxtwitter)\.com/([a-zA-Z0-9_]+)/status/(\d+)", url_or_id)
        if m:
            return "tweet", m.group(1), m.group(2)
        m_profile = re.search(r"(?:twitter|x|fxtwitter|vxtwitter)\.com/([a-zA-Z0-9_]+)/?$", url_or_id)
        if m_profile and m_profile.group(1) not in ("home", "explore", "messages", "search"):
            return "profile", m_profile.group(1), None
        m_id = re.search(r"^\d+$", url_or_id.strip())
        if m_id:
            return "tweet", "user", m_id.group(0)
        return None, None, None

    @classmethod
    def fetch_profile(cls, username):
        url = f"{cls.FX_API}/{username}"
        status, body, _ = http_get(url)
        data = json.loads(body)
        if data.get("code") == 200 and "user" in data:
            u = data["user"]
            ver = u.get("verification", {}) or {}
            return {
                "platform": "x",
                "type": "profile",
                "screen_name": u.get("screen_name"),
                "name": u.get("name"),
                "url": u.get("url"),
                "followers": u.get("followers") or 0,
                "following": u.get("following") or 0,
                "likes": u.get("likes") or 0,
                "tweets_count": u.get("tweets") or 0,
                "media_count": u.get("media_count") or 0,
                "joined": u.get("joined"),
                "description": u.get("description", ""),
                "verified": ver.get("verified", False),
                "verification_type": ver.get("type", "none"),
                "avatar_url": u.get("avatar_url"),
            }
        raise RuntimeError(f"No se pudo obtener el perfil de @{username} en X.")

    @classmethod
    def fetch_tweet(cls, user, tweet_id):
        for fx_url in [f"{cls.FX_API}/status/{tweet_id}", f"{cls.FX_API}/{user}/status/{tweet_id}"]:
            try:
                status, body, _ = http_get(fx_url, timeout=10)
                data = json.loads(body)
                if data.get("code") == 200 and "tweet" in data and data["tweet"]:
                    return cls._normalize_fx_tweet(data["tweet"])
            except Exception:
                continue

        try:
            token = f"{(int(tweet_id) / 1e15) * 3.14159:.0f}"
            synd_url = f"{cls.SYNDICATION_API}?id={tweet_id}&token={token}"
            status, body, _ = http_get(synd_url, timeout=10)
            data = json.loads(body)
            if "text" in data:
                return cls._normalize_syndication_tweet(data)
        except Exception:
            pass

        jina_url = f"https://r.jina.ai/https://x.com/{user}/status/{tweet_id}"
        try:
            status, body, _ = http_get(jina_url, timeout=12)
            if body and len(body) > 100:
                lines = [line.strip() for line in body.split("\n") if line.strip()]
                return {
                    "platform": "x",
                    "type": "tweet",
                    "id": tweet_id,
                    "url": f"https://x.com/{user}/status/{tweet_id}",
                    "created_at": None,
                    "timestamp": None,
                    "author": {"name": user, "screen_name": user, "avatar_url": None, "followers": 0, "following": 0},
                    "text": "\n".join(lines[:30]),
                    "metrics": {"likes": 0, "retweets": 0, "replies": 0, "views": 0},
                    "replying_to": None,
                    "quoted_tweet": None,
                    "media": [],
                }
        except Exception as e:
            raise RuntimeError(f"Fallo en todos los adaptadores para X (Tweet {tweet_id}): {e}")

        raise RuntimeError(f"No se pudo extraer el tweet {tweet_id} de X.")

    @classmethod
    def unfold_thread(cls, user, tweet_id, max_depth=15):
        visited_ids = set()
        thread_chain = []
        initial_tweet = cls.fetch_tweet(user, tweet_id)
        thread_chain.append(initial_tweet)
        visited_ids.add(initial_tweet["id"])
        author_screen_name = initial_tweet["author"]["screen_name"]

        parent_id = initial_tweet.get("replying_to")
        depth = 0
        while parent_id and parent_id not in visited_ids and depth < max_depth:
            try:
                parent_tweet = cls.fetch_tweet(author_screen_name, parent_id)
                if parent_tweet["author"]["screen_name"].lower() == author_screen_name.lower():
                    thread_chain.insert(0, parent_tweet)
                    visited_ids.add(parent_id)
                    parent_id = parent_tweet.get("replying_to")
                    depth += 1
                else:
                    break
            except Exception:
                break

        full_text = "\n\n".join(f"[{i+1}/{len(thread_chain)}] {t['text']}" for i, t in enumerate(thread_chain))

        return {
            "platform": "x",
            "type": "thread",
            "id": tweet_id,
            "root_id": thread_chain[0]["id"],
            "author": thread_chain[0]["author"],
            "url": thread_chain[0]["url"],
            "total_tweets": len(thread_chain),
            "tweets": thread_chain,
            "text": full_text,
            "metrics": {
                "total_likes": sum(t["metrics"]["likes"] for t in thread_chain),
                "total_retweets": sum(t["metrics"]["retweets"] for t in thread_chain),
                "total_replies": sum(t["metrics"]["replies"] for t in thread_chain),
                "total_views": sum(t["metrics"]["views"] for t in thread_chain),
            }
        }

    @classmethod
    def _normalize_fx_tweet(cls, t):
        author = t.get("author", {}) or {}
        media_list = []
        if "media" in t and t["media"]:
            if "photos" in t["media"] and t["media"]["photos"]:
                for p in t["media"]["photos"]:
                    media_list.append({"type": "photo", "url": p.get("url")})
            if "videos" in t["media"] and t["media"]["videos"]:
                for v in t["media"]["videos"]:
                    media_list.append({"type": "video", "url": v.get("url")})

        quoted = None
        if "quote" in t and t["quote"]:
            q = t["quote"]
            q_author = q.get("author", {}) or {}
            quoted = {
                "author": q_author.get("name"),
                "screen_name": q_author.get("screen_name"),
                "text": q.get("text"),
                "id": q.get("id"),
                "url": q.get("url"),
            }

        return {
            "platform": "x",
            "type": "tweet",
            "id": t.get("id"),
            "url": t.get("url") or f"https://x.com/{author.get('screen_name')}/status/{t.get('id')}",
            "created_at": t.get("created_at"),
            "timestamp": t.get("created_timestamp"),
            "author": {
                "name": author.get("name") or author.get("screen_name"),
                "screen_name": author.get("screen_name"),
                "avatar_url": author.get("avatar_url"),
                "followers": author.get("followers") or 0,
                "following": author.get("following") or 0,
            },
            "text": t.get("text", ""),
            "metrics": {
                "likes": t.get("likes") or 0,
                "retweets": t.get("retweets") or 0,
                "replies": t.get("replies") or 0,
                "views": t.get("views") or 0,
            },
            "replying_to": t.get("replying_to_status"),
            "quoted_tweet": quoted,
            "media": media_list,
        }

    @classmethod
    def _normalize_syndication_tweet(cls, t):
        user = t.get("user", {}) or {}
        return {
            "platform": "x",
            "type": "tweet",
            "id": t.get("id_str"),
            "url": f"https://x.com/{user.get('screen_name', 'i')}/status/{t.get('id_str')}",
            "created_at": t.get("created_at"),
            "timestamp": None,
            "author": {
                "name": user.get("name"),
                "screen_name": user.get("screen_name"),
                "avatar_url": user.get("profile_image_url_https"),
                "followers": 0,
                "following": 0,
            },
            "text": t.get("text", ""),
            "metrics": {
                "likes": t.get("favorite_count") or 0,
                "retweets": t.get("conversation_count") or 0,
                "replies": 0,
                "views": 0,
            },
            "replying_to": t.get("in_reply_to_status_id_str"),
            "quoted_tweet": None,
            "media": [],
        }


# -----------------------------------------------------------------------------
# ADAPTER 2: Substack Engine
# -----------------------------------------------------------------------------

class SubstackAdapter:
    @staticmethod
    def parse_url(url):
        u = url.strip()
        parsed = urllib.parse.urlparse(u)
        hostname = parsed.netloc.lower()

        note_m = re.search(r"substack\.com/@([a-zA-Z0-9_\-\.]+)/note/([a-zA-Z0-9_\-]+)", u)
        if note_m:
            return {"type": "note", "user": note_m.group(1), "note_id": note_m.group(2), "domain": hostname}

        post_m = re.search(r"/p/([a-zA-Z0-9_\-]+)", parsed.path)
        slug = post_m.group(1) if post_m else None

        subdomain_m = re.search(r"^([a-zA-Z0-9_\-]+)\.substack\.com", hostname)
        pub_name = subdomain_m.group(1) if subdomain_m else hostname

        return {
            "type": "post" if slug else "publication",
            "domain": hostname,
            "publication": pub_name,
            "slug": slug,
        }

    @classmethod
    def fetch_publication_archive(cls, domain, limit=25, offset=0):
        url = f"https://{domain}/api/v1/archive?sort=new&limit={limit}&offset={offset}"
        try:
            status, body, _ = http_get(url)
            posts_raw = json.loads(body)
            results = []
            for p in posts_raw:
                author_name = None
                if p.get("primary_author"):
                    author_name = p["primary_author"].get("name")
                elif p.get("published_by"):
                    author_name = p["published_by"].get("name")

                results.append({
                    "id": p.get("id"),
                    "title": p.get("title"),
                    "subtitle": p.get("subtitle"),
                    "slug": p.get("slug"),
                    "canonical_url": p.get("canonical_url"),
                    "post_date": p.get("post_date"),
                    "audience": p.get("audience"),
                    "word_count": p.get("wordcount") or 0,
                    "reaction_count": (p.get("reactions") or {}).get("❤", 0),
                    "comments_count": p.get("comment_count") or 0,
                    "author": author_name or domain,
                })
            return {
                "platform": "substack",
                "type": "archive",
                "domain": domain,
                "total_fetched": len(results),
                "posts": results,
            }
        except Exception:
            return cls.fetch_rss_feed(domain, limit=limit)

    @classmethod
    def fetch_rss_feed(cls, domain, limit=25):
        rss_url = f"https://{domain}/feed"
        status, body, _ = http_get(rss_url)
        root = ET.fromstring(body)
        channel = root.find("channel")
        items = channel.findall("item") if channel is not None else []
        results = []
        for it in items[:limit]:
            title = it.findtext("title") or "Sin título"
            link = it.findtext("link") or ""
            pub_date = it.findtext("pubDate") or ""
            creator = it.findtext("{http://purl.org/dc/elements/1.1/}creator") or domain
            results.append({
                "id": link,
                "title": title,
                "subtitle": "",
                "slug": link.split("/p/")[-1] if "/p/" in link else "",
                "canonical_url": link,
                "post_date": pub_date,
                "audience": "everyone",
                "word_count": 0,
                "reaction_count": 0,
                "comments_count": 0,
                "author": creator,
            })
        return {
            "platform": "substack",
            "type": "archive",
            "domain": domain,
            "total_fetched": len(results),
            "posts": results,
        }

    @classmethod
    def fetch_post(cls, domain, slug, fetch_comments=True):
        url = f"https://{domain}/api/v1/posts/{slug}"
        try:
            status, body, _ = http_get(url)
            p = json.loads(body)
            raw_html = p.get("body_html", "")
            text_clean = clean_html(raw_html)
            author = (p.get("primary_author") or {}).get("name") or domain
            post_id = p.get("id")

            comments = []
            if fetch_comments and post_id:
                try:
                    c_url = f"https://{domain}/api/v1/posts/{post_id}/comments?all_comments=true"
                    c_status, c_body, _ = http_get(c_url, timeout=8)
                    c_data = json.loads(c_body)
                    for comment in c_data.get("comments", [])[:30]:
                        c_user = comment.get("user", {}) or {}
                        comments.append({
                            "author": c_user.get("name") or "[reader]",
                            "body": clean_html(comment.get("body", "")),
                            "likes": comment.get("reactions", {}).get("❤", 0),
                            "date": comment.get("date"),
                        })
                except Exception:
                    pass

            return {
                "platform": "substack",
                "type": "post",
                "id": post_id,
                "title": p.get("title"),
                "subtitle": p.get("subtitle") or "",
                "slug": p.get("slug"),
                "canonical_url": p.get("canonical_url") or f"https://{domain}/p/{slug}",
                "post_date": p.get("post_date"),
                "author": author,
                "word_count": p.get("wordcount") or len(text_clean.split()),
                "likes": (p.get("reactions") or {}).get("❤", 0),
                "comments_count": p.get("comment_count") or len(comments),
                "paywalled": p.get("audience") != "everyone",
                "content": text_clean,
                "comments": comments,
            }
        except Exception:
            jina_url = f"https://r.jina.ai/https://{domain}/p/{slug}"
            status, body, _ = http_get(jina_url)
            return {
                "platform": "substack",
                "type": "post",
                "id": None,
                "title": slug,
                "subtitle": "",
                "slug": slug,
                "canonical_url": f"https://{domain}/p/{slug}",
                "post_date": None,
                "author": domain,
                "word_count": len(body.split()),
                "likes": 0,
                "comments_count": 0,
                "paywalled": False,
                "content": body,
                "comments": [],
            }

    @classmethod
    def audit_recommendation_network(cls, domain):
        url = f"https://{domain}/api/v1/recommendations"
        try:
            status, body, _ = http_get(url)
            recs_raw = json.loads(body)
            recommendations = []
            for r in recs_raw:
                pub = r.get("recommended_publication", {}) or {}
                recommendations.append({
                    "name": pub.get("name"),
                    "subdomain": pub.get("subdomain"),
                    "custom_domain": pub.get("custom_domain"),
                    "blurb": r.get("blurb"),
                    "subscribers": pub.get("ranking_detail_free_subscribers"),
                })
            return {
                "platform": "substack",
                "type": "recommendations",
                "source_publication": domain,
                "total_recommended": len(recommendations),
                "is_cartelized": len(recommendations) > 15,
                "recommendations": recommendations,
            }
        except Exception as e:
            return {
                "platform": "substack",
                "type": "recommendations",
                "source_publication": domain,
                "error": f"No se pudieron auditar las recomendaciones: {e}",
                "recommendations": [],
            }


# -----------------------------------------------------------------------------
# ADAPTER 3: Reddit Engine
# -----------------------------------------------------------------------------

class RedditAdapter:
    BASE_URL = "https://www.reddit.com"

    @staticmethod
    def parse_url(url):
        u = url.strip()
        m_thread = re.search(r"reddit\.com/r/([a-zA-Z0-9_\-]+)/comments/([a-zA-Z0-9]+)", u)
        if m_thread:
            return {"type": "thread", "subreddit": m_thread.group(1), "post_id": m_thread.group(2)}

        m_user = re.search(r"reddit\.com/u(?:ser)?/([a-zA-Z0-9_\-]+)", u)
        if m_user:
            return {"type": "user", "username": m_user.group(1), "post_id": None}

        m_sub = re.search(r"reddit\.com/r/([a-zA-Z0-9_\-]+)", u)
        if m_sub:
            return {"type": "subreddit", "subreddit": m_sub.group(1), "post_id": None}

        m_short_u = re.search(r"^u/([a-zA-Z0-9_\-]+)$", u)
        if m_short_u:
            return {"type": "user", "username": m_short_u.group(1), "post_id": None}

        m_short = re.search(r"^r/([a-zA-Z0-9_\-]+)$", u)
        if m_short:
            return {"type": "subreddit", "subreddit": m_short.group(1), "post_id": None}

        return None

    @classmethod
    def fetch_user_dossier(cls, username, limit=50):
        json_url = f"{cls.BASE_URL}/user/{username}/submitted.json?limit={limit}"
        posts = []
        sub_distribution = {}

        try:
            headers = {"User-Agent": USER_AGENT}
            status, body, _ = http_get(json_url, headers=headers, timeout=10)
            data = json.loads(body)
            children = data.get("data", {}).get("children", [])
            for c in children:
                p = c.get("data", {})
                sub = p.get("subreddit", "unknown")
                sub_distribution[sub] = sub_distribution.get(sub, 0) + 1
                posts.append({
                    "title": p.get("title"),
                    "subreddit": sub,
                    "score": p.get("score", 0),
                    "created_utc": p.get("created_utc"),
                    "permalink": f"https://reddit.com{p.get('permalink')}",
                })
        except Exception:
            rss_url = f"{cls.BASE_URL}/user/{username}/submitted.rss?limit={limit}"
            try:
                status, body, _ = http_get(rss_url, headers={"User-Agent": USER_AGENT}, timeout=10)
                root = ET.fromstring(body)
                ns = {"atom": "http://www.w3.org/2005/Atom"}
                for e in root.findall("atom:entry", ns):
                    title = e.findtext("atom:title", "", ns)
                    cat_node = e.find("atom:category", ns)
                    sub = cat_node.get("term", "unknown") if cat_node is not None else "unknown"
                    sub_distribution[sub] = sub_distribution.get(sub, 0) + 1
                    link_node = e.find("atom:link", ns)
                    plink = link_node.get("href") if link_node is not None else ""
                    posts.append({
                        "title": title,
                        "subreddit": sub,
                        "score": 0,
                        "created_utc": e.findtext("atom:published", "", ns),
                        "permalink": plink,
                    })
            except Exception as e:
                raise RuntimeError(f"No se pudo generar el dossier para /u/{username}: {e}")

        entropy = calculate_shannon_entropy(sub_distribution)
        is_burner = entropy < 0.85 and len(posts) > 5

        return {
            "platform": "reddit",
            "type": "user_dossier",
            "username": username,
            "url": f"https://reddit.com/user/{username}",
            "total_submitted_indexed": len(posts),
            "subreddit_distribution": sub_distribution,
            "subreddit_entropy": entropy,
            "entropy_verdict": "⚠️ CUENTA MONO-TEMÁTICA / RIESGO SHILL" if is_burner else "✅ DISTRIBUCIÓN DIVERSIFICADA (Orgánica)",
            "recent_posts": posts[:10],
        }

    @classmethod
    def search_subreddit(cls, subreddit, query, limit=25, sort="relevance"):
        url = f"{cls.BASE_URL}/r/{subreddit}/search.json?q={urllib.parse.quote(query)}&restrict_sr=1&sort={sort}&limit={limit}"
        headers = {"User-Agent": USER_AGENT}
        status, body, _ = http_get(url, headers=headers)
        data = json.loads(body)
        children = data.get("data", {}).get("children", [])
        results = []
        for c in children:
            p = c.get("data", {})
            results.append({
                "title": p.get("title"),
                "author": p.get("author"),
                "score": p.get("score", 0),
                "num_comments": p.get("num_comments", 0),
                "permalink": f"https://reddit.com{p.get('permalink')}",
            })
        return {
            "platform": "reddit",
            "type": "search",
            "subreddit": subreddit,
            "query": query,
            "total_results": len(results),
            "results": results,
        }

    @classmethod
    def fetch_subreddit(cls, subreddit, sort="hot", limit=25, after=None):
        json_url = f"{cls.BASE_URL}/r/{subreddit}/{sort}.json?limit={limit}"
        if after:
            json_url += f"&after={after}"

        try:
            headers = {"User-Agent": USER_AGENT}
            status, body, _ = http_get(json_url, headers=headers, timeout=8)
            data = json.loads(body)
            children = data.get("data", {}).get("children", [])
            if children:
                posts = []
                for c in children:
                    p = c.get("data", {})
                    if p.get("stickied"):
                        continue
                    score = p.get("score") or 0
                    ratio = p.get("upvote_ratio") or 1.0
                    num_comments = p.get("num_comments") or 0
                    c_index = round((1.0 - ratio) * (num_comments ** 0.5), 2)
                    posts.append({
                        "id": p.get("id"),
                        "title": p.get("title"),
                        "author": p.get("author") or "[deleted]",
                        "score": score,
                        "upvote_ratio": ratio,
                        "controversy_index": c_index,
                        "num_comments": num_comments,
                        "permalink": f"https://reddit.com{p.get('permalink')}",
                        "created_utc": p.get("created_utc"),
                        "selftext": (p.get("selftext") or "")[:500],
                        "domain": p.get("domain"),
                        "url": p.get("url"),
                    })
                return {
                    "platform": "reddit",
                    "type": "subreddit",
                    "subreddit": subreddit,
                    "sort": sort,
                    "total_posts": len(posts),
                    "after": data.get("data", {}).get("after"),
                    "posts": posts,
                }
        except Exception:
            pass

        rss_url = f"{cls.BASE_URL}/r/{subreddit}/{sort}.rss?limit={limit}"
        try:
            status, body, _ = http_get(rss_url, headers={"User-Agent": USER_AGENT}, timeout=10)
            return cls._parse_reddit_atom(body, subreddit, sort)
        except Exception as e:
            raise RuntimeError(f"Fallo en todos los adaptadores para r/{subreddit}: {e}")

    @classmethod
    def _parse_reddit_atom(cls, xml_text, subreddit, sort):
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        root = ET.fromstring(xml_text)
        entries = root.findall("atom:entry", ns)
        posts = []

        for e in entries:
            title = e.findtext("atom:title", "", ns)
            author_node = e.find("atom:author/atom:name", ns)
            author = author_node.text.replace("/u/", "") if author_node is not None and author_node.text else "[unknown]"
            link_node = e.find("atom:link", ns)
            permalink = link_node.get("href") if link_node is not None else ""
            content = e.findtext("atom:content", "", ns)
            clean_content = clean_html(content)[:500]

            posts.append({
                "id": permalink.split("/comments/")[-1].split("/")[0] if "/comments/" in permalink else "",
                "title": title,
                "author": author,
                "score": 0,
                "upvote_ratio": 1.0,
                "controversy_index": 0.0,
                "num_comments": 0,
                "permalink": permalink,
                "created_utc": e.findtext("atom:published", "", ns),
                "selftext": clean_content,
                "domain": f"reddit.com/r/{subreddit}",
                "url": permalink,
            })

        return {
            "platform": "reddit",
            "type": "subreddit",
            "subreddit": subreddit,
            "sort": sort,
            "total_posts": len(posts),
            "after": None,
            "posts": posts,
        }

    @classmethod
    def fetch_thread(cls, subreddit, post_id, depth=3, comment_limit=40):
        json_url = f"{cls.BASE_URL}/r/{subreddit}/comments/{post_id}.json?limit={comment_limit}&depth={depth}"
        try:
            headers = {"User-Agent": USER_AGENT}
            status, body, _ = http_get(json_url, headers=headers, timeout=10)
            data = json.loads(body)
            if isinstance(data, list) and len(data) >= 2:
                post_raw = data[0].get("data", {}).get("children", [{}])[0].get("data", {})
                post_info = {
                    "platform": "reddit",
                    "type": "thread",
                    "id": post_raw.get("id"),
                    "subreddit": post_raw.get("subreddit") or subreddit,
                    "title": post_raw.get("title"),
                    "author": post_raw.get("author"),
                    "score": post_raw.get("score") or 0,
                    "upvote_ratio": post_raw.get("upvote_ratio") or 1.0,
                    "num_comments": post_raw.get("num_comments") or 0,
                    "selftext": post_raw.get("selftext") or "",
                    "permalink": f"https://reddit.com{post_raw.get('permalink')}",
                    "created_utc": post_raw.get("created_utc"),
                }

                comments_raw = data[1].get("data", {}).get("children", [])
                parsed_comments = []

                def parse_comment_node(node, current_depth):
                    if node.get("kind") != "t1":
                        return None
                    c = node.get("data", {})
                    c_author = c.get("author", "[deleted]")
                    c_body = c.get("body", "")
                    c_score = c.get("score", 0)

                    children_replies = []
                    if current_depth < depth and "replies" in c and isinstance(c["replies"], dict):
                        sub_children = c["replies"].get("data", {}).get("children", [])
                        for sub in sub_children:
                            res = parse_comment_node(sub, current_depth + 1)
                            if res:
                                children_replies.append(res)

                    return {
                        "author": c_author,
                        "score": c_score,
                        "body": c_body,
                        "depth": current_depth,
                        "replies": children_replies,
                    }

                for c_node in comments_raw[:comment_limit]:
                    res = parse_comment_node(c_node, 1)
                    if res:
                        parsed_comments.append(res)

                post_info["comments"] = parsed_comments
                return post_info
        except Exception:
            pass

        jina_url = f"https://r.jina.ai/https://www.reddit.com/r/{subreddit}/comments/{post_id}"
        try:
            status, body, _ = http_get(jina_url, timeout=12)
            lines = [l.strip() for l in body.split("\n") if l.strip()]
            title = lines[0] if lines else f"Hilo {post_id}"
            return {
                "platform": "reddit",
                "type": "thread",
                "id": post_id,
                "subreddit": subreddit,
                "title": title,
                "author": "[unknown]",
                "score": 0,
                "upvote_ratio": 1.0,
                "num_comments": 0,
                "selftext": "\n".join(lines[1:25]),
                "permalink": f"https://reddit.com/r/{subreddit}/comments/{post_id}",
                "created_utc": None,
                "comments": [],
            }
        except Exception as e:
            raise RuntimeError(f"Fallo al recuperar hilo {post_id} en r/{subreddit}: {e}")


# -----------------------------------------------------------------------------
# ADAPTER 4: YouTube Engine
# -----------------------------------------------------------------------------

class YouTubeAdapter:
    OEMBED_API = "https://www.youtube.com/oembed"

    @staticmethod
    def parse_url(url):
        u = url.strip()
        m_watch = re.search(r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([a-zA-Z0-9_\-]{11})", u)
        if m_watch:
            return {"type": "video", "video_id": m_watch.group(1)}
        return None

    @classmethod
    def fetch_video(cls, video_id):
        target_url = f"https://www.youtube.com/watch?v={video_id}"
        oembed_url = f"{cls.OEMBED_API}?url={urllib.parse.quote(target_url)}&format=json"

        title = f"YouTube Video {video_id}"
        author = "YouTube Creator"
        thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"

        try:
            status, body, _ = http_get(oembed_url, timeout=8)
            data = json.loads(body)
            title = data.get("title", title)
            author = data.get("author_name", author)
            thumbnail_url = data.get("thumbnail_url", thumbnail_url)
        except Exception:
            pass

        transcript_text = ""
        try:
            jina_url = f"https://r.jina.ai/{target_url}"
            status, body, _ = http_get(jina_url, timeout=12)
            if body:
                transcript_text = body[:10000]
        except Exception:
            pass

        return {
            "platform": "youtube",
            "type": "video",
            "id": video_id,
            "url": target_url,
            "title": title,
            "author": author,
            "thumbnail_url": thumbnail_url,
            "transcript": transcript_text,
            "content": transcript_text,
            "text": transcript_text,
        }


# -----------------------------------------------------------------------------
# ADAPTER 5: Hacker News Engine (Algolia & Firebase REST)
# -----------------------------------------------------------------------------

class HackerNewsAdapter:
    """Extrae historias, árboles de comentarios y perfiles en Hacker News (cero auth)."""

    ALGOLIA_API = "https://hn.algolia.com/api/v1"
    FIREBASE_API = "https://hacker-news.firebaseio.com/v0"

    @staticmethod
    def parse_url(url):
        u = url.strip()
        m_item = re.search(r"news\.ycombinator\.com/item\?id=(\d+)", u)
        if m_item:
            return {"type": "item", "item_id": m_item.group(1)}
        m_user = re.search(r"news\.ycombinator\.com/user\?id=([a-zA-Z0-9_\-]+)", u)
        if m_user:
            return {"type": "user", "username": m_user.group(1)}
        m_id = re.search(r"^hn:(\d+)$", u)
        if m_id:
            return {"type": "item", "item_id": m_id.group(1)}
        return None

    @classmethod
    def fetch_item(cls, item_id):
        url = f"{cls.ALGOLIA_API}/items/{item_id}"
        status, body, _ = http_get(url)
        data = json.loads(body)

        comments = []
        def parse_hn_children(children, current_depth=1):
            if not children or current_depth > 3:
                return
            for c in children[:20]:
                c_author = c.get("author") or "[deleted]"
                c_text = clean_html(c.get("text") or "")
                if c_text:
                    comments.append({"author": c_author, "body": c_text, "depth": current_depth})
                parse_hn_children(c.get("children"), current_depth + 1)

        parse_hn_children(data.get("children", []))

        return {
            "platform": "hackernews",
            "type": "item",
            "id": str(data.get("id")),
            "title": data.get("title") or "Sin título",
            "author": data.get("author"),
            "url": f"https://news.ycombinator.com/item?id={item_id}",
            "external_url": data.get("url"),
            "points": data.get("points") or 0,
            "created_at": data.get("created_at"),
            "text": clean_html(data.get("text") or ""),
            "content": clean_html(data.get("text") or ""),
            "comments": comments,
        }

    @classmethod
    def fetch_user(cls, username):
        url = f"{cls.FIREBASE_API}/user/{username}.json"
        status, body, _ = http_get(url)
        data = json.loads(body)
        if not data:
            raise RuntimeError(f"Usuario {username} no encontrado en Hacker News.")
        return {
            "platform": "hackernews",
            "type": "user",
            "id": username,
            "username": username,
            "url": f"https://news.ycombinator.com/user?id={username}",
            "karma": data.get("karma", 0),
            "created": data.get("created"),
            "about": clean_html(data.get("about") or ""),
            "submitted_count": len(data.get("submitted", [])),
        }


# -----------------------------------------------------------------------------
# ADAPTER 6: Bluesky Engine (AT Protocol Public API)
# -----------------------------------------------------------------------------

class BlueskyAdapter:
    """Extrae hilos, publicaciones y perfiles en Bluesky sin autenticación."""

    PUBLIC_API = "https://public.api.bsky.app/xrpc"

    @staticmethod
    def parse_url(url):
        u = url.strip()
        m_post = re.search(r"bsky\.app/profile/([a-zA-Z0-9_\-\.]+)/post/([a-zA-Z0-9]+)", u)
        if m_post:
            return {"type": "post", "handle": m_post.group(1), "rkey": m_post.group(2)}
        m_profile = re.search(r"bsky\.app/profile/([a-zA-Z0-9_\-\.]+)/?$", u)
        if m_profile:
            return {"type": "profile", "handle": m_profile.group(1)}
        return None

    @classmethod
    def fetch_post(cls, handle, rkey):
        uri = f"at://{handle}/app.bsky.feed.post/{rkey}"
        url = f"{cls.PUBLIC_API}/app.bsky.feed.getPostThread?uri={urllib.parse.quote(uri)}&depth=2"
        status, body, _ = http_get(url)
        data = json.loads(body)
        thread = data.get("thread", {})
        post = thread.get("post", {})
        record = post.get("record", {})
        author = post.get("author", {})

        return {
            "platform": "bluesky",
            "type": "post",
            "id": rkey,
            "url": f"https://bsky.app/profile/{handle}/post/{rkey}",
            "author": {
                "handle": author.get("handle"),
                "displayName": author.get("displayName"),
                "avatar": author.get("avatar"),
            },
            "text": record.get("text", ""),
            "content": record.get("text", ""),
            "created_at": record.get("createdAt"),
            "metrics": {
                "likes": post.get("likeCount", 0),
                "reposts": post.get("repostCount", 0),
                "replies": post.get("replyCount", 0),
            }
        }

    @classmethod
    def fetch_profile(cls, handle):
        url = f"{cls.PUBLIC_API}/app.bsky.actor.getProfile?actor={urllib.parse.quote(handle)}"
        status, body, _ = http_get(url)
        data = json.loads(body)
        return {
            "platform": "bluesky",
            "type": "profile",
            "id": data.get("did"),
            "handle": data.get("handle"),
            "displayName": data.get("displayName"),
            "description": data.get("description", ""),
            "followersCount": data.get("followersCount", 0),
            "followsCount": data.get("followsCount", 0),
            "postsCount": data.get("postsCount", 0),
            "url": f"https://bsky.app/profile/{handle}",
        }


# -----------------------------------------------------------------------------
# ADAPTER 7: Telegram Engine (Web Preview Zero-Auth)
# -----------------------------------------------------------------------------

class TelegramAdapter:
    """Extrae mensajes y canales públicos de Telegram mediante la vista previa web t.me/s/."""

    @staticmethod
    def parse_url(url):
        u = url.strip()
        m = re.search(r"t(?:elegram)?\.me/(?:s/)?([a-zA-Z0-9_\-]+)(?:/(\d+))?", u)
        if m:
            return {"type": "channel" if not m.group(2) else "post", "channel": m.group(1), "post_id": m.group(2)}
        return None

    @classmethod
    def fetch_channel(cls, channel, post_id=None):
        target_url = f"https://t.me/s/{channel}"
        if post_id:
            target_url += f"/{post_id}"

        status, body, _ = http_get(target_url)

        # Parsear mensajes desde el HTML público
        messages = []
        raw_msgs = re.findall(r'<div class="tgme_widget_message_text[^"]*">(.*?)</div>', body, flags=re.DOTALL)
        views = re.findall(r'<span class="tgme_widget_message_views">([^<]+)</span>', body)

        for i, m_text in enumerate(raw_msgs[:15]):
            v_count = views[i] if i < len(views) else "N/A"
            clean_m = clean_html(m_text)
            if clean_m:
                messages.append({"text": clean_m, "views": v_count})

        all_text = "\n\n---\n\n".join(m["text"] for m in messages)

        return {
            "platform": "telegram",
            "type": "post" if post_id else "channel",
            "channel": channel,
            "url": f"https://t.me/{channel}" + (f"/{post_id}" if post_id else ""),
            "total_messages": len(messages),
            "messages": messages,
            "text": all_text,
            "content": all_text,
            "author": f"@{channel}",
        }


# -----------------------------------------------------------------------------
# ADAPTER 8: GitHub Engine (Atom Feeds & Public REST)
# -----------------------------------------------------------------------------

class GitHubAdapter:
    """Extrae actividad pública, historial de commits y metadatos de repositorios en GitHub."""

    @staticmethod
    def parse_url(url):
        u = url.strip()
        m_repo = re.search(r"github\.com/([a-zA-Z0-9_\-\.]+)/([a-zA-Z0-9_\-\.]+)(?:/(?:issues|pull)/(\d+))?", u)
        if m_repo and m_repo.group(1) not in ("features", "marketplace", "topics", "collections"):
            return {
                "type": "issue" if m_repo.group(3) else "repo",
                "owner": m_repo.group(1),
                "repo": m_repo.group(2),
                "issue_id": m_repo.group(3)
            }
        m_user = re.search(r"github\.com/([a-zA-Z0-9_\-\.]+)/?$", u)
        if m_user and m_user.group(1) not in ("features", "marketplace", "about"):
            return {"type": "user", "username": m_user.group(1)}
        return None

    @classmethod
    def fetch_user_activity(cls, username):
        feed_url = f"https://github.com/{username}.atom"
        status, body, _ = http_get(feed_url)
        root = ET.fromstring(body)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        entries = []
        for e in root.findall("atom:entry", ns)[:20]:
            title = clean_html(e.findtext("atom:title", "", ns))
            published = e.findtext("atom:published", "", ns)
            link_node = e.find("atom:link", ns)
            plink = link_node.get("href") if link_node is not None else ""
            entries.append({"title": title, "date": published, "link": plink})

        all_text = "\n".join(e["title"] for e in entries)

        return {
            "platform": "github",
            "type": "user_activity",
            "username": username,
            "url": f"https://github.com/{username}",
            "total_events": len(entries),
            "events": entries,
            "text": all_text,
            "content": all_text,
            "author": username,
        }

    @classmethod
    def fetch_repo_feed(cls, owner, repo):
        feed_url = f"https://github.com/{owner}/{repo}/commits.atom"
        status, body, _ = http_get(feed_url)
        root = ET.fromstring(body)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        commits = []
        for e in root.findall("atom:entry", ns)[:25]:
            title = clean_html(e.findtext("atom:title", "", ns))
            updated = e.findtext("atom:updated", "", ns)
            author_node = e.find("atom:author/atom:name", ns)
            author = author_node.text if author_node is not None else "unknown"
            commits.append({"commit": title, "author": author, "date": updated})

        all_text = "\n".join(f"{c['date'][:10]} [{c['author']}]: {c['commit']}" for c in commits)

        return {
            "platform": "github",
            "type": "repo_commits",
            "owner": owner,
            "repo": repo,
            "url": f"https://github.com/{owner}/{repo}",
            "total_commits": len(commits),
            "commits": commits,
            "text": all_text,
            "content": all_text,
            "author": f"{owner}/{repo}",
        }


# -----------------------------------------------------------------------------
# ADAPTER 9: Mastodon Engine (Fediverse Abierto)
# -----------------------------------------------------------------------------

class MastodonAdapter:
    """Extrae toots e hilos en instancias federadas de Mastodon."""

    @staticmethod
    def parse_url(url):
        u = url.strip()
        m = re.search(r"https?://([a-zA-Z0-9_\-\.]+)/@([a-zA-Z0-9_\-\.]+)/(\d+)", u)
        if m:
            return {"type": "status", "instance": m.group(1), "user": m.group(2), "status_id": m.group(3)}
        return None

    @classmethod
    def fetch_status(cls, instance, status_id):
        url = f"https://{instance}/api/v1/statuses/{status_id}"
        status, body, _ = http_get(url)
        data = json.loads(body)
        acc = data.get("account", {})

        return {
            "platform": "mastodon",
            "type": "status",
            "id": status_id,
            "instance": instance,
            "url": data.get("url"),
            "author": acc.get("acct") or acc.get("username"),
            "created_at": data.get("created_at"),
            "content": clean_html(data.get("content", "")),
            "text": clean_html(data.get("content", "")),
            "metrics": {
                "replies": data.get("replies_count", 0),
                "reblogs": data.get("reblogs_count", 0),
                "favourites": data.get("favourites_count", 0),
            }
        }


# -----------------------------------------------------------------------------
# ADAPTER 10: Prediction Markets Engine (Polymarket & Manifold)
# -----------------------------------------------------------------------------

class PredictionMarketAdapter:
    """Extrae sentimiento predictivo cuantificado en Polymarket y Manifold Markets."""

    @staticmethod
    def parse_url(url):
        u = url.strip()
        m_poly = re.search(r"polymarket\.com/event/([a-zA-Z0-9_\-]+)", u)
        if m_poly:
            return {"platform": "polymarket", "slug": m_poly.group(1)}
        m_mani = re.search(r"manifold\.markets/[a-zA-Z0-9_\-]+/([a-zA-Z0-9_\-]+)", u)
        if m_mani:
            return {"platform": "manifold", "slug": m_mani.group(1)}
        return None

    @classmethod
    def fetch_polymarket(cls, slug):
        url = f"https://gamma-api.polymarket.com/events?slug={slug}"
        status, body, _ = http_get(url)
        events = json.loads(body)
        if not events:
            raise RuntimeError(f"Evento {slug} no encontrado en Polymarket.")
        ev = events[0]
        markets = ev.get("markets", [])
        outcomes_data = []

        for m in markets:
            outcomes_data.append({
                "question": m.get("question"),
                "outcome_prices": m.get("outcomePrices"),
                "volume": m.get("volume"),
            })

        desc = ev.get("description", "")
        summary_text = f"Mercado: {ev.get('title')}\n\nDescripción:\n{desc}\n\nResultados:\n" + json.dumps(outcomes_data, indent=2)

        return {
            "platform": "polymarket",
            "type": "prediction_event",
            "title": ev.get("title"),
            "slug": slug,
            "url": f"https://polymarket.com/event/{slug}",
            "volume": ev.get("volume"),
            "markets": outcomes_data,
            "content": summary_text,
            "text": summary_text,
            "author": "Polymarket",
        }

    @classmethod
    def fetch_manifold(cls, slug):
        url = f"https://api.manifold.markets/v0/slug/{slug}"
        status, body, _ = http_get(url)
        data = json.loads(body)

        prob = data.get("probability")
        prob_str = f"{prob * 100:.1f}%" if prob is not None else "N/A"
        summary = f"Mercado: {data.get('question')}\nProbabilidad: {prob_str}\nVolumen: ${data.get('volume', 0):,.2f}\nCreador: {data.get('creatorUsername')}"

        return {
            "platform": "manifold",
            "type": "prediction_market",
            "title": data.get("question"),
            "slug": slug,
            "url": data.get("url"),
            "probability": prob,
            "volume": data.get("volume", 0),
            "content": summary,
            "text": summary,
            "author": data.get("creatorUsername"),
        }


# -----------------------------------------------------------------------------
# ADAPTER 11: Wikipedia Engine (Historial de Revisiones y Disputas)
# -----------------------------------------------------------------------------

class WikipediaAdapter:
    """Extrae historial de revisiones, disputas editoriales y guerras de edición en Wikipedia."""

    @staticmethod
    def parse_url(url):
        u = url.strip()
        m = re.search(r"https?://([a-zA-Z]{2,3})\.wikipedia\.org/wiki/([^#\?]+)", u)
        if m:
            return {"lang": m.group(1), "title": urllib.parse.unquote(m.group(2))}
        return None

    @classmethod
    def fetch_revisions(cls, lang, title):
        clean_title = title.replace("_", " ")
        api_url = f"https://{lang}.wikipedia.org/w/api.php?action=query&prop=revisions&titles={urllib.parse.quote(clean_title)}&rvprop=timestamp|user|comment|size&rvlimit=50&format=json"
        status, body, _ = http_get(api_url)
        data = json.loads(body)

        pages = data.get("query", {}).get("pages", {})
        page = list(pages.values())[0] if pages else {}
        revisions = page.get("revisions", [])

        # Analizar guerras de edición y concentración de editores
        editors = {}
        reverts = 0
        for r in revisions:
            usr = r.get("user", "[anonymous]")
            editors[usr] = editors.get(usr, 0) + 1
            comm = (r.get("comment") or "").lower()
            if any(term in comm for term in ["revert", "undid", "rv", "deshecha", "vandalismo"]):
                reverts += 1

        edit_war_index = round(reverts / max(1, len(revisions)), 2)
        editor_entropy = calculate_shannon_entropy(editors)

        comments_text = "\n".join(f"[{r.get('timestamp')[:10]}] {r.get('user')}: {r.get('comment')}" for r in revisions[:20])

        return {
            "platform": "wikipedia",
            "type": "article_audit",
            "title": clean_title,
            "lang": lang,
            "url": f"https://{lang}.wikipedia.org/wiki/{title}",
            "total_revisions_indexed": len(revisions),
            "revert_count": reverts,
            "edit_war_index": edit_war_index,
            "editor_entropy": editor_entropy,
            "verdict": "⚠️ ALTA POLARIZACIÓN / GUERRA DE EDICIÓN" if edit_war_index > 0.25 else "✅ EDICIÓN ESTABLE Y CONSENSUADA",
            "top_editors": sorted(editors.items(), key=lambda x: x[1], reverse=True)[:5],
            "content": comments_text,
            "text": comments_text,
            "author": "Wikipedia Editors",
        }


# -----------------------------------------------------------------------------
# SQLite WAL Storage & Telemetry (Sovereign Archival Vault)
# -----------------------------------------------------------------------------

def init_vault(db_path=DEFAULT_DB_PATH):
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    conn = sqlite3.connect(db_path, timeout=5)
    conn.execute("PRAGMA journal_mode = WAL;")
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS socint_vault (
                record_id TEXT PRIMARY KEY,
                platform TEXT NOT NULL,
                target_type TEXT NOT NULL,
                url TEXT NOT NULL,
                author TEXT,
                title TEXT,
                raw_content TEXT,
                metrics_json TEXT,
                epistemic_counts_json TEXT,
                snr_score REAL,
                captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    conn.close()


def save_to_vault(data, db_path=DEFAULT_DB_PATH):
    init_vault(db_path)
    conn = sqlite3.connect(db_path, timeout=5)
    with conn:
        rec_id = str(data.get("id") or data.get("permalink") or data.get("url") or f"{data.get('platform')}_{int(time.time())}")
        plat = data.get("platform", "unknown")
        target_type = data.get("type", "unknown")
        url = data.get("url") or data.get("canonical_url") or data.get("permalink") or ""
        author = ""
        if isinstance(data.get("author"), dict):
            author = data["author"].get("screen_name") or data["author"].get("handle") or data["author"].get("name") or ""
        elif isinstance(data.get("author"), str):
            author = data.get("author")

        title = data.get("title") or (data.get("text", "")[:80] if data.get("text") else "")
        content = data.get("text") or data.get("content") or data.get("selftext") or ""
        metrics_json = json.dumps(data.get("metrics") or {})
        epistemic = data.get("epistemic_audit") or {}
        epistemic_counts = json.dumps(epistemic.get("counts") or {})
        snr = epistemic.get("signal_ratio", 0.50)

        conn.execute("""
            INSERT OR REPLACE INTO socint_vault
            (record_id, platform, target_type, url, author, title, raw_content, metrics_json, epistemic_counts_json, snr_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (rec_id, plat, target_type, url, author, title, content, metrics_json, epistemic_counts, snr))

    conn.close()
    return rec_id


def vault_stats(db_path=DEFAULT_DB_PATH):
    init_vault(db_path)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    total_records = cur.execute("SELECT COUNT(*) FROM socint_vault;").fetchone()[0]
    platforms = cur.execute("SELECT platform, COUNT(*) FROM socint_vault GROUP BY platform;").fetchall()
    avg_snr = cur.execute("SELECT AVG(snr_score) FROM socint_vault;").fetchone()[0] or 0.0
    latest = cur.execute("SELECT record_id, platform, author, snr_score, captured_at FROM socint_vault ORDER BY captured_at DESC LIMIT 5;").fetchall()
    conn.close()

    lines = [
        f"=== TELEMETRÍA DE BÓVEDA SOCINT C5-REAL (SQLite WAL) ===",
        f"Base de datos: {db_path}",
        f"Registros Totales: {total_records}",
        f"Score SNR Medio Global: {avg_snr * 100:.1f}%",
        f"",
        f"Distribución por Plataforma:",
    ]
    for p, c in platforms:
        lines.append(f"  • {p.upper():14s}: {c} registros")
    lines.append("")
    lines.append("Últimos Registros Archivados:")
    for r in latest:
        lines.append(f"  - [{r[4]}] {r[1].upper()} | ID: {r[0]} | Autor: {r[2]} | SNR: {r[3]*100:.0f}%")

    return "\n".join(lines)


def vault_query(sql_query, db_path=DEFAULT_DB_PATH):
    init_vault(db_path)
    clean_sql = sql_query.strip()
    if not clean_sql.lower().startswith("select"):
        raise ValueError("Solo se autorizan sentencias de lectura SELECT en la bóveda.")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(clean_sql)
    col_names = [d[0] for d in cur.description]
    rows = cur.fetchall()
    conn.close()

    lines = [" | ".join(col_names), "-" * (len(" | ".join(col_names)) + 5)]
    for r in rows:
        lines.append(" | ".join(str(val) for val in r))
    return "\n".join(lines)


# -----------------------------------------------------------------------------
# Markdown Report Generator (Omnivectorial)
# -----------------------------------------------------------------------------

def generate_markdown_report(data, epistemic_audit=None, astroturf_audit=None):
    plat = data.get("platform", "unknown").upper()
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = [
        f"# Informe de Inteligencia Social SOCINT C5-REAL: {plat}",
        f"",
        f"> **Auditoría Forense C5:** Extracción Determinista en Silicio  ",
        f"> **Fecha de Captura:** `{ts}`  ",
        f"> **Estado del Canal:** `Soberano · Zero Cloud Leak`  ",
        f"",
        f"---",
        f"",
    ]

    if plat == "X":
        if data.get("type") == "profile":
            lines.extend([
                f"## 👤 Auditoría Forense de Perfil X (Twitter): @{data.get('screen_name')}",
                f"",
                f"- **Nombre:** **{data.get('name')}** (`@{data.get('screen_name')}`)",
                f"- **Verificación:** `{'✅ ' + str(data.get('verification_type')).upper() if data.get('verified') else '❌ No verificado'}`",
                f"- **Audiencia:** {data.get('followers', 0):,} Followers | {data.get('following', 0):,} Siguiendo",
                f"- **Actividad:** {data.get('tweets_count', 0):,} Tweets | {data.get('media_count', 0):,} Media | {data.get('likes', 0):,} Likes",
                f"- **Fecha de Creación:** `{data.get('joined', 'N/A')}`",
                f"",
                f"### Biografía",
                f"> {data.get('description', '*(Sin biografía)*')}",
                f"",
            ])
        elif data.get("type") == "thread":
            author = data.get("author", {}) or {}
            metrics = data.get("metrics", {}) or {}
            lines.extend([
                f"## 🧵 Hilo Desenlazado de X (Twitter): @{author.get('screen_name')}",
                f"",
                f"- **Autor:** **{author.get('name')}** (`@{author.get('screen_name')}`)",
                f"- **Total de Entregas:** `{data.get('total_tweets')}` tweets encadenados",
                f"- **Impacto Agregado:** {metrics.get('total_likes', 0):,} Likes | {metrics.get('total_retweets', 0):,} RTs | {metrics.get('total_replies', 0):,} Replies",
                f"- **Enlace Raíz:** [{data.get('url')}]({data.get('url')})",
                f"",
                f"### Contenido Completo del Hilo",
                f"",
                f"```text",
                f"{data.get('text', '')}",
                f"```",
                f"",
            ])
        else:
            author = data.get("author", {}) or {}
            metrics = data.get("metrics", {}) or {}
            likes = int(metrics.get("likes") or 0)
            retweets = int(metrics.get("retweets") or 0)
            replies = int(metrics.get("replies") or 0)
            views = int(metrics.get("views") or 0)

            author_display = (author.get('name') or author.get('screen_name')) if isinstance(author, dict) else str(author)
            screen_display = author.get('screen_name', author_display) if isinstance(author, dict) else str(author)
            lines.extend([
                f"## 🛰️ Telemetría de Publicación (X/Twitter)",
                f"",
                f"- **Autor:** **{author_display}** (`@{screen_display}`)",
                f"- **URL:** [{data.get('url')}]({data.get('url')})",
                f"- **Fecha:** `{data.get('created_at', 'N/A')}`",
                f"- **Métricas de Impacto:** {likes:,} Likes | {retweets:,} RTs | {replies:,} Replies | {views:,} Views",
                f"",
                f"### Contenido Extraído",
                f"",
                f"```text",
                f"{data.get('text', '')}",
                f"```",
                f"",
            ])

    elif plat == "SUBSTACK":
        if data.get("type") == "post":
            likes = int(data.get("likes") or 0)
            comments = int(data.get("comments_count") or 0)
            lines.extend([
                f"## 📰 Publicación de Substack: {data.get('title')}",
                f"",
                f"- **Autor:** `{data.get('author')}`",
                f"- **URL:** [{data.get('canonical_url')}]({data.get('canonical_url')})",
                f"- **Fecha:** `{data.get('post_date')}` | Palabras: `{data.get('word_count')}`",
                f"- **Engagement:** {likes:,} Likes | {comments:,} Comentarios",
                f"- **Acceso:** `{'🔒 Paywalled' if data.get('paywalled') else '🔓 Abierto'}`",
                f"",
                f"### Extracto / Cuerpo del Artículo",
                f"",
                f"{data.get('content', '')[:2500]}...",
                f"",
            ])

    elif plat == "REDDIT":
        if data.get("type") == "user_dossier":
            dist = data.get("subreddit_distribution", {})
            lines.extend([
                f"## 🕵️ Dossier Forense de Usuario Reddit: /u/{data.get('username')}",
                f"",
                f"- **URL:** [{data.get('url')}]({data.get('url')})",
                f"- **Posts Indexados:** `{data.get('total_submitted_indexed')}`",
                f"- **Entropía de Subreddits (H):** `{data.get('subreddit_entropy')} bits`",
                f"- **Veredicto:** `{data.get('entropy_verdict')}`",
                f"",
                f"### Distribución de Actividad por Subreddit",
                f"",
                f"| Subreddit | Frecuencia | Proporción |",
                f"| :--- | :--- | :--- |",
            ])
            tot = max(1, data.get("total_submitted_indexed", 1))
            for sub, cnt in sorted(dist.items(), key=lambda x: x[1], reverse=True)[:10]:
                lines.append(f"| `r/{sub}` | {cnt} posts | {cnt/tot*100:.1f}% |")
            lines.append("")
        elif data.get("type") == "thread":
            lines.extend([
                f"## 👾 Hilo de Discusión en Reddit: r/{data.get('subreddit')}",
                f"",
                f"- **Título:** **{data.get('title')}**",
                f"- **Autor:** `/u/{data.get('author')}`",
                f"- **Puntuación:** `{data.get('score', 0):,}` (Upvote Ratio: `{float(data.get('upvote_ratio', 1.0))*100:.1f}%`)",
                f"- **Enlace:** [{data.get('permalink')}]({data.get('permalink')})",
                f"",
                f"### Texto Principal",
                f"{data.get('selftext', '*(Sin texto)*')[:1500]}",
                f"",
            ])

    elif plat == "YOUTUBE":
        lines.extend([
            f"## 📺 Telemetría de YouTube: {data.get('title')}",
            f"",
            f"- **Creador / Canal:** **{data.get('author')}**",
            f"- **URL:** [{data.get('url')}]({data.get('url')})",
            f"",
            f"### Transcripción de Audio",
            f"{data.get('transcript', '')[:2000]}...",
            f"",
        ])

    elif plat == "HACKERNEWS":
        if data.get("type") == "item":
            lines.extend([
                f"## 🟠 Hacker News: {data.get('title')}",
                f"",
                f"- **Autor:** `/u/{data.get('author')}` | Puntos: `{data.get('points')}`",
                f"- **URL HN:** [{data.get('url')}]({data.get('url')})",
                f"- **Enlace Externo:** {data.get('external_url', 'N/A')}",
                f"",
                f"### Comentarios Destacados ({len(data.get('comments', []))} analizados)",
                f"",
            ])
            for c in data.get("comments", [])[:6]:
                lines.append(f"- **{c.get('author')}** (Nivel {c.get('depth')}): {c.get('body')[:200]}")
            lines.append("")
        elif data.get("type") == "user":
            lines.extend([
                f"## 🟠 Hacker News Usuario: {data.get('username')}",
                f"",
                f"- **Karma:** `{data.get('karma'):,}` | Envíos: `{data.get('submitted_count')}`",
                f"- **Biografía:** {data.get('about', '*(Sin biografía)*')}",
                f"",
            ])

    elif plat == "BLUESKY":
        if data.get("type") == "post":
            author = data.get("author", {}) or {}
            metrics = data.get("metrics", {}) or {}
            lines.extend([
                f"## 🦋 Bluesky (ATProto): @{author.get('handle')}",
                f"",
                f"- **Autor:** **{author.get('displayName')}** (`@{author.get('handle')}`)",
                f"- **Engagement:** {metrics.get('likes', 0):,} Likes | {metrics.get('reposts', 0):,} Reposts | {metrics.get('replies', 0):,} Respuestas",
                f"- **URL:** [{data.get('url')}]({data.get('url')})",
                f"",
                f"### Post",
                f"```text\n{data.get('text', '')}\n```",
                f"",
            ])
        elif data.get("type") == "profile":
            lines.extend([
                f"## 🦋 Bluesky Perfil: @{data.get('handle')}",
                f"",
                f"- **Nombre:** **{data.get('displayName')}** | Posts: `{data.get('postsCount', 0):,}`",
                f"- **Seguidores:** `{data.get('followersCount', 0):,}` | Siguiendo: `{data.get('followsCount', 0):,}`",
                f"- **Biografía:** {data.get('description', '')}",
                f"",
            ])

    elif plat == "TELEGRAM":
        lines.extend([
            f"## ✈️ Canal de Telegram: {data.get('channel')}",
            f"",
            f"- **URL:** [{data.get('url')}]({data.get('url')})",
            f"- **Mensajes Extraídos:** `{data.get('total_messages')}`",
            f"",
            f"### Telemetría de Mensajes Recientes",
            f"",
        ])
        for idx, m in enumerate(data.get("messages", [])[:5], 1):
            lines.append(f"{idx}. `[{m.get('views')} vistas]` {m.get('text')[:250]}...")
        lines.append("")

    elif plat == "GITHUB":
        if data.get("type") == "user_activity":
            lines.extend([
                f"## 🐙 Actividad Pública de Desarrollador: @{data.get('username')}",
                f"",
                f"- **Eventos Recientes Indexados:** `{data.get('total_events')}`",
                f"- **Perfil:** [{data.get('url')}]({data.get('url')})",
                f"",
                f"### Historial Cronológico",
                f"",
            ])
            for ev in data.get("events", [])[:8]:
                lines.append(f"- `[{ev.get('date')[:10]}]` [{ev.get('title')}]({ev.get('link')})")
            lines.append("")
        elif data.get("type") == "repo_commits":
            lines.extend([
                f"## 🐙 Historial de Commits: {data.get('owner')}/{data.get('repo')}",
                f"",
                f"Total de commits indexados: **{data.get('total_commits')}**",
                f"",
            ])
            for c in data.get("commits", [])[:8]:
                lines.append(f"- `[{c.get('date')[:10]}]` **{c.get('author')}**: {c.get('commit')}")
            lines.append("")

    elif plat == "MASTODON":
        metrics = data.get("metrics", {})
        lines.extend([
            f"## 🐘 Fediverse / Mastodon ({data.get('instance')})",
            f"",
            f"- **Autor:** `@{data.get('author')}`",
            f"- **URL:** [{data.get('url')}]({data.get('url')})",
            f"- **Engagement:** {metrics.get('favourites', 0)} Likes | {metrics.get('reblogs', 0)} Boosts | {metrics.get('replies', 0)} Respuestas",
            f"",
            f"### Toot",
            f"{data.get('content', '')}",
            f"",
        ])

    elif plat in ("POLYMARKET", "MANIFOLD"):
        prob_str = f"{float(data.get('probability', 0.5))*100:.1f}%" if data.get("probability") is not None else "Multi-resultado"
        lines.extend([
            f"## 🎲 Mercado de Predicción ({plat}): {data.get('title')}",
            f"",
            f"- **Probabilidad Implícita:** `{prob_str}`",
            f"- **Volumen:** `${float(data.get('volume', 0)):,.2f}`",
            f"- **URL:** [{data.get('url')}]({data.get('url')})",
            f"",
            f"### Resumen de Mercado",
            f"{data.get('content', '')}",
            f"",
        ])

    elif plat == "WIKIPEDIA":
        lines.extend([
            f"## 📖 Auditoría de Wikipedia: {data.get('title')} ({data.get('lang')}.wikipedia.org)",
            f"",
            f"- **Revisiones Indexadas:** `{data.get('total_revisions_indexed')}` | Reversiones: `{data.get('revert_count')}`",
            f"- **Índice de Guerra de Edición:** `{data.get('edit_war_index') * 100:.1f}%`",
            f"- **Entropía de Editores:** `{data.get('editor_entropy')} bits`",
            f"- **Veredicto Forense:** `{data.get('verdict')}`",
            f"- **URL:** [{data.get('url')}]({data.get('url')})",
            f"",
            f"### Editores Principales",
            f"",
        ])
        for ed, cnt in data.get("top_editors", []):
            lines.append(f"- **{ed}**: {cnt} revisiones")
        lines.append("")

    # Auditoría Forense de Astroturfing
    if astroturf_audit and astroturf_audit.get("verdict"):
        lines.extend([
            f"---",
            f"",
            f"## 🤖 Auditoría de Astroturfing & Shilling (Jaccard N-Grams)",
            f"",
            f"- **Veredicto Forense:** `{astroturf_audit.get('verdict')}`",
            f"- **Índice de Riesgo Astroturf:** `{astroturf_audit.get('astroturf_risk_score') * 100:.1f}%`",
            f"- **Concentración de Autores:** `{astroturf_audit.get('author_concentration') * 100:.1f}%`",
            f"- **Pares de Comentarios Cuasi-Idénticos:** `{astroturf_audit.get('duplicate_clusters')}`",
            f"",
        ])

    # Auditoría Epistemológica
    if epistemic_audit:
        c = epistemic_audit.get("counts", {})
        lines.extend([
            f"---",
            f"",
            f"## ⚖️ Matriz de Auditoría Epistemológica C5-REAL",
            f"",
            f"- **Ratio de Señal/Ruido (SNR):** `{epistemic_audit.get('signal_ratio') * 100:.1f}%`",
            f"- **Hechos Verificados:** `{c.get('hechos_verificados')}`",
            f"- **Evidencia Experimental & Telemetría:** `{c.get('evidencia_experimental')}`",
            f"- **Modelos & Doctrina:** `{c.get('modelos_doctrina')}`",
            f"- **Especulación & Sesgo / Falsa Causalidad:** `{c.get('especulacion_sesgo')}`",
            f"",
        ])

    # Análisis de Dispersión Léxica
    lexical = data.get("lexical_dispersion")
    if lexical:
        lines.extend([
            f"---",
            f"",
            f"## 📚 Dispersión Léxica & Entropía de Vocabulario",
            f"",
            f"- **Tokens Totales:** `{lexical.get('total_tokens')}`",
            f"- **Vocabulario Único:** `{lexical.get('vocabulary')}`",
            f"- **Densidad Léxica:** `{lexical.get('lexical_density') * 100:.1f}%`",
            f"- **Ratio Hapax Legomena (Unicidad):** `{lexical.get('hapax_ratio') * 100:.1f}%`",
            f"- **Diagnóstico:** `{lexical.get('verdict')}`",
            f"",
        ])

    # Análisis de Dinámica Temporal
    temporal = data.get("temporal_forensics")
    if temporal:
        lines.extend([
            f"---",
            f"",
            f"## ⏱️ Dinámica Temporal & Ráfagas (CIB Detection)",
            f"",
            f"- **Veredicto Temporal:** `{temporal.get('verdict')}`",
            f"- **Índice de Burstiness (B):** `{temporal.get('burstiness')}`",
            f"- **Factor de Fano:** `{temporal.get('fano_factor')}`",
            f"- **Ráfagas Coordinadas (<=15s):** `{temporal.get('coordinated_clusters')}`",
            f"- **Intervalo Medio entre Llegadas:** `{temporal.get('mean_delta_sec')}s`",
            f"",
        ])

    # Análisis de Sentimiento y Afecto
    sentiment = data.get("sentiment_affect")
    if sentiment:
        lines.extend([
            f"---",
            f"",
            f"## 🎭 Análisis de Sentimiento & Volatilidad Emocional",
            f"",
            f"- **Veredicto de Tono:** `{sentiment.get('verdict')}`",
            f"- **Polaridad Media:** `{sentiment.get('mean_polarity') * 100:+.1f}%`",
            f"- **Volatilidad Emocional:** `{sentiment.get('emotional_volatility')}`",
            f"- **Alerta de Indignación Polarizada:** `{'SÍ' if sentiment.get('outrage_flag') else 'NO'}`",
            f"",
        ])

    # Sello Criptográfico Merkle
    merkle_seal = data.get("merkle_seal")
    if merkle_seal:
        lines.extend([
            f"---",
            f"",
            f"## 🔒 Sello Criptográfico de Evidencia (Merkle Attestation)",
            f"",
            f"- **Merkle Root:** `{merkle_seal.get('merkle_root')}`",
            f"- **Campos Sellados:** `{merkle_seal.get('leaf_count')}`",
            f"- **Timestamp de Sello:** `{merkle_seal.get('sealed_at')}`",
            f"",
        ])

    # Métricas de Centralidad y Actores Clave
    centrality = data.get("network_centrality")
    if centrality:
        lines.extend([
            f"---",
            f"",
            f"## 🌐 Centralidad de Red & Actores Clave (PageRank & Degree)",
            f"",
        ])
        for inf in centrality.get("top_influencers", [])[:5]:
            lines.append(f"- **{inf['node']}**: PageRank `{inf['score']:.5f}` | In-Degree `{inf['in_degree']}`")
        lines.append("")

    # Matriz de Acción Coordinada (CIB)
    co_actions = data.get("coordinated_actions")
    if co_actions:
        lines.extend([
            f"---",
            f"",
            f"## 🤝 Matriz de Acción Coordinada (CIB Co-Occurrence)",
            f"",
            f"- **Veredicto de Sincronización:** `{co_actions.get('verdict')}`",
            f"- **Score de Sincronización CIB:** `{co_actions.get('cib_synchronization_score') * 100:.1f}%`",
            f"- **Pares Sincronizados:** `{co_actions.get('total_synchronized_pairs')}`",
            f"",
        ])
        for p in co_actions.get("co_actions", [])[:5]:
            lines.append(f"- **@{p['actor_a']}** ⟷ **@{p['actor_b']}**: `{p['co_occurrences']}` co-ocurrencias en ráfaga")
        lines.append("")

    return "\n".join(lines)


# -----------------------------------------------------------------------------
# Main CLI Orchestrator (Omnivectorial)
# -----------------------------------------------------------------------------


def generate_html_report(data, epistemic_audit=None, astroturf_audit=None, actor_network=None):
    """Genera un panel HTML autónomo, sin dependencias CDN, con modo oscuro y CSS embebido."""
    plat = data.get("platform", "UNKNOWN")
    url = data.get("url", "")
    extracted_at = data.get("extracted_at", "")

    snr_val = f"{epistemic_audit.get('signal_ratio', 0.5) * 100:.1f}%" if epistemic_audit else "N/A"
    astroturf_val = f"{astroturf_audit.get('astroturf_risk_score', 0.0) * 100:.1f}%" if astroturf_audit else "N/A"
    verdict = astroturf_audit.get("verdict", "No evaluado") if astroturf_audit else "No evaluado"

    net_nodes = actor_network.to_dict()["total_nodes"] if actor_network else 0
    net_edges = actor_network.to_dict()["total_edges"] if actor_network else 0

    html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SOCINT Forensics · {html.escape(plat)}</title>
<style>
  :root {{
    --bg: #0d1117;
    --card-bg: #161b22;
    --border: #30363d;
    --text: #c9d1d9;
    --heading: #f0f6fc;
    --accent: #58a6ff;
    --success: #3fb950;
    --warning: #d29922;
    --danger: #f85149;
  }}
  body {{
    margin: 0;
    padding: 24px;
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.6;
  }}
  .container {{ max-width: 960px; margin: 0 auto; }}
  header {{ border-bottom: 1px solid var(--border); padding-bottom: 16px; margin-bottom: 24px; }}
  h1, h2, h3 {{ color: var(--heading); }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 24px; }}
  .card {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 16px; }}
  .metric {{ font-size: 28px; font-weight: bold; color: var(--accent); }}
  .badge {{ display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; background: var(--border); }}
  pre, code {{ background: #0b0e14; border: 1px solid var(--border); border-radius: 6px; padding: 12px; overflow-x: auto; color: #79c0ff; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }}
  footer {{ margin-top: 40px; padding-top: 16px; border-top: 1px solid var(--border); font-size: 13px; color: #8b949e; text-align: center; }}
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>🔍 SOCINT Forensic Dossier · <span style="color:var(--accent);">{html.escape(plat)}</span></h1>
    <div><strong>Objetivo:</strong> <a href="{html.escape(url)}" style="color:var(--accent);" target="_blank">{html.escape(url)}</a></div>
    <div><small>Indexado en silicio: {html.escape(extracted_at)}</small></div>
  </header>

  <div class="grid">
    <div class="card">
      <div class="badge">EPISTEMIC SNR</div>
      <div class="metric">{snr_val}</div>
      <small>Pureza metodológica C5-REAL</small>
    </div>
    <div class="card">
      <div class="badge">ASTROTURF RISK</div>
      <div class="metric">{astroturf_val}</div>
      <small>{html.escape(verdict)}</small>
    </div>
    <div class="card">
      <div class="badge">ACTOR NETWORK</div>
      <div class="metric">{net_nodes} / {net_edges}</div>
      <small>Nodos / Interacciones mapeadas</small>
    </div>
  </div>

  <div class="card" style="margin-bottom:24px;">
    <h2>📄 Telemetría Primaria</h2>
    <pre>{html.escape(json.dumps(data, indent=2, ensure_ascii=False))}</pre>
  </div>

  <footer>
    C5-REAL Forensic Engine · Zero External Dependencies · Borja Fernández Angulo
  </footer>
</div>
</body>
</html>"""
    return html_template


def generate_csv_report(data_list):
    """Genera un reporte tabular en formato CSV RFC 4180."""
    import csv
    import io
    out = io.StringIO()
    writer = csv.writer(out, quoting=csv.QUOTE_MINIMAL)
    writer.writerow([
        "platform", "url", "author", "extracted_at",
        "epistemic_snr", "astroturf_risk", "total_comments", "content_preview"
    ])

    for item in data_list:
        author = item.get("author") or item.get("username") or item.get("channel") or "anon"
        snr = item.get("epistemic_audit", {}).get("signal_ratio", "") if item.get("epistemic_audit") else ""
        astro = item.get("astroturf_audit", {}).get("astroturf_risk_score", "") if item.get("astroturf_audit") else ""
        comments_cnt = len(item.get("comments", []))
        content = item.get("text") or item.get("content") or item.get("selftext") or item.get("description") or ""
        preview = re.sub(r'\s+', ' ', content)[:200].strip()

        writer.writerow([
            item.get("platform", ""),
            item.get("url", ""),
            author,
            item.get("extracted_at", ""),
            snr,
            astro,
            comments_cnt,
            preview
        ])

    return out.getvalue()


def main():
    parser = argparse.ArgumentParser(
        description="Suite Soberana de Inteligencia Social (SOCINT C5-REAL): Extracción omnivectorial sin API de pago en 11 plataformas."
    )
    parser.add_argument("--url", "-u", type=str, help="URL de la publicación, hilo, perfil o mercado a investigar.")
    parser.add_argument("--batch", "-b", type=str, help="Archivo con lista de URLs a procesar en lote.")
    parser.add_argument("--platform", "-p", choices=[
        "auto", "x", "substack", "reddit", "youtube", "hackernews",
        "bluesky", "telegram", "github", "mastodon", "prediction", "wikipedia"
    ], default="auto", help="Plataforma de destino.")
    parser.add_argument("--limit", "-l", type=int, default=25, help="Límite de elementos a recuperar.")
    parser.add_argument("--depth", "-d", type=int, default=3, help="Profundidad de comentarios.")
    parser.add_argument("--format", "-f", choices=["json", "markdown", "html", "csv"], default="markdown", help="Formato de salida.")
    parser.add_argument("--output", "-o", type=str, help="Ruta de archivo para guardar el resultado.")
    parser.add_argument("--unfold", action="store_true", help="Desenrollar hilos completos en X (Twitter).")
    parser.add_argument("--search", "-s", type=str, help="Buscar término dentro de un subreddit.")
    parser.add_argument("--audit-pods", action="store_true", help="Auditar red de recomendaciones en Substack.")
    parser.add_argument("--network", action="store_true", help="Construir y reportar el grafo de red de actores.")
    parser.add_argument("--export-mermaid", type=str, help="Exportar grafo de interacción en sintaxis Mermaid.")
    parser.add_argument("--export-dot", type=str, help="Exportar grafo de interacción en sintaxis Graphviz DOT.")
    parser.add_argument("--export-gexf", type=str, help="Exportar grafo de interacción en formato Gephi XML GEXF.")
    parser.add_argument("--centrality-check", action="store_true", help="Calcular métricas de centralidad y PageRank en el grafo de actores.")
    parser.add_argument("--cib-matrix", action="store_true", help="Analizar sincronización temporal y co-ocurrencia de pares de cuentas sospechosas.")
    parser.add_argument("--export-stix", type=str, help="Exportar paquete de inteligencia de amenazas en formato STIX 2.1 JSON.")
    parser.add_argument("--pivot", type=str, help="Generar dossier de investigación unificada para un handle a través de las 11 plataformas.")
    parser.add_argument("--burst-check", action="store_true", help="Auditar dinámica temporal de comentarios para detectar bots periódicos o ráfagas CIB.")
    parser.add_argument("--lexical-check", action="store_true", help="Calcular densidad léxica y ratio de Hapax Legomena contra texto sintético.")
    parser.add_argument("--sentiment-check", action="store_true", help="Calcular polaridad y volatilidad emocional en comentarios.")
    parser.add_argument("--merkle-seal", action="store_true", help="Sellar evidencia con raíz criptográfica de Merkle (tamper-evidence).")
    parser.add_argument("--save-vault", action="store_true", help="Almacenar registro en SQLite WAL vault.")
    parser.add_argument("--vault-stats", action="store_true", help="Consultar estadísticas y telemetría de la bóveda SQLite.")
    parser.add_argument("--vault-query", type=str, help="Ejecutar consulta SELECT en la bóveda SQLite.")
    parser.add_argument("--vault-db", type=str, default=DEFAULT_DB_PATH, help="Ruta de base de datos SQLite WAL.")

    args = parser.parse_args()

    if args.vault_stats:
        print(vault_stats(args.vault_db))
        return

    if args.vault_query:
        print(vault_query(args.vault_query, args.vault_db))
        return

    if args.pivot:
        dossier = IdentityPivotEngine.generate_dossier_targets(args.pivot)
        if args.format == "json":
            print(json.dumps(dossier, indent=2, ensure_ascii=False))
        else:
            print(f"=== DOSSIER DE IDENTIDAD UNIFICADA (OSINT PIVOT) · @{dossier['handle']} ===")
            for t in dossier["targets"]:
                print(f"  [{t['platform'].upper():<12}] {t['candidate_url']}")
        return

    if not args.url and not args.batch:
        parser.print_help()
        sys.exit(1)

    urls_to_process = []
    if args.batch:
        batch_path = os.path.expanduser(args.batch)
        if not os.path.exists(batch_path):
            print(f"[!] Error: Archivo batch no encontrado: {batch_path}", file=sys.stderr)
            sys.exit(1)
        with open(batch_path, "r", encoding="utf-8") as bf:
            urls_to_process = [line.strip() for line in bf if line.strip() and not line.startswith("#")]
    else:
        urls_to_process = [args.url.strip()]

    all_reports = []
    extracted_items_for_csv = []

    for target_url in urls_to_process:
        platform = args.platform
        if platform == "auto":
            if any(k in target_url for k in ["twitter.com", "x.com", "fxtwitter.com"]):
                platform = "x"
            elif "substack.com" in target_url or "/p/" in target_url:
                platform = "substack"
            elif any(target_url.startswith(p) for p in ["r/", "u/"]) or "reddit.com" in target_url:
                platform = "reddit"
            elif any(k in target_url for k in ["youtube.com", "youtu.be"]):
                platform = "youtube"
            elif any(k in target_url for k in ["news.ycombinator.com", "hn:"]):
                platform = "hackernews"
            elif "bsky.app" in target_url:
                platform = "bluesky"
            elif any(k in target_url for k in ["t.me", "telegram.me"]):
                platform = "telegram"
            elif "github.com" in target_url:
                platform = "github"
            elif any(k in target_url for k in ["polymarket.com", "manifold.markets"]):
                platform = "prediction"
            elif "wikipedia.org" in target_url:
                platform = "wikipedia"
            elif re.search(r"https?://[^/]+/@", target_url):
                platform = "mastodon"
            else:
                print(f"[!] Advertencia: No se pudo auto-detectar plataforma para: {target_url}", file=sys.stderr)
                continue

        extracted_data = None
        text_for_audit = ""
        comments_for_astroturf = []

        if platform == "x":
            kind, user, tweet_id = XAdapter.parse_url(target_url)
            if kind == "profile":
                extracted_data = XAdapter.fetch_profile(user)
                text_for_audit = extracted_data.get("description", "")
            elif kind == "tweet" and tweet_id:
                if args.unfold:
                    extracted_data = XAdapter.unfold_thread(user, tweet_id)
                else:
                    extracted_data = XAdapter.fetch_tweet(user, tweet_id)
                text_for_audit = extracted_data.get("text", "")

        elif platform == "substack":
            sub_info = SubstackAdapter.parse_url(target_url)
            if sub_info:
                if sub_info["type"] == "post":
                    extracted_data = SubstackAdapter.fetch_post(sub_info["domain"], sub_info["slug"])
                    text_for_audit = extracted_data.get("content", "")
                    comments_for_astroturf = extracted_data.get("comments", [])
                else:
                    if args.audit_pods:
                        extracted_data = SubstackAdapter.audit_recommendation_network(sub_info["domain"])
                    else:
                        extracted_data = SubstackAdapter.fetch_publication_archive(sub_info["domain"], limit=args.limit)

        elif platform == "reddit":
            red_info = RedditAdapter.parse_url(target_url)
            if red_info:
                if red_info["type"] == "user":
                    extracted_data = RedditAdapter.fetch_user_dossier(red_info["username"], limit=args.limit)
                    text_for_audit = " ".join(p.get("title", "") for p in extracted_data.get("recent_posts", []))
                elif red_info["type"] == "thread":
                    extracted_data = RedditAdapter.fetch_thread(red_info["subreddit"], red_info["post_id"], depth=args.depth, comment_limit=args.limit)
                    text_for_audit = (extracted_data.get("selftext") or "") + "\n" + "\n".join(
                        c.get("body", "") for c in extracted_data.get("comments", [])
                    )
                    comments_for_astroturf = extracted_data.get("comments", [])
                elif red_info["type"] == "subreddit":
                    if args.search:
                        extracted_data = RedditAdapter.search_subreddit(red_info["subreddit"], args.search, limit=args.limit)
                    else:
                        extracted_data = RedditAdapter.fetch_subreddit(red_info["subreddit"], limit=args.limit)

        elif platform == "youtube":
            yt_info = YouTubeAdapter.parse_url(target_url)
            if yt_info:
                extracted_data = YouTubeAdapter.fetch_video(yt_info["video_id"])
                text_for_audit = extracted_data.get("transcript", "")

        elif platform == "hackernews":
            hn_info = HackerNewsAdapter.parse_url(target_url)
            if hn_info:
                if hn_info["type"] == "item":
                    extracted_data = HackerNewsAdapter.fetch_item(hn_info["item_id"])
                    text_for_audit = extracted_data.get("text", "") + "\n" + "\n".join(c.get("body", "") for c in extracted_data.get("comments", []))
                    comments_for_astroturf = extracted_data.get("comments", [])
                elif hn_info["type"] == "user":
                    extracted_data = HackerNewsAdapter.fetch_user(hn_info["username"])
                    text_for_audit = extracted_data.get("about", "")

        elif platform == "bluesky":
            bsky_info = BlueskyAdapter.parse_url(target_url)
            if bsky_info:
                if bsky_info["type"] == "post":
                    extracted_data = BlueskyAdapter.fetch_post(bsky_info["handle"], bsky_info["rkey"])
                    text_for_audit = extracted_data.get("text", "")
                elif bsky_info["type"] == "profile":
                    extracted_data = BlueskyAdapter.fetch_profile(bsky_info["handle"])
                    text_for_audit = extracted_data.get("description", "")

        elif platform == "telegram":
            tg_info = TelegramAdapter.parse_url(target_url)
            if tg_info:
                extracted_data = TelegramAdapter.fetch_channel(tg_info["channel"], tg_info.get("post_id"))
                text_for_audit = extracted_data.get("text", "")

        elif platform == "github":
            gh_info = GitHubAdapter.parse_url(target_url)
            if gh_info:
                if gh_info["type"] == "user":
                    extracted_data = GitHubAdapter.fetch_user_activity(gh_info["username"])
                else:
                    extracted_data = GitHubAdapter.fetch_repo_feed(gh_info["owner"], gh_info["repo"])
                text_for_audit = extracted_data.get("text", "")

        elif platform == "mastodon":
            masto_info = MastodonAdapter.parse_url(target_url)
            if masto_info:
                extracted_data = MastodonAdapter.fetch_status(masto_info["instance"], masto_info["status_id"])
                text_for_audit = extracted_data.get("content", "")

        elif platform == "prediction":
            pred_info = PredictionMarketAdapter.parse_url(target_url)
            if pred_info:
                if pred_info["platform"] == "polymarket":
                    extracted_data = PredictionMarketAdapter.fetch_polymarket(pred_info["slug"])
                else:
                    extracted_data = PredictionMarketAdapter.fetch_manifold(pred_info["slug"])
                text_for_audit = extracted_data.get("content", "")

        elif platform == "wikipedia":
            wiki_info = WikipediaAdapter.parse_url(target_url)
            if wiki_info:
                extracted_data = WikipediaAdapter.fetch_revisions(wiki_info["lang"], wiki_info["title"])
                text_for_audit = extracted_data.get("content", "")

        if not extracted_data:
            print(f"[!] Error procesando objetivo: {target_url}", file=sys.stderr)
            continue

        epistemic_audit = None
        if text_for_audit.strip():
            epistemic_audit = EpistemicClassifier.classify_text(text_for_audit)
            extracted_data["epistemic_audit"] = epistemic_audit

        astroturf_audit = None
        if comments_for_astroturf:
            astroturf_audit = AstroturfDetector.analyze_comments(comments_for_astroturf)
            extracted_data["astroturf_audit"] = astroturf_audit

        if args.save_vault:
            rec_id = save_to_vault(extracted_data, args.vault_db)
            extracted_data["vault_record_id"] = rec_id

        if comments_for_astroturf:
            ts_list = [
                c.get("created_utc") or c.get("timestamp")
                for c in comments_for_astroturf
                if (c.get("created_utc") or c.get("timestamp")) is not None
            ]
            if ts_list:
                extracted_data["temporal_forensics"] = TemporalForensics.analyze_timestamps(ts_list)

        if text_for_audit.strip():
            extracted_data["lexical_dispersion"] = LexicalDispersion.analyze_text(text_for_audit)

        if comments_for_astroturf:
            extracted_data["sentiment_affect"] = SentimentAffectEngine.analyze_thread(comments_for_astroturf)

        merkle_root = compute_merkle_root(extracted_data)
        extracted_data["merkle_seal"] = {
            "merkle_root": merkle_root,
            "leaf_count": len(extracted_data),
            "sealed_at": datetime.now(timezone.utc).isoformat()
        }

        actor_network = None
        if args.network or args.centrality_check or args.export_mermaid or args.export_dot or args.export_gexf or args.format == "html":
            actor_network = ActorNetwork.extract_from_data(extracted_data)
            extracted_data["actor_network"] = actor_network.to_dict()

        if (args.centrality_check or args.network) and actor_network:
            extracted_data["network_centrality"] = actor_network.compute_centrality()

        if args.cib_matrix and comments_for_astroturf:
            extracted_data["coordinated_actions"] = CoordinatedActionMatrix.analyze_co_actions(comments_for_astroturf)

        if args.export_stix:
            stix_bundle = StixThreatIntel.generate_bundle(
                extracted_data,
                astroturf_audit,
                extracted_data.get("temporal_forensics"),
                extracted_data.get("sentiment_affect")
            )
            with open(os.path.expanduser(args.export_stix), "w", encoding="utf-8") as sf:
                json.dump(stix_bundle, sf, indent=2, ensure_ascii=False)
            print(f"[✓] Bundle STIX 2.1 exportado en: {args.export_stix}")

        if args.export_mermaid and actor_network:
            with open(os.path.expanduser(args.export_mermaid), "w", encoding="utf-8") as mf:
                mf.write(actor_network.to_mermaid())
            print(f"[✓] Grafo Mermaid exportado en: {args.export_mermaid}")

        if args.export_dot and actor_network:
            with open(os.path.expanduser(args.export_dot), "w", encoding="utf-8") as df:
                df.write(actor_network.to_dot())
            print(f"[✓] Grafo Graphviz DOT exportado en: {args.export_dot}")

        if args.export_gexf and actor_network:
            with open(os.path.expanduser(args.export_gexf), "w", encoding="utf-8") as gf:
                gf.write(actor_network.to_gexf())
            print(f"[✓] Grafo Gephi GEXF exportado en: {args.export_gexf}")

        if args.format == "json":
            all_reports.append(json.dumps(extracted_data, indent=2, ensure_ascii=False))
        elif args.format == "html":
            all_reports.append(generate_html_report(extracted_data, epistemic_audit, astroturf_audit, actor_network))
        elif args.format == "csv":
            extracted_items_for_csv.append(extracted_data)
        else:
            rep = generate_markdown_report(extracted_data, epistemic_audit, astroturf_audit)
            if args.network and actor_network:
                rep += f"\n\n## 🕸️ Grafo de Interacciones (Mermaid)\n\n```mermaid\n{actor_network.to_mermaid()}\n```\n"
            all_reports.append(rep)

    if args.format == "csv":
        final_output = generate_csv_report(extracted_items_for_csv)
    else:
        final_output = "\n\n---\n\n".join(all_reports)

    if args.output:
        out_path = os.path.expanduser(args.output)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(final_output)
        print(f"[✓] Extracción completada. Guardado en: {out_path}")
    else:
        print(final_output)


if __name__ == "__main__":
    main()
