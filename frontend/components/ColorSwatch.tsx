"use client";

import { useState, useRef } from "react";
import { ColorSwatchProps } from "@/lib/types";
import { copyToClipboard } from "@/lib/api-client";

export default function ColorSwatch({
  color,
  name,
  locked,
  index,
  onToggleLock,
  showAccessibility = false,
  accessibilityInfo,
}: ColorSwatchProps) {
  const [copied, setCopied] = useState(false);
  const swatchRef = useRef<HTMLDivElement>(null);

  const handleCopyColor = async () => {
    try {
      await copyToClipboard([color]);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error("Failed to copy color:", error);
    }
  };

  const handleToggleLock = (e: React.MouseEvent | React.KeyboardEvent) => {
    e.stopPropagation();
    onToggleLock(index);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'Enter':
      case ' ':
        e.preventDefault();
        handleCopyColor();
        break;
      case 'l':
      case 'L':
        e.preventDefault();
        handleToggleLock(e);
        break;
      case 'ArrowRight':
      case 'ArrowDown':
        e.preventDefault();
        focusNextSwatch();
        break;
      case 'ArrowLeft':
      case 'ArrowUp':
        e.preventDefault();
        focusPreviousSwatch();
        break;
    }
  };

  const focusNextSwatch = () => {
    const nextSwatch = document.querySelector(`[data-swatch-index="${index + 1}"]`) as HTMLElement;
    if (nextSwatch) {
      nextSwatch.focus();
    }
  };

  const focusPreviousSwatch = () => {
    const prevSwatch = document.querySelector(`[data-swatch-index="${index - 1}"]`) as HTMLElement;
    if (prevSwatch) {
      prevSwatch.focus();
    }
  };

  return (
    <div 
      className="color-swatch group relative focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded-xl"
      ref={swatchRef}
      tabIndex={0}
      data-swatch-index={index}
      data-testid={`color-swatch-${index}`}
      onKeyDown={handleKeyDown}
      role="button"
      aria-label={`Color ${color} ${name || 'Unnamed'}. ${locked ? 'Locked' : 'Unlocked'}. Press Enter to copy, L to toggle lock, arrow keys to navigate.`}
    >
      {/* Color Display */}
      <div
        className="w-full h-24 rounded-xl shadow-lg mb-3 border-2 border-white/50 cursor-pointer transition-all duration-300 hover:shadow-xl hover:scale-105 focus-within:ring-2 focus-within:ring-blue-500"
        style={{ backgroundColor: color }}
        onClick={handleCopyColor}
        title={`Click to copy ${color}`}
      >
        {/* Lock/Unlock Button */}
        <button
          onClick={handleToggleLock}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              handleToggleLock(e);
            }
          }}
          className={`absolute top-2 right-2 w-8 h-8 rounded-full shadow-md transition-all duration-300 hover:scale-110 focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            locked
              ? "bg-yellow-500 text-white"
              : "bg-white/80 text-gray-600 hover:bg-white"
          }`}
          title={locked ? "Click to unlock color (or press L)" : "Click to lock color (or press L)"}
          aria-label={locked ? "Unlock color" : "Lock color"}
        >
          {locked ? "🔒" : "🔓"}
        </button>

        {/* Copy Feedback */}
        {copied && (
          <div className="absolute inset-0 bg-black/50 rounded-xl flex items-center justify-center">
            <div className="bg-white text-black px-3 py-1 rounded-lg text-sm font-medium">
              Copied!
            </div>
          </div>
        )}
      </div>

      {/* Color Information */}
      <div className="text-center space-y-1">
        <p className="font-mono text-sm font-medium transition-colors" style={{ color: 'var(--foreground)' }}>
          {color}
        </p>
        <p className="text-xs capitalize" style={{ color: 'var(--secondary)' }}>
          {name || "Unnamed"}
        </p>

        {/* Accessibility Information */}
        {showAccessibility && accessibilityInfo && (
          <div className="text-xs space-y-1">
            <p style={{ color: 'var(--secondary)' }}>
              Contrast: {accessibilityInfo.contrastRatio.toFixed(2)}
            </p>
            <p
              className={`font-medium ${
                accessibilityInfo.wcagLevel === 'fail'
                  ? 'text-red-500'
                  : accessibilityInfo.wcagLevel === 'AAA'
                  ? 'text-green-500'
                  : 'text-yellow-500'
              }`}
            >
              WCAG {accessibilityInfo.wcagLevel}
            </p>
          </div>
        )}
      </div>

      {/* Locked Indicator */}
      {locked && (
        <div className="absolute -top-1 -left-1 w-4 h-4 bg-yellow-500 rounded-full flex items-center justify-center">
          <span className="text-white text-xs">🔒</span>
        </div>
      )}
    </div>
  );
}