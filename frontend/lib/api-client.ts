/**
 * API client configuration for ChromaCraft MVP
 * Provides centralized HTTP client with error handling, retries, and type safety
 */

import { 
  ColorExtractionResponse,
  MoodGenerationResponse,
  PaletteEditResponse,
  RandomGenerationResponse,
  ConceptGenerationResponse,
  AccessibilityValidationResponse,
  MoodGenerationRequest,
  PaletteEditRequest,
  RandomGenerationRequest,
  ConceptGenerationRequest,
  AccessibilityValidationRequest,
  ExportRequest
} from './types';
import { 
  ChromaCraftError, 
  classifyError, 
  withRetry, 
  DEFAULT_RETRY_OPTIONS,
  logError 
} from './errors';
import { API_ENDPOINTS, API_CONFIG } from './constants';

// HTTP client configuration
interface RequestConfig {
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  headers?: Record<string, string>;
  body?: unknown;
  timeout?: number;
  retryOptions?: Partial<typeof DEFAULT_RETRY_OPTIONS>;
}

class APIClient {
  private baseURL: string;
  private defaultHeaders: Record<string, string>;
  private defaultTimeout: number;

  constructor(baseURL: string) {
    this.baseURL = baseURL.replace(/\/$/, ''); // Remove trailing slash
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
    this.defaultTimeout = API_CONFIG.DEFAULT_TIMEOUT;
  }

  // Core HTTP request method
  private async request<T>(endpoint: string, config: RequestConfig): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const headers = { ...this.defaultHeaders, ...config.headers };
    
    // Handle FormData (for file uploads)
    let body = config.body;
    if (config.body instanceof FormData) {
      // Remove Content-Type header for FormData (browser will set it with boundary)
      delete headers['Content-Type'];
    } else if (config.body && typeof config.body === 'object') {
      body = JSON.stringify(config.body);
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), config.timeout || this.defaultTimeout);

    try {
      const response = await withRetry(async () => {
        const fetchResponse = await fetch(url, {
          method: config.method,
          headers,
          body,
          signal: controller.signal,
        });

        if (!fetchResponse.ok) {
          const errorData = await fetchResponse.json().catch(() => ({}));
          throw new ChromaCraftError(
            errorData.error || errorData.detail || `HTTP ${fetchResponse.status}`,
            fetchResponse.status,
            errorData
          );
        }

        return fetchResponse;
      }, config.retryOptions);

      clearTimeout(timeoutId);

      // Handle different response types
      const contentType = response.headers.get('content-type');
      if (contentType?.includes('application/json')) {
        return await response.json();
      } else if (contentType?.includes('image/') || contentType?.includes('application/octet-stream')) {
        return response.blob() as T;
      } else {
        return await response.text() as T;
      }

    } catch (error) {
      clearTimeout(timeoutId);
      const chromaCraftError = classifyError(error);
      logError(chromaCraftError, `API Request: ${config.method} ${endpoint}`);
      throw chromaCraftError;
    }
  }

  // Convenience methods
  private get<T>(endpoint: string, config: Partial<RequestConfig> = {}): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET', ...config });
  }

  private post<T>(endpoint: string, body?: unknown, config: Partial<RequestConfig> = {}): Promise<T> {
    return this.request<T>(endpoint, { method: 'POST', body, ...config });
  }

  // Color extraction from image
  async extractColors(file: File): Promise<ColorExtractionResponse> {
    const formData = new FormData();
    formData.append('file', file);

    return this.post<ColorExtractionResponse>(API_ENDPOINTS.EXTRACT_COLORS, formData, {
      timeout: API_CONFIG.UPLOAD_TIMEOUT,
      retryOptions: { maxAttempts: 2 }, // Fewer retries for file uploads
    });
  }

  // Random palette generation
  async generateRandomPalette(request: RandomGenerationRequest = {}): Promise<RandomGenerationResponse> {
    return this.post<RandomGenerationResponse>(API_ENDPOINTS.GENERATE_RANDOM, request);
  }

  // Concept-based palette generation using OpenAI
  async generateConceptPalette(request: ConceptGenerationRequest): Promise<ConceptGenerationResponse> {
    return this.post<ConceptGenerationResponse>(API_ENDPOINTS.GENERATE_CONCEPT, request, {
      timeout: API_CONFIG.AI_TIMEOUT,
    });
  }

  // Mood-based palette generation
  async generateMoodPalette(request: MoodGenerationRequest): Promise<MoodGenerationResponse> {
    return this.post<MoodGenerationResponse>(API_ENDPOINTS.GENERATE_MOOD, request, {
      timeout: API_CONFIG.AI_TIMEOUT,
    });
  }

  // Palette editing with natural language
  async editPalette(request: PaletteEditRequest): Promise<PaletteEditResponse> {
    return this.post<PaletteEditResponse>(API_ENDPOINTS.EDIT_PALETTE, request);
  }

  // Accessibility validation
  async validateAccessibility(request: AccessibilityValidationRequest): Promise<AccessibilityValidationResponse> {
    return this.post<AccessibilityValidationResponse>(API_ENDPOINTS.VALIDATE_ACCESSIBILITY, request);
  }

  // Export functions
  async exportPNG(request: ExportRequest): Promise<Blob> {
    const formData = new FormData();
    formData.append('colors', JSON.stringify(request.colors));
    formData.append('names', JSON.stringify(request.names));
    if (request.formatOptions) {
      formData.append('format_options', JSON.stringify(request.formatOptions));
    }

    return this.post<Blob>(API_ENDPOINTS.EXPORT_PNG, formData, {
      timeout: API_CONFIG.EXPORT_TIMEOUT,
    });
  }

  async exportJSON(request: ExportRequest): Promise<Record<string, unknown>> {
    const params = new URLSearchParams({
      colors: request.colors.join(','),
      names: request.names.join(','),
    });

    return this.get<Record<string, unknown>>(`${API_ENDPOINTS.EXPORT_JSON}?${params}`);
  }

  async exportASE(request: ExportRequest): Promise<Blob> {
    return this.post<Blob>(API_ENDPOINTS.EXPORT_ASE, request, {
      timeout: API_CONFIG.EXPORT_TIMEOUT,
    });
  }

  // Health check
  async healthCheck(): Promise<{ message: string }> {
    return this.get<{ message: string }>('/');
  }

  // Memory usage (development)
  async getMemoryUsage(): Promise<{ memory_mb: number }> {
    return this.get<{ memory_mb: number }>('/mem');
  }
}

// Create and export singleton instance
export const apiClient = new APIClient(process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000');

// Export class for testing
export { APIClient };

// Utility functions for common operations
export async function copyToClipboard(colors: string[]): Promise<void> {
  try {
    const colorText = colors.join('\n');
    await navigator.clipboard.writeText(colorText);
  } catch {
    // Fallback for browsers that don't support clipboard API
    const textArea = document.createElement('textarea');
    textArea.value = colors.join('\n');
    textArea.style.position = 'fixed';
    textArea.style.opacity = '0';
    document.body.appendChild(textArea);
    textArea.select();
    
    try {
      document.execCommand('copy');
    } catch {
      throw new ChromaCraftError('Unable to copy to clipboard. Please select and copy manually.');
    } finally {
      document.body.removeChild(textArea);
    }
  }
}

// File validation utilities
export function validateImageFile(file: File): void {
  const maxSize = API_CONFIG.MAX_FILE_SIZE;
  const allowedTypes = API_CONFIG.ALLOWED_FILE_TYPES;

  if (file.size > maxSize) {
    throw new ChromaCraftError(`File size (${(file.size / 1024 / 1024).toFixed(1)}MB) exceeds the ${maxSize / 1024 / 1024}MB limit.`);
  }

  if (!allowedTypes.includes(file.type as string)) {
    throw new ChromaCraftError(`File type "${file.type}" is not supported. Please use JPG or PNG files.`);
  }
}

// Color validation utilities
export function validateHexColor(color: string): boolean {
  const hexRegex = /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/;
  return hexRegex.test(color);
}

export function validateColorPalette(colors: string[]): void {
  if (!colors || colors.length === 0) {
    throw new ChromaCraftError('Color palette cannot be empty.');
  }

  if (colors.length > API_CONFIG.MAX_PALETTE_SIZE) {
    throw new ChromaCraftError(`Palette cannot contain more than ${API_CONFIG.MAX_PALETTE_SIZE} colors.`);
  }

  for (const color of colors) {
    if (!validateHexColor(color)) {
      throw new ChromaCraftError(`Invalid color format: "${color}". Please use valid HEX colors (e.g., #FF5733).`);
    }
  }
}