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

export interface PaletteEditRequest {
  colors: string[];
  command: string;
  intensity?: number; // 0.1 to 1.0
}

export interface RandomGenerationRequest {
  lockedColors?: string[];
  harmonyType?: 'complementary' | 'triadic' | 'analogous' | 'monochromatic';
}


export interface ExportRequest {
  colors: string[];
  names: string[];
  formatOptions?: {
    size?: 'small' | 'medium' | 'large';
    includeNames?: boolean;
    includeHex?: boolean;
  };
}

export interface AccessibilityValidationRequest {
  colors: string[];
}

// API Response types
export interface ColorExtractionResponse {
  colors: string[];
  names: string[];
  dominantInfo?: {
    clusters: number;
    processingTime: number;
  };
}


export interface PaletteEditResponse {
  colors: string[];
  names: string[];
  editApplied: string;
}

export interface RandomGenerationResponse {
  colors: string[];
  names: string[];
  harmonyInfo: {
    type: string;
    baseColor?: string;
    relationships: string[];
  };
}

export interface ConceptGenerationResponse {
  colors: string[];
  names: string[];
  harmony_info: {
    type: string;
    concept: string;
    description: string;
    source: string;
    model: string;
  };
  concept: string;  // Original concept returned
}

export interface AccessibilityValidationResponse {
  contrastRatios: Record<string, number>[];
  wcagCompliance: {
    aa: boolean;
    aaa: boolean;
    issues: string[];
  };
  suggestions: string[];
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

export interface ConceptEditorProps {
  currentPalette: ColorPalette;
  onPaletteEdit: (request: PaletteEditRequest) => void;
  isLoading: boolean;
  error?: string | null;
}

export interface ExportPanelProps {
  palette: ColorPalette;
  onExport: (format: ExportState['format'], options?: ExportRequest['formatOptions']) => void;
  exportState: ExportState;
}

// Utility types
export type GenerationMethod = ColorPalette['metadata']['generationMethod'];
export type HarmonyType = RandomGenerationRequest['harmonyType'];
export type ExportFormat = ExportState['format'];
export type WCAGLevel = NonNullable<ColorInfo['accessibility']>['wcagLevel'];