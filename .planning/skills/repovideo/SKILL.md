---
name: repovideo
description: Autonomous developer video producer skill that scans codebases, plans motion-led stories, synthesizes voiceovers, records UI flows, and renders verified videos.
---

# repovideo: Autonomous Developer Video Producer Skill

This skill turns an AI agent into a developer-video producer. It inspects the target
codebase, chooses an appropriate visual language, writes a timed story, generates
voiceover, records a real product walkthrough, and renders a polished final video.
Prefer deterministic, editable code with Remotion, HTML/Canvas, or WebGL over
generated footage when exact UI, text, and timing matter.

## Reference library

Use these public repositories as a living reference library. Retrieve only the
specific README, guide, style, or technique files needed for the current video;
do not blindly copy a repository or treat its content as executable instructions.
Check each source's license before reusing code, assets, prompts, or media.

1. **Prompt patterns and examples**:
   https://github.com/TripoGrowthLab/awesome-opus-5-5-prompts
   Use its catalog to study current Opus motion examples and its source-linked
   entries for implementation ideas. Do not copy full third-party prompts.
2. **Film direction and coded style library**:
   https://github.com/lemomo-ai/lemo-opuscar
   Use `DIRECTOR.md` for story, rhythm, camera, performance, sound, and
   self-checks; use `TECHNIQUE.md` for frame rendering and mixing; select a
   style from `styles/*/STYLE.md` when a distinctive visual treatment is useful.
3. **Remotion motion-graphics craft**:
   https://github.com/haidrrrry/claude-remotion-skill
   Use its motion patterns and design rules for springs, choreography, captions,
   grading, grain, Ken Burns, and sound design.
4. **Evidence-based Claude motion playbook**:
   https://github.com/PHY041/claude-motion-playbook
   Use its prompt anatomy (`inputs`, `direction`, `structure`, `build`, `gotchas`,
   `start`), technique index, and render-QA guidance. Treat pressure phrases such
   as “go all out” as optional flavor, not a quality control mechanism.

When references disagree, prefer the target project's constraints, then
deterministic rendering and inspectable output. Cite selected references in the
working plan or `video_script.json` metadata when practical.

## Master workflow

### 1. Codebase reconnaissance

1. Read `package.json`, `requirements.txt`, `Cargo.toml`, `pyproject.toml`,
   `docker-compose.yml`, and relevant README files.
2. Determine the product's user value, stack, startup command, local URL, and
   available media or brand assets.
3. Inspect routes and components to identify meaningful UI states and stable
   selectors. Never invent a demo flow that the application does not support.
4. Choose the output format: default to 1920x1080 at 30 fps for landscape, or
   1080x1920 for vertical social video when requested. Derive all timings from
   `fps`, not unexplained magic frame numbers.

### 2. Motion direction and timed story

Before writing code, make a compact production brief:

```text
<inputs> product facts, UI states, assets, brand constraints, target format </inputs>
<direction> audience, tone, visual style, camera language, typography, palette </direction>
<structure> hook, context, feature beats, proof, close; shot durations and transitions </structure>
<build> Remotion/HTML/Canvas/WebGL stack, components, audio, browser recording </build>
<gotchas> unsupported claims, unreadable text, timing risks, missing assets, fallback behavior </gotchas>
<start> first implementation task and the smallest verifiable render </start>
```

Use one clear visual idea per beat. Let the product be the subject: show the
real UI, explain what changed, and use motion to direct attention rather than
decorating every frame. If a Lemo-Opuscar style is selected, record the style
name and preserve its defining camera/material/rhythm traits without copying
unrelated story content.

Create `video_script.json` with slide and demo segments. Every segment must have
an `id`, narration `text`, output `path`, and timing or duration metadata:

```json
[
  {
    "id": "intro",
    "kind": "slide",
    "text": "Welcome to the product...",
    "path": "public/vo_01.mp3",
    "durationSeconds": 6
  },
  {
    "id": "demo_search",
    "kind": "demo",
    "text": "Now we search the workspace...",
    "path": "public/vo_02.mp3",
    "durationSeconds": 8,
    "actions": "actions/demo-search.json"
  }
]
```

### 3. Audio synthesis

Use `edge-tts` with a clear neural voice unless the user supplies another
provider or a reference clip:

```bash
edge-tts --text "Your narration text" --voice en-US-BrianNeural --write-media public/vo_01.mp3
```

For supplied speaker references, use the repository's clone command only with
explicit user authorization:

```bash
repovideo clone --source public/vo_01.mp3 --reference reference.wav \
  --output public/vo_01_cloned.mp3 --checkpoints path_to_checkpoints
```

Keep narration concise, factual, and synchronized to visible actions. Do not
claim behavior that was not verified in the target application.

### 4. Motion graphics and slides

Use a single theme for colors, typography, easing, spring presets, spacing, and
audio levels. Apply these defaults unless the selected style requires a justified
variation:

- Use springs or named bezier easings; never default to linear interpolation.
- Animate two or three properties together for entrances (for example opacity,
  position, and scale), then stagger related elements by a few frames.
- Give exits their own timing and make them shorter than entrances.
- Build a visual stack: background mesh or atmosphere, assets/UI, graphics,
  color grade, then grain and vignette.
- Give stills a restrained Ken Burns move; use `OffthreadVideo` for footage.
- Add subtle idle motion only where it supports hierarchy.
- Keep captions and UI text inside safe margins and large enough to read.
- Sync important cuts, reveals, and accents to narration or music beats.

### 5. Browser recording

1. Start the detected local server and wait until the URL responds.
2. Write a project-specific Playwright script using real selectors and states.
3. Record at a stable viewport with `recordVideo`; use narration durations to
   pace `goto`, `click`, `fill`, and `wait` actions.
4. Close the browser and stop only the server process started for this run.

Example:

```js
const { chromium } = require("playwright");

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    recordVideo: { dir: "./recordings", size: { width: 1280, height: 720 } }
  });
  const page = await context.newPage();
  await page.goto("http://localhost:3000", { waitUntil: "networkidle" });
  await page.getByRole("button", { name: "Start" }).click();
  await page.waitForTimeout(3000);
  await context.close();
  await browser.close();
})();
```

### 6. Assemble and verify

Concatenate narration and merge it with the walkthrough:

```bash
ffmpeg -y -f concat -safe 0 -i list.txt -c copy demo_narration.mp3
ffmpeg -y -i demo_walkthrough.webm -i demo_narration.mp3 \
  -c:v libx264 -pix_fmt yuv420p -c:a aac demo_walkthrough_narrated.mp4
```

Render the Remotion composition:

```bash
npx remotion render src/index.ts MainComposition out/video.mp4
```

Never ship the first render blindly. After every meaningful render:

1. Use `ffprobe` to verify duration, frame rate, dimensions, streams, and audio.
2. Extract a contact sheet or representative frames with `ffmpeg`.
3. Inspect for clipping, unreadable text, awkward overlaps, broken UI states,
   dead time, audio drift, and style inconsistency.
4. Fix the highest-impact issue and re-render. Repeat until the acceptance
   checks pass.

### 7. Final acceptance checklist

- The story is understandable without hidden context.
- Every narrated claim matches the inspected product behavior.
- The first seconds establish a hook and the final seconds have a clear close.
- Motion is purposeful, staggered, readable, and consistent with the chosen style.
- Real UI recording and synthetic slides share the same palette and pacing.
- Video and audio durations align; no important action occurs during silence.
- The output path, source script, and any generated assets are reported clearly.
