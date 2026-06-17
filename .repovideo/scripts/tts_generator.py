#!/usr/bin/env python3
import asyncio
import os
import sys
import argparse
import json
import edge_tts

async def synthesize(text, voice, rate, pitch, output_path):
    # Format rate and pitch adjustments if specified (e.g. "+0%", "-10Hz")
    # edge-tts expects rate/pitch format like "+0%" or "-10%" or "+50Hz"
    # standard values: rate="+0%", pitch="+0Hz"
    
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(output_path)

async def main():
    parser = argparse.ArgumentParser(description="Generate neural audio files from text using edge-tts.")
    parser.add_argument("--text", help="Direct text input to synthesize.")
    parser.add_argument("--script-json", help="JSON file mapping texts to output filenames. format: [[text, filename], ...]")
    parser.add_argument("--voice", default="en-US-BrianNeural", help="Voice locale/actor name (default: en-US-BrianNeural).")
    parser.add_argument("--rate", default="+0%", help="Speech rate modification e.g. +10%% or -10%% (default: +0%%).")
    parser.add_argument("--pitch", default="+0Hz", help="Speech pitch modification e.g. +10Hz or -10Hz (default: +0Hz).")
    parser.add_argument("--out-dir", default="demo_voiceovers", help="Output directory for generated files.")
    parser.add_argument("--output", help="Output filename if using --text directly.")

    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    tasks = []
    if args.text:
        out_file = args.output if args.output else "output.mp3"
        out_path = os.path.join(args.out_dir, out_file)
        print(f"Synthesizing text to {out_path} using voice {args.voice}...")
        await synthesize(args.text, args.voice, args.rate, args.pitch, out_path)
    elif args.script_json:
        try:
            with open(args.script_json, 'r', encoding='utf-8') as f:
                entries = json.load(f)
            for item in entries:
                if isinstance(item, list) and len(item) >= 2:
                    text, filename = item[0], item[1]
                elif isinstance(item, dict):
                    text, filename = item.get("text"), item.get("filename")
                else:
                    continue
                
                out_path = os.path.join(args.out_dir, filename)
                print(f"Queueing synthesis: '{text[:30]}...' -> {out_path}")
                tasks.append(synthesize(text, args.voice, args.rate, args.pitch, out_path))
            
            if tasks:
                await asyncio.gather(*tasks)
                print("All synthesis tasks completed successfully.")
        except Exception as e:
            print(f"Error processing script JSON: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    asyncio.run(main())
