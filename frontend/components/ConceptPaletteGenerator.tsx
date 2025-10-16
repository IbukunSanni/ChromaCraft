"use client";

import { useState } from "react";
import { apiClient } from "@/lib/api-client";
import { ConceptGenerationRequest, ConceptGenerationResponse, ColorPalette } from "@/lib/types";

interface ConceptPaletteGeneratorProps {
  onPaletteGenerated?: (palette: ColorPalette) => void;
  className?: string;
}

const MAX_CONCEPT_LENGTH = 200;

const EXAMPLE_CONCEPTS = [
  "sunset over the ocean",
  "cozy autumn cabin",
  "neon cyberpunk city", 
  "spring cherry blossoms",
  "desert sunrise",
  "tropical paradise",
  "winter wonderland",
  "vintage coffee shop",
  "mystical forest",
  "modern minimalist",
];

export default function ConceptPaletteGenerator({ 
  onPaletteGenerated, 
  className = "" 
}: ConceptPaletteGeneratorProps) {
  const [concept, setConcept] = useState("");
  const [colorCount, setColorCount] = useState(5);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastGenerated, setLastGenerated] = useState<ColorPalette | null>(null);
  const [characterCount, setCharacterCount] = useState(0);

  const handleConceptChange = (value: string) => {
    setConcept(value);
    setCharacterCount(value.length);
    
    // Clear error if user starts typing within limit
    if (value.length <= MAX_CONCEPT_LENGTH && error?.includes("character")) {
      setError(null);
    }
  };

  const generatePalette = async () => {
    const trimmedConcept = concept.trim();
    
    // Validation
    if (!trimmedConcept) {
      setError("Please describe a concept for your palette");
      return;
    }
    
    if (trimmedConcept.length > MAX_CONCEPT_LENGTH) {
      setError(`Concept must be ${MAX_CONCEPT_LENGTH} characters or less`);
      return;
    }

    setIsGenerating(true);
    setError(null);

    try {
      const request: ConceptGenerationRequest = {
        concept: trimmedConcept,
        color_count: colorCount,
      };

      const response: ConceptGenerationResponse = await apiClient.generateConceptPalette(request);

      // Convert to ColorPalette format
      const colorPalette: ColorPalette = {
        colors: response.colors,
        names: response.names,
        metadata: {
          generationMethod: 'concept',
          timestamp: new Date().toISOString(),
          source: `AI Concept: "${response.concept || trimmedConcept}"`,
        },
      };

      setLastGenerated(colorPalette);
      onPaletteGenerated?.(colorPalette);

    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : "Failed to generate palette. Please try again.";
      setError(errorMessage);
      console.error("Concept generation error:", err);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleExampleClick = (exampleConcept: string) => {
    setConcept(exampleConcept);
    setCharacterCount(exampleConcept.length);
    setError(null);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      generatePalette();
    }
  };

  const isOverLimit = characterCount > MAX_CONCEPT_LENGTH;
  const isNearLimit = characterCount > MAX_CONCEPT_LENGTH * 0.8;

  const ColorPreview = ({ palette }: { palette: ColorPalette }) => (
    <div className="mt-6 p-6 card-gradient rounded-2xl">
      <div className="mb-4">
        <h3 className="text-lg font-semibold" style={{ color: 'var(--foreground)' }}>
          ✨ Generated Palette
        </h3>
        <p className="text-sm" style={{ color: 'var(--secondary)' }}>
          From concept: &ldquo;{concept}&rdquo;
        </p>
      </div>
      
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
        {palette.colors.map((color, index) => (
          <div
            key={index}
            className="group cursor-pointer transform hover:scale-105 transition-transform"
            onClick={() => navigator.clipboard.writeText(color)}
            title={`Click to copy ${color}`}
          >
            <div
              className="w-full h-16 rounded-lg border-2 border-white/50 shadow-lg mb-2"
              style={{ backgroundColor: color }}
            />
            <div className="text-center space-y-1">
              <p className="font-mono text-xs font-medium" style={{ color: 'var(--foreground)' }}>
                {color}
              </p>
              <p className="text-xs capitalize" style={{ color: 'var(--secondary)' }}>
                {palette.names[index] || "Color"}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className={`card-gradient rounded-2xl p-8 ${className}`}>
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-2" style={{ color: 'var(--foreground)' }}>
          🤖 AI Concept Palette Generator
        </h2>
        <p style={{ color: 'var(--secondary)' }}>
          Describe a concept, scene, or idea and let AI create a beautiful color palette
        </p>
      </div>

      {/* Concept Input */}
      <div className="space-y-4">
        <div>
          <div className="flex justify-between items-center mb-2">
            <label className="block text-sm font-medium" style={{ color: 'var(--foreground)' }}>
              Describe your concept
            </label>
            <span 
              className={`text-xs ${
                isOverLimit ? 'text-red-500' : 
                isNearLimit ? 'text-orange-500' : 
                'text-gray-500'
              }`}
            >
              {characterCount}/{MAX_CONCEPT_LENGTH}
            </span>
          </div>
          <textarea
            value={concept}
            onChange={(e) => handleConceptChange(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="e.g., sunset over the ocean, cozy autumn cabin, neon cyberpunk city..."
            className={`w-full px-4 py-3 rounded-xl border transition-all duration-200 resize-none
                     ${isOverLimit 
                       ? 'border-red-500 bg-red-50 dark:bg-red-900/10' 
                       : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800'
                     }
                     text-gray-900 dark:text-gray-100
                     focus:ring-2 focus:ring-blue-500 focus:border-transparent
                     disabled:opacity-50 disabled:cursor-not-allowed`}
            rows={3}
            disabled={isGenerating}
            maxLength={MAX_CONCEPT_LENGTH + 50} // Allow slight overflow for UX
          />
          {isOverLimit && (
            <p className="text-xs text-red-500 mt-1">
              Concept is too long. Please shorten by {characterCount - MAX_CONCEPT_LENGTH} characters.
            </p>
          )}
        </div>

        {/* Color Count Selector */}
        <div className="flex items-center gap-4">
          <label className="text-sm font-medium" style={{ color: 'var(--foreground)' }}>
            Colors:
          </label>
          <select
            value={colorCount}
            onChange={(e) => setColorCount(Number(e.target.value))}
            className="px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 
                     bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100
                     focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isGenerating}
          >
            <option value={3}>3 colors</option>
            <option value={4}>4 colors</option>
            <option value={5}>5 colors</option>
            <option value={6}>6 colors</option>
            <option value={8}>8 colors</option>
          </select>
        </div>

        {/* Example Concepts */}
        <div>
          <p className="text-sm font-medium mb-2" style={{ color: 'var(--foreground)' }}>
            Need inspiration? Try these concepts:
          </p>
          <div className="flex flex-wrap gap-2">
            {EXAMPLE_CONCEPTS.map((example, index) => (
              <button
                key={index}
                onClick={() => handleExampleClick(example)}
                className="px-3 py-1 text-sm rounded-full border border-gray-300 dark:border-gray-600
                         hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors
                         disabled:opacity-50 disabled:cursor-not-allowed"
                style={{ color: 'var(--secondary)' }}
                disabled={isGenerating}
              >
                {example}
              </button>
            ))}
          </div>
        </div>

        {/* Generate Button */}
        <button
          onClick={generatePalette}
          disabled={isGenerating || !concept.trim() || isOverLimit}
          className="w-full px-6 py-4 text-white font-bold text-lg rounded-xl shadow-lg 
                   hover:shadow-xl transform hover:scale-105 transition-all duration-300 
                   disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
          style={{ background: `linear-gradient(to right, var(--primary), var(--accent))` }}
        >
          {isGenerating ? (
            <span className="flex items-center justify-center gap-3">
              <div className="animate-spin w-5 h-5 border-2 border-white border-t-transparent rounded-full"></div>
              Generating Palette...
            </span>
          ) : (
            <span className="flex items-center justify-center gap-3">
              ✨ Generate AI Palette
            </span>
          )}
        </button>

        {/* Error Display */}
        {error && (
          <div className="p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800">
            <p className="text-red-600 dark:text-red-400 text-sm">
              {error}
            </p>
          </div>
        )}
      </div>

      {/* Generated Palette Preview */}
      {lastGenerated && <ColorPreview palette={lastGenerated} />}
    </div>
  );
}