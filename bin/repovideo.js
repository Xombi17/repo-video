#!/usr/bin/env node
const { spawn } = require('child_process');
const path = require('path');

const args = process.argv.slice(2);
const pythonScript = path.join(__dirname, 'repovideo.py');

const child = spawn('python3', [pythonScript, ...args], { stdio: 'inherit' });
child.on('close', (code) => {
  process.exit(code);
});
