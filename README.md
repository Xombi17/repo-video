# 🎬 repovideo: The AI Video Producer Skill

`repovideo` is an autonomous developer video producer designed for developers and AI coding assistants (like Antigravity, Claude Code, Gemini CLI, and Codex). 

With a single command, `repovideo` scans a local codebase, drafts a timed walkthrough script, synthesizes high-fidelity voice narration, performs automated browser recording using Playwright, and stitches the assets into a professional demo video complete with technical transition slides.

---

## 🛠️ How it Works under the Hood

```
[Target Codebase] ──> 1. Scan Codebase (analyze) ──> 2. Generate Voiceover Script
                                                              │
   ┌──────────────────────────────────────────────────────────┴─────────────────────┐
   ▼                                                                                ▼
3. Voice Synthesis (voice)                                           4. UI Recording (record)
   └───────────────┬────────────────────────────────────────────────────────────────┘
                   ▼
       5. Stitch Tracks (stitch) ──> 6. Technical Slides (Remotion) ──> [final_demo.mp4]
```

1. **Analyze**: Detects technologies, entry points, and script commands.
2. **Voice**: Synthesizes high-fidelity speech narration from text paragraphs using `edge-tts`.
3. **Record**: Plays back simulated browser walkthrough interactions (clicking, scrolling, typing) headlessly, synced to audio timings.
4. **Stitch**: Merges screen captures, background music, and audio narration into a unified video.
5. **Remotion**: Renders structured technical slide cards and transitions at the start of the video.

---

## 🚀 How to Publish & Distribute `repovideo`

Because this tool relies on **Python** (for audio synthesis and metadata analysis) and **Node.js** (for Playwright browser recording and Remotion rendering), publishing it as a **unified NPM Package** is the recommended method.

### Publish as a Global NPM Package
1. **Initialize npm**: Add a root `package.json` that bundles the Python scripts and lists `playwright` and `@remotion/cli` as dependencies.
2. **Executable Binary**: Define a `"bin"` key in `package.json` pointing to `bin/repovideo.py` (which runs via Python).
3. **Publish to Registry**:
   ```bash
   npm login
   npm publish --access public
   ```

---

## 💻 How a User in the World Will Use It

A random user who wants to generate a video for their project will follow these simple steps:

### 1. Installation
The user installs `repovideo` globally from npm:
```bash
npm install -g repovideo
```
*(This automatically installs Playwright browsers and sets up local execution scripts)*.

### 2. Auto-generate the Video with an AI Agent
If the user is using an AI coding assistant (like Antigravity or Claude Code) inside their project, they can simply type:
> *"Hey, use the `ai-video-generator` skill to create a 1-minute demo video of my landing page."*

The AI agent will:
1. Scan their code layout: `repovideo analyze .`
2. Spin up the user's dev server in the background (e.g. `npm run dev`).
3. Generate the script narration `voiceover.json` and synthesize the audio files.
4. Draft browser recording actions `actions.json` and record the UI demo.
5. Concat and stitch everything into a final high-definition MP4.

### 3. Manual Command Line Usage
Users can also run the stages manually using the CLI:

```bash
# Step 1: Scan target codebase
repovideo analyze .

# Step 2: Generate narration audio clips
repovideo voice --script-json voiceover.json --out-dir outputs/voiceovers

# Step 3: Record UI flow from actions file
repovideo record actions.json 1280 720 outputs/recordings

# Step 4: Stitch video and voiceover with background music
repovideo stitch --video outputs/recordings/recording_123.webm --audio-list-file list.txt --bg-music music.mp3 --output final.mp4
```

---

## 📁 Repository Structure
* **`bin/`**: Contains the main CLI wrapper entry point.
* **`scripts/`**: Core utilities:
  * `analyze.py`: Python codebase scanner.
  * `tts_generator.py`: edge-tts voiceover engine.
  * `record.js`: Playwright browser automation script.
  * `stitch.py`: FFmpeg stitcher and audio mixer.
* **`templates/`**: Boilerplate configurations for React-based Remotion slides.
* **`SKILL.md`**: Specification document for AI Agents to ingest this skill.
