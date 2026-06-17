# 🎬 repovideo

`repovideo` is an autonomous developer video producer CLI tool and AI agent skill. It automatically scans a codebase, drafts a timed walkthrough script, synthesizes high-fidelity voice narration, performs automated browser recording, and stitches the assets into a professional demo video complete with technical transition slides.

---

## 🛠️ How it Works

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

1. **Analyze**: Scans your project to understand technology stack, frameworks, local servers, and active ports.
2. **Voice**: Synthesizes clean narration from text using high-fidelity edge-tts voiceover actors.
3. **Record**: Launches headless Chromium (via Playwright) to run simulated browser actions synced to target narration lengths.
4. **Stitch**: Combines generated audio tracks, screen recordings, and optional background music using FFmpeg.
5. **Slides (Optional)**: Sequenced slide transitions in Remotion to give your video a polished, programmatic introduction.

---

## 🚀 Installation & Agent Skill Setup

You can install `repovideo` globally as a CLI or load it directly as a skill for your AI Coding Assistant (e.g. Claude Code, Copilot, Cursor, Windsurf, Gemini CLI, etc.):

### Option A: Install via the Skills Package Manager (Recommended)
Add `repovideo` directly as a capability to your AI coding agent environment using the agent skills CLI:
```bash
npx skills add Xombi17/repo-video
```

### Option B: Global NPM CLI Install
Install `repovideo` globally on your machine:
```bash
npm install -g repovideo
```

Then, initialize the AI agent skill configuration in your workspace directory or globally:
```bash
# Initialize locally for the current repository
npx repovideo init --local

# Initialize globally for all projects (installs in user home directory)
npx repovideo init --global
```
*This command automatically populates the required scripts and registers `SKILL.md` inside your agent configuration directories (supporting `.claude`, `.agents`, `.gemini`, `.planning`, `.cursorrules`, `.windsurfrules`, and `.github/copilot-instructions.md`).*

---

## 💻 How to Use

### Method A: Automated Run via AI Agents
If you are using an AI coding assistant in your project workspace, you can simply instruct the agent to run the video generation skill. The agent will read `SKILL.md` and handle all step executions automatically.

### Method B: Manual CLI Usage
You can execute each step manually using the CLI commands:

```bash
# Step 1: Scan target codebase
repovideo analyze .

# Step 2: Generate narration audio clips from script JSON
repovideo voice --script-json voiceover.json --out-dir output_voiceovers

# Step 3: Record UI walkthrough from actions JSON
repovideo record actions.json 1280 720 output_recordings

# Step 4: Stitch narration tracks, screen capture and background music
repovideo stitch \
  --video output_recordings/recording_123.webm \
  --audio-list-file list.txt \
  --bg-music ambient_loop.mp3 \
  --bg-volume 0.1 \
  --output final_demo.mp4
```

---

## 📁 Repository Structure
* **`bin/`**: Core CLI command wrapper entries.
* **`scripts/`**: Tool modules:
  * `analyze.py`: Python codebase scanner utility.
  * `tts_generator.py`: TTS narration audio synthesizer.
  * `record.js`: Playwright automated UI recording engine.
  * `stitch.py`: FFmpeg stitcher and audio ducking mixer.
* **`templates/`**: Boilerplate React/Remotion timeline configurations.
* **`SKILL.md`**: Specification document for AI Agents to ingest this skill.
