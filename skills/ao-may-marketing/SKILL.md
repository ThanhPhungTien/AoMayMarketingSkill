---
name: ao-may-marketing
description: "Làm marketing cho chuỗi nhượng quyền Áo Mây Laundry và từng cửa hàng: đọc đúng bài và đúng cửa hàng trong Notion, viết caption Facebook, lập kế hoạch 14 ngày, thiết kế poster giữ logo gốc và kiểm tra chất lượng. Dùng khi người dùng nhắc Áo Mây, tên hoặc mã một cửa hàng Áo Mây (Tân Hưng/TH, Chánh Hưng/CH, Dương Quảng Hàm/DQH, Tân Phú/TP, Nguyễn Xí/NX, An Khánh/AK), thương hiệu Miu Miu (MM) hoặc yêu cầu gen poster facebook từ ảnh mẫu, mẫu DQH-01 hoặc bài số trong lịch Áo Mây."
metadata:
  version: 1.4.10
---

# Áo Mây Marketing

Áo Mây is a laundry **franchise brand**; each franchise store has its own profile (store code, contacts, services, assets, poster route). Read [brand context](references/brand-context.md) first. Respond in Vietnamese unless requested otherwise. This skill supplies instructions, brand context and bundled assets; it does not provide an image model or a Facebook publisher.

## 0. Precedence (read before anything else)
Apply in this order when sources conflict:
1. The user's explicit instruction in the current conversation.
2. Official Áo Mây brand kit (not received yet).
3. The store's own profile and approved template (`assets/stores/<CODE>/spec.json`, its Notion store row).
4. Chain-wide rules (brand-context, Notion 01/03).
5. Within any source, a newer dated entry overrides an older one.

Where each kind of information lives — one place only:
| Information | Source |
|---|---|
| How to work (workflow, checks) | this SKILL.md |
| Chain rules, voice, prohibitions, store index | references/brand-context.md |
| Store facts: address, hotline, fanpage, services, offers, hashtags | Notion database **02 Cửa hàng** (brand-context holds a dated snapshot only) |
| Posts, captions, briefs | Notion **07 Content Calendar** (DQH posts may still sit in 06 until migrated) |
| Fonts, coordinates, colours, file names, SHA-256, poster route | `assets/stores/<CODE>/spec.json` |
| Logo, CTA, background, reference images | files under `assets/` — made by the user only |

If a Notion page describes a production workflow that differs from this skill, follow this skill and mention the difference in one sentence.

## Choose the workflow
- Brand context and positioning: product-marketing.
- Facebook captions, 14-day plans, short video scripts: social.
- Campaign angles and hook variants: ad-creative.
- Poster: §3, route taken from the store's spec.json.
- New persuasive copy: copywriting; polish existing copy: copy-editing.
The bundled general skills are subordinate to current user instructions and verified Áo Mây requirements. Never apply miu-miu-marketing guidance, colours or assets to Áo Mây.

## 1. Resolve store and source
1. **Store:** map the user's words to exactly one store code using the store index in brand-context (names and aliases). Ambiguous or unknown → ask. Never borrow facts, assets, hashtags or offers from another store.
2. **Readiness:** load `assets/stores/<CODE>/spec.json` (locate the skill folder as in §3 Preflight). If `status` is `draft`, captions/plans may use only confirmed facts and **no poster is made** — tell the user which fields or files are missing.
3. **Post:** use the host Notion connection. Fetch the Calendar schema before querying. Filter by store (relation `Cửa hàng` once migrated; until then the legacy select `Cửa hàng` in 07 or `Chi nhánh` in 06) AND post number together. Post numbers repeat across stores — never match by number alone.
4. Fetch the matching page. Read Bài đăng, Cửa hàng, Caption, Hook/Ý tưởng, Brief poster, Ngày đăng, Trạng thái, Ghi chú and page body. Keep the page URL.
5. Reconcile contradictions. Explicitly revised production properties beat old draft text. Do not silently combine versions. Ask only if the conflict changes the deliverable.
6. Re-fetch the store row in 02 for contacts, services and offers. A field that is empty or marked unconfirmed must not appear on a poster or in a caption as fact.
7. Record a compact source lock: store code, post number, title, source URL, hook, topic, caption, brief, contact facts, uncertainties. Check it again before delivery. Do not change a numbered post's topic.
8. If Notion tools are unavailable, say so and use an actual user-supplied brief. Never claim a live read or invent missing rows.
9. A request with a user photo and no post number ("thay nội dung theo ảnh này") → the photo + the user's message are the brief.

## 2. Produce the copy or plan
Use a strong varied hook, relatable situation, specific supported benefit, one CTA and a few local hashtags. Preserve an existing caption unless editing is requested. Keep image copy short. A 14-day plan has one row per day and store with objective, service, hook, caption, CTA, visual brief and status. Vary topics and creative treatment between stores posting the same day. Mark proposals and unknown service availability. Do not invent prices, promotions, opening hours, free delivery, express turnaround or guaranteed results; use only offers confirmed for that store.

### Caption length and substance (user-updated 2026-10-23)
The user wants copy that is engaging and sufficiently developed, neither verbose nor skeletal. Default to one hook plus 3 short paragraphs (a concrete situation, practical service benefit, one CTA), then store contacts and 3–4 relevant hashtags. For a regular Facebook service post, aim for roughly 120–170 whitespace-separated Vietnamese words before contacts as an editorial guide, not a quota; shorten if the topic is simple. Every sentence must add information or emotional relevance. Do not stretch a thin post with filler, repeated rhetorical questions or several versions of the same pain point.

Develop one specific customer moment and explain how the service helps that moment. Use 1–2 grounded benefits, supported by verified service facts. Avoid turning the entire caption into 'send item / ask timing / get quote'. Keep timing or availability qualifications in one natural sentence when relevant. Rotate situations, hooks and CTA wording across nearby posts. When the user says a numbered post is too sparse, rewrite that exact store/post Caption and matching body section in Notion, preserving poster, topic, approval status and unrelated content.

Hashtags: use the store's saved set (Notion 02 / brand-context store index) and swap only the service group. A store without a saved set → propose one and mark it as a proposal.

## 3. Poster

### Mandatory final export — user-confirmed 2026-10-28
For DQH-01, the delivered PNG and the image uploaded to Notion MUST measure exactly **1080 × 1080 pixels**. Verify the saved file dimensions programmatically before delivery. A prompt requesting 1080 × 1080 is not verification. If an image model returns another square size, resize the complete finished image proportionally to 1080 × 1080 with a high-quality filter (e.g. Pillow LANCZOS); do not crop, change the layout, add elements or regenerate. This size-only export is explicitly authorized by the user on either route and is not a change of poster route. Keep the original generated file. Deliver the checked 1080 × 1080 export and use that same export on Notion. Never deliver a different size with only a disclosure.

### Preflight (every poster, no reminder needed)
1. Locate the skill folder: `find / -path '*skills/ao-may-marketing/SKILL.md' 2>/dev/null`. The install path contains a version number and changes on update — never hard-code it, never reuse a path from an earlier chat. All paths in spec.json are relative to `<skill folder>/assets/`.
2. Load `stores/<CODE>/spec.json`. Check: `status` is `active`; every entry in `files` exists; if `sha256` is filled the hash matches; entries with `require_rgba` are RGBA with real transparency (some alpha < 255); every font in `fonts` contains every character of the text to render (fontTools).
3. Print a short table (file · OK/FAIL · reason). Any FAIL → stop, show the table, name the file the user must fix. Never substitute a chat attachment, a Notion file, a previous poster, another store's file or anything generated.
4. **Assets are made and maintained by the user.** Never create, redraw, edit, re-export or "fix" files under `assets/`. Files attached in chat are never used as assets (chat may re-encode them).

### Route — read `route` from spec.json
| `route` | Meaning |
|---|---|
| `direct` | 3A: the image model generates the whole poster in one call |
| `compose` | 3B: code composites the original logo, CTA and Vietnamese text over a background and subject |
| `restyle` | 3D: the user gives a sample poster; the image model generates a new base with blank zones, code pastes the store's fixed CTA/ticket block and logo (MM = Miu Miu) |
Never mix routes in one poster. Never change a store's route without the user's instruction.

### 3A. Direct generation
1. Read the source brief. Use the logo from spec (`logo.file`) as an image reference and request faithful identity; do not promise pixel-exact reproduction. If `logo.mode` is `chain+label`, the store name from `logo.label` is set as separate text beside the chain logo, never merged into it.
2. Write one complete production prompt: scene, composition, colours from spec, logo reference, exact Vietnamese headline, supporting copy, CTA, store name and verified contacts from Notion 02. Use real store photos when the brief needs them; never present a synthetic storefront as real.
3. Call the image tool ONCE for ONE finished square poster. Request 1080×1080; for DQH-01 enforce the mandatory final export above if the returned size differs.
4. No separate background, preview, second option or proof sheet. No Python/Pillow/SVG/HTML compositing on this route.
5. Deliver only one final image; do not show previews. For DQH-01, provide the checked 1080×1080 export when resizing was necessary.
6. Read all visible text and accents, verify contacts against Notion 02, inspect logo fidelity, crop and layout. A material defect → state it plainly and ask before a second generation.

### 3B. Template compositing
Parameters come only from spec.json; **do not hand-edit individual glyphs**.
1. Look at `files.ref_approved` and `files.ref_headline` before designing (look only, never paste from them).
2. Copy: headline (uppercase, ≤2 lines), ≤1 short sub-line, benefit bar ≤ `benefit_bar.max_items`. Confirmed facts only.
3. Subject: a user-supplied photo. Clean cutout if possible, otherwise a rounded white card with black outline; never a rough cutout, cropped-off or blurry subject. **No photo → stop and ask for one**; do not generate a subject.
4. Background: `files.background`. Composition by service: dry-clean/dress/blazer → garment dominant; pickup/delivery → service scene; stuffed toys → subject dominant. No podium unless the brief asks.
5. Compose with Python/Pillow at exactly the spec canvas:
   - Logo: paste `files.logo` with `logo.scale` at `logo.paste_at`, uniform scale only, no effects, nothing over it.
   - Headline: a pre-cut PNG in `files.headline_dir` matching the exact phrase → use it (uniform scale only). Otherwise render with `fonts.headline`: NFC-normalise, uppercase, then apply `embolden_px`, `tracking_px`, `stroke_px`/`stroke_color`, `shadow_offset_px`/`shadow_color`, `shear` exactly as specified.
     Render at the real size (`one_line_cap_px` for one line, `two_line_cap_px` for two); all px values in the spec are for that size — never render small and scale up, never test at a smaller size.
     **Diacritic check:** after rendering, inspect every stacked or crowded mark at 100% (Ấ Ầ Ẩ Ẫ Ậ, Ắ Ằ Ẳ Ẵ Ặ, Ế Ề Ể Ễ Ệ, Ố Ồ Ổ Ỗ Ộ, Ớ Ờ Ở Ỡ Ợ, Ứ Ừ Ử Ữ Ự, Đ). Judge the **black fill only**: each black mark must be separate and recognisable, not touching another black mark or a letter, and black letters must not touch each other. The white stroke and the shadow MAY merge around marks and between letters — that is the approved sticker style (see ref-approved and ref-headline), not a defect. If the black fill fails, stop and report the spec values that cause it — do not adjust glyphs by hand.
   - Sub-line and benefit bar: `fonts.secondary` / `fonts.body` per spec boxes.
   - Footer: paste `files.footer` unchanged at `footer.box`. Never retype hotline or address.
6. **Logo pixel check:** crop the logo area from the saved output, compare with `files.logo` resized by the same factor and composited on the same background crop. Mean absolute difference must be ≤ 2 (0–255); otherwise rebuild, do not deliver.
7. QC: view the full image and a 360 px downscale; read every word and diacritic; compare the headline with the references on weight, width, corner softness, slant, spacing, stroke and shadow. Never claim "khớp 100%". If `headline.font_status` is `provisional`, say in one line that the headline font is not yet approved.
8. Deliver exactly one final PNG named per brand-context convention, plus one line: `Assets: preflight OK · logo SHA-256 <khớp/chưa khai báo> · pixel diff <value>`. Do not show intermediate composites.

### 3C. Restyle from a reference poster (user gives a sample poster and asks to change brand, colour, logo or contacts)
Learned from failed runs; apply every time.
1. **The sample is the base, not an inspiration.** Edit that exact image: keep layout, subject, objects, photos and every Vietnamese word. Never redesign, never swap the subject (a wedding-dress sample stays a wedding dress), never add benefits, badges, offers or other brands' names or patterns (no CHANEL, GUCCI, LV).
2. **Logo:** only the logo file the user attached, as one lockup (wordmark + tagline + emblem together). Never redraw it, never split its parts. No logo attached → stop and ask. Unless the user says otherwise, place it top-left, about 5% from the top and left edges, about 28% of the image width, with no backing card or patch; use the same position and size on every poster of a series.
3. **Colour:** change the palette as told; keep subjects whose colour matters (a white dress stays white). Recolour design elements (bars, icons, buttons, headline accent, corner blocks); do not tint neutral photo areas (suits, shirts, tables, walls): that leaves pink or purple smears.
4. **Contacts:** replace hotline and address with exactly the text the user gave; the old store's contacts must not survive anywhere.
   The old brand's name must disappear everywhere, including headlines ("TẠI ÁO MÂY"), photos (embroidered apron, signage) and tags. Service promises such as "miễn phí giao nhận" also stay out unless confirmed for the new store.
   Claims that belong to the sample's store (founding year such as "since 2017", standards such as "tiêu chuẩn châu Âu", awards, ticket or barcode cards naming the old store) are not facts about the new store: remove them unless the user confirms them.
5. **Icons** must be drawn as vectors or taken from the sample; font glyphs for phone, pin or arrow can render as empty boxes, and the model may swap a phone icon for a smiley. Check each icon is the right symbol.
6. **Proofread before delivery:** read every word and diacritic against the sample, line by line (known slips: "nhăn nhàu" → "nếp nhăn mẹ", "Cầu Vồng" → "Cầu Vông"). Confirm the output size is the requested one.
7. One image per request, then wait for approval before the next sample. If an A/B "which image do you like more" prompt appears, skip it.
8a. Miu Miu brand pink for recoloured design details is **#F58B9F** (user-confirmed 2026-10-30); the Miu Miu logo file itself is never recoloured.
8. **Fixed blocks are built by code, not drawn by the image model.** Paste the user's logo file (transparent background, never re-rendered); draw the contact block and the CTA button with the fonts in `assets/chain/fonts`. Contact block: phone and pin icons the same diameter, the glyph centred inside its pink circle; phone number and address in the same font; about 3% margin from every edge; nothing cropped by the image edge. CTA button: label centred, arrow on the same line, whole button inside its block. Ticket or voucher card: fully inside the image, clean edges, no leftover white patch from the sample, brand name text clear of the button.
9. **Do not iterate the same image through many model edit rounds.** Each round tends to add a new defect (blur, patches, mis-typed diacritics). If two rounds do not fix a block, rebuild that block by code.

### 3D. Route `restyle` — poster from a sample, per store (code MM and any store whose spec.json has `route: restyle`)
**ONE TURN, NO EXCEPTIONS. Follow this checklist literally and tick it off in your head before you stop:**
**[A] First tool call of the turn = Python `restyle_poster.py check <CODE>`; paste its table into your reply text. No image tool call is allowed before [A] is done.**
**[B] Call the image tool once for the base.**
**[C] The image tool returning is NOT the end of the turn. Your very next action MUST be a Python tool call: save the returned image as `nen.png`, resize to the canvas with Pillow LANCZOS, then run `restyle_poster.py paste <CODE> nen.png <name>.png --block cta|ticket`. Do not write any text and do not end your reply between [B] and [C].**
**[D] Reply only after the script printed `PASTE: OK`: show the script output verbatim and link the final file. A reply containing only the generated base, or ending right after the image tool, is a failed task.**
**If you notice the base exists but [C] has not run, run [C] now, in this same turn, without asking.**
Everything store-specific comes from `stores/<CODE>/spec.json` (`files`, `fonts`, `colors`, `contacts`, `restyle`); never hard-code it here and never take it from chat. Script: `scripts/restyle_poster.py` (needs Pillow; fontTools optional).
0. **Information gate — before any generation.** Run `python3 scripts/restyle_poster.py check <CODE>` and print the table. It verifies: status active, route restyle, canvas, logo (exists, SHA-256, RGBA, wide enough for `logo_width`), CTA and ticket block (exist, SHA-256, RGBA, same size as canvas), fonts (exist, contain every Vietnamese letter), colours (`text_accent`, `logo_accent`, `on_pink` valid hex), contacts (hotline, address), block and logo coordinates. Any FAIL → stop, name the missing item and ask the user to supply it. Never invent, substitute or generate a missing logo, CTA, font, colour or contact.
1. **Read the sample:** layout of every zone, every Vietnamese word exactly (with diacritics), the benefit area, brands of customers visible, whether it needs the CTA or the ticket block. Remove the old store's name (`restyle.forbid_text`) and claims specific to the old store (§3C item 4); keep `restyle.keep_brands`. Summarise in a few lines; if the user said "chạy luôn", do not wait.
2. **Generate the base** (image model, one image, `restyle.canvas`): layout is FREE (`restyle.layout_mode`): do not copy the sample's arrangement, arrange the components yourself, but pick the poster type from the sample (`restyle.poster_types`: compare = two TRƯỚC/SAU frames, single = one hero image with no before/after labels) and include every item of `restyle.components` and obey `restyle.layout_constraints`; only the logo and the CTA/ticket block have fixed positions (placed by code). Keep the sample's wording; subject photos need not match, background may change but keep the tone. The prompt must state: background per `restyle.background`: light only (the logo is dark), rotate `restyle.background_variants` across a batch so posters do not look identical, never one flat colour, no flowers or props; all content must end 35px above the block's `reserve` top (the gate rejects text there); `restyle.logo_zone` empty, same soft background as its surroundings with a smooth gradient — no separate lighter box, no hard edge (the gate rejects a visible patch, `zone_edge_max`); every headline line starts below `restyle.headline_top_min` px from the top and nothing may overlap the logo zone; the block's `reserve` band empty; no logo, hotline, address or contact bar; `restyle.forbid_people`; headline in `restyle.headline.font_style`, line 1 `headline_main` colour, line 2 `text_accent`, text on pink backgrounds `on_pink`; script lead-in per `restyle.script_font`. Quote colour values from spec.json.
3. **Paste by code only** (never the image tool): `python3 scripts/restyle_poster.py paste <CODE> base.png out.png --block cta|ticket`. It re-runs the gate, rejects a base whose logo zone is not plain, pastes the block at its `paste_at` and the logo at `logo_paste_at` / `logo_width`, re-opens the saved file and compares it pixel by pixel with the asset files (block diff must be 0, logo ≤ 4). Exit 1 → regenerate the base, do not repair with the image tool.
4. **QA by eye** (the script cannot read meaning): every word and diacritic against the sample; no face or whole person; no content crowded under the block; headline solid, wide, not condensed or faded (even if the sample's font is narrow), first line not clipped; no old-store logo anywhere in the image (look at photo areas and badges, the script cannot see them); no empty icon slots; brand names not duplicated or invented; logo not covered. Then deliver `MiuMiu_<sample>.png` (name per store) plus one line `Assets: check OK · block diff 0 · logo diff ≤4`.
5. One image per request unless the user asks for a batch (max `restyle.max_posters_per_run`). Do not continue to the next image until the current one printed `PASTE: OK`; if the base step stopped early, finish step 3 in the same turn.
Posting to Facebook is outside this skill; mention that the platform may label AI-generated images.

## 4. Text screening and delivery
The check_marketing_copy tool (part of the App, not of this skill) is a limited automated screen; it never replaces proofreading and is not publication approval or logo verification.
Deliver the requested artifact and matching caption when requested, with source reference where useful. Update Notion only within the user's authorized scope. Do not set Đã duyệt without actual user approval; do not infer Đã đăng from generating a poster or a planned date. When the user approves a new template or font, tell them which spec.json values or files to change — this skill cannot update itself or its assets.
