/**
 * Constants and configuration values for ChromaCraft MVP
 * Centralized configuration for API endpoints, limits, and application settings
 */

// API Configuration
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const API_ENDPOINTS = {
  // Color generation endpoints
  GENERATE_RANDOM: '/generate/random',
  GENERATE_CONCEPT: '/generate/concept',
  GENERATE_MOOD: '/generate/mood',
  EXTRACT_COLORS: '/extract-colors',
  
  // Palette editing endpoints
  EDIT_PALETTE: '/edit/palette',
  
  // Validation endpoints
  VALIDATE_ACCESSIBILITY: '/validate/accessibility',
  
  // Export endpoints
  EXPORT_PNG: '/export-png',
  EXPORT_JSON: '/export/json',
  EXPORT_ASE: '/export/ase',
  
  // Utility endpoints
  HEALTH_CHECK: '/',
  MEMORY_USAGE: '/mem',
  
  // Legacy endpoints (for backward compatibility)
  ADJUST_MOOD: '/adjust-mood',
} as const;

export const API_CONFIG = {
  // Timeout configurations (in milliseconds)
  DEFAULT_TIMEOUT: 10000,      // 10 seconds
  UPLOAD_TIMEOUT: 30000,       // 30 seconds for file uploads
  AI_TIMEOUT: 15000,           // 15 seconds for AI operations
  EXPORT_TIMEOUT: 20000,       // 20 seconds for exports
  
  // File upload limits
  MAX_FILE_SIZE: 10 * 1024 * 1024,  // 10MB
  ALLOWED_FILE_TYPES: ['image/jpeg', 'image/jpg', 'image/png'],
  
  // Palette constraints
  MAX_PALETTE_SIZE: 10,
  DEFAULT_PALETTE_SIZE: 5,
  MIN_PALETTE_SIZE: 2,
  
  // Retry configuration
  MAX_RETRY_ATTEMPTS: 3,
  RETRY_DELAY_MS: 1000,
  RETRY_BACKOFF_MULTIPLIER: 2,
} as const;

// Color theory constants
export const COLOR_HARMONY_TYPES = {
  COMPLEMENTARY: 'complementary',
  TRIADIC: 'triadic',
  ANALOGOUS: 'analogous',
  MONOCHROMATIC: 'monochromatic',
  TETRADIC: 'tetradic',
  SPLIT_COMPLEMENTARY: 'split-complementary',
} as const;

// Mood adjustment constants
export const MOOD_COMMANDS = {
  PASTEL: ['make it pastel', 'pastel', 'softer', 'lighter'],
  CONTRAST: ['add contrast', 'more contrast', 'increase contrast', 'bolder'],
  WARMER: ['make it warmer', 'warmer', 'warm tones', 'add warmth'],
  COOLER: ['make it cooler', 'cooler', 'cool tones', 'add coolness'],
  DARKER: ['make it darker', 'darker', 'deep', 'rich'],
  BRIGHTER: ['make it brighter', 'brighter', 'vivid', 'vibrant'],
  SATURATED: ['more saturated', 'saturated', 'intense', 'bold'],
  DESATURATED: ['less saturated', 'desaturated', 'muted', 'subtle'],
} as const;

// Export format constants
export const EXPORT_FORMATS = {
  PNG: 'png',
  JSON: 'json',
  ASE: 'ase',
  CLIPBOARD: 'clipboard',
} as const;

export const EXPORT_SIZES = {
  SMALL: { width: 400, height: 100 },
  MEDIUM: { width: 600, height: 150 },
  LARGE: { width: 800, height: 200 },
} as const;

// Accessibility constants
export const WCAG_LEVELS = {
  AA: 'AA',
  AAA: 'AAA',
  FAIL: 'fail',
} as const;

export const CONTRAST_RATIOS = {
  AA_NORMAL: 4.5,
  AA_LARGE: 3.0,
  AAA_NORMAL: 7.0,
  AAA_LARGE: 4.5,
} as const;

// UI constants
export const ANIMATION_DURATIONS = {
  FAST: 150,
  NORMAL: 300,
  SLOW: 500,
} as const;

export const BREAKPOINTS = {
  SM: 640,
  MD: 768,
  LG: 1024,
  XL: 1280,
  '2XL': 1536,
} as const;

// Local storage keys
export const STORAGE_KEYS = {
  PALETTE_HISTORY: 'chromacraft_palette_history',
  USER_PREFERENCES: 'chromacraft_user_preferences',
  LOCKED_COLORS: 'chromacraft_locked_colors',
  THEME_PREFERENCE: 'chromacraft_theme',
} as const;

// Error tracking constants
export const ERROR_CATEGORIES = {
  NETWORK: 'network',
  VALIDATION: 'validation',
  FILE_PROCESSING: 'file_processing',
  AI_PROCESSING: 'ai_processing',
  EXPORT: 'export',
  UNKNOWN: 'unknown',
} as const;

// Feature flags (for gradual rollout)
export const FEATURE_FLAGS = {
  ENABLE_AI_MOOD_GENERATION: process.env.NEXT_PUBLIC_ENABLE_AI_MOOD === 'true',
  ENABLE_ACCESSIBILITY_VALIDATION: process.env.NEXT_PUBLIC_ENABLE_A11Y === 'true',
  ENABLE_ASE_EXPORT: process.env.NEXT_PUBLIC_ENABLE_ASE === 'true',
  ENABLE_PALETTE_HISTORY: process.env.NEXT_PUBLIC_ENABLE_HISTORY === 'true',
  ENABLE_ADVANCED_EDITING: process.env.NEXT_PUBLIC_ENABLE_ADVANCED_EDIT === 'true',
} as const;

// Development constants
export const DEV_CONFIG = {
  ENABLE_LOGGING: process.env.NODE_ENV === 'development',
  ENABLE_PERFORMANCE_MONITORING: process.env.NODE_ENV === 'development',
  MOCK_API_RESPONSES: process.env.NEXT_PUBLIC_MOCK_API === 'true',
} as const;

// Default values
export const DEFAULTS = {
  PALETTE_SIZE: API_CONFIG.DEFAULT_PALETTE_SIZE,
  HARMONY_TYPE: COLOR_HARMONY_TYPES.COMPLEMENTARY,
  EXPORT_FORMAT: EXPORT_FORMATS.PNG,
  EXPORT_SIZE: 'medium' as keyof typeof EXPORT_SIZES,
  MOOD_INTENSITY: 0.5,
  EDIT_INTENSITY: 0.5,
} as const;