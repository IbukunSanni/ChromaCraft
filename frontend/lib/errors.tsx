/**
 * Error handling utilities for ChromaCraft MVP
 * Provides standardized error handling, user-friendly messages, and retry logic
 */

import React from 'react';

// Custom error classes
export class ChromaCraftError extends Error {
  public readonly statusCode: number;
  public readonly details: Record<string, unknown>;
  public readonly timestamp: string;

  constructor(message: string, statusCode: number = 500, details: Record<string, unknown> = {}) {
    super(message);
    this.name = 'ChromaCraftError';
    this.statusCode = statusCode;
    this.details = details;
    this.timestamp = new Date().toISOString();
  }
}

export class ValidationError extends ChromaCraftError {
  constructor(message: string, details: Record<string, unknown> = {}) {
    super(message, 400, details);
    this.name = 'ValidationError';
  }
}

export class NetworkError extends ChromaCraftError {
  constructor(message: string, details: Record<string, unknown> = {}) {
    super(message, 0, details);
    this.name = 'NetworkError';
  }
}

export class FileProcessingError extends ChromaCraftError {
  constructor(message: string, details: Record<string, unknown> = {}) {
    super(message, 422, details);
    this.name = 'FileProcessingError';
  }
}

// Error message mapping for user-friendly display
export const ERROR_MESSAGES = {
  // Network errors
  NETWORK_ERROR: 'Unable to connect to the server. Please check your internet connection.',
  TIMEOUT_ERROR: 'Request timed out. Please try again.',
  SERVER_ERROR: 'Server is temporarily unavailable. Please try again later.',
  
  // File upload errors
  FILE_TOO_LARGE: 'File size exceeds 10MB limit. Please choose a smaller image.',
  INVALID_FILE_TYPE: 'Please upload a valid JPG or PNG image file.',
  CORRUPTED_FILE: 'The uploaded file appears to be corrupted. Please try a different image.',
  
  // Color processing errors
  COLOR_EXTRACTION_FAILED: 'Unable to extract colors from the image. Please try a different image.',
  INVALID_COLOR_FORMAT: 'Invalid color format. Please use valid HEX color codes.',
  PALETTE_GENERATION_FAILED: 'Failed to generate color palette. Please try again.',
  
  // AI/Concept processing errors
  CONCEPT_PROCESSING_FAILED: 'Unable to process concept description. Please try a different description.',
  AI_SERVICE_UNAVAILABLE: 'AI service is temporarily unavailable. Please try again later.',
  
  // Export errors
  EXPORT_FAILED: 'Failed to export palette. Please try again.',
  CLIPBOARD_FAILED: 'Unable to copy to clipboard. Please try manually selecting the colors.',
  
  // Validation errors
  EMPTY_PALETTE: 'No colors available to export. Please generate a palette first.',
  INVALID_COMMAND: 'Unrecognized editing command. Try "make it pastel", "add contrast", or "make it warmer".',
  
  // Generic fallback
  UNKNOWN_ERROR: 'An unexpected error occurred. Please try again.',
} as const;

// Error classification helper
export function classifyError(error: unknown): ChromaCraftError {
  if (error instanceof ChromaCraftError) {
    return error;
  }

  if (error instanceof TypeError && error.message.includes('fetch')) {
    return new NetworkError(ERROR_MESSAGES.NETWORK_ERROR);
  }

  if (error instanceof Error) {
    // Check for specific error patterns
    if (error.message.includes('timeout')) {
      return new NetworkError(ERROR_MESSAGES.TIMEOUT_ERROR);
    }
    
    if (error.message.includes('file') && error.message.includes('size')) {
      return new FileProcessingError(ERROR_MESSAGES.FILE_TOO_LARGE);
    }
    
    if (error.message.includes('invalid') && error.message.includes('image')) {
      return new FileProcessingError(ERROR_MESSAGES.INVALID_FILE_TYPE);
    }

    return new ChromaCraftError(error.message);
  }

  return new ChromaCraftError(ERROR_MESSAGES.UNKNOWN_ERROR);
}

// User-friendly error message generator
export function getUserFriendlyMessage(error: ChromaCraftError): string {
  // Check if we have a predefined user-friendly message
  const predefinedMessage = Object.values(ERROR_MESSAGES).find(msg => 
    error.message.includes(msg) || msg.includes(error.message)
  );
  
  if (predefinedMessage) {
    return predefinedMessage;
  }

  // Map by status code
  switch (error.statusCode) {
    case 400:
      return 'Invalid request. Please check your input and try again.';
    case 404:
      return 'Requested resource not found.';
    case 413:
      return ERROR_MESSAGES.FILE_TOO_LARGE;
    case 422:
      return 'Unable to process the provided data. Please check your input.';
    case 429:
      return 'Too many requests. Please wait a moment and try again.';
    case 500:
      return ERROR_MESSAGES.SERVER_ERROR;
    case 503:
      return 'Service temporarily unavailable. Please try again later.';
    default:
      return error.message || ERROR_MESSAGES.UNKNOWN_ERROR;
  }
}

// Retry logic helper
export interface RetryOptions {
  maxAttempts: number;
  delayMs: number;
  backoffMultiplier: number;
  retryableErrors: number[];
}

export const DEFAULT_RETRY_OPTIONS: RetryOptions = {
  maxAttempts: 3,
  delayMs: 1000,
  backoffMultiplier: 2,
  retryableErrors: [0, 408, 429, 500, 502, 503, 504], // Network errors and server errors
};

export async function withRetry<T>(
  operation: () => Promise<T>,
  options: Partial<RetryOptions> = {}
): Promise<T> {
  const config = { ...DEFAULT_RETRY_OPTIONS, ...options };
  let lastError: ChromaCraftError;

  for (let attempt = 1; attempt <= config.maxAttempts; attempt++) {
    try {
      return await operation();
    } catch (error) {
      lastError = classifyError(error);
      
      // Don't retry if it's not a retryable error
      if (!config.retryableErrors.includes(lastError.statusCode)) {
        throw lastError;
      }
      
      // Don't retry on the last attempt
      if (attempt === config.maxAttempts) {
        throw lastError;
      }
      
      // Wait before retrying
      const delay = config.delayMs * Math.pow(config.backoffMultiplier, attempt - 1);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw lastError!;
}

// Error logging helper (for development)
export function logError(error: ChromaCraftError, context?: string): void {
  if (process.env.NODE_ENV === 'development') {
    console.group(`🚨 ChromaCraft Error${context ? ` (${context})` : ''}`);
    console.error('Message:', error.message);
    console.error('Status Code:', error.statusCode);
    console.error('Details:', error.details);
    console.error('Timestamp:', error.timestamp);
    console.error('Stack:', error.stack);
    console.groupEnd();
  }
}

// Error boundary helper for React components
export function createErrorBoundaryFallback(componentName: string) {
  return function ErrorFallback({ error, resetError }: { error: Error; resetError: () => void }) {
    const chromaCraftError = classifyError(error);
    const userMessage = getUserFriendlyMessage(chromaCraftError);
    
    logError(chromaCraftError, componentName);

    return (
      <div className="flex flex-col items-center justify-center p-8 bg-red-50 border border-red-200 rounded-lg">
        <div className="text-red-600 text-lg font-semibold mb-2">
          Something went wrong
        </div>
        <div className="text-red-700 text-center mb-4 max-w-md">
          {userMessage}
        </div>
        <button
          onClick={resetError}
          className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
        >
          Try Again
        </button>
      </div>
    );
  };
}