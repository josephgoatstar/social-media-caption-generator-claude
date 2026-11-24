# Social Caption Engine — Claude Code Skill

Turn any script, flyer, screenshot, competitor post, or one-line idea into ready-to-post
copy for **Instagram, TikTok, and Discord** (plus Threads, Facebook, YouTube Shorts, X),
built for **every format**: reels, carousels, flyers, stories, and Discord announcements.
The skill writes in your brand voice and checks each caption with a linter.

> Forked from [rediumvex/social-media-caption-generator-claude](https://github.com/rediumvex/social-media-caption-generator-claude)
> (MIT, © Roman Knox) and extended: Discord, Stories, flyers, brand profile, hook scoring,
> and an automated caption checker.

---

## What's new vs. upstream

| | Upstream v2 | This fork v3 |
|---|---|---|
| Platforms | IG, TikTok, Threads, FB, YT Shorts | + **Discord**, **X** |
| Formats | Reels, carousels (one caption each) | + **flyers** (on-graphic copy + alt text), **stories** (frame-by-frame + stickers), **Discord announcements** (markdown, timestamps, ping strategy) |
| Voice | Generic | Reads your **`brand/brand-profile.md`** every time |
| Output | Always all 7 platforms | Only what you ask for, or your default platforms |
| Quality control | Checklist | 3 hooks drafted & scored per piece + **`scripts/check_caption.py`** lint (length, truncation, hashtags, bait, FB triggers, Discord pings/timestamps) |
| Structure | One 300-line file | Lean `SKILL.md` + per-platform `references/` loaded on demand |

---

## Install

**Option A: global skill (works in any project)**
```bash
mkdir -p ~/.claude/skills
git clone https://github.com/josephgoatstar/social-media-caption-generator-claude.git ~/.claude/skills/social-captions
```
Restart Claude Code, then use `/social-captions`.

**Option B: caption workspace**
```bash
git clone https://github.com/josephgoatstar/social-media-caption-generator-claude.git
cd social-media-caption-generator-claude && claude
```
`CLAUDE.md` tells Claude to follow the skill for any caption request in this folder.

**Then do this once:** fill in `brand/brand-profile.md` with your voice, hashtags, links,
default platforms, and Discord roles. This file has the biggest effect on quality.

---

## Usage

```
/social-captions reel script: [paste]
/social-captions [attach flyer image] instagram + discord
/social-captions story sequence for our Friday drop
/social-captions discord event: game night Sat 8pm ET in #voice, prize is Nitro
/social-captions carousel: 5 mistakes beginners make with [topic]
/social-captions competitor post doing numbers: [paste] — beat it
/social-captions launch kit all: winter collection drops Dec 12
```

Modifiers: `variants: 3` · `tone: hype|calm|expert|funny|raw` · `short` · `no emoji` ·
`goal: saves|sales|attendance` · `event` / `drop` / `update` / `giveaway` / `recap` · `all`

Each piece comes back with: ready-to-paste copy, on-screen hook (video/flyer/story),
an alternate hook, and formula · hook type · CTA · signal · checked character count.

### Lint a caption yourself
```bash
python3 scripts/check_caption.py --platform instagram --format carousel --text "..."
python3 scripts/check_caption.py --platform discord --file announcement.md
```

---

## Layout
```
SKILL.md                      # workflow, routing, output format
brand/brand-profile.md        # YOUR voice, hashtags, links, Discord roles (fill in)
references/
  instagram.md  tiktok.md  discord.md  other-platforms.md
  formats.md                  # reels, carousels, flyers, stories, launch kits
  hooks-and-formulas.md       # hook types, formulas, CTA menu, power words
  anti-patterns.md            # what never to write
scripts/check_caption.py      # caption linter (stdlib Python)
examples/example-output.md    # full worked example (flyer → IG, TikTok, Discord, Story)
```

## License
MIT. See `LICENSE`. Original work © 2026 Roman Knox.
