#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { spawn, execSync } = require('child_process');
const readline = require('readline');

const BASE_DIR = path.dirname(__dirname);
const SCRIPTS_DIR = path.join(BASE_DIR, "scripts");
const TEMPLATES_DIR = path.join(BASE_DIR, "templates");

// Helper to prompt user
function prompt(question) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.trim());
    });
  });
}

// Helper to copy directory recursively
function copyDirSync(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (let entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDirSync(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
      fs.chmodSync(destPath, 0o755); // make executable
    }
  }
}

// Function to initialize skill in current directory
function initializeSkill(targetDir = '.') {
  const absoluteTarget = path.resolve(targetDir);
  console.log(`\n⚙️  Initializing repovideo skill in: ${absoluteTarget}`);

  // Create .repovideo directory
  const repovideoDir = path.join(absoluteTarget, '.repovideo');
  
  try {
    // Copy scripts
    copyDirSync(SCRIPTS_DIR, path.join(repovideoDir, 'scripts'));
    
    // Copy templates
    copyDirSync(TEMPLATES_DIR, path.join(repovideoDir, 'templates'));
    
    // Copy SKILL.md to workspace root
    fs.copyFileSync(path.join(BASE_DIR, 'SKILL.md'), path.join(absoluteTarget, 'SKILL.md'));
    
    // Create local bin wrapper or links if needed
    console.log(`\n✅ Skill initialized successfully!`);
    console.log(`   - Created .repovideo/ directory with internal generator scripts.`);
    console.log(`   - Added SKILL.md to workspace root. Any AI agent opened in this directory can now run repovideo workflows!`);
  } catch (err) {
    console.error(`❌ Error initializing skill:`, err);
  }
}

// Interactive CLI Wizard
async function launchWizard() {
  console.clear();
  console.log("\x1b[35m%s\x1b[0m", "==================================================");
  console.log("\x1b[35m%s\x1b[0m", "     🎬 repovideo - AI Video Producer Wizard      ");
  console.log("\x1b[35m%s\x1b[0m", "==================================================");
  console.log("Welcome! Select one of the options below:\n");
  console.log("  [1] ⚙️  Initialize repovideo skill in current project");
  console.log("  [2] 🤖 Run fully autonomous AI generator (requires GEMINI_API_KEY)");
  console.log("  [3] 🔍 Scan codebase details (analyze)");
  console.log("  [4] 🎙️  Synthesize script voiceover (voice)");
  console.log("  [5] 📹 Record UI demo with Playwright (record)");
  console.log("  [6] 🎛️  Stitch clips and voiceover together (stitch)");
  console.log("  [7] 🚪 Exit");
  console.log("");

  const choice = await prompt("Enter choice (1-7): ");

  switch (choice) {
    case '1':
      initializeSkill();
      break;
    case '2':
      let apiKey = process.env.GEMINI_API_KEY;
      if (!apiKey) {
        apiKey = await prompt("Enter your GEMINI_API_KEY: ");
        if (apiKey) {
          process.env.GEMINI_API_KEY = apiKey;
        } else {
          console.log("Error: GEMINI_API_KEY is required for autonomous generation.");
          break;
        }
      }
      runScript("auto_generator.py");
      break;
    case '3':
      runScript("analyze.py", ['.']);
      break;
    case '4':
      const scriptJson = await prompt("Path to voiceover script JSON file (e.g. voiceover.json): ");
      if (scriptJson) {
        runScript("tts_generator.py", ["--script-json", scriptJson]);
      }
      break;
    case '5':
      const actionsJson = await prompt("Path to actions JSON file (e.g. actions.json): ");
      if (actionsJson) {
        runScript("record.js", [actionsJson]);
      }
      break;
    case '6':
      const video = await prompt("Path to raw recording video (e.g. demo.webm): ");
      const audioList = await prompt("Path to audio list text file: ");
      const out = await prompt("Output filename (default: final_demo.mp4): ") || "final_demo.mp4";
      if (video && audioList) {
        runScript("stitch.py", ["--video", video, "--audio-list-file", audioList, "--output", out]);
      }
      break;
    case '7':
      console.log("Goodbye!");
      process.exit(0);
      break;
    default:
      console.log("Invalid choice. Press Enter to return to menu...");
      await prompt("");
      launchWizard();
  }
}

function runScript(scriptName, args = []) {
  const scriptPath = path.join(SCRIPTS_DIR, scriptName);
  let proc;
  if (scriptName.endsWith('.py')) {
    proc = spawn('python3', [scriptPath, ...args], { stdio: 'inherit' });
  } else {
    proc = spawn('node', [scriptPath, ...args], { stdio: 'inherit' });
  }

  proc.on('close', (code) => {
    console.log(`\nProcess finished with exit code ${code}`);
  });
}

// Parse Command Line
const args = process.argv.slice(2);
if (args.length === 0) {
  launchWizard();
} else if (args[0] === 'init') {
  initializeSkill(args[1] || '.');
} else {
  // Direct CLI command routing
  const cmd = args[0];
  const cmdArgs = args.slice(1);
  if (cmd === 'analyze') {
    runScript("analyze.py", cmdArgs);
  } else if (cmd === 'voice') {
    runScript("tts_generator.py", cmdArgs);
  } else if (cmd === 'record') {
    runScript("record.js", cmdArgs);
  } else if (cmd === 'stitch') {
    runScript("stitch.py", cmdArgs);
  } else if (cmd === 'auto') {
    runScript("auto_generator.py", cmdArgs);
  } else {
    console.log(`Unknown command: ${cmd}`);
    console.log("Usage: npx repovideo [init | analyze | voice | record | stitch | auto]");
  }
}
