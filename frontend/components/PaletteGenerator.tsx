"use client";

import { useState, useCallback } from "react";
import { ColorPalette, PaletteGeneratorState, RandomGenerationRequest } from "@/lib/types";
import { apiClient } from "@/lib/api-client";
import PaletteDisplay from "./PaletteDisplay";

interface PaletteGeneratorProps {
  onPaletteChange?: (palette: ColorPalette | null) => void;
  initialPalette?: ColorPalette | null;
}

export default function PaletteGenerator({
  onPaletteChange,
  initialPalette = null,
}: PaletteGeneratorProps) {
  const [state, setState] = useState<PaletteGeneratorState>({
    currentPalette: initialPalette,
    lockedColors: new Set<number>(),
    generationMethod: 'random',
    isLoading: false,
    error: null,
  });

  const updateState = useCallback((updates: Partial<PaletteGeneratorState>) => {
    setState(prev => {
      const newState = { ...prev, ...updates };
      if (updates.currentPalette !== undefined && onPaletteChange) {
        onPaletteChange(newState.currentPalette);
      }
      return newState;
    });
  }, [onPaletteChange]);

  const handleToggleLock = useCallback((index: number) => {
    setState(prev => {
      const newLockedColors = new Set(prev.lockedColors);
      if (newLockedColors.has(index)) {
        newLockedColors.delete(index);
      } else {
        newLockedColors.add(index);
      }
      return { ...prev, lockedColors: newLockedColors };
    });
  }, []);

  const generateRandomPalette = useCallback(async (harmonyType?: string) => {
    updateState({ isLoading: true, error: null, generationMethod: 'random' });

    try {
      // Prepare locked colors for the API request
      const lockedColors: string[] = [];
      if (state.currentPalette && state.lockedColors.size > 0) {
        state.lockedColors.forEach(index => {
          if (state.currentPalette!.colors[index]) {
            lockedColors.push(state.currentPalette!.colors[index]);
          }
        });
      }

      const request: RandomGenerationRequest = {
        lockedColors: lockedColors.length > 0 ? lockedColors : undefined,
        harmonyType: harmonyType as 'complementary' | 'triadic' | 'analogous' | 'monochromatic',
      };

      const response = await apiClient.generateRandomPalette(request);

      const newPalette: ColorPalette = {
        colors: response.colors,
        names: response.names,
        metadata: {
          generationMethod: 'random',
          timestamp: new Date().toISOString(),
          source: `${harmonyType || 'random'} harmony`,
        },
      };

      updateState({ 
        currentPalette: newPalette, 
        isLoading: false,
        error: null,
      });

    } catch (error) {
      console.error('Failed to generate random palette:', error);
      updateState({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : 'Failed to generate palette' 
      });
    }
  }, [state.currentPalette, state.lockedColors, updateState]);

  // Expose setPalette for external use (e.g., parent components)
  // const setPalette = useCallback((palette: ColorPalette) => {
  //   updateState({ 
  //     currentPalette: palette,
  //     lockedColors: new Set(), // Reset locked colors when setting new palette
  //     error: null,
  //   });
  // }, [updateState]);

  return (
    <div className="space-y-6">
      {/* Generation Controls */}
      <div className="card-gradient rounded-2xl p-8" role="region" aria-label="Palette generation controls">
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-3" style={{ color: 'var(--foreground)' }}>
          🎲 Generate Palette
        </h2>

        <div className="space-y-4">
          {/* Random Generation Buttons */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3" role="group" aria-label="Color harmony generation options">
            <button
              onClick={() => generateRandomPalette()}
              disabled={state.isLoading}
              className="px-4 py-3 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors duration-300 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2"
              aria-label="Generate random color palette"
            >
              🎲 Random
            </button>
            <button
              onClick={() => generateRandomPalette('complementary')}
              disabled={state.isLoading}
              className="px-4 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors duration-300 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              aria-label="Generate complementary color harmony palette"
            >
              🔄 Complementary
            </button>
            <button
              onClick={() => generateRandomPalette('triadic')}
              disabled={state.isLoading}
              className="px-4 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors duration-300 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
              aria-label="Generate triadic color harmony palette"
            >
              🔺 Triadic
            </button>
            <button
              onClick={() => generateRandomPalette('analogous')}
              disabled={state.isLoading}
              className="px-4 py-3 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors duration-300 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2"
              aria-label="Generate analogous color harmony palette"
            >
              🌈 Analogous
            </button>
          </div>

          {/* Loading State */}
          {state.isLoading && (
            <div className="flex items-center justify-center py-4" role="status" aria-live="polite">
              <div className="animate-spin w-6 h-6 border-2 border-purple-500 border-t-transparent rounded-full mr-3" aria-hidden="true"></div>
              <span style={{ color: 'var(--secondary)' }}>Generating palette...</span>
            </div>
          )}

          {/* Error State */}
          {state.error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg" role="alert" aria-live="assertive">
              <p className="font-medium">Generation Failed</p>
              <p className="text-sm">{state.error}</p>
            </div>
          )}

          {/* Locked Colors Info */}
          {state.lockedColors.size > 0 && (
            <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded-lg" role="status" aria-live="polite">
              <p className="text-sm">
                🔒 {state.lockedColors.size} color{state.lockedColors.size !== 1 ? 's' : ''} will remain locked during generation
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Palette Display */}
      {state.currentPalette && (
        <PaletteDisplay
          palette={state.currentPalette}
          lockedColors={state.lockedColors}
          onToggleLock={handleToggleLock}
          showAccessibility={false}
        />
      )}

      {/* Instructions */}
      {!state.currentPalette && (
        <div className="card-gradient rounded-2xl p-8 text-center">
          <div className="space-y-4">
            <div className="text-6xl">🎨</div>
            <h3 className="text-xl font-bold" style={{ color: 'var(--foreground)' }}>
              Generate Your First Palette
            </h3>
            <p style={{ color: 'var(--secondary)' }}>
              Choose a harmony type above to create a beautiful color palette
            </p>
          </div>
        </div>
      )}
    </div>
  );
}