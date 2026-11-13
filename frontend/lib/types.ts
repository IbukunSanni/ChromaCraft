/**
 * Core TypeScript interfaces for ChromaCraft MVP
 * Defines data models for color palettes, API requests/responses, and UI state
 */

// Core color and palette types
export interface ColorInfo {
  hex: string;
  name: string;
  locked: boolean;
  accessibility?: {
    contrastRatio: number;
    wcagLevel: 'AA' | 'AAA' | 'fail';
  };
}

export interface ColorPalette {
  colors: string[];
  names: string[];
  metadata: {
    generationMethod: 'random' | 'concept' | 'image' | 'edited';
    timestamp: string;
    source?: string;
  };
}

// API Request types
export interface ConceptGenerationRequest {
  concept: string;
  color_count?: number;
  stylePreferences?: {
    saturation: 'low' | 'medium' | 'high';
    brightness: 'dark' | 'medium' | 'light';
    temperature: 'cool' | 'neutral' | 'warm';
  };
}

// Harmony types accepted by POST /generate/random
export type HarmonyType =
  | 'complementary'
  | 'triadic'
  | 'analogous'
  | 'tetradic'
  | 'monochromatic'
  | 'split_complementary';

// Field names match the FastAPI request model (snake_case)
export interface RandomGenerationRequest {
  locked_colors?: string[];
  harmony_type?: HarmonyType;
}


export interface ExportRequest {
  colors: string[];
}

// API Response types
// Response types mirror backend/models (FastAPI response models)
export interface ColorExtractionResponse {
  colors: string[];
  names: string[];
}

export interface ConceptAdjustmentResponse {
  adjusted_colors: string[];
  names: string[];
}

export interface RandomGenerationResponse {
  colors: string[];
  names: string[];
  harmony_info: {
    valid: boolean;
    harmony_type: string;
    confidence: number;
    details?: Record<string, unknown>;
    locked_colors_count?: number;
    locked_colors?: string[];
  };
}

export interface ConceptGenerationResponse {
  colors: string[];
  names: string[];
  harmony_info: {
    type: string;
    mood: string;
    description: string;
    source: string;
    model: string;
  };
}

// Error types
export interface APIError {
  message: string;
  statusCode: number;
  details?: Record<string, unknown>;
  timestamp: string;
}

// UI State types
export interface PaletteGeneratorState {
  currentPalette: ColorPalette | null;
  lockedColors: Set<number>;
  generationMethod: 'random' | 'concept' | 'image' | 'edited';
  isLoading: boolean;
  error: string | null;
}

export interface ExportState {
  isExporting: boolean;
  format: 'png' | 'json' | 'ase' | 'clipboard';
  progress: number;
  error: string | null;
}

// Component prop types
export interface ColorSwatchProps {
  color: string;
  name: string;
  locked: boolean;
  index: number;
  onToggleLock: (index: number) => void;
  showAccessibility?: boolean;
  accessibilityInfo?: ColorInfo['accessibility'];
}

export interface PaletteDisplayProps {
  palette: ColorPalette;
  lockedColors: Set<number>;
  onToggleLock: (index: number) => void;
  showAccessibility?: boolean;
}

export interface ConceptInputProps {
  onConceptGenerate: (request: ConceptGenerationRequest) => void;
  isLoading: boolean;
  error?: string | null;
}

export interface ExportPanelProps {
  palette: ColorPalette;
  onExport: (format: ExportState['format']) => void;
  exportState: ExportState;
}

// Utility types
export type GenerationMethod = ColorPalette['metadata']['generationMethod'];
export type ExportFormat = ExportState['format'];
export type WCAGLevel = NonNullable<ColorInfo['accessibility']>['wcagLevel'];