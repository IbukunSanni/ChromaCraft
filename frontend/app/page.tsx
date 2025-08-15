"use client";

import { useState, useEffect } from "react";
import Layout from "@/components/Layout";
import ImageUploader from "@/components/ImageUploader";
import MoodInput from "@/components/MoodInput";
import { API_BASE_URL } from "@/lib/constants";

export default function Home() {
  const [mood, setMood] = useState<string>("");
  const [palette, setPalette] = useState<string[]>([]);
  const [colorNames, setColorNames] = useState<string[]>([]);
  const [newPalette, setNewPalette] = useState<string[]>([]);
  const [newColorNames, setNewColorNames] = useState<string[]>([]);
  const [isAdjusting, setIsAdjusting] = useState(false);

  const handleAdjustMood = async () => {
    if (!Array.isArray(palette) || palette.length === 0 || !mood) return;

    setIsAdjusting(true);
    const formData = new FormData();
    formData.append("mood", mood);
    palette.forEach((color) => {
      formData.append("base_colors", color);
    });

    try {
      const res = await fetch(`${API_BASE_URL}/adjust-mood`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setNewPalette(data?.adjusted_colors || []);
      setNewColorNames(data?.names || []);
    } catch (err) {
      console.error("Mood adjust failed:", err);
    } finally {
      setIsAdjusting(false);
    }
  };

  const copyToClipboard = (color: string) => {
    navigator.clipboard.writeText(color);
  };

  const ColorPalette = ({ colors, names, title, subtitle }: {
    colors: string[];
    names: string[];
    title: string;
    subtitle?: string;
  }) => (
    <div className="card-gradient rounded-2xl p-8">
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-2" style={{ color: 'var(--foreground)' }}>{title}</h2>
        {subtitle && <p style={{ color: 'var(--secondary)' }}>{subtitle}</p>}
      </div>
      
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
        {colors.map((color, index) => (
          <div
            key={index}
            className="color-swatch group cursor-pointer"
            onClick={() => copyToClipboard(color)}
            title={`Click to copy ${color}`}
          >
            <div
              className="w-full h-24 rounded-xl shadow-lg mb-3 border-2 border-white/50"
              style={{ backgroundColor: color }}
            />
            <div className="text-center space-y-1">
              <p className="font-mono text-sm font-medium transition-colors" style={{ color: 'var(--foreground)' }}>
                {color}
              </p>
              <p className="text-xs capitalize" style={{ color: 'var(--secondary)' }}>
                {names?.[index] || "Unnamed"}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  useEffect(() => {
    // Debug log
    // console.log("palette changed:", palette);
    // console.log("names changed:", colorNames);
  }, [palette, colorNames]);

  return (
    <Layout>
      {/* Step 1: Image Upload */}
      <ImageUploader
        onColorExtracted={(colors: string[]) => setPalette(colors || [])}
        onColorNamesExtracted={(names: string[]) => setColorNames(names || [])}
      />

      {/* Step 2: Show Extracted Colors */}
      {Array.isArray(palette) && palette.length > 0 && (
        <ColorPalette
          colors={palette}
          names={colorNames}
          title="🎨 Extracted Colors"
          subtitle="Colors extracted from your image"
        />
      )}

      {/* Step 3: Mood Input */}
      {palette.length > 0 && (
        <MoodInput onMoodChange={(m: string) => setMood(m)} />
      )}

      {/* Step 4: Adjust Button */}
      {palette.length > 0 && mood && (
        <div className="text-center">
          <button
            onClick={handleAdjustMood}
            disabled={isAdjusting}
            className="px-8 py-4 text-white font-bold text-lg rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            style={{ background: `linear-gradient(to right, var(--primary), var(--accent))` }}
          >
            {isAdjusting ? (
              <span className="flex items-center gap-3">
                <div className="animate-spin w-5 h-5 border-2 border-white border-t-transparent rounded-full"></div>
                Adjusting Colors...
              </span>
            ) : (
              <span className="flex items-center gap-3">
                ✨ Transform with AI
              </span>
            )}
          </button>
        </div>
      )}

      {/* Step 5: Show Adjusted Colors */}
      {Array.isArray(newPalette) && newPalette.length > 0 && (
        <ColorPalette
          colors={newPalette}
          names={newColorNames}
          title="✨ AI-Adjusted Palette"
          subtitle={`Transformed to feel "${mood}"`}
        />
      )}

      {/* Instructions */}
      {palette.length === 0 && (
        <div className="card-gradient rounded-2xl p-8 text-center">
          <div className="space-y-4">
            <div className="text-6xl">🚀</div>
            <h2 className="text-2xl font-bold" style={{ color: 'var(--foreground)' }}>Get Started</h2>
            <div className="space-y-2 max-w-2xl mx-auto" style={{ color: 'var(--secondary)' }}>
              <p className="text-lg">Transform your images into mood-based color palettes with AI</p>
              <div className="grid md:grid-cols-3 gap-4 mt-6 text-sm">
                <div className="space-y-2">
                  <div className="text-2xl">📸</div>
                  <p className="font-medium">1. Upload Image</p>
                  <p>Choose any image to extract colors from</p>
                </div>
                <div className="space-y-2">
                  <div className="text-2xl">🧠</div>
                  <p className="font-medium">2. Describe Mood</p>
                  <p>Tell AI how you want the colors to feel</p>
                </div>
                <div className="space-y-2">
                  <div className="text-2xl">✨</div>
                  <p className="font-medium">3. Get Magic</p>
                  <p>AI transforms colors to match your mood</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </Layout>
  );
}
