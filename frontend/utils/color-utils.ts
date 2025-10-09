/**
 * Color utility functions for ChromaCraft MVP
 * Provides color conversion, validation, and accessibility calculations
 */

import { CONTRAST_RATIOS, WCAG_LEVELS } from '../lib/constants';
import { ColorInfo } from '../lib/types';

// Color conversion utilities
export interface RGB {
  r: number;
  g: number;
  b: number;
}

export interface HSL {
  h: number;
  s: number;
  l: number;
}

// Convert HEX to RGB
export function hexToRgb(hex: string): RGB | null {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null;
}

// Convert RGB to HEX
export function rgbToHex(r: number, g: number, b: number): string {
  const toHex = (n: number) => {
    const hex = Math.round(Math.max(0, Math.min(255, n))).toString(16);
    return hex.length === 1 ? '0' + hex : hex;
  };
  return `#${toHex(r)}${toHex(g)}${toHex(b)}`;
}

// Convert RGB to HSL
export function rgbToHsl(r: number, g: number, b: number): HSL {
  r /= 255;
  g /= 255;
  b /= 255;

  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  let h = 0;
  let s = 0;
  const l = (max + min) / 2;

  if (max !== min) {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);

    switch (max) {
      case r: h = (g - b) / d + (g < b ? 6 : 0); break;
      case g: h = (b - r) / d + 2; break;
      case b: h = (r - g) / d + 4; break;
    }
    h /= 6;
  }

  return {
    h: Math.round(h * 360),
    s: Math.round(s * 100),
    l: Math.round(l * 100)
  };
}

// Convert HSL to RGB
export function hslToRgb(h: number, s: number, l: number): RGB {
  h /= 360;
  s /= 100;
  l /= 100;

  const hue2rgb = (p: number, q: number, t: number) => {
    if (t < 0) t += 1;
    if (t > 1) t -= 1;
    if (t < 1/6) return p + (q - p) * 6 * t;
    if (t < 1/2) return q;
    if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
    return p;
  };

  let r, g, b;

  if (s === 0) {
    r = g = b = l; // achromatic
  } else {
    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;
    r = hue2rgb(p, q, h + 1/3);
    g = hue2rgb(p, q, h);
    b = hue2rgb(p, q, h - 1/3);
  }

  return {
    r: Math.round(r * 255),
    g: Math.round(g * 255),
    b: Math.round(b * 255)
  };
}

// Convert HEX to HSL
export function hexToHsl(hex: string): HSL | null {
  const rgb = hexToRgb(hex);
  return rgb ? rgbToHsl(rgb.r, rgb.g, rgb.b) : null;
}

// Convert HSL to HEX
export function hslToHex(h: number, s: number, l: number): string {
  const rgb = hslToRgb(h, s, l);
  return rgbToHex(rgb.r, rgb.g, rgb.b);
}

// Accessibility calculations
export function getLuminance(hex: string): number {
  const rgb = hexToRgb(hex);
  if (!rgb) return 0;

  const { r, g, b } = rgb;
  const [rs, gs, bs] = [r, g, b].map(c => {
    c = c / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });

  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
}

export function getContrastRatio(color1: string, color2: string): number {
  const lum1 = getLuminance(color1);
  const lum2 = getLuminance(color2);
  const brightest = Math.max(lum1, lum2);
  const darkest = Math.min(lum1, lum2);
  return (brightest + 0.05) / (darkest + 0.05);
}

export function getWCAGLevel(contrastRatio: number, isLargeText: boolean = false): NonNullable<ColorInfo['accessibility']>['wcagLevel'] {
  if (isLargeText) {
    if (contrastRatio >= CONTRAST_RATIOS.AAA_LARGE) return WCAG_LEVELS.AAA;
    if (contrastRatio >= CONTRAST_RATIOS.AA_LARGE) return WCAG_LEVELS.AA;
  } else {
    if (contrastRatio >= CONTRAST_RATIOS.AAA_NORMAL) return WCAG_LEVELS.AAA;
    if (contrastRatio >= CONTRAST_RATIOS.AA_NORMAL) return WCAG_LEVELS.AA;
  }
  return WCAG_LEVELS.FAIL;
}

// Color manipulation utilities
export function adjustBrightness(hex: string, amount: number): string {
  const hsl = hexToHsl(hex);
  if (!hsl) return hex;

  hsl.l = Math.max(0, Math.min(100, hsl.l + amount));
  return hslToHex(hsl.h, hsl.s, hsl.l);
}

export function adjustSaturation(hex: string, amount: number): string {
  const hsl = hexToHsl(hex);
  if (!hsl) return hex;

  hsl.s = Math.max(0, Math.min(100, hsl.s + amount));
  return hslToHex(hsl.h, hsl.s, hsl.l);
}

export function adjustHue(hex: string, amount: number): string {
  const hsl = hexToHsl(hex);
  if (!hsl) return hex;

  hsl.h = (hsl.h + amount + 360) % 360;
  return hslToHex(hsl.h, hsl.s, hsl.l);
}

// Color harmony calculations
export function getComplementaryColor(hex: string): string {
  return adjustHue(hex, 180);
}

export function getTriadicColors(hex: string): [string, string] {
  return [adjustHue(hex, 120), adjustHue(hex, 240)];
}

export function getAnalogousColors(hex: string): [string, string] {
  return [adjustHue(hex, 30), adjustHue(hex, -30)];
}

export function getSplitComplementaryColors(hex: string): [string, string] {
  return [adjustHue(hex, 150), adjustHue(hex, 210)];
}

// Color distance calculation (for similarity)
export function getColorDistance(hex1: string, hex2: string): number {
  const rgb1 = hexToRgb(hex1);
  const rgb2 = hexToRgb(hex2);
  
  if (!rgb1 || !rgb2) return Infinity;

  const rDiff = rgb1.r - rgb2.r;
  const gDiff = rgb1.g - rgb2.g;
  const bDiff = rgb1.b - rgb2.b;

  return Math.sqrt(rDiff * rDiff + gDiff * gDiff + bDiff * bDiff);
}

// Palette analysis utilities
export function analyzePaletteContrast(colors: string[]): Array<{
  color1: string;
  color2: string;
  ratio: number;
  wcagLevel: ColorInfo['accessibility']['wcagLevel'];
}> {
  const results = [];
  
  for (let i = 0; i < colors.length; i++) {
    for (let j = i + 1; j < colors.length; j++) {
      const ratio = getContrastRatio(colors[i], colors[j]);
      const wcagLevel = getWCAGLevel(ratio);
      
      results.push({
        color1: colors[i],
        color2: colors[j],
        ratio,
        wcagLevel
      });
    }
  }
  
  return results;
}

export function getPaletteDominantHue(colors: string[]): number {
  const hues = colors
    .map(color => hexToHsl(color))
    .filter(hsl => hsl !== null)
    .map(hsl => hsl!.h);

  if (hues.length === 0) return 0;

  // Calculate average hue (accounting for circular nature)
  const x = hues.reduce((sum, hue) => sum + Math.cos(hue * Math.PI / 180), 0) / hues.length;
  const y = hues.reduce((sum, hue) => sum + Math.sin(hue * Math.PI / 180), 0) / hues.length;
  
  let avgHue = Math.atan2(y, x) * 180 / Math.PI;
  if (avgHue < 0) avgHue += 360;
  
  return Math.round(avgHue);
}

// Validation utilities
export function isValidHexColor(hex: string): boolean {
  return /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/.test(hex);
}

export function normalizeHexColor(hex: string): string {
  if (!hex.startsWith('#')) {
    hex = '#' + hex;
  }
  
  // Convert 3-digit hex to 6-digit
  if (hex.length === 4) {
    hex = '#' + hex[1] + hex[1] + hex[2] + hex[2] + hex[3] + hex[3];
  }
  
  return hex.toUpperCase();
}

// Color name utilities (basic color names)
export function getBasicColorName(hex: string): string {
  const hsl = hexToHsl(hex);
  if (!hsl) return 'Unknown';

  const { h, s, l } = hsl;

  // Grayscale colors
  if (s < 10) {
    if (l < 20) return 'Black';
    if (l < 40) return 'Dark Gray';
    if (l < 60) return 'Gray';
    if (l < 80) return 'Light Gray';
    return 'White';
  }

  // Chromatic colors
  if (h < 15 || h >= 345) return 'Red';
  if (h < 45) return 'Orange';
  if (h < 75) return 'Yellow';
  if (h < 105) return 'Yellow Green';
  if (h < 135) return 'Green';
  if (h < 165) return 'Blue Green';
  if (h < 195) return 'Cyan';
  if (h < 225) return 'Blue';
  if (h < 255) return 'Blue Violet';
  if (h < 285) return 'Violet';
  if (h < 315) return 'Magenta';
  return 'Pink';
}