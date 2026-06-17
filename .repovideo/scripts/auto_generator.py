#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.error
import subprocess
import time
from analyze import analyze_directory

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash:generateContent"

def call_gemini(prompt, api_key):
    url = f"{GEMINI_API_URL}?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            text_response = res_data["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(text_response)
    except urllib.error.HTTPError as e:
        print(f"Gemini API HTTP Error: {e.code} - {e.read().decode('utf-8')}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error calling Gemini: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is not set.", file=sys.stderr)
        print("Please set it: export GEMINI_API_KEY='your_key_here'", file=sys.stderr)
        sys.exit(1)

    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    target_dir = os.path.abspath(target_dir)

    print("Step 1: Analyzing codebase layout...")
    analysis = analyze_directory(target_dir)
    print("Detected Tech Stack:", analysis["detected_frameworks"])

    # Gather sample code files to provide context (e.g. main index files)
    sample_code = {}
    main_extensions = ('.js', '.jsx', '.ts', '.tsx', '.py')
    count = 0
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules", ".venv", "venv", "build", "dist"}]
        for file in files:
            if file.endswith(main_extensions) and count < 5:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, target_dir)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        # Grab first 100 lines for context
                        sample_code[rel_path] = "".join(f.readlines()[:100])
                    count += 1
                except Exception:
                    pass

    prompt = f"""
You are an AI video producer. Analyze the following project analysis summary and sample file contents to create an automated video walkthrough plan.

Project Analysis:
{json.dumps(analysis, indent=2)}

Sample Code File Contents:
{json.dumps(sample_code, indent=2)}

You need to output a JSON object containing two keys:
1. "voiceover": A list of list pairs `[ [text, audio_filename], ... ]` where text is the narration for that segment.
2. "actions": A list of browser automation actions to run via Playwright. Each action is an object with a "type". Supported types and parameters:
   - {{ "type": "goto", "url": "http://localhost:3000" }} (assumed port from analysis, change if frontend is different)
   - {{ "type": "click", "selector": "css_selector" }}
   - {{ "type": "type", "selector": "css_selector", "text": "value", "delay": 50 }}
   - {{ "type": "wait", "ms": 1000 }}
   - {{ "type": "scroll", "x": 0, "y": 250 }}
   - {{ "type": "hover", "selector": "css_selector" }}
   - {{ "type": "clear", "selector": "css_selector" }}

Match the durations of the visual browser interactions and "wait" ms values to the narration lengths (roughly 130 words per minute / 2 words per second). Keep the demo simple and under 60 seconds.

Return ONLY a JSON object with this schema:
{{
  "voiceover": [
    ["Welcome to our app demo...", "01_intro.mp3"],
    ["Clicking the launch button redirects us...", "02_redirect.mp3"]
  ],
  "actions": [
    {{ "type": "goto", "url": "http://localhost:3000" }},
    {{ "type": "wait", "ms": 8000 }},
    {{ "type": "click", "selector": "button" }}
  ]
}}
"""

    print("Step 2: Designing video script and recording actions via Gemini...")
    walkthrough_plan = call_gemini(prompt, api_key)
    
    voiceover_file = "voiceover.json"
    actions_file = "actions.json"
    
    with open(voiceover_file, "w") as f:
        json.dump(walkthrough_plan["voiceover"], f, indent=2)
    with open(actions_file, "w") as f:
        json.dump(walkthrough_plan["actions"], f, indent=2)
        
    print(f"Generated {voiceover_file} and {actions_file}.")

    # Step 3: Start server
    # We choose the main start command or ask the user to make sure the app server is already running.
    # To prevent port clashes, we warn the user to run their local server first, or we attempt to launch it.
    print("\n--- Next Steps (Automated execution starting) ---")
    print("Please make sure your local server is running on the target ports.")
    print("Step 3: Synthesizing neural audio narration clips...")
    
    # Run voice synthesis
    tts_script = os.path.join(os.path.dirname(__file__), "tts_generator.py")
    subprocess.run([sys.executable, tts_script, "--script-json", voiceover_file, "--out-dir", "demo_voiceovers"], check=True)

    # Step 4: Record Browser
    print("Step 4: Executing headless browser recording...")
    record_script = os.path.join(os.path.dirname(__file__), "record.js")
    subprocess.run(["node", record_script, actions_file, "1280", "720", "demo_recordings"], check=True)

    # Step 5: Stitch Video
    print("Step 5: Stitching video & audio together...")
    # Generate list.txt for stitcher
    list_file = "temp_list.txt"
    with open(list_file, "w") as f:
        for text, filename in walkthrough_plan["voiceover"]:
            f.write(f"demo_voiceovers/{filename}\n")

    # Find the newly created recording webm file
    recordings_dir = "demo_recordings"
    webm_files = [f for f in os.listdir(recordings_dir) if f.endswith(".webm")]
    if not webm_files:
        print("Error: No browser recording video was found.", file=sys.stderr)
        sys.exit(1)
    
    # Get the latest webm file
    webm_files.sort(key=lambda x: os.path.getmtime(os.path.join(recordings_dir, x)), reverse=True)
    latest_webm = os.path.join(recordings_dir, webm_files[0])

    stitch_script = os.path.join(os.path.dirname(__file__), "stitch.py")
    subprocess.run([
        sys.executable, stitch_script,
        "--video", latest_webm,
        "--audio-list-file", list_file,
        "--output", "final_walkthrough_demo.mp4"
    ], check=True)

    # Clean up temp files
    if os.path.exists(list_file):
        os.remove(list_file)
        
    print("\n🎉 Success! Your automated video demo has been generated: final_walkthrough_demo.mp4")

if __name__ == "__main__":
    main()
