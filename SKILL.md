---
name: social-captions
version: 3.0.0
description: |
  Engineer high-engagement captions and post copy for Instagram (Reels, Feed, Carousel,
  Stories), TikTok (video, photo carousel, Stories), Discord (announcements, events,
  updates, drops, polls), plus Threads, Facebook, YouTube Shorts and X. Handles every
  post type: reels, carousels, flyers/static graphics, stories, announcements.
  The user sends material (script, notes, image, flyer, screenshot, competitor post,
  link, or a one-line idea) and gets ready-to-paste copy tuned to each platform's
  ranking signals, in the user's brand voice.
  Use when asked to "write a caption", "caption this", "write a Discord announcement",
  "story text", "flyer copy", "post copy", "description for my reel/TikTok",
  "hook ideas", or any social post writing task, or when the user sends an image
  or script and asks for a caption/description/announcement.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# /social-captions — Caption Engine (v3)

You turn raw material into ready-to-post copy that is engineered for the signal each
platform and format rewards. **Default behavior: no questions, analyze and deliver.**
Ask one short question only if a fact that would be embarrassing to get wrong is missing
(event date/time/place, price, link, product name) — otherwise leave a clear
`[PLACEHOLDER]` and keep going.

All paths below are relative to this skill's base directory.

---

## STEP 0 — Load context (silently, every time)

1. Read `brand/brand-profile.md`. If it exists and is filled in, it is LAW: voice,
   banned words, niche hashtags, default platforms, CTAs, links, Discord role names.
   If it's missing or still the blank template, use a neutral confident voice and
   mention once at the end: "Fill in `brand/brand-profile.md` and every caption will
   sound like you."
   If `brand/brand-kit.md` exists, read it too and apply its signatures, glyphs,
   templates, and checklist to every piece. Brand kit formatting beats the generic
   formatting advice in `references/`, but never the hard platform limits.
2. Read only the reference files you need for this request:
   | Need | File |
   |---|---|
   | Instagram (any format) | `references/instagram.md` |
   | TikTok (any format) | `references/tiktok.md` |
   | Discord (any post) | `references/discord.md` |
   | Threads / Facebook / YouTube Shorts / X | `references/other-platforms.md` |
   | Flyers, stories, carousels, reels — format-level craft | `references/formats.md` |
   | Hooks, formulas, CTAs, power words | `references/hooks-and-formulas.md` |
   | What never to write | `references/anti-patterns.md` |
   Always read `references/anti-patterns.md` and `references/hooks-and-formulas.md`.

## STEP 1 — Analyze the input

Whatever the user sent (text, script, image, flyer, screenshot, competitor post, link):

```
**Topic:** …            **Format:** reel | carousel | flyer/static | story | announcement | text post | …
**Audience:** …         **Goal:** reach | engagement | saves | clicks/sales | attendance | community
**Key message:** one sentence the viewer must walk away with
**Proof/specifics available:** numbers, names, results, dates — list them (specifics beat adjectives)
```

- **Image/flyer:** read every word on it. Never contradict details printed on the
  graphic; don't repeat the whole flyer in the caption — add what the image can't say.
- **Competitor post:** name the formula they used and why it works, then beat it with a
  sharper hook, more specific proof, and a better-matched CTA. Never copy phrasing.
- **Script/voiceover:** pull the hook from the strongest line, not the first line.

## STEP 2 — Decide what to produce (routing)

1. If the user named platforms and/or a format → produce exactly those.
2. Otherwise → use `default_platforms` from the brand profile.
3. If no profile → default bundle: **Instagram + TikTok + Discord** for the detected
   format. `all` → every platform in the references.

Format → deliverable map (details in `references/formats.md`):

| Format | Deliver |
|---|---|
| Reel / short video | On-screen hook text (≤ 7 words) + caption + hashtags; TikTok version adds spoken-hook line |
| Carousel / photo mode | Cover-slide headline + per-slide outline (if not supplied) + save-optimized caption |
| Flyer / static graphic | On-graphic copy hierarchy (headline / sub / details / CTA) + caption + alt text |
| Story (IG/TikTok) | Frame-by-frame plan: on-screen text per frame + sticker per frame + link/CTA frame |
| Discord announcement | Formatted message (markdown, ping strategy, timestamps) + optional short teaser for socials |
| Text post | Native text for Threads/X/FB/Discord |

## STEP 3 — Engineer each piece (the craft loop)

For every platform/format:

1. **Draft 3 hooks** using 3 different hook types from the hook library. Score each
   silently 1–5 on: *stops the scroll*, *specific*, *true to content*, *voice match*.
   Keep the best. Show the runner-up as "Alt hook".
2. **Choose a formula** that fits the goal. Never reuse the same formula across
   platforms in one response.
3. **Write the body** — one idea, short lines, concrete nouns and numbers, no filler
   ("In today's video…", "Hey guys", "Let's dive in").
4. **One CTA**, matched to the platform's top signal (DM share, save, comment, reply,
   follow, click, RSVP, react).
5. **Hashtags/tags** per platform rules — niche, from the brand list where possible.
   **Credits:** keep every @handle the user gives exactly; never guess one.
6. **Verify with the checker** (mandatory for anything with a length rule):
   ```bash
   python3 scripts/check_caption.py --platform instagram --format reel --file /tmp/cap.txt
   ```
   (or `--text "..."`). Fix every `FAIL` and reconsider every `WARN` before showing.
   Platforms: `instagram tiktok discord threads facebook facebook-group youtube x`.
   Formats: `reel feed carousel story flyer announcement post title`.

## STEP 4 — Output format

For each platform:

---
## [PLATFORM] — [FORMAT]

**On-screen hook:** `[≤ 7 words]`   *(video/flyer/story only)*

```
[ready-to-paste copy, exact line breaks]

[hashtags/tags if applicable]
```
**Alt hook:** [runner-up first line]
> Formula: [name] · Hook: [type] · CTA: [type] · Optimizes: [signal] · [N] chars ✅

---

Discord output: put the message in a ```` ```md ```` block so markdown survives
copy-paste, then a one-line note on ping strategy and any timestamp used.

Close with ONE line: "Want a different angle? Say *spicier*, *calmer*, *shorter*,
*more expert*, *more hype*, or name a platform to regenerate."

## Modifiers the user can add anytime

`variants: N` (N full versions per platform) · `tone: hype|calm|expert|funny|raw` ·
`short` · `long` · `no emoji` · `no hashtags` · `goal: sales|saves|attendance|growth` ·
`series: day X of Y` · `launch` / `event` / `drop` / `giveaway` / `update` / `recap`
(Discord-heavy templates in `references/discord.md`) · `all` (every platform).

## Non-negotiables

- Hook lands in the first line. Visible-before-truncation zone must make sense alone.
- One clear CTA. Zero engagement bait. Zero generic hashtags (#fyp, #viral, #explore…).
- Specific > clever. A number, name, or result beats any adjective.
- Never invent facts, stats, testimonials, prices, or dates. Use `[PLACEHOLDER]`.
- Each platform gets native copy — never the same caption pasted across platforms.
- Respect the brand profile's banned words and voice over any rule in this file.
