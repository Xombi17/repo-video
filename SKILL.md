---
name: repovideo
description: Autonomous developer video producer skill to dynamically scan codebases, generate scripts, synthesize voiceovers, record UI flows via Playwright, and stitch them.
---

# 🎬 repovideo: Autonomous Developer Video Producer Skill

This skill turns any AI Agent into a professional developer video producer. Instead of running rigid, static templates, the agent dynamically inspects the codebase, writes custom interaction scripts, runs a local server, captures screen recordings, synthesizes voiceovers, and compiles them.

---

## 📋 The Master Workflow Sequence

When you are asked to generate a video for a project, execute these steps sequentially:

### 🛠️ STEP 1: CODEBASE RECONNAISSANCE & MAPPING
1. **Scan the directory**: Read files like `package.json`, `requirements.txt`, `cargo.toml`, `pyproject.toml`, or `docker-compose.yml` to understand the setup.
2. **Determine**:
   - What the application does (its core domain and user value).
   - The exact tech stack (e.g., Next.js, Django, FastAPI, React, PostgreSQL).
   - Startup commands to run the local server(s) (e.g., `npm run dev`, `uvicorn main:app`).
   - The local homepage URL (e.g., `http://localhost:3000`).
3. **Inspect Frontend Layouts**: Search for page components, routes, or HTML files to identify important interactive selectors (e.g., inputs, submit buttons, upload boxes).

---

### 📝 STEP 2: NARRATION SCRIPT WRITING (JSON FORMAT)
Create a `video_script.json` file in the workspace containing the voiceover layout. The script is split into:
1. **Slide Narration**: 4 paragraphs explaining the Tech Stack, Architecture, Data Flow, and Core Algorithms.
2. **Demo Narration**: 4–5 steps describing what is happening on screen during the live browser walkthrough.

#### Target JSON Schema (`video_script.json`):
```json
[
  { "id": "slide_1_intro", "text": "Welcome to our application demo...", "path": "public/vo_1.mp3" },
  { "id": "slide_2_arch", "text": "Built on top of React and FastAPI...", "path": "public/vo_2.mp3" },
  { "id": "slide_3_logic", "text": "Our data flow handles real-time calibration...", "path": "public/vo_3.mp3" },
  { "id": "demo_1_landing", "text": "Entering the dashboard, we see the primary workspace...", "path": "public/demo_1.mp3" },
  { "id": "demo_2_action", "text": "Let's enter some text and trigger the analyzer...", "path": "public/demo_2.mp3" }
]
```

---

### 🎙️ STEP 3: AUDIO SYNTHESIS
Synthesize the narration text segments into MP3 audio files using the `edge-tts` CLI tool.
Use a clean neural voice (e.g., `en-US-BrianNeural` or `en-US-AndrewNeural`).

#### Option A: Standard Synthesis (edge-tts)
```bash
edge-tts --text "Your narration text here" --voice en-US-BrianNeural --write-media public/vo_1.mp3
```

#### Option B: Cloned Voice Synthesis (OpenVoice)
If the user provides a speaker reference clip (e.g. `reference.wav`), first synthesize the base audio using Option A, and then clone the speaker tone color:
```bash
repovideo clone --source public/vo_1.mp3 --reference reference.wav --output public/vo_1_cloned.mp3 --checkpoints path_to_checkpoints
```
*Loop through all segments in `video_script.json` to generate their matching audio assets.*

---

### 🎨 STEP 4: GENERATING SLIDE GRAPHICS (REMOTION)
1. Initialize a clean, minimalistic Remotion project inside the workspace (or use a provided starter template).
2. Create 4 clean React slide components corresponding to your slide voiceovers (`vo_1` to `vo_3`).
3. Apply modern, premium styles (e.g., dark mode, Outfit/Inter typography, spring animations, mesh gradients) with centered layouts.
4. Set composition durations to match the exact duration of your synthesized voiceover audios.

---

### 📹 STEP 5: AUTOMATING THE BROWSER RECORDER (PLAYWRIGHT)
1. **Launch Server**: Start the application's dev server in the background (e.g., `npm run dev`) and wait for the port to respond.
2. **Write Recording Script**: Create a custom Playwright automation script `record_demo.js` tailored specifically to the project's actual HTML elements and classes.
3. **Pacing Sync**: Implement timed interactions in the script synced to your voiceover segment durations.
4. **Record Walkthrough**: Run the script headlessly to capture interactions into `demo_walkthrough.webm`.

#### Playwright Recording Skeleton (`record_demo.js`):
```javascript
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    recordVideo: { dir: './', size: { width: 1280, height: 720 } }
  });
  const page = await context.newPage();
  
  // Custom interaction steps (goto, click, type, wait)
  await page.goto('http://localhost:3000');
  await page.waitForTimeout(8000); // Sync with intro narration duration
  
  await context.close();
  await browser.close();
})();
```
5. **Clean Up**: Stop the background server process once recording finishes.

---

### 🎛️ STEP 6: AUDIO/VIDEO CONCAT & STITCH
1. Concatenate all walkthrough audio clips:
   ```bash
   ffmpeg -y -f concat -safe 0 -i list.txt -c copy demo_full_narration.mp3
   ```
2. Merge the combined walkthrough audio track with the browser video recording:
   ```bash
   ffmpeg -y -i demo_walkthrough.webm -i demo_full_narration.mp3 -c:v libx264 -pix_fmt yuv420p -c:a aac demo_walkthrough_narrated.mp4
   ```
3. Load `demo_walkthrough_narrated.mp4` into your Remotion composition timeline (sequenced right after the slide graphics intro), and render the final presentation video:
   ```bash
   npx remotion render src/index.ts MainComposition out/video.mp4
   ```
