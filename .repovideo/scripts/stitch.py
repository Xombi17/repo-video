#!/usr/bin/env python3
import argparse
import subprocess
import os
import sys

def run_command(command, description="Command"):
    print(f"Running {description}: {' '.join(command)}")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error executing {description}:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)
    return result.stdout

def concat_audios(audio_files, output_audio):
    """Concatenates a list of audio files using FFmpeg's concat filter or demuxer."""
    # Write list.txt for concat demuxer
    list_path = "temp_audio_list.txt"
    try:
        with open(list_path, "w", encoding="utf-8") as f:
            for file in audio_files:
                # Ensure path is absolute or escaped properly
                f.write(f"file '{os.path.abspath(file)}'\n")
        
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", list_path,
            "-c", "copy",
            output_audio
        ]
        run_command(cmd, "Audio Concatenation")
    finally:
        if os.path.exists(list_path):
            os.remove(list_path)

def merge_video_audio(video_in, audio_in, output_video, bg_music=None, bg_volume=0.15):
    """Merges a video and an audio track, with optional background music mixing."""
    if not bg_music:
        # Simple merge
        cmd = [
            "ffmpeg", "-y",
            "-i", video_in,
            "-i", audio_in,
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "128k",
            "-map", "0:v:0",
            "-map", "1:a:0",
            output_video
        ]
        run_command(cmd, "Merging Video & Audio")
    else:
        # Complex filter to mix voiceover with background music (ducking)
        # We loop the background music and trim it to match the main audio/video duration
        cmd = [
            "ffmpeg", "-y",
            "-i", video_in,
            "-i", audio_in,
            "-stream_loop", "-1", "-i", bg_music,
            "-filter_complex",
            f"[1:a]volume=1.0[voice]; [2:a]volume={bg_volume}[bg]; [voice][bg]amix=inputs=2:duration=first[a]",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "128k",
            "-map", "0:v:0",
            "-map", "[a]",
            output_video
        ]
        run_command(cmd, "Merging Video & Voiceover with Background Music")

def main():
    parser = argparse.ArgumentParser(description="Stitch and merge video/audio tracks using FFmpeg.")
    parser.add_argument("--video", required=True, help="Input video track (e.g. Playwright raw recording WebM).")
    parser.add_argument("--audios", nargs="+", help="List of narration audio files to concatenate.")
    parser.add_argument("--audio-list-file", help="File containing list of audio paths, one per line.")
    parser.add_argument("--bg-music", help="Background music audio file to loop/mix in.")
    parser.add_argument("--bg-volume", type=float, default=0.15, help="Background music volume multiplier (default: 0.15).")
    parser.add_argument("--output", default="output_stitched.mp4", help="Final output video path.")
    
    args = parser.parse_args()

    # Determine audio inputs
    audio_files = []
    if args.audios:
        audio_files = args.audios
    elif args.audio_list_file:
        with open(args.audio_list_file, "r", encoding="utf-8") as f:
            audio_files = [line.strip() for line in f if line.strip()]
    
    if not audio_files:
        print("Error: No narration audio inputs specified.", file=sys.stderr)
        sys.exit(1)

    # Temporary concatenated voiceover file
    temp_voiceover = "temp_voiceover.mp3"
    try:
        print(f"Concatenating {len(audio_files)} voiceover clips...")
        concat_audios(audio_files, temp_voiceover)
        
        print("Merging video and voiceover track...")
        merge_video_audio(args.video, temp_voiceover, args.output, args.bg_music, args.bg_volume)
        print(f"Stitching completed successfully! Output file: {args.output}")
    finally:
        if os.path.exists(temp_voiceover):
            os.remove(temp_voiceover)

if __name__ == "__main__":
    main()
