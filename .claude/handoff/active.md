---
saved-at: 2026-11-20T21:10:36Z
saved-at-sha: 06d3fbf
saved-at-branch: claude/festive-johnson-53hwwe
saved-from-cwd: /home/user/ClimbingCoach
---

- **Pick up:** keep coaching Elad per `CLAUDE.md`. Week 1 (started Mon 2026-11-16). Next: **Sat 21 Park A** (full; pull-ups 5×4 ≈60% of max 7; monkey bars only if wrist <2), **Sun 22 rest + first weekly check**: 7-day average of morning weights (72.3 on 19 and 20 Nov) + waist at navel. Ask how Park A went; log it.
- **Read first:** `log.md`, `coach-rules.md` (State: ECU rules), `athlete.md` (ultrasound 16 Nov = mild ECU tenosynovitis; physio still to book: ask, and ask him to have it checked dynamically for subluxation/clicking).
- **Open questions:** creatine: label is 0.5 g/capsule; he said "7–8 g/day". Unanswered whether he meant capsules (→ 3.5–4 g, fine) or grams; target 5 g = 10 capsules. Protein: aiming 120 g this week (hit 128 g on 18 Nov), 140 g from week 2. Calories ~2,000 training / ~1,750 rest; Cal AI under-counts. Spotify ducking fix (cue audio split into <5 s parts) untested on his phone; if it fails, offer Spotify Web API (needs Premium + dev app).
- **Constraints:** wrist pain ≤2/10; no loaded pronation/supination; no right-hand underclings/slopers/wide pinches; no ball-grip hangs until physio clears. Phase 1: 1 climb/week, projects capped ≤V5, ≤5–6 attempts, no full crimp. He likes projecting; the once-a-week "mixed" climb format is approved.
- **App:** https://climbing-coach-eladsch.vercel.app/ — after timer/guide edits: `python3 tools/build_site.py`, commit, push branch + `main`, redeploy Vercel project `climbing-coach` (team `eladsch`) with the git SHA. Timer now has a "Time" picker (fitSession/TRIM_STEPS in `workout-timer.html`).
- **Images:** follow `.claude/skills/exercise-illustration/` (+ `tools/dream.py` driver). Skipped on purpose: reverse wrist curls, finger bands, pronation/supination, Y-T-W "W" frame — don't retry unless he asks.
- **Offered, never set up:** daily 07:40 check-in scheduled task.
