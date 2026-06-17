#!/usr/bin/env node
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function run() {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.log("Usage: node record.js <actions_json_file> [viewport_width] [viewport_height] [output_dir]");
    process.exit(1);
  }

  const actionsFile = args[0];
  const width = parseInt(args[1] || '1280');
  const height = parseInt(args[2] || '720');
  const outputDir = args[3] || './demo_recordings';

  if (!fs.existsSync(actionsFile)) {
    console.error(`Error: Action file ${actionsFile} does not exist.`);
    process.exit(1);
  }

  let actions;
  try {
    actions = JSON.parse(fs.readFileSync(actionsFile, 'utf8'));
  } catch (err) {
    console.error("Error parsing actions JSON:", err);
    process.exit(1);
  }

  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  console.log(`Launching headless browser with viewport ${width}x${height}...`);
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width, height },
    recordVideo: { dir: outputDir, size: { width, height } }
  });
  
  const page = await context.newPage();

  console.log(`Starting execution of ${actions.length} actions...`);
  try {
    for (let i = 0; i < actions.length; i++) {
      const action = actions[i];
      console.log(`[Action ${i + 1}/${actions.length}] Type: ${action.type}`, action);

      switch (action.type) {
        case 'goto':
          await page.goto(action.url);
          break;
        case 'click':
          await page.click(action.selector);
          break;
        case 'type':
          await page.type(action.selector, action.text, { delay: action.delay || 50 });
          break;
        case 'wait':
          await page.waitForTimeout(action.ms);
          break;
        case 'scroll':
          // Scroll dynamically using page.evaluate or mouse wheel
          await page.evaluate(({ x, y }) => window.scrollBy(x, y), { x: action.x || 0, y: action.y || 0 });
          break;
        case 'upload':
          await page.setInputFiles(action.selector, action.files);
          break;
        case 'hover':
          await page.hover(action.selector);
          break;
        case 'press':
          await page.keyboard.press(action.key);
          break;
        case 'clear':
          await page.locator(action.selector).focus();
          await page.keyboard.press('Control+A');
          await page.keyboard.press('Backspace');
          break;
        default:
          console.warn(`Warning: Unknown action type '${action.type}'`);
      }
    }
  } catch (err) {
    console.error("Error executing browser automation actions:", err);
  } finally {
    const video = page.video();
    await context.close();
    await browser.close();

    if (video) {
      const videoPath = await video.path();
      console.log(`Recording completed. Raw video saved to: ${videoPath}`);
      
      // Rename or link video if desired
      const destName = `recording_${Date.now()}.webm`;
      const destPath = path.join(outputDir, destName);
      fs.copyFileSync(videoPath, destPath);
      console.log(`Saved a copy to: ${destPath}`);
    } else {
      console.error("No video was captured by Playwright.");
    }
  }
}

run();
