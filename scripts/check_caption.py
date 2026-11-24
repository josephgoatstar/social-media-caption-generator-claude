#!/usr/bin/env python3
"""Lint a social caption against platform/format rules.

Usage:
  python3 scripts/check_caption.py --platform instagram --format reel --text "..."
  python3 scripts/check_caption.py --platform discord --format announcement --file post.md
  echo "..." | python3 scripts/check_caption.py --platform tiktok

Exit code 1 if any FAIL, else 0. Stdlib only.
"""
import argparse
import re
import sys

# (min_chars, max_chars_soft, hard_limit, visible_preview_chars, max_hashtags)
RULES = {
    ("instagram", "reel"): (80, 200, 2200, 125, 5),
    ("instagram", "feed"): (60, 600, 2200, 125, 5),
    ("instagram", "flyer"): (60, 600, 2200, 125, 5),
    ("instagram", "carousel"): (300, 900, 2200, 125, 5),
    ("instagram", "story"): (1, 80, None, None, 0),  # per-frame text
    ("tiktok", "reel"): (100, 300, 4000, 90, 5),
    ("tiktok", "carousel"): (150, 500, 4000, 90, 5),
    ("tiktok", "title"): (10, 90, 90, None, 0),
    ("tiktok", "story"): (1, 80, None, None, 0),
    ("discord", "announcement"): (80, 1200, 2000, None, 0),
    ("discord", "post"): (1, 1200, 2000, None, 0),
    ("threads", "post"): (100, 280, 500, None, 1),
    ("facebook", "post"): (40, 80, 63206, None, 2),
    ("facebook", "reel"): (40, 150, 63206, None, 2),
    ("facebook-group", "post"): (200, 500, 63206, None, 0),
    ("youtube", "title"): (40, 70, 100, None, 0),
    ("youtube", "reel"): (150, 300, 5000, 100, 5),
    ("x", "post"): (70, 200, 280, None, 1),
}
DEFAULT_FORMAT = {
    "instagram": "reel", "tiktok": "reel", "discord": "announcement",
    "threads": "post", "facebook": "post", "facebook-group": "post",
    "youtube": "reel", "x": "post",
}
FORMAT_ALIASES = {"video": "reel", "short": "reel", "shorts": "reel",
                  "description": "reel", "photo": "carousel", "static": "flyer",
                  "image": "feed", "text": "post"}

BANNED_TAGS = {"fyp", "foryou", "foryoupage", "viral", "trending", "explore",
               "explorepage", "instagood", "like4like", "likeforlike",
               "follow4follow", "followforfollow", "f4f", "l4l", "xyzbca", "fypシ"}
BAIT = [r"\blike if\b", r"\bcomment yes\b", r"\btag \d+ friends?\b",
        r"\btag (a|your) friends?\b", r"\bshare before\b", r"\bdouble tap\b",
        r"\bfollow for follow\b", r"\breact with\b"]
FILLER_OPENERS = [r"^hey guys", r"^in today'?s video", r"^so,?\s", r"^let'?s dive in",
                  r"^check this out", r"^i'?m so excited to announce", r"^happy \w+day"]
AI_HYPE = ["game-changer", "game changer", "revolutionary", "unlock your potential",
           "elevate your", "delve", "seamless", "next level", "fast-paced world",
           "look no further"]
FB_TRIGGERS = ["buy now", "limited time", "click here", "giveaway", "contest",
               "make money", "income", "act now", "order now"]
RISKY = ["guaranteed income", "get rich quick", "100% guaranteed", "risk-free",
         "lose weight fast", "miracle"]

EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF←-⇿⬀-⯿]")
HASHTAG_RE = re.compile(r"(?<![\w&])#(\w+)", re.UNICODE)


def check(text, platform, fmt):
    results = []  # (level, msg)
    fmt = FORMAT_ALIASES.get(fmt, fmt)
    key = (platform, fmt)
    if key not in RULES:
        key = (platform, DEFAULT_FORMAT[platform])
        results.append(("WARN", f"No rule for {platform}/{fmt}; using {key[1]} rules"))
    mn, soft, hard, preview, max_tags = RULES[key]

    body = text.strip()
    n = len(body)
    lower = body.lower()
    first_line = body.splitlines()[0].strip() if body else ""

    # Length
    if hard and n > hard:
        results.append(("FAIL", f"{n} chars exceeds hard limit {hard}"))
    elif n > soft:
        results.append(("WARN", f"{n} chars is above the {mn}-{soft} sweet spot"))
    elif n < mn:
        results.append(("WARN", f"{n} chars is below the {mn}-{soft} sweet spot"))
    else:
        results.append(("OK", f"{n} chars (target {mn}-{soft})"))

    if preview:
        cut = body[:preview].replace("\n", " ⏎ ")
        results.append(("INFO", f"Visible before 'more' (~{preview}): \"{cut}\""))
        if len(first_line) > preview:
            results.append(("WARN", f"First line is {len(first_line)} chars; hook gets truncated"))

    # Hashtags (Discord headers start with '# ' so they won't match \w+ right after #)
    tags = HASHTAG_RE.findall(body)
    if platform == "discord":
        tags = [t for t in tags if not t.isdigit()]
    if len(tags) > max_tags:
        lvl = "FAIL" if platform == "instagram" and len(tags) > 5 else "WARN"
        results.append((lvl, f"{len(tags)} hashtags (max {max_tags} for {platform}/{key[1]})"))
    elif tags:
        results.append(("OK", f"{len(tags)} hashtags"))
    bad = sorted({t for t in tags if t.lower() in BANNED_TAGS})
    if bad:
        results.append(("FAIL", "Generic/banned hashtags: " + ", ".join("#" + b for b in bad)))
    if len({t.lower() for t in tags}) != len(tags):
        results.append(("WARN", "Duplicate hashtags"))

    # Bait / filler / hype / risky
    for pat in BAIT:
        if re.search(pat, lower) and not (platform == "discord" and "react" in pat):
            results.append(("FAIL", f"Engagement bait: /{pat}/"))
    for pat in FILLER_OPENERS:
        if re.search(pat, first_line.lower()):
            results.append(("WARN", f"Filler opener in hook: /{pat}/"))
    for w in AI_HYPE:
        if w in lower:
            results.append(("WARN", f"Generic hype phrase: '{w}'"))
    for w in RISKY:
        if w in lower:
            results.append(("FAIL", f"Risky claim: '{w}'"))
    if platform in ("facebook", "facebook-group"):
        hits = [w for w in FB_TRIGGERS if w in lower]
        if re.search(r"\bFREE\b", body):
            hits.append("FREE (caps)")
        if hits:
            results.append(("FAIL" if len(hits) >= 3 else "WARN",
                            "Facebook reach-trigger words: " + ", ".join(hits)))
        if re.search(r"https?://", body):
            results.append(("WARN", "Link in body — put it in the first comment"))

    if platform in ("instagram", "tiktok") and re.search(r"https?://", body):
        results.append(("WARN", "Raw URL won't be clickable — use 'link in bio'"))

    # Emoji in first char for reels
    if fmt == "reel" and first_line and EMOJI_RE.match(first_line):
        results.append(("WARN", "Caption starts with an emoji — lead with words"))

    # Wall of text
    for para in re.split(r"\n\s*\n", body):
        if len(para) > 400 and para.count("\n") < 2:
            results.append(("WARN", "Paragraph over 400 chars without line breaks"))
            break

    # Discord-specific
    if platform == "discord":
        if re.search(r"@everyone", body):
            results.append(("WARN", "@everyone used — confirm this is a major announcement"))
        first_ping = re.search(r"@(everyone|here)|<@&\d+>", body)
        if first_ping and first_ping.start() < len(body) * 0.5:
            results.append(("WARN", "Ping is in the first half — move it to the end"))
        if len(re.findall(r"(?m)^# ", body)) > 1:
            results.append(("WARN", "More than one H1 (# ) header"))
        date_words = re.search(r"\b(mon|tue|wed|thu|fri|sat|sun)\w*\b.*\b\d{1,2}(:\d\d)?\s?(am|pm)\b"
                               r"|\b\d{1,2}(:\d\d)?\s?(am|pm)\b", lower)
        if date_words and "<t:" not in body:
            results.append(("WARN", "Time mentioned without a Discord <t:UNIX:F> timestamp"))
        raw_urls = re.findall(r"(?<![(<])https?://\S+", body)
        if len(raw_urls) > 1:
            results.append(("WARN", f"{len(raw_urls)} raw URLs — mask with [text](url) or wrap in <>"))

    if "[placeholder]" in lower or re.search(r"\[[A-Z][A-Z _/]+\]", body):
        results.append(("INFO", "Contains [PLACEHOLDER] values to fill in"))
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--platform", required=True, choices=sorted(DEFAULT_FORMAT))
    ap.add_argument("--format", default=None, help="reel|feed|carousel|story|flyer|announcement|post|title")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--text")
    src.add_argument("--file")
    a = ap.parse_args()

    if a.text is not None:
        text = a.text
    elif a.file:
        with open(a.file, encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    fmt = a.format or DEFAULT_FORMAT[a.platform]
    results = check(text, a.platform, fmt)
    icons = {"OK": "✅", "INFO": "ℹ️ ", "WARN": "⚠️ ", "FAIL": "❌"}
    print(f"== {a.platform} / {fmt} ==")
    for lvl, msg in results:
        print(f"{icons[lvl]} {lvl}: {msg}")
    fails = sum(1 for l, _ in results if l == "FAIL")
    warns = sum(1 for l, _ in results if l == "WARN")
    print(f"-- {fails} fail, {warns} warn")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
