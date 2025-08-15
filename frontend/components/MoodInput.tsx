"use client";
import { useState } from "react";

const moodSuggestions = [
  "warm and cozy", "dark and mysterious", "bright and energetic", 
  "calm and serene", "vibrant and bold", "soft and dreamy",
  "earthy and natural", "cool and refreshing", "elegant and sophisticated"
];

export default function MoodInput({ onMoodChange }: { onMoodChange: (mood: string) => void }) {
  const [mood, setMood] = useState("");

  const handleSuggestionClick = (suggestion: string) => {
    setMood(suggestion);
    onMoodChange(suggestion);
  };

  return (
    <div className="card-gradient rounded-2xl p-8">
      <h2 className="text-2xl font-bold mb-6 flex items-center gap-3" style={{ color: 'var(--foreground)' }}>
        🧠 Describe Your Mood
      </h2>
      
      <div className="space-y-4">
        <div className="relative">
          <input
            type="text"
            value={mood}
            onChange={(e) => {
              setMood(e.target.value);
              onMoodChange(e.target.value);
            }}
            className="w-full border-2 rounded-xl p-4 text-lg focus:outline-none transition-colors duration-300 backdrop-blur-sm"
            style={{
              borderColor: 'var(--muted)',
              backgroundColor: 'var(--glass-bg)',
              color: 'var(--foreground)',
              ':focus': { borderColor: 'var(--primary)' }
            }}
            placeholder="e.g. warm and cozy, dark and mysterious..."
          />
          <div className="absolute right-4 top-1/2 transform -translate-y-1/2 text-2xl">
            🎭
          </div>
        </div>

        <div className="space-y-3">
          <p className="text-sm font-medium" style={{ color: 'var(--secondary)' }}>Quick suggestions:</p>
          <div className="flex flex-wrap gap-2">
            {moodSuggestions.map((suggestion, index) => (
              <button
                key={index}
                onClick={() => handleSuggestionClick(suggestion)}
                className="px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 hover:shadow-md"
                style={{
                  backgroundColor: mood === suggestion ? 'var(--primary)' : 'var(--muted)',
                  color: mood === suggestion ? 'white' : 'var(--foreground)',
                  boxShadow: mood === suggestion ? '0 4px 6px -1px rgba(0, 0, 0, 0.1)' : 'none'
                }}
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
