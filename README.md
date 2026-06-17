# 🎬 repovideo

[![npm version](https://img.shields.io/npm/v/repovideo.svg?style=flat-square)](https://www.npmjs.com/package/repovideo)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

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

## 🚀 Quick Start & Installation

### Option A: Install via the Skills Package Manager (Recommended)
Add `repovideo` directly as a capability to your AI coding agent environment using the agent skills CLI:
```bash
npx skills add Xombi17/repo-video
```

### Option B: Global NPM CLI Install
Install the CLI tool globally on your system:
```bash
npm install -g repovideo
```

Once installed globally, bootstrap the AI agent skill configuration inside your project repository or globally:
```bash
# Initialize locally for the current repository
repovideo init --local

# Initialize globally for all projects (installs in user home directory)
repovideo init --global
```
*This command automatically populates the required scripts and registers `SKILL.md` inside your agent configuration directories (supporting `.claude`, `.agents`, `.gemini`, `.planning`, `.cursorrules`, `.windsurfrules`, and `.github/copilot-instructions.md`).*

---

## 💻 Usage & Workflows

### Method A: Automated Run via AI Agents
If you are using an AI coding assistant (like Claude Code or Cursor) in your project workspace, you can simply instruct the agent to run the video generation skill:
> *"Hey, run the repovideo skill to generate a 1-minute walkthrough video of my application."*

The agent will read the configured skill instructions and handle all step executions automatically on the fly.

### Method B: Interactive CLI Wizard
Simply run the wrapper command to launch the terminal-based interactive GUI wizard:
```bash
repovideo
```
This will launch a prompt select menu to let you run the steps manually, initialize skills, or run the autonomous script generator.

---

## ⚙️ Manual Commands

If you prefer to run individual pipeline steps manually via terminal scripts:

| Command | Action | Arguments |
| :--- | :--- | :--- |
| `repovideo analyze` | Scan codebase setup | `[path_to_project]` (default: `.`) |
| `repovideo voice` | Generate speech files | `--script-json <path> --out-dir <output_dir>` |
| `repovideo record` | Record browser interactions | `<actions_json_file> [width] [height] [out_dir]` |
| `repovideo stitch` | Mix and stitch media | `--video <file> --audio-list-file <file> --output <file>` |
| `repovideo clone` | Tone voice cloning (OpenVoice) | `--source <file> --reference <file> --output <file>` |
| `repovideo auto` | Run full pipeline autonomously | `[path_to_project]` (requires `GEMINI_API_KEY`) |

---

## 📁 Repository Directory Structure

* **`bin/`**: Core CLI wrapper entry points.
* **`scripts/`**: Tool modules:
  * `analyze.py`: Python codebase scanner utility.
  * `tts_generator.py`: TTS narration audio synthesizer.
  * `openvoice_generator.py`: OpenVoice speaker tone color cloner.
  * `record.js`: Playwright automated UI recording engine.
  * `stitch.py`: FFmpeg stitcher and audio ducking mixer.
* **`templates/`**: Boilerplate React/Remotion timeline configurations.
* **`SKILL.md`**: Specification document for AI Agents to ingest this skill.
