"use client";

import { useRef } from "react";
import { PaletteDisplayProps } from "@/lib/types";
import ColorSwatch from "./ColorSwatch";

export default function PaletteDisplay({
  palette,
  lockedColors,
  onToggleLock,
  showAccessibility = false,
}: PaletteDisplayProps) {
  const paletteRef = useRef<HTMLDivElement>(null);

  if (!palette || !palette.colors || palette.colors.length === 0) {
    return null;
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    // Handle global palette keyboard shortcuts
    if (e.ctrlKey || e.metaKey) {
      switch (e.key) {
        case 'c':
          e.preventDefault();
          copyAllColors();
          break;
        case 'u':
          e.preventDefault();
          unlockAllColors();
          break;
      }
    }
  };

  const copyAllColors = async () => {
    try {
      const colorText = palette.colors.join('\n');
      await navigator.clipboard.writeText(colorText);
    } catch (error) {
      console.error('Failed to copy colors:', error);
    }
  };

  const unlockAllColors = () => {
    palette.colors.forEach((_, index) => {
      if (lockedColors.has(index)) {
        onToggleLock(index);
      }
    });
  };

  return (
    <div 
      className="card-gradient rounded-2xl p-8 focus-within:ring-2 focus-within:ring-blue-500"
      ref={paletteRef}
      onKeyDown={handleKeyDown}
      role="region"
      aria-label={`Color palette with ${palette.colors.length} colors, ${lockedColors.size} locked`}
    >
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-2" style={{ color: 'var(--foreground)' }}>
          🎨 Color Palette
        </h2>
        <p style={{ color: 'var(--secondary)' }}>
          Generated via {palette.metadata.generationMethod} • {palette.colors.length} colors
        </p>
        {lockedColors.size > 0 && (
          <p className="text-sm mt-1" style={{ color: 'var(--secondary)' }}>
            🔒 {lockedColors.size} color{lockedColors.size !== 1 ? 's' : ''} locked
          </p>
        )}
        <div className="text-xs mt-2 opacity-75" style={{ color: 'var(--secondary)' }}>
          Keyboard shortcuts: Arrow keys to navigate, Enter/Space to copy, L to lock/unlock, Ctrl+C to copy all, Ctrl+U to unlock all
        </div>
      </div>
      
      <div 
        className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4"
        role="grid"
        aria-label="Color swatches"
      >
        {palette.colors.map((color, index) => (
          <div key={`${color}-${index}`} role="gridcell">
            <ColorSwatch
              color={color}
              name={palette.names[index]}
              locked={lockedColors.has(index)}
              index={index}
              onToggleLock={onToggleLock}
              showAccessibility={showAccessibility}
            />
          </div>
        ))}
      </div>

      {/* Palette Actions */}
      <div className="mt-6 flex flex-wrap gap-3 justify-center" role="toolbar" aria-label="Palette actions">
        <button
          onClick={copyAllColors}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          aria-label="Copy all colors to clipboard (Ctrl+C)"
        >
          📋 Copy All Colors
        </button>
        
        {lockedColors.size > 0 && (
          <button
            onClick={unlockAllColors}
            className="px-4 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-offset-2"
            aria-label={`Unlock all ${lockedColors.size} locked colors (Ctrl+U)`}
          >
            🔓 Unlock All
          </button>
        )}
      </div>
    </div>
  );
}