# Seedream 5.5 and Image-Model Best Practices: Research Brief for a Claude Code SKILL.md (November 2026)

Seedream 5.5 is ByteDance Seed's current image generation and editing model, released November 9, 2026.\[1\] Use it by default for cheap, realistic stills and for long chains of revisions on one image, through fal.ai (`bytedance/seedream/v5.5/text-to-image`, `/edit`, `/layerize`) at $0.03–$0.0405 per image.\[2\] Switch to GPT Image 2.6 only when exact long text or top-of-leaderboard quality is worth roughly 5–10× the price. "SC Dream 5.5" is almost certainly Seedream 5.5; no product by that other name exists.

## TL;DR

- **What it is and how to call it:** Seedream 5.5 has three headline upgrades over Seedream 5.0 Pro: stable multi-round editing, native RGBA (transparent) output, and more realistic light, skin and small text.\[3\] On fal there are three endpoints at $0.03 per image (1K/1.5K) or $0.0405 (2K). On Volcengine Ark the model ID is `doubao-seedream-5-5-261028` at ¥0.13–0.23 per output plus ¥0.05 per input image.\[4\] The BytePlus ID `dola-seedream-5-5-261028` is early-access and unconfirmed. Output tops out at about 2K (4,624,220 pixels); there is no seed, no negative-prompt field, no streaming and no sequential/group generation.
- **How to prompt it:** write coherent natural-language sentences (subject → action → environment → style/light/camera), state the intended use, and put any on-image text in "double quotes".\[1\] Refer to inputs as Image 1/Image 2 and give each one role. For edits, name one change per round and list what must stay unchanged. Write exclusions inline ("no text or logos") and keep them to one or two. Hebrew is not on ByteDance's list of supported languages, so treat Hebrew text as untested and plan to overlay it in post.\[5\]
- **How the agent should work:** plan → write a prompt file → generate one draft at 1K → inspect the image visually → edit rather than re-roll → upscale or finalize at 2K → log every prompt, parameter and URL. Download outputs immediately, because hosted URLs expire (ModelArk documents 24 hours).\[1\] For video, design the keyframe at the delivery aspect ratio, then prompt the image-to-video model with motion only.\[6\]

## Key Findings

1. **Version and release status.** ByteDance Seed released Seedream 5.5 on November 9, 2026, with a gradual rollout on Jimeng (Dreamina's Chinese counterpart), Doubao, Doubao Work and Volcano (Volcengine) Ark.\[7\] ByteDance's Seed blog says "A Pro version of the Seedream 5.5 series will follow. Stay tuned." without giving a date. fal lists all three 5.5 endpoints as "new", and third-party APIs (Atlas Cloud, WaveSpeed, Kie, Flaq, Higgsfield) already serve it.\[8\]\[9\]
2. **What actually changed versus 5.0 Pro, per ByteDance:**
   - The Seed blog says the model will "Preserve unedited regions at the pixel level and eliminate color shifts in those areas... This supports continued work on the same image across 100 rounds of editing," with a demo that made 100 successive edits on an image of the same person.
   - Native transparent and semi-transparent RGBA output.\[2\]\[10\]
   - More natural lighting and skin, with less excessive gloss and overexposure.\[11\]
   - Per the Seed blog, "Seedream 5.5's severe text corruption rate fell to 0.4%, while its minor text corruption rate fell to 1.7%" across Chinese and English, including dense small text.
   - The Seed blog says 5.5 "received positive GSB scores against the previous version in all four comparisons, reaching +55.62% for realism in image-to-image tasks," and names GPT Image 2.5 Sunburst and Nano Banana 2.1 as the rival models it compared against.
   - Testing six use cases on its MagicArena platform, ByteDance reports: "In film and television and in office productivity, usability rates were more than twice those of the previous version."
   - BigGo Finance, citing Volcano Engine figures, reports that 5.5 "generates images nearly 40% faster than the previous-generation Seedream 5.0 Pro"; Apiyi.com attributes this figure to media reports and says it could not find it in the official announcement.

   These are all vendor claims. The Seed blog says 100 rounds, but BytePlus's Lumina page and Atlas Cloud say "80-plus" rounds, and nobody has published a drift metric.\[12\]
3. **Independent rankings place it as a value leader, not the quality leader.**
   - On Artificial Analysis's text-to-image arena, Seedream 5.5 is #10 at Elo 1134 for $20 per 1,000 images. GPT Image 2.6 Sunburst (max) is #1 at 1261 for $210.72 per 1,000, and Nano Banana 2.1 is #6 at 1176 for $33.60 per 1,000.\[13\]
   - On the editing arena, Seedream 5.5 rises to #6 at Elo 1159 for $28 per 1,000, ahead of Nano Banana 2.1 at 1152.\[14\]
4. **Hard API limits an agent must respect:**
   - Output is 921,600–4,624,220 total pixels, with aspect ratio between 1:16 and 16:1.\[3\]\[15\]\[16\]
   - Up to 10 reference images. Each must be ≤30 MB with sides >14 px.\[3\]
   - Recommended prompt length is within 300 Chinese characters or 600 English words.\[3\]
   - A JPEG output can never be transparent.\[3\]\[17\]
   - The output does not automatically follow the aspect ratio of the input image, so set the size explicitly.\[3\]
5. **Early "4K / 8.29 MP" claims for 5.5 are outdated.** A ByteDance engineer's ComfyUI pull request implementing the 5.5 API says the "superseded 8,294,400-pixel maximum is not used" after a November 7 size correction.\[17\] Plan for a 2K ceiling and upscale separately when you need 4K.

## Details

### 1. Seedream lineage (what an agent needs to know about versions)

| Version | Release | Official model ID(s) | Notable traits |
|---|---|---|---|
| Seedream 3.0 | 2025 | `seedream-3-0-t2i` | Text-to-image only. The only Seedream model that officially honors `seed`. |
| Seedream 4.0 | 2025 | `seedream-4-0-250828` | Unified generation and editing; batch/sequential output; $0.03 per image on ModelArk. |
| Seedream 4.5 | Dec 3, 2025 | `seedream-4-5-251128` | Up to 14 references (inputs plus outputs ≤15); up to 4K; aspect ratios 1:16–16:1. |
| Seedream 5.0 Lite | Feb 24, 2026 | `seedream-5-0-260128` / `seedream-5-0-lite-260128` | Reasoning and web search; batch and streaming; up to 3K on fal. |
| Seedream 5.0 Pro | Jul 8, 2026 | `dola-seedream-5-0-pro-260628` (BytePlus), `doubao-seedream-5-0-pro-260628` (Volcengine) | Box/point/sketch interactive editing; layer split (16 layers); text in about 10–14 languages including right-to-left Arabic; no batch or streaming.\[18\]\[19\] |
| Seedream 5.0 Flash | Sep 2026 | `dola-seedream-5-0-flash-260915` | Fast, cheap 5.0 tier (≈$0.018 per request via a reseller). |
| **Seedream 5.5** | **Nov 9, 2026** | **`doubao-seedream-5-5-261028` (Volcengine); `dola-seedream-5-5-261028` (BytePlus, early access)** | Pixel-stable multi-round edits; native RGBA; layer decomposition up to 99 layers plus base with OCR; 1K/1.5K/2K.\[20\]\[21\] |

Model IDs are dated suffixes (YYMMDD). Never guess them: query the provider's models list or console. One open-source integration was broken by sending `seedream-5-0-pro-260628` without the `dola-` prefix that BytePlus requires.\[22\]

### 2. Seedream 5.5 capabilities and limitations

**Capabilities:**
- Text-to-image.
- Single- and multi-reference editing, with 1–10 images.\[3\]
- Region targeting via coordinates, boxes, arrows or marks drawn on the input image.\[3\]
- Native transparent backgrounds (`background: transparent` with PNG). Transparency works even when the inputs have no alpha channel.\[3\]\[23\]
- Layer decomposition into an opaque base plus up to 99 transparent PNG layers, with optional rich-text OCR.\[3\]\[8\]\[24\]
- Multi-round editing: feed each result back in as the next input.\[3\]

**Not available on 5.5, according to the API contract described in the ByteDance PR:**
- Streaming.\[17\]
- "Related-image group generation" (Seedream's `sequential_image_generation`).\[17\]
- Web search.\[17\]
- The `fast` prompt-optimization mode (standard only).\[17\]
- A documented `seed` or "thinking" parameter.\[17\]

For a set of storyboard frames, call the model once per frame. Do not rely on a batch "group" mode.

**Known failure modes and caveats:**
- **Text:** the error rate is low but not zero. In Atlas Cloud's blind 5-round test against GPT Image 2.6, Seedream 5.5 won 4:3 overall and had "the best edit stability in the test, with one misspelled label in 20 edits". On the long label inside a five-step edit chain, GPT Image 2.6 scored 4/4 and Seedream 3/4.\[21\] Always verify text character by character.
- **Transparency:** one tester found that `output_format: "png"` alone returned a 24-bit RGB image with a white background; only `background: "transparent"` produced a 32-bit ARGB image.\[25\] Translucent subjects (glass, liquids, ribbons) are where alpha edges fail. Check them on both dark and light backgrounds.\[2\]
- **Reference fidelity:** BytePlus's own guide warns that reference images "do not guarantee pixel-level identity or exact preservation", so check brand, product and text details in every output.\[1\]
- **Long prompts:** ByteDance's field reference says overly long prompts scatter the information, so the model ignores details and elements go missing.\[26\]
- **Moderation:** hosts run strict prompt and input-image filters (e.g. Mage checks the prompt and first image before generation).\[27\]\[28\] Volcengine does not charge for unsuccessful outputs.\[4\]
- **Independent verification:** at launch, ByteDance's materials published no failure-mode section and no maximum resolution, and the 100-round claim was untested by third parties.\[25\]

### 3. Access routes, pricing and parameters

| Route | Identifier | Price (Nov 2026) | Notes |
|---|---|---|---|
| fal.ai | `bytedance/seedream/v5.5/text-to-image`, `/edit`, `/layerize` | $0.03 per output at 1K/1.5K (custom ≤2,610,000 px); $0.0405 at 2K; edit adds ~$0.012 per input image per output | Queue/async via `fal.subscribe`; "Commercial use"; edit takes up to 10 references. |
| Volcengine Ark (China) | `doubao-seedream-5-5-261028` | ¥0.05 per input image; ¥0.13 per output ≤2.61 MP; ¥0.23 per output 2.61–4.63 MP; text not billed\[29\] | A 2K square edit with one reference ≈ ¥0.28, under half the cost of 5.0 Pro (¥0.60).\[30\] |
| BytePlus ModelArk (international) | `dola-seedream-5-5-261028` (early access) | "Starting at $0.02/image"; first-purchase bundles of 700 / 1,800 / 3,500 images\[31\] | Endpoint `POST https://ark.ap-southeast.bytepluses.com/api/v3/images/generations` (an EU mirror exists); requires activating the model. |
| Atlas Cloud | `bytedance/seedream-v5.5/edit` | $0.016 per image\[3\] | Async submit + poll; offers an MCP server and Claude Code skills.\[3\] |
| WaveSpeed / Kie / Flaq / MuAPI | e.g. `bytedance/seedream-v5.5`, `seedream/5-5-text-to-image` | WaveSpeed from $0.02 generation / $0.028 edit\[2\] | Parameter names differ by host. |
| Consumer apps | Jimeng/Dreamina, Doubao, Higgsfield, Mage | Credits/subscription | Not for automated pipelines. |

**Conflict to flag:** as of November 11, some reviewers found no dated 5.5 ID in BytePlus's public ModelArk docs, while the BytePlus console banner reads "Dola-Seedream-5.5 Is Now Available".\[32\] Treat the BytePlus ID as provisional and confirm it in your console.

**Parameter reference (normalized across official and host schemas):**

| Concept | ModelArk/Volcengine native | fal | Atlas Cloud | Notes/gotchas |
|---|---|---|---|---|
| Prompt | `prompt` | `prompt` | `prompt` | ≤300 Chinese characters / 600 English words recommended. |
| Size | `size`: `1K`/`1.5K`/`2K` or `WxH` (default 2K) | `image_size` preset (`auto_1K`, `auto_1.5K`, `auto_2K`, `landscape_16_9`, etc.) or `{width,height}` | `size` e.g. `"2816*1584"` | 921,600–4,624,220 px; 1:16–16:1. Set the size explicitly; it does not inherit from the input. |
| Reference images | `image` (URL or Base64; string or array) | `image_urls` (≤10) | `reference_images` (1–10) | JPEG/PNG/WEBP/BMP/TIFF/GIF/HEIC/HEIF; ≤30 MB; >14 px per side; ≤36 MP total across references. |
| Format | `output_format` png (default)/jpeg | `output_format` | png default | JPEG plus transparent is rejected. |
| Transparency | `background` auto/transparent/opaque | Supported ("transparent PNG backgrounds") | `background` | The actual result is returned per image. |
| Count | One image per call (no group generation) | `num_images` ("batch generation") | One per call | Treat `num_images` as N independent calls, billed N times. |
| Seed | Not documented for 5.5 | Absent from 5.5 sample output | Not exposed | Reproducibility comes from logging prompt + inputs + model ID, not from a seed. |
| Watermark | `watermark` (default true on 5.0 Pro ModelArk) | `watermark` | — | Always set `watermark: false` explicitly when allowed. |
| Safety | Platform content filter; optional `safety_identifier` (≤64 printable ASCII; use a hash) | `enable_safety_checker` (default true; disabling requires account authorization) | — | A block is not a bug; rephrase and retry once. |
| Response | `response_format` url / b64_json | `images[].url`, `content_type`, `file_name`, `file_size` | `prediction_id` → poll | URLs are temporary; download immediately. |
| Layers | `layer_decomposition_options.max_images` 2–100 (default 30); `text_recognition` (default false)\[4\] | `/layerize` | `/layer-decomposition` | Bills each layer as an output; one input image only.\[4\] |

**Note on the fal schema:** the exact v5.5 fal parameter list was not retrievable (the page renders in JavaScript). fal's 5.0 Pro schema is the closest proxy: `image_size` default `auto_2K`, `output_format` default `"jpeg"`, `enable_safety_checker` default true, `enhance_prompt_mode` standard/fast, `sync_mode`, `watermark`, and no `seed` or `max_images`.\[15\] Before first use, the agent should fetch `https://fal.ai/api/openapi/queue/openapi.json?endpoint_id=bytedance/seedream/v5.5/text-to-image` (and the matching `/edit` URL) and validate against it.

**Request examples:**

```js
// fal (JS) — draft at 1K-tier, 16:9
import { fal } from "@fal-ai/client";
const r = await fal.subscribe("bytedance/seedream/v5.5/text-to-image", {
  input: {
    prompt: "Documentary still for a 16:9 film opening: an elderly fisherman mending a red net on a wooden pier at dawn. Low side light from the left, cool mist over the water, muted teal-and-amber palette, 35mm lens at eye level, natural skin texture, subtle film grain. No text or logos.",
    image_size: { width: 1424, height: 800 },   // ~1.1 MP, $0.03 tier
    output_format: "png"
  }
});
// r.data.images[0].url -> download now, save alongside a JSON sidecar
```

```bash
# fal edit — one change per round, preservation list
curl -X POST https://queue.fal.run/bytedance/seedream/v5.5/edit \
 -H "Authorization: Key $FAL_KEY" -H "Content-Type: application/json" \
 -d '{"prompt":"In Image 1, change only the sky to heavy overcast. Keep the fisherman, net, pier, camera angle, framing and colour grade exactly unchanged.",
      "image_urls":["https://.../shot03_v002.png"],
      "image_size":{"width":2816,"height":1584},"output_format":"png"}'
```

```bash
# ModelArk native (BytePlus) — verify model ID in console first
curl https://ark.ap-southeast.bytepluses.com/api/v3/images/generations \
 -H "Authorization: Bearer $ARK_API_KEY" -H "Content-Type: application/json" \
 -d '{"model":"dola-seedream-5-5-261028","prompt":"...","size":"2K",
      "output_format":"png","background":"transparent","watermark":false,
      "response_format":"url"}'
```

### 4. Prompting Seedream 5.5

**Official guidance (BytePlus/ByteDance):**
- Use coherent natural language rather than loose keywords.\[1\] ByteDance's Seedream 3.0 guide says to use "natural language to describe the picture content (subject + action + environment, etc.)" and "short phrases to describe the picture aesthetics (style, color, light and shadow, composition, etc.)".\[33\]
- Name the image's usage and type, e.g. "PPT cover background" or "documentary photography".\[33\]
- BytePlus's template: *Create [image type] for [purpose]. Show [subject and action] in [environment]. Use [style, color, lighting, and composition]. Preserve [fixed elements] and change [target elements].*\[1\]
- Put text that must appear in the image inside double quotes.\[1\]\[34\]
- With multiple references, "identify each image and state exactly what the model should take from it."\[1\]
- For edits, separate the change from the elements that must stay fixed, e.g. "Replace the red chair with a light-oak chair. Keep the table, camera angle, room layout, and lighting unchanged."\[1\]
- Long prompts do not guarantee better results.\[33\]

The official ModelArk prompt guide covers versions 4.0–4.5 (updated Sep 28, 2026).\[35\] There is no 5.5-specific prompt guide yet, so the rules above are carried forward from those guides.

**ByteDance's own 5.5 showcase prompts** follow a consistent pattern: medium/format first, then subject, materials, light source and direction, camera/film stock, and the aspect ratio stated in words. For example: "A vertical 3:4 street photograph after rain, taken from a low angle… Warm golden light contrasts with deep-blue reflections… No full building, people or vehicles appear." Transparent-asset prompts say it outright: "Output each character as a separate image with a transparent background".\[36\]

**Negative prompting:** there is no negative-prompt field on 5.x. Unknown keys such as `negative_prompt`, `seed` or `n` can fail strict validation on some hosts.\[26\]\[37\] Write exclusions as sentences ("No text or logos anywhere in the image.") and keep them to one or two; long exclusion lists produce inconsistent results (community guidance).\[28\]\[38\] Google's guidance for Nano Banana recommends "semantic negative prompts" ("an empty, deserted street" rather than "no cars"), and that phrasing works across models.\[39\]

**Language:**
- English and Chinese are the strongest prompt languages. ByteDance's 5.5 text-accuracy figures cover only Chinese and English.\[40\]
- For on-image text, 5.0 Pro officially names Chinese, English, French, German, Russian, Japanese, Korean, Spanish and Arabic,\[41\] and ByteDance demonstrates right-to-left Arabic layout.\[5\]\[42\]
- **Hebrew is not on any official list, and no tests were found.** Mixed Arabic + Latin in one line already caused visual-order errors in a single third-party test,\[43\] and a guide on 5.0 Pro warns that unlisted languages "work, but in-image text and local-culture accuracy are weaker."\[44\]
- Recommendation for Hebrew: write the prompt in English, ask for a clean text-free area ("leave the lower third empty for a title"), and add the Hebrew typography in post (After Effects/Premiere/Figma/ImageMagick with a proper RTL-capable font). If you do test in-model Hebrew, put the exact string in quotes, keep it to 1–4 words, and avoid mixing it with Latin text or digits.

**Multi-reference and consistency:**
- Refer to inputs by position ("Image 1", "Image 2"; ByteDance's own posts also use "Figure 1/2") and give each a single role.\[45\] For example: "Use Image 1 only for the face and hairstyle; use Image 2 only for the jacket; use Image 3 only for lighting and palette."
- Put the most important reference first.
- For hard-to-describe regions, draw a box or arrow on the image and refer to it ("insert a TV where the red box is").\[46\] 5.0 Pro also accepts `<bbox>x1 y1 x2 y2</bbox>` in 0–999 normalized coordinates.\[1\]
- For a recurring character, build a **character sheet** once (front/three-quarter/profile on a neutral background, plus a costume detail sheet). Pass it as Image 1 in every shot, and keep a fixed "identity block" sentence that you paste verbatim into every prompt.

**Editing discipline:** one change per round, and name what must not change. In testers' experience, "Keep her face, hair, pose and the light exactly as they are" did more for stability than describing the new background in more detail.\[25\] Chain edits from the latest approved version and keep every intermediate version.

**Good vs bad prompts:**

| Bad | Why it fails | Good |
|---|---|---|
| "cool car, neon, city, night, 8k, masterpiece" | Keyword soup; quality tags do nothing; no use, framing or light | "Cinematic 16:9 wide shot for a music-video opening: a matte-black 1970s coupe parked on a rain-soaked Tokyo side street at night. Pink and cyan neon reflect in puddles; light rain; 24mm lens at bumper height; shallow haze. No people, no readable signage." |
| "Make it better and change the background and add a dog and make her smile" | Four edits at once, nothing protected | Round 1: "In Image 1, replace only the background with a sunlit park. Keep the woman, her pose, clothing, face and lighting direction unchanged." Round 2: "Add a small beagle sitting at her left foot…" |
| "poster that says שלום עולם with lots of text" | Unlisted RTL script plus dense text | "Minimal 9:16 poster… leave the top third as flat, empty dark-blue space for a title added later. No text." |
| "Use these images to make a scene" (3 refs) | No roles assigned to the references | "Place the woman from Image 1 wearing the coat from Image 2 into the street from Image 3; match Image 3's light and perspective." |
| "negative_prompt: blurry, ugly, extra fingers…" | No such field on 5.x; long negative lists | "…sharp focus on the hands, natural five-finger hands resting on the table." |

### 5. General image-model practices for a coding agent

**The loop: plan → prompt → generate → inspect → refine → finalize.**

1. **Plan.** Write a shot list (`shots.yaml`) with the ID, purpose, delivery format, aspect ratio, references, must-have text and model choice. Fix the aspect ratio before writing the prompt, because composition and empty space depend on it.
2. **Prompt.** Fill a template; store the prompt as a file, not just inline.
3. **Generate cheap.** Make one image at 1K/1.5K ($0.03 on fal), not a batch of eight. Only fan out (2–4 variants) once the prompt is producing the right composition.
4. **Inspect visually.** The agent must actually open and look at every output (read the PNG). Check against a rubric: subject correct; composition and empty space as specified; text spelled exactly; hands, faces and anatomy; reference fidelity (identity, product, logo); artifacts at the edges; alpha edges on light and dark backgrounds; style consistent with the anchor frame.
5. **Refine.** If an image is about 80% right, edit it; don't re-roll (this is also Google's top rule for Nano Banana).\[47\] Change one variable per iteration. After three failed attempts on the same issue, change strategy: rewrite the prompt structure, add a reference, or switch models.
6. **Finalize.** Re-render or edit at 2K, upscale if the delivery needs 4K, then colour-match in post.

**Reproducibility and logging.** Seedream 4.x/5.x ignore or lack seeds, so reproducibility means archiving everything:
- Naming: `project/shots/<shot_id>/<shot_id>_v<NNN>_<model>_<WxH>.png`.
- Sidecar JSON with: model ID/endpoint, the full request body, prompt text, reference file hashes and URLs, timestamp, request ID, cost tier, the parent version (for edit chains), and a verdict note.
- A rolling `generations.jsonl` log.
- Download immediately: ModelArk-returned URLs are retained for 24 hours, and fal CDN links should also be treated as temporary.\[1\]

**Cost control.**
- Draft at the low tier. On fal, 1K and 1.5K cost the same ($0.03), so draft at 1.5K.\[48\] Volcengine's ¥0.13 tier covers anything ≤2.61 MP.
- Every reference image costs money on edits (fal ~$0.012, Volcengine ¥0.05), so pass only the references a shot needs.
- `num_images` or batch loops multiply cost linearly.
- Layer decomposition bills every layer, so cap `max_images`.\[49\]
- Set a per-session budget in the skill (e.g. stop and ask the user after $5 or 100 images).

**Aspect ratios and sizes for delivery.** All sizes below are within Seedream 5.5's pixel window:

| Delivery | Ratio | Seedream 5.5 size (2K tier) | Draft size |
|---|---|---|---|
| YouTube/film frame, I2V keyframe | 16:9 | 2816×1584 (or 2048×1152) | 1424×800 |
| Reels/TikTok/Shorts | 9:16 | 1584×2816 | 800×1424 |
| YouTube thumbnail (1280×720 delivery) | 16:9 | 2048×1152, then downscale | 1424×800 |
| Instagram feed | 4:5 / 3:4 | 1776×2368 (3:4) | 864×1152 |
| Cinemascope plate | 21:9 | 3136×1344 | 1568×672 |
| Square/social/sticker | 1:1 | 2048×2048 | 1024×1024 |

For thumbnails, keep faces and objects large, leave space for text, and add the text in post unless it is short English. For 4K video plates (3840×2160), generate at 2816×1584 and upscale with a dedicated upscaler (fal hosts several image and video upscalers, e.g. LTX 2.5 Upscale for video up to 4K/8K).\[8\]

**Editing vs regenerating.**
- Edit when the composition is right and a bounded region is wrong. Seedream 5.5's pixel-stable edits make this its strongest mode.
- Regenerate when the composition, camera or concept is wrong.
- Use `background: transparent` instead of a separate background remover for stickers, props and lower-thirds.
- Use `layerize` when a designer needs editable layers.

**Failures and moderation.**
- Handle three classes separately: (a) validation errors (bad size or unknown key): fix the schema, don't retry blindly; (b) transient 429/5xx/timeouts: exponential backoff, max 3 retries; (c) content-filter refusals: rephrase neutrally (clothing, violence and real-person likeness are typical triggers), retry once, then report to the user.
- Never try to evade filters, and use only reference images and likenesses you have permission to process.\[1\]
- Judge success by the status field. One host returned the output URL in `fail_reason` on success.\[25\]

**Batch patterns.** Use an async queue (fal `queue.submit` + status/result, or webhooks), with concurrency capped at 2–4 so you don't hit rate limits. Make jobs idempotent, keyed by shot ID and version, so a crashed run resumes without paying twice. Run the visual review in a separate pass, and keep a contact sheet (a montage of thumbnails) for the user.

### 6. Model-selection guide (November 2026)

| Need | First choice | Why / evidence |
|---|---|---|
| Default photoreal stills, cheap iteration, long revision chains, transparent assets, layered design files | **Seedream 5.5** | AA editing #6 (Elo 1159) at $28 per 1,000; T2I Elo 1134 at $20 per 1,000; native RGBA; 99-layer split.\[13\]\[14\] |
| Highest absolute quality, exact long or dense English text, hero frames where cost is secondary | **GPT Image 2.6** (Sunburst/Flare) | AA T2I #1 (1261) and editing #1 (1210), but $210.72 per 1,000; 4/4 vs 3/4 on long labels in edit chains.\[13\]\[14\]\[21\] |
| Fast, cheap, reference-consistent photoreal; conversational edits; search-grounded facts | **Nano Banana 2.1** (Gemini) | AA T2I #6 (1176) at $33.60 per 1,000; up to 14 references; up to 4K.\[13\] |
| Open/self-hostable pipelines, LoRA training, layout control | **FLUX 3** (Image / Klein) | FLUX 3 Image is AA #17 (1115) at $48 per 1,000; Klein is open-weights at $9 per 1,000.\[13\] |
| Typography-led posters/logos | Ideogram 4.x, GPT Image 2.6 | Text-first models. |
| Art direction and moodboards (manual) | Midjourney V8.x | Strong aesthetics inside its own app; no official public API, so not suitable as an agent's pipeline step.\[50\] |
| Many-reference composition, >2K native | MiniMax H3 Image (edit: up to 16 references, 20 MP), Seedream 4.5 (4K)\[8\] | When Seedream 5.5's 2K/10-reference ceiling is a blocker. |
| Chinese-ecosystem / open model | Qwen-Image 3 | Available on fal. |
| Imagen | Avoid for new work | Google's Firebase AI Logic migration guide states "All Imagen models are deprecated and will shut down as early as August 17, 2026," naming gemini-nano-banana-2.1 as the replacement. |

Rule of thumb for the skill: draft and iterate on Seedream 5.5. Escalate a single hero frame to GPT Image 2.6 or Nano Banana 2.1 only if text or quality fails after three targeted edits. Never mix models within one sequence without re-anchoring the style with references.

### 7. Images as keyframes in AI video pipelines

1. **Design the keyframe at the publish aspect ratio.** On BytePlus ModelArk, Seedance 2.5's output follows the start image's aspect ratio, so a 16:9 keyframe gives a 16:9 clip. Make all the hard decisions (composition, identity, product, light) on the cheap still before paying for video.\[6\]
2. **Prompt only the motion.** Re-describing the whole image "competes with the frame". Say what moves, the direction, the single action, the camera move, and explicitly what stays still ("Nothing else in the frame moves"), plus audio if the model generates sound.\[51\]\[52\]
3. **First/last frames.** One frame animates forward; two interpolate. Kling supports first-only or first+last, but not last-only. For a seamless loop, pass the same still as both first and last frame.\[51\]\[53\] Seedream 5.5's pixel-stable edit mode is ideal for producing a matching end frame: edit the first frame ("same shot, the door now open"), so everything except the change stays identical.
4. **Continuity across shots.** Chain clips by extracting the last frame of clip A (ffmpeg) and using it as the first frame of clip B. Keep the character sheet and style anchor as references for every keyframe.
5. **Model notes:**
   - Seedance 2.5 accepts up to 30 reference images plus video clips and a 10,000-character prompt.\[54\]
   - Kling 3.0 allows 2,500 characters; Veo 3.1 allows 2,000 and always generates audio.\[54\]
   - Draft motion at 480–720p before final renders.
6. **Clean inputs.** ByteDance's Seedance guide recommends removing non-essential text from reference images before using them, and Seedream edit mode can do this.\[55\]
7. **Documentary caution.** Label generated imagery as such, avoid fabricating real people or events, and keep C2PA/provenance metadata where the platform provides it.

## Recommendations (condensable into SKILL.md)

**DO**
- Confirm the endpoint/model ID and fetch the live schema before the first call; never invent parameters.
- Draft one image at 1K–1.5K, inspect it visually, then iterate.
- Write natural-language prompts: [type + purpose] → subject/action → environment → light → camera/lens → style/palette → text in "quotes" → 1–2 inline exclusions.
- Set the size explicitly to the delivery aspect ratio; edits don't inherit the input ratio.
- In edits: one change per round + an explicit "keep unchanged" list; chain from the last approved version.
- Label references "Image 1…N" with one role each; reuse a character sheet and a style anchor.
- Use `background: "transparent"` + PNG for cut-outs; check alpha on dark and light backgrounds.
- Download outputs immediately; save a JSON sidecar and a `generations.jsonl` entry for every call.
- Set `watermark: false` where permitted; track spend against a budget.
- For video: keyframe at the final aspect ratio, motion-only prompt, and first/last frames made via edits.

**DON'T**
- Don't send `negative_prompt`, `seed` or `n` to Seedream 5.x, or expect a seed to reproduce results.
- Don't ask for 4K natively from 5.5 (the ceiling is ~4.62 MP); upscale instead.
- Don't request transparency with JPEG.
- Don't batch 8 variants of an unproven prompt.
- Don't bundle several edits in one request or re-roll an image that is 80% right.
- Don't trust on-image text, logos or product details without checking them character by character.
- Don't render Hebrew (or mixed RTL + Latin) text in-model for final delivery; add it in post.
- Don't use vague keyword soup or "8k, masterpiece" tags; don't exceed ~600 English words.
- Don't retry moderation blocks repeatedly or try to evade filters.

**Prompt template (generation):**
`[Medium/format, aspect ratio] for [purpose]. [Subject + distinguishing details] [action] in [environment, time, weather]. [Light source, direction, quality]. [Camera: shot size, lens, angle]. [Style/palette/film stock/texture]. Text: "[exact words]" in [font description] at [position]. [1–2 exclusions].`

**Prompt template (edit):**
`In Image 1, [single change, location]. Use Image 2 only for [role]. Keep [face, pose, clothing, camera angle, framing, lighting, colour grade, all other objects] exactly unchanged.`

## Caveats

- **Seedream 5.5 is five days old.** Nearly all quality claims (100 rounds, 0.4%/1.7% text corruption, realism gains) are ByteDance's own.\[2\]\[25\] Independent evidence is limited to arena Elo rankings and a few small tests (three-round and five-round edit chains). The rounds claim itself conflicts between sources (100 vs 80-plus).
- **Model IDs and schemas are still settling.** The BytePlus `dola-seedream-5-5-261028` ID comes from an early-access pull request that had not been live-tested.\[17\] fal's exact 5.5 parameter list could not be retrieved here, so 5.0 Pro's schema was used as a proxy. Fields such as `num_images` vs one image per call, the `watermark` default, and the exact `background` field name on fal must be verified against the live OpenAPI schema.
- **Prices vary by host and change often.** fal $0.03/$0.0405; Atlas $0.016; BytePlus "from $0.02"; Volcengine ¥0.13/¥0.23 plus ¥0.05 per input.\[3\]\[29\]\[31\] Re-check before budgeting.
- **Hebrew rendering is unverified** for all Seedream versions. Arabic is the only demonstrated right-to-left script.
- **Community tips are labelled as such** (e.g. keep negations to 1–2, imperfection cues for realism, three-strikes model switching). They are sensible heuristics, not documented behaviour.
- **Competitor data (GPT Image 2.6, Nano Banana 2.1, FLUX 3) comes from leaderboards and secondary coverage** current to early-to-mid November 2026; the Imagen shutdown comes from Google's own Firebase documentation. Rankings shift monthly.

## Sources

1. [What is Seedream? A guide to image generation and editing](https://ai.byteplus.com/resources/what-is-seedream-ai)
2. [Seedream 5.5: 100-Round Editing, Transparent PNG and Pricing](https://maverickframe.com/blog/seedream-latest-version/)
3. <https://www.atlascloud.ai/models/bytedance/seedream-v5.5/edit>
4. [模型价格](https://api.tu-zi.com/pricing)
5. [Seedream 5.0 Pro: the image model that ships you layers](https://packetnebula.com/articles/seedream-5-0-pro-ships-editable-layers/)
6. [Image-to-Video AI Workflow (2026): From Key Frame to Motion](https://www.clipspeed.ai/blog/image-to-video-ai-workflow.html)
7. [Seedream 5.5: 100 Edit Rounds and Native Transparency](https://www.eachlabs.ai/blog/seedream-5-5)
8. [Recently Added | fal](https://fal.ai/explore/recently-added)
9. [Seedream 5.5 is on fal with edit and layer endpoints](https://creatorstoolbox.com/@scout/post/n_13koqy6mxc34b)
10. [Seedream 5.5 Release: What ByteDance Confirmed — and What to Do Today](https://blog.sandbase.ai/seedream-5-5-release-whats-new-2026/)
11. [ByteDance released Seedream 5.5, supporting...](https://www.chaincatcher.com/en/article/2302965)
12. [ByteDance Seedream 5.5 AI Image Editor Claims 100 Edits Without Drift, Publishes No Drift Data](https://www.techtimes.com/articles/330349/20261110/bytedance-seedream-55-ai-image-editor-claims-100-edits-without-drift-publishes-no-drift-data.htm)
13. [AA-Image-T2I v2.1 Leaderboard - Top AI Image Models](https://artificialanalysis.ai/image/leaderboard/text-to-image)
14. [AA-Image-Editing v2.1 Leaderboard - Top AI Image Models](https://artificialanalysis.ai/image/leaderboard/editing)
15. [Seedream 5.0 Pro Text to Image API Docs](https://fal.ai/models/bytedance/seedream/v5/pro/text-to-image/api)
16. [Seedream 5.5 API for Image Generation and Layer Decomposition - APIXO](https://apixo.ai/docs/models/image/seedream-5-5)
17. [Add early-access Seedream 5.5 support by ArthurReimus-ByteDance · Pull Request #29 · byteplus-sa/ComfyUI-BytePlus-ModelArk](https://github.com/byteplus-sa/ComfyUI-BytePlus-ModelArk/pull/29)
18. [Seedream 5.0 Pro Review: Features, Prompts & Verdict](https://www.jxp.com/seedream/blog/seedream-5-0-pro-review)
19. [Seedream 5.0 Pro: The Complete Guide to Specs, API, Pricing, and 50+ Use Cases](https://promptslove.com/blog/seedream-5-pro-the-complete-guide/)
20. [How to choose between Seedream 5.5, 5.0 Pro, and 5.0 Flash? Comparison of feature differences, pricing, and four upgrade scenarios across the three models - Apiyi.com Blog](https://help.apiyi.com/en/seedream-5-5-vs-5-0-pro-vs-5-0-flash-comparison-en.html)
21. [Seedream 5.5 vs GPT Image 2.6: A Blind 5-Round Image Model Test](https://www.atlascloud.ai/blog/tips/seedream-5-5-vs-gpt-image-2-6)
22. [\[Bug\]: Seedream sends a model id BytePlus ModelArk does not list · Issue #162 · tryonlabs/opentryon · GitHub](https://github.com/tryonlabs/opentryon/issues/162)
23. [Seedream 5.5 API](https://runware.ai/docs/models/bytedance-seedream-5-5)
24. [Seedream v5.5 Layer Decomposition (I2I) API Image by BYTEDANCE - Prix Compétitifs - Accès API Unifié](https://www.atlascloud.ai/fr/models/bytedance/seedream-v5.5/layer-decomposition)
25. [Seedream 5.5 API: Pricing, 100-Round Edits & Tested Prompts](https://blog.siray.ai/seedream-5-5-api-pricing-prompts/)
26. [Seedream 5.0 Pro Bugs: Documented Limits and Retests](https://reapi.ai/blog/seedream-5-0-pro-bugs-and-fixes)
27. [Seedream 5.5: What's New and How to Use It Online (2026)](https://www.mage.space/blog/seedream-5-5)
28. [How to Prompt Seedream: Prompting Guide with Examples](https://www.mage.space/models/seedream/prompting-guide)
29. [Seedream 5.5 Official API Pricing Announced: Image Generation Starts at 0.13 Yuan; How Much Do Continuous Image Editing and Layer Separation Cost Respectively? - Apiyi.com Blog](https://help.apiyi.com/en/seedream-5-5-api-pricing-generation-editing-layers-en.html)
30. [Build a Product Image Automation Workflow with Seedream 5.5: 4 Steps to Connect Generation, Image Editing, Transparent Assets, and Layer Separation - Apiyi.com Blog](https://help.apiyi.com/en/seedream-5-5-product-image-automation-workflow-en.html)
31. [Seedream 5.5: 100 Rounds of Editing, Native Transparency](https://cellcog.ai/blog/seedream-5-5/)
32. [Seedream 5.5 Review: Official Specs, Pricing and Access](https://myclaw.ai/blog/seedream-5-5-review)
33. [Seedream 3.0 Prompt Guide--ModelArk-Byteplus](https://docs.byteplus.com/en/docs/modelark/1795150)
34. [Seedream 4.5: A Complete Guide With Python](https://www.datacamp.com/tutorial/seedream-4-5)
35. [BytePlus](https://docs.byteplus.com/en/docs/modelark/seedream-4-0-5-0-prompt-guide?redirect=1)
36. [Seedream 5.5](https://seed.bytedance.com/en/seedream5_5)
37. [How to Use Seedream 5.5 and 5.0: Prompts, Edits and Text (2026)](https://www.mage.space/blog/how-to-use-seedream-5)
38. [Seedream 5.0 Pro Prompt Guide How to Get the Best Results (2026)](https://www.imagine.art/blogs/seedream-5-0-pro-prompt-guide)
39. [Gemini Generate Content API (Legacy) | Google AI for Developers](https://ai.google.dev/gemini-api/docs/generate-content/image-generation)
40. [Seedream 5.5: Editing, RGBA Assets and Small Text](https://beatapi.io/blog/what-is-seedream-5-5)
41. [Seedream 5.0 Pro API - Multimodal AI Image Model](https://fal.ai/seedream-5.0)
42. [Seedream 5.0 Pro](https://seed.bytedance.com/en/seedream5_0_pro)
43. [AI Image Generator Multilingual Text Test: Chinese, Arabic & Hindi](https://seedreamv5.com/blog/ai-image-generator-multilingual-text-test)
44. [Seedream 5.0: ByteDance's New AI Image Generator](https://artlist.io/ai/models/seedream-5-0)
45. [Seedream 5.0 Lite Prompt Guide: Tested Tips](https://fuser.studio/articles/seedream-prompt-guide)
46. [Seedream 4.5 Prompt Guide: Examples That Work](https://apimart.ai/blog/seedream-4-5-prompt-guide)
47. [Nano-Banana Pro: Prompting Guide & Strategies - DEV Community](https://dev.to/googleai/nano-banana-pro-prompting-guide-strategies-1h9n)
48. [Seedream 5.5 (Text to Image) API on fal](https://fal.ai/models/bytedance/seedream/v5.5/text-to-image)
49. [Seedream 5.5 Layerize (Image to Image) API on fal](https://fal.ai/models/bytedance/seedream/v5.5/layerize)
50. [Best AI Image Models Nov 2026: Ranked, With Prices](https://www.teamday.ai/blog/best-ai-image-models-2026)
51. [Image to video and keyframes — Seedance 2.5 API](https://runware.ai/docs/models/bytedance-seedance-2-5/guides/image-to-video)
52. [Seedance 2.5 Image to Video: Start and End Frames](https://videoai.me/blog/how-to-use-seedance-2-5-image-to-video)
53. [First-Frame and Last-Frame Control in AI Video](https://prompt-architects.com/blog/371-first-frame-and-last-frame-control)
54. [50 AI Video Prompt Examples: Cinematic, Product, Social & More](https://www.seeddance.io/blog/ai-video-prompt-examples)
55. [document--ModelArk-Byteplus](https://docs.byteplus.com/en/docs/modelark/seedance-2-0-prompt-guide&gsessionid=MAaA8_FEgzuPen1Y_ozS4d-nEgPqoGQ2pTIKuPTpuTUpuVAPG2qNvA)
