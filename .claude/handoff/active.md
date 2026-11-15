---
saved-at: 2026-11-15T08:59:32Z
saved-at-sha: 2072d1f
saved-at-branch: claude/festive-johnson-53hwwe
saved-from-cwd: /home/user/ClimbingCoach
---

- **Pick up:** keep coaching Elad per `CLAUDE.md`. Week 1 starts Mon 2026-11-16. Today (Sun 15) is a rest day; he did his first Abrahangs this morning. Open item: he says he hasn't lost weight after ~4 days. Answer his pending reply (average Cal AI intake? started creatine?), get **daily morning weigh-ins** (after toilet, before food) into `log.md`, and judge on the 7-day average at the week-2 check (Sun 22), per `coach-rules.md`. Only the 73 kg after-breakfast reading exists; it's not a baseline.
- **Week 1 plan given to him:** Mon 20 mm BW hang test (cap 15 s, after warm-up) + Park B · Tue Abrahangs + shoulders + hips · Wed Abrahangs or climb · Thu climb (bouldering + optional auto-belay ropes, volume V2–V3, few V4) · Fri recovery · Sat Park A · Sun rest. Confirm his climb day (Wed or Thu). Log the hang test in Benchmarks.
- **Read first:** `CLAUDE.md`, `log.md`, `coach-rules.md` (State), `athlete.md` (right-wrist ECU injury; ultrasound + physio planned this week — ask for results).
- **App:** give him **https://climbing-coach-eladsch.vercel.app/** (sound works there, not in the claude.ai artifact on his Android). After timer/guide edits: `python3 tools/build_site.py`, commit, push, redeploy Vercel project `climbing-coach` (team `eladsch`) via `mcp__Vercel__create_deployment` with the git SHA. Deployment protection stays ON (he's fine with it).
- **Images:** follow `.claude/skills/exercise-illustration/` (real YouTube frames from `i.ytimg.com` as pose refs, FitnessFAQs preferred, Gemini free-tier check, edit frame 1 → frame 2). Do NOT redo existing animations unless he asks. Grip pictures are hand-drawn SVG diagrams on purpose (Seedream drew hands wrong); he asked "why not Seedream?" — offered a diagram-as-reference Seedream retry (~50 credits), awaiting his answer.
- **Keys:** ElevenLabs and Gemini keys are proxy-injected (`xi-api-key: proxy-injected`, `Authorization: Bearer proxy-injected` on Gemini's OpenAI-compatible endpoint). Use the ElevenLabs API, never the connector (too costly). Gemini: free tier only. Dreamina needs `dreamina-canvas` installed + login in each new container.
- **Branches:** work was merged into `main` on 2026-11-15 at his request; keep `main` up to date (he OK'd pushing there). Vercel production should deploy from `main`.
- **Open questions:** Daily 07:40 check-in scheduled task — offered, never set up.
