# Discord

Discord isn't algorithmic — engagement comes from **members actually reading, reacting,
and showing up.** The enemies are ping fatigue, walls of text, and buried details.
Optimize for: *scannable in 5 seconds · the one action is obvious · details are exact.*

Hard limits: message 2,000 chars (4,000 with Nitro — don't rely on it) · embed title 256 ·
embed description 4,096 · embed field value 1,024 · embed total 6,000 · forum post title 100.

---

## Formatting toolkit (Discord markdown)
| Syntax | Use |
|---|---|
| `# Title` / `## Sub` / `### Small` | Headers — must start the line. One `#` per post max. |
| `-# small text` | Subtext for fine print, credits, "react below" hints |
| `**bold**` `*italic*` `__underline__` `~~strike~~` | Emphasis — bold the details people scan for |
| `- item` / `1. item` | Lists (indent with 2 spaces for sub-bullets) |
| `> quote` / `>>> block quote` | Callouts, quoting feedback/testimonials |
| `[text](https://url)` | Masked links — cleaner than raw URLs |
| `<https://url>` | Suppress the link preview embed |
| `\|\|spoiler\|\|` | Spoilers, surprise reveals |
| `` `code` `` | Commands, codes, promo codes |
| `<t:UNIX:F>` / `<t:UNIX:R>` | **Timestamps** — auto-convert to each reader's time zone |
| `<#channel_id>` / `<@&role_id>` | Channel links / role mentions (use names from brand profile; leave `@RoleName` if no ID) |
| `:emoji_name:` | Custom server emoji (from brand profile) |

**Timestamps:** always use them for events/deadlines. Compute with Bash:
```bash
TZ="America/New_York" date -d "2026-12-05 20:00" +%s   # → use as <t:SECONDS:F> and <t:SECONDS:R>
```
Formats: `F` = "Saturday, December 5, 2026 8:00 PM", `f` = short date+time, `R` = "in 3 days",
`t` = time only, `D` = date only. Pair `F` + `R`: `<t:X:F> (<t:X:R>)`.

## Ping strategy (state it in the output)
- **@everyone** — only for big moments (launch, major event, server-wide change). Overuse = muted server.
- **@here** — time-sensitive, for online members only (going live now, drop is live).
- **Role pings** (@Events, @Drops, @Updates) — the default. Opt-in = no resentment.
- **No ping** — routine updates, recaps, reminders posted alongside a scheduled event.
- Put the ping at the **end** of the message or on its own last line so the preview
  notification shows the headline, not "@everyone".

## Announcement anatomy
```
# [emoji] [Headline — what's happening, ≤ 8 words]
[1–2 line hook: why it matters / what's in it for them]

**📅 When:** <t:X:F> (<t:X:R>)
**📍 Where:** [channel / venue / link]
**🎟️ Cost / How:** [details]

[optional: 2–4 bullets of what to expect]

**→ [ONE action]:** [react ✅ / RSVP in #events / link]
-# [fine print]
@Role
```
Rules: headline first, details bolded and stacked, ONE call to action, ≤ ~1,200 chars
for most posts. If it needs more, split into a post + thread or use a forum post.

## Templates by type (modifier keyword → template)
- **event** — anatomy above + "Click *Interested* on the Server Event" if one exists, react to RSVP.
- **drop / launch** — `# 🚨 [Product] is live` · 1 line hook · price/qty · link · `@Drops` · `-# limited qty / while supplies last` only if true.
- **update / patch notes** — `## What's new` (✨) · `## Fixes` (🔧) · `## Coming next` (👀). Bullets, ≤ 10 words each.
- **giveaway** — prize · how to enter (one method) · end time `<t:X:R>` · winner announcement method · rules link. (Discord has no reach penalty for the word "giveaway", unlike Facebook.)
- **poll** — recommend Discord's native poll (up to 10 answers); give the question + answers. Or reactions: `🅰️ / 🅱️` list.
- **reminder** — 2–3 lines max, timestamp `R`, link to original announcement. `@here` or role, never `@everyone`.
- **welcome** — server purpose in 1 line, 3 channel links to start with, 1 icebreaker prompt.
- **recap** — headline + 3 highlight bullets + thank-you + what's next with a timestamp.
- **teaser** — `||spoiler||` reveal, a date with `R` timestamp, no details. Builds anticipation.

## Cross-posting from Instagram/TikTok
When announcing a new post in Discord: don't paste the IG caption. Write a 1–2 line
"why you should watch" + link, ask for a specific reaction or comment, and put the link
on its own line so the embed preview renders.

## Tone
Community voice: "we", "y'all", inside references from the brand profile are welcome here
(unlike public platforms). Emoji as section markers, not decoration.
