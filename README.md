# Climbing Coach

A Claude Code project that acts as a personal climbing coach. Ask it "what do I do today?" and it reads the log and the rules, adjusts, and tells you.

## Setup
1. Create a **private GitHub repo** (e.g. `climbing-coach`) and put these files in it.
2. Open it in Claude Code on the web (claude.ai/code) or the Claude app, so you can use it from phone or desktop.
3. Edit the start date in `coach-rules.md` if you're not starting Monday 2026-11-16.
4. Start a session: "Morning. Yesterday I climbed hard, tomorrow I'm resting. What's today?"

Claude updates `log.md` and commits it, so the history follows you across devices.

## Daily morning check-in (scheduled task)
Create a scheduled task on this repo/environment, daily at ~07:40 Israel time, with push notifications on, using this prompt:

> You are my climbing coach. Follow CLAUDE.md. Read log.md and coach-rules.md, work out today's date, program week and phase. Based on the log (assume the plan was followed for unreported days, but don't write invented entries), give me today's session in short form, the calorie target for today, and ask me one question about how yesterday went. Reply in Hebrew.

Then reply in that session (or a new one) to log what actually happened.

## Weekly review (optional scheduled task)
Sundays ~19:40:

> Follow CLAUDE.md. Review the last 7 days in log.md: sessions done vs planned, finger/elbow notes, sleep, weight trend (7-day average). Say whether to advance, hold or deload next week, and whether calories need adjusting per coach-rules.md. Update the State section of coach-rules.md if needed and commit. Keep it short.

## Files
- `CLAUDE.md` — how the coach behaves
- `athlete.md` — profile, equipment, goals
- `coach-rules.md` — program state, phase calendar, gates, daily decision rules
- `research/report.md` — the full research
- `log.md` — training log and benchmarks
