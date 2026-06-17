# AI Video Generator Skill

An autonomous, AI-driven developer video producer skill designed for AI coding assistants. This skill enables any AI agent to automatically scan a target codebase, draft technical scripts, synthesize high-fidelity neural voiceovers, record custom headless user interactions via Playwright, and stitch the components into a professional demo video.

---

## 💡 Brainstorming & Core Concepts

### 1. The Autonomous AI Video Producer Model
In standard video production, humans write scripts, record screen captures, record voiceovers, and edit them. 
This skill turns the **AI Agent** into the video producer:
- **Codebase Discovery**: The AI scans directory files (e.g., config packages, routes, dependencies) to instantly grasp the project's purpose and tech stack.
- **Narrative Writing**: The AI drafts a concise, time-coded presentation script (intro, key system mechanics, user actions, outro).
- **Automation Execution**: The AI compiles custom Playwright scripts to interact with the target web application and record the browser screen.
- **Seamless Merging**: FFmpeg merges the dynamic slideshows, narrated audios, and walkthrough clips into a unified 3-minute video.

### 2. Generalizing Beyond Single Projects
For this skill to run in *any* project folder globally, it implements modular components:
- **Codebase Analyzer (`analyze.py`)**: A parser script that detects technologies (FastAPI, React, Django, Next.js, etc.) and exposes package commands to run local servers.
- **TTS Synthesis Engine (`tts_generator.py`)**: Uses high-quality edge-tts APIs to generate custom audio files from the script text.
- **Dynamic Action Parser (`playwright_template.js`)**: A script skeleton that allows AI agents to easily inject application-specific test runs (clicks, fills, drops, page loads) and output video segments.
- **FFmpeg Stitcher (`stitch.py`)**: Merges slides, narration tracks, background loops, and browser recordings with millisecond sync.

---

## 🚀 Future Ideas & Expansion
- **Dynamic Slide Templates**: Integrate pre-built Tailwind and Canvas slide builders that AI agents can write to dynamically.
- **Audio Overlays**: Support background music library categories (e.g. ambient tech, corporate, upbeat) that loop and dip automatically during spoken sentences.
- **Cursor Highlight Visuals**: Automate cursor halo and click animations on screen recording captures to draw focus to user actions.
- **Voice Customization**: Support full localized language locales and pitch/rate adjustments directly via config overrides.
- **Cloud Renderer Pipeline**: Expose serverless renders (e.g. via GitHub Actions or Vercel) so developers can generate videos directly from pull requests.
