# Caption Studio

This repo is a Claude Code skill (`SKILL.md`) for writing social media copy.

When the user is working inside this repo and asks for a caption, post, story text, flyer
copy, Discord announcement, or hooks — follow `SKILL.md` exactly, even if they don't type
`/social-captions`. Read `brand/brand-profile.md` first.

When the user asks to change the rules (new platform, new banned word, new format):
- Platform rules → `references/<platform>.md`
- Format craft → `references/formats.md`
- Voice/hashtags/links → `brand/brand-profile.md`
- Lint rules → `scripts/check_caption.py` (keep stdlib-only; test with a passing and failing sample)
