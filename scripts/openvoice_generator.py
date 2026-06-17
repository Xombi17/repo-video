#!/usr/bin/env python3
import os
import sys
import argparse

def clone_voice(source_audio, reference_audio, output_path, checkpoint_dir):
    try:
        import torch
        from openvoice import se_extractor
        from openvoice.api import ToneColorConverter
    except ImportError:
        print("Error: OpenVoice dependencies (torch, openvoice) are not installed.", file=sys.stderr)
        print("Please install them: pip install openvoice-cli torch", file=sys.stderr)
        sys.exit(1)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading OpenVoice on device: {device}...")
    
    if not os.path.exists(checkpoint_dir):
        print(f"Error: OpenVoice checkpoint directory '{checkpoint_dir}' does not exist.", file=sys.stderr)
        print("Please download the base checkpoints first.", file=sys.stderr)
        sys.exit(1)

    # Initialize Tone Color Converter
    config_path = os.path.join(checkpoint_dir, "config.json")
    checkpoint_path = os.path.join(checkpoint_dir, "checkpoint.pth")
    
    try:
        tone_color_converter = ToneColorConverter(config_path, device=device)
        tone_color_converter.load_checkpoint(protocol='v2', ckpt_path=checkpoint_path)
    except Exception as e:
        print(f"Error loading OpenVoice checkpoints: {e}", file=sys.stderr)
        sys.exit(1)

    # Extract source speaker tone color profile (using default config speakers)
    # OpenVoice requires a source tone color profile to map from.
    # We assume base speaker profile exists in checkpoint folder
    source_se_path = os.path.join(checkpoint_dir, "base_se.pth")
    if os.path.exists(source_se_path):
        source_se = torch.load(source_se_path, map_location=device)
    else:
        print(f"Warning: Base speaker SE not found at '{source_se_path}', attempting to extract from source audio...")
        try:
            source_se, _ = se_extractor.get_se(source_audio, tone_color_converter, target_dir='processed', vad=True)
        except Exception as e:
            print(f"Error extracting base speaker profile: {e}", file=sys.stderr)
            sys.exit(1)

    # Extract target tone color profile from reference audio clip
    print(f"Extracting voice profile from reference: {reference_audio}...")
    try:
        target_se, _ = se_extractor.get_se(reference_audio, tone_color_converter, target_dir='processed', vad=True)
    except Exception as e:
        print(f"Error extracting target voice profile: {e}", file=sys.stderr)
        sys.exit(1)

    # Convert voice tone
    print(f"Cloning voice profile and exporting to: {output_path}...")
    try:
        tone_color_converter.convert(
            model=None,
            src_path=source_audio,
            src_se=source_se,
            tgt_se=target_se,
            output_path=output_path
        )
        print("Voice cloning completed successfully!")
    except Exception as e:
        print(f"Error during voice tone conversion: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Clone voice tone color from a reference audio onto a source audio via OpenVoice.")
    parser.add_argument("--source", required=True, help="Input source audio file (e.g. base edge-tts audio).")
    parser.add_argument("--reference", required=True, help="Reference voice audio file to clone.")
    parser.add_argument("--output", required=True, help="Output target audio file path.")
    parser.add_argument("--checkpoints", default="checkpoints", help="Path to OpenVoice checkpoints directory.")
    
    args = parser.parse_args()
    
    clone_voice(args.source, args.reference, args.output, args.checkpoints)

if __name__ == "__main__":
    main()
