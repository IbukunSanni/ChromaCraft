"use client";

import { useTheme } from '@/contexts/ThemeContext';

export default function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      className="fixed top-6 right-6 z-50 p-3 rounded-full glass hover:scale-110 transition-all duration-300 shadow-lg"
      aria-label="Toggle theme"
    >
      <div className="text-2xl">
        {theme === 'light' ? '🌙' : '☀️'}
      </div>
    </button>
  );
}