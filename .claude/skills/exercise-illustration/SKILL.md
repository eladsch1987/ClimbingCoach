---
name: exercise-illustration
description: Create or fix exercise illustrations and 2-frame animations for the climbing coach app (workout-timer.html, exercise-guide.html) with Dreamina / Seedream 5.5. Use whenever an exercise picture, pose, animation, rest image or any generated image for this project is created or corrected, or the user says a body position looks wrong.
---

# Exercise illustrations (Seedream 5.5 via dreamina-canvas)

Goal: a beginner must be able to copy the body position from the picture. **A wrong position is worse than no picture.** Accuracy beats beauty. Full research brief: `references/seedream-5.5-research-brief.md` (read §4 and §5 before writing new prompts).

## Non-negotiable workflow (per exercise)

1. **Get the truth from a real video first. Never prompt a pose from memory.**
   - Pick 1–3 YouTube tutorials filmed from the side. **Preferred source: FitnessFAQs (https://www.youtube.com/@FitnessFAQs) — the user trusts his technique; search his channel first** (e.g. `gh`-free: WebSearch with `allowed_domains: ["youtube.com"]` and "FitnessFAQs <exercise>"). Exercise libraries like OPEX are a good second choice for clean side views.
   - Ask Gemini to watch it (free tier only, `tools/gemini_ask.py`, OpenAI-compatible endpoint, model `gemini-3.5-flash-lite`; `gemini-3.8-flash` may be overloaded). Ask for: timestamps of each end position, body angle to the floor, joint angles, where hands/feet/elbows are, and the common mistakes the picture must NOT show. Save the answer to `images/ref-notes-<exercise>.md`.
   - Get real frames: `https://i.ytimg.com/vi/<id>/maxres1.jpg|maxres2|maxres3|hq1-3|maxresdefault.jpg` (auto frames at ~25/50/75%). This works from the cloud; video download (yt-dlp) and youtube.com pages are blocked by bot checks here. Contact-sheet them, look, and choose one frame per position.
2. **Import the chosen frames by URL**, not file: `dreamina-canvas resource upload --source-url <i.ytimg url> --project-id <canvas>` (local file upload fails with DNS errors here).
3. **Frame 1 (start position):** i2i with two references, each with ONE role, most important first:
   - `--ref node:<our character node>` → "Image 1: character, clothes, setting, flat vector style only"
   - `--ref res:<video frame>` → "Image 2: body position and camera angle only. Do not copy the photo's gym, logo, text or person."
   - Add the Gemini numbers in plain sentences (e.g. "body one straight line at ~45°, arms fully straight").
4. **Frame 2 (end position): EDIT frame 1, don't generate fresh.** Prompt template:
   `Edit {{node:<frame1>}}. Change only <single change>. Keep the man, clothes, background, camera position, framing, lighting, style and <anchored body parts, e.g. heels on the same spot> exactly unchanged.`
   One change per round. Say what moves AND what stays (e.g. ring row top: body lifts toward the rings, angle steeper, heels fixed).
5. **Generate 2 candidates per frame** (two nodes, not `--count 2`), then **verify**:
   - Look at both yourself (contact sheet).
   - Ask Gemini a strict YES/NO checklist on each (direction faced, is X in front/behind, both feet off ground, anatomy errors). Reject on any NO.
   - Never show the user an unverified frame. If 3 attempts fail on the same issue, change strategy (better reference frame, different camera angle), don't keep re-rolling.
6. **Build the animation** (`anim/<key>.webp`, 640×480): hold each frame ~1000 ms with a 6-step crossfade (70 ms) for strength/stretch moves; **no crossfade** (450 ms cuts) for fast moves like jump rope. Exactly 2 frames unless the user asks for more.
7. **Publish** the timer and guide with the changed `anim/*` files (same URLs), commit + push, and log node/submit/resource IDs in `images/dreamina-state.json`.

## dreamina-canvas specifics learned here

- Canvas: project `d4b8f86e-5963-4298-ade9-e6b8932bd97b` ("Climbing exercise illustrations"). Model `seedream_5.5`, `--ratio 4:3 --resolution 1.5K --count 1` (1.5K costs the same as 1K: 6 credits/image).
- Node IDs must be `node_` + 10 lowercase Crockford base32 chars (`0-9a-hjkmnp-tv-z`).
- Batches over ~50 credits need `node confirm --credit-ceiling <quote total>` and `--credit-token` on `node run`, otherwise nothing runs. Use one `--submit-id` per node; on an unclear result use `operation status/wait <submitId>` — never resubmit blindly.
- Failed generations are not charged. Moderation: rear views of the hips/shorts as an i2i input get rejected ("Input image failed content moderation") — use front/side views; don't try to evade filters.
- Download results immediately (`resource download <id> --output ...`).
- Always ask the user before spending; they approved generous Dreamina use but care about correctness.

## Prompt rules (from the brief)

- Natural sentences: [type + purpose] → subject/action → environment → light → camera → style → 1–2 inline exclusions ("No text or logos."). No keyword soup, no "8k", no negative_prompt/seed fields.
- Name references "Image 1 / Image 2" (or `{{node:}}`/`{{res:}}` placeholders) and give each exactly one role.
- Pure side view for anything where front/behind matters (rope, rows, levers). State which way he faces ("he faces RIGHT of the image") and put spatial words in caps when critical (BEHIND, IN FRONT).
- No text in images; Hebrew text never in-model.

## House style

One athletic man, late 30s, short dark hair, plain grey t-shirt, dark shorts; flat vector instructional style; off-white or simple outdoor-park background; full body visible. Rest screen: `anim/rest.jpg` (towel over shoulder, water bottle).

## Audio cues (separate)

Voice cues are ElevenLabs **API** (not the connector — too costly), voice Curtis `l7mlSJVCAXDwFX44amqm`, `eleven_multilingual_v2`, key is proxy-injected (`xi-api-key: proxy-injected`). Texts in `audio/cues.json`, files `audio/cues/<key>.mp3`. Voice plays only when the user taps "Hear how".
