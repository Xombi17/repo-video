---
name: ai-video-generator
description: Autonomous developer video producer skill to scan codebases, generate scripts, synthesize voiceovers, record UI flows via Playwright, and stitch them.
---

# AI Video Generator Skill

This skill allows an AI Agent to autonomously scan a codebase and generate a high-fidelity narrated video walkthrough of the application.

## 📋 Recommended Workflow

### 1. Codebase Discovery
Run the analyzer tool on the workspace root to understand the framework, run scripts, and local endpoints:
```bash
python3 scripts/analyze.py .
```

### 2. Scripting & Timeline Planning
Draft a structured sequence of slides and application demo phases. Create a timed script. For the demo recordings, draft a JSON file containing simulated actions mapped to the speech duration.

#### Example Actions JSON (`actions.json`):
```json
[
  { "type": "goto", "url": "http://localhost:3000" },
  { "type": "wait", "ms": 5000 },
  { "type": "click", "selector": "button#analyzer-start" },
  { "type": "type", "selector": "textarea", "text": "This product is amazing!", "delay": 50 },
  { "type": "click", "selector": "button[type='submit']" },
  { "type": "wait", "ms": 8000 }
]
```

#### Example Voiceover JSON (`voiceover.json`):
```json
[
  ["Welcome to the demo. Today we will explore our application's dashboard.", "01_intro.mp3"],
  ["Let's input a review and click analyze to see aspect classification in action.", "02_interaction.mp3"]
]
```

### 3. Generate Audio Narrations
Run the voice synthesizer using edge-tts:
```bash
python3 scripts/tts_generator.py --script-json voiceover.json --out-dir demo_voiceovers
```

### 4. Headless UI Interaction Recording
First, launch the local development server in the background (detected in the Discovery phase). Once running, execute the recording tool:
```bash
node scripts/record.js actions.json 1280 720 ./demo_recordings
```

### 5. Media Assembly & Stitching
Combine all components into a final production-ready demo video:
```bash
python3 scripts/stitch.py \
  --video demo_recordings/recording_XXXXX.webm \
  --audio-list-file list.txt \
  --output final_demo.mp4
```
*(Optionally provide `--bg-music <path>` and `--bg-volume 0.1` to mix in ambient background audio)*
