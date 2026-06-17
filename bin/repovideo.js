#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');
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

// Function to initialize skill (locally or globally)
function initializeSkill(targetDir = '.', isGlobal = false) {
  const absoluteTarget = path.resolve(targetDir);
  const baseFolder = isGlobal ? os.homedir() : absoluteTarget;
  
  console.log(`\n⚙️  Initializing repovideo skill ${isGlobal ? 'GLOBALLY' : 'LOCALLY'} in: ${baseFolder}`);

  // Create .repovideo directory in the target base (either project root or user home directory)
  const repovideoDir = path.join(baseFolder, '.repovideo');
  
  try {
    // Copy scripts
    copyDirSync(SCRIPTS_DIR, path.join(repovideoDir, 'scripts'));
    
    // Copy templates
    copyDirSync(TEMPLATES_DIR, path.join(repovideoDir, 'templates'));
    
    // Pre-install Remotion boilerplate dependencies
    const boilerplatePath = path.join(repovideoDir, 'templates', 'remotion-boilerplate');
    if (fs.existsSync(boilerplatePath)) {
      console.log(`📦  Installing Remotion dependencies inside boilerplate...`);
      try {
        execSync('npm install --no-audit --no-fund', { cwd: boilerplatePath, stdio: 'inherit' });
        console.log(`✅  Remotion dependencies installed successfully!`);
      } catch (err) {
        console.warn(`⚠️  Warning: Could not automatically run 'npm install' inside boilerplate: ${err.message}`);
      }
    }

    // Define target paths for SKILL.md copy to be picked up by various agents
    const skillDestinations = [
      path.join(baseFolder, '.claude', 'skills', 'repovideo', 'SKILL.md'),
      path.join(baseFolder, '.agents', 'skills', 'repovideo', 'SKILL.md'),
      path.join(baseFolder, '.gemini', 'config', 'skills', 'repovideo', 'SKILL.md'),
      path.join(baseFolder, '.planning', 'skills', 'repovideo', 'SKILL.md')
    ];

    const sourceSkill = path.join(BASE_DIR, 'SKILL.md');
    let skillAdded = false;

    for (const dest of skillDestinations) {
      try {
        fs.mkdirSync(path.dirname(dest), { recursive: true });
        fs.copyFileSync(sourceSkill, dest);
        console.log(`   - Saved skill configuration to: ${path.relative(baseFolder, dest)}`);
        skillAdded = true;
      } catch (e) {
        // Suppress errors if a specific directory cannot be created
      }
    }

    // Define target rule files for Cursor, Windsurf, and GitHub Copilot
    const ruleFiles = [
      path.join(baseFolder, '.cursorrules'),
      path.join(baseFolder, '.windsurfrules'),
      path.join(baseFolder, '.github', 'copilot-instructions.md')
    ];

    const skillContent = fs.readFileSync(sourceSkill, 'utf8');

    for (const ruleFile of ruleFiles) {
      try {
        fs.mkdirSync(path.dirname(ruleFile), { recursive: true });
        if (fs.existsSync(ruleFile)) {
          const existing = fs.readFileSync(ruleFile, 'utf8');
          if (!existing.includes('repovideo')) {
            fs.appendFileSync(ruleFile, `\n\n${skillContent}`);
            console.log(`   - Appended skill instructions to: ${path.relative(baseFolder, ruleFile)}`);
            skillAdded = true;
          }
        } else {
          fs.writeFileSync(ruleFile, skillContent);
          console.log(`   - Created rules file with skill instructions: ${path.relative(baseFolder, ruleFile)}`);
          skillAdded = true;
        }
      } catch (e) {
        // Suppress errors
      }
    }
    
    console.log(`\n✅ Skill initialized successfully!`);
    console.log(`   - Created ${isGlobal ? '~' : ''}/.repovideo/ directory with internal generator scripts.`);
    if (skillAdded) {
      console.log(`   - Configured SKILL.md in agent directories (${isGlobal ? 'global' : 'local'} .claude, .agents, .gemini, .planning).`);
      console.log(`   - Any AI agent opened in this directory can now run repovideo workflows!`);
    } else {
      console.log(`   - Note: Could not write SKILL.md. Please check folder permissions.`);
    }
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
      console.log("\nChoose Scope:");
      console.log("  [1] Local (only for this repository)");
      console.log("  [2] Global (for all projects via home directory)");
      const scopeChoice = await prompt("Select scope (1-2): ");
      initializeSkill('.', scopeChoice === '2');
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
  const isGlobal = args.includes('--global') || args.includes('-g');
  const cleanArgs = args.filter(a => a !== 'init' && a !== '--global' && a !== '-g' && a !== '--local' && a !== '-l');
  const target = cleanArgs[0] || '.';
  initializeSkill(target, isGlobal);
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
  } else if (cmd === 'clone') {
    runScript("openvoice_generator.py", cmdArgs);
  } else {
    console.log(`Unknown command: ${cmd}`);
    console.log("Usage: npx repovideo [init [--global | -g] | analyze | voice | record | stitch | auto | clone]");
  }
}
