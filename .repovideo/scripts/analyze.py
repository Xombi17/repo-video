#!/usr/bin/env python3
import os
import json
import sys

def analyze_directory(root_path):
    root_path = os.path.abspath(root_path)
    analysis = {
        "detected_languages": set(),
        "detected_frameworks": set(),
        "package_files": [],
        "run_commands": {},
        "entry_points": []
    }

    # Files/directories to ignore
    ignore_dirs = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", ".next", ".cache"}

    for root, dirs, files in os.walk(root_path):
        # Prune ignored directories in place
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, root_path)

            # Node.js
            if file == "package.json":
                analysis["package_files"].append(rel_path)
                analysis["detected_languages"].add("JavaScript/TypeScript")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Scripts
                        if "scripts" in data:
                            for name, cmd in data["scripts"].items():
                                analysis["run_commands"][f"npm run {name}"] = cmd
                        # Dependencies detection
                        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                        if "next" in deps:
                            analysis["detected_frameworks"].add("Next.js")
                        if "react" in deps:
                            analysis["detected_frameworks"].add("React")
                        if "vue" in deps:
                            analysis["detected_frameworks"].add("Vue")
                        if "svelte" in deps:
                            analysis["detected_frameworks"].add("Svelte")
                        if "angular" in deps or "@angular/core" in deps:
                            analysis["detected_frameworks"].add("Angular")
                        if "express" in deps:
                            analysis["detected_frameworks"].add("Express")
                        if "fastapi" in deps:
                            analysis["detected_frameworks"].add("FastAPI")
                except Exception as e:
                    pass

            # Python
            elif file in ["requirements.txt", "Pipfile", "poetry.lock", "pyproject.toml"]:
                analysis["package_files"].append(rel_path)
                analysis["detected_languages"].add("Python")
                if file == "pyproject.toml":
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if "poetry" in content:
                                analysis["detected_frameworks"].add("Poetry")
                    except Exception:
                        pass
            elif file == "manage.py":
                analysis["detected_languages"].add("Python")
                analysis["detected_frameworks"].add("Django")
                analysis["run_commands"]["python manage.py runserver"] = "Start Django server"
            elif file in ["main.py", "app.py"]:
                analysis["detected_languages"].add("Python")
                # Look for fastapi/flask indicators inside
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if "FastAPI" in content:
                            analysis["detected_frameworks"].add("FastAPI")
                            analysis["run_commands"]["uvicorn main:app --reload"] = "Start FastAPI server (assumed)"
                        if "Flask" in content:
                            analysis["detected_frameworks"].add("Flask")
                            analysis["run_commands"]["flask run"] = "Start Flask server"
                except Exception:
                    pass

            # Go
            elif file == "go.mod":
                analysis["package_files"].append(rel_path)
                analysis["detected_languages"].add("Go")

            # Rust
            elif file == "Cargo.toml":
                analysis["package_files"].append(rel_path)
                analysis["detected_languages"].add("Rust")

            # Docker
            elif file in ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"]:
                analysis["package_files"].append(rel_path)
                analysis["detected_frameworks"].add("Docker")

    # Clean up set to list for JSON serialization
    analysis["detected_languages"] = list(analysis["detected_languages"])
    analysis["detected_frameworks"] = list(analysis["detected_frameworks"])

    return analysis

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    result = analyze_directory(target)
    print(json.dumps(result, indent=2))
