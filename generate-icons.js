#!/usr/bin/env node
// generate-icons.js — run with: node generate-icons.js
// Requires: npm install canvas

const { createCanvas } = require('canvas');
const fs = require('fs');
const path = require('path');

function generateShopifyIcon(size) {
  const canvas = createCanvas(size, size);
  const ctx = canvas.getContext('2d');

  // Background: Shopify green
  ctx.fillStyle = '#95bf47';
  const r = size * 0.18;
  ctx.beginPath();
  ctx.moveTo(r, 0);
  ctx.lineTo(size - r, 0);
  ctx.quadraticCurveTo(size, 0, size, r);
  ctx.lineTo(size, size - r);
  ctx.quadraticCurveTo(size, size, size - r, size);
  ctx.lineTo(r, size);
  ctx.quadraticCurveTo(0, size, 0, size - r);
  ctx.lineTo(0, r);
  ctx.quadraticCurveTo(0, 0, r, 0);
  ctx.closePath();
  ctx.fill();

  // Shopify "S" bag icon in white
  const cx = size / 2;
  const cy = size / 2;
  const scale = size / 100;

  ctx.fillStyle = 'rgba(255,255,255,0.95)';
  ctx.save();
  ctx.translate(cx, cy);
  ctx.scale(scale, scale);

  // Bag body
  ctx.beginPath();
  ctx.roundRect(-22, -8, 44, 30, 4);
  ctx.fill();

  // Bag handle
  ctx.fillStyle = '#95bf47';
  ctx.beginPath();
  ctx.arc(0, -14, 12, Math.PI, 0);
  ctx.fill();

  ctx.fillStyle = 'rgba(255,255,255,0.95)';
  ctx.beginPath();
  ctx.arc(0, -14, 7, Math.PI, 0);
  ctx.fill();

  // Dollar/order symbol
  ctx.fillStyle = '#95bf47';
  ctx.font = `bold ${14}px sans-serif`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('S', 0, 8);

  ctx.restore();

  return canvas.toBuffer('image/png');
}

const outDir = path.join(__dirname, 'public', 'icons');
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

[192, 512].forEach(size => {
  const buf = generateShopifyIcon(size);
  const outPath = path.join(outDir, `icon-${size}.png`);
  fs.writeFileSync(outPath, buf);
  console.log(`Generated: ${outPath}`);
});

console.log('Done!');
