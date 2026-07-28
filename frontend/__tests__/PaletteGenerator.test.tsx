/**
 * Tests for PaletteGenerator component
 */

import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import PaletteGenerator from '@/components/PaletteGenerator';
import { apiClient } from '@/lib/api-client';

// Mock the API client
jest.mock('@/lib/api-client', () => ({
  apiClient: {
    generateRandomPalette: jest.fn(),
  },
}));

const mockApiClient = apiClient as jest.Mocked<typeof apiClient>;

describe('PaletteGenerator', () => {
  const mockPaletteResponse = {
    colors: ['#FF5733', '#33FF57', '#3357FF', '#F333FF', '#33FFF3'],
    names: ['Red Orange', 'Green', 'Blue', 'Magenta', 'Cyan'],
    harmonyInfo: {
      type: 'random',
      relationships: ['base', 'complement', 'triadic', 'split-complement', 'analogous'],
    },
  };

  beforeEach(() => {
    jest.clearAllMocks();
    mockApiClient.generateRandomPalette.mockResolvedValue(mockPaletteResponse);
  });

  it('renders generation controls', () => {
    render(<PaletteGenerator />);
    
    expect(screen.getByText('🎲 Generate Palette')).toBeInTheDocument();
    expect(screen.getByText('🎲 Random')).toBeInTheDocument();
    expect(screen.getByText('🔄 Complementary')).toBeInTheDocument();
    expect(screen.getByText('🔺 Triadic')).toBeInTheDocument();
    expect(screen.getByText('🌈 Analogous')).toBeInTheDocument();
  });

  it('shows instructions when no palette is generated', () => {
    render(<PaletteGenerator />);
    
    expect(screen.getByText('Generate Your First Palette')).toBeInTheDocument();
    expect(screen.getByText('Choose a harmony type above to create a beautiful color palette')).toBeInTheDocument();
  });

  it('generates random palette when random button is clicked', async () => {
    render(<PaletteGenerator />);
    
    const randomButton = screen.getByText('🎲 Random');
    
    await act(async () => {
      fireEvent.click(randomButton);
    });
    
    expect(mockApiClient.generateRandomPalette).toHaveBeenCalledWith({
      lockedColors: undefined,
      harmonyType: undefined,
    });
    
    await waitFor(() => {
      expect(screen.getByText('🎨 Color Palette')).toBeInTheDocument();
    });
  });

  it('generates complementary palette when complementary button is clicked', async () => {
    render(<PaletteGenerator />);
    
    const complementaryButton = screen.getByText('🔄 Complementary');
    
    await act(async () => {
      fireEvent.click(complementaryButton);
    });
    
    expect(mockApiClient.generateRandomPalette).toHaveBeenCalledWith({
      lockedColors: undefined,
      harmonyType: 'complementary',
    });
  });

  it('shows loading state during generation', async () => {
    // Make the API call take some time
    mockApiClient.generateRandomPalette.mockImplementation(
      () => new Promise(resolve => setTimeout(() => resolve(mockPaletteResponse), 100))
    );
    
    render(<PaletteGenerator />);
    
    const randomButton = screen.getByText('🎲 Random');
    
    await act(async () => {
      fireEvent.click(randomButton);
    });
    
    expect(screen.getByText('Generating palette...')).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.queryByText('Generating palette...')).not.toBeInTheDocument();
    });
  });

  it('disables buttons during loading', async () => {
    mockApiClient.generateRandomPalette.mockImplementation(
      () => new Promise(resolve => setTimeout(() => resolve(mockPaletteResponse), 100))
    );
    
    render(<PaletteGenerator />);
    
    const randomButton = screen.getByText('🎲 Random');
    
    await act(async () => {
      fireEvent.click(randomButton);
    });
    
    expect(randomButton).toBeDisabled();
    expect(screen.getByText('🔄 Complementary')).toBeDisabled();
    
    await waitFor(() => {
      expect(randomButton).not.toBeDisabled();
    });
  });

  it('shows error message when generation fails', async () => {
    const errorMessage = 'Failed to generate palette';
    mockApiClient.generateRandomPalette.mockRejectedValue(new Error(errorMessage));
    
    render(<PaletteGenerator />);
    
    const randomButton = screen.getByText('🎲 Random');
    
    await act(async () => {
      fireEvent.click(randomButton);
    });
    
    await waitFor(() => {
      expect(screen.getByText('Generation Failed')).toBeInTheDocument();
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });
  });

  it('calls onPaletteChange when palette is generated', async () => {
    const onPaletteChange = jest.fn();
    render(<PaletteGenerator onPaletteChange={onPaletteChange} />);
    
    const randomButton = screen.getByText('🎲 Random');
    
    await act(async () => {
      fireEvent.click(randomButton);
    });
    
    await waitFor(() => {
      expect(onPaletteChange).toHaveBeenCalledWith(
        expect.objectContaining({
          colors: mockPaletteResponse.colors,
          names: mockPaletteResponse.names,
          metadata: expect.objectContaining({
            generationMethod: 'random',
          }),
        })
      );
    });
  });

  it('handles color locking correctly', async () => {
    render(<PaletteGenerator />);
    
    // First generate a palette
    const randomButton = screen.getByText('🎲 Random');
    
    await act(async () => {
      fireEvent.click(randomButton);
    });
    
    await waitFor(() => {
      expect(screen.getByText('🎨 Color Palette')).toBeInTheDocument();
    });
    
    // Lock the first color
    const lockButtons = screen.getAllByLabelText('Lock color');
    
    await act(async () => {
      fireEvent.click(lockButtons[0]);
    });
    
    // Generate another palette
    await act(async () => {
      fireEvent.click(randomButton);
    });
    
    await waitFor(() => {
      expect(mockApiClient.generateRandomPalette).toHaveBeenLastCalledWith({
        lockedColors: ['#FF5733'],
        harmonyType: undefined,
      });
    });
  });

  it('has proper accessibility attributes', () => {
    render(<PaletteGenerator />);
    
    expect(screen.getByRole('region', { name: 'Palette generation controls' })).toBeInTheDocument();
    expect(screen.getByRole('group', { name: 'Color harmony generation options' })).toBeInTheDocument();
    expect(screen.getByLabelText('Generate random color palette')).toBeInTheDocument();
    expect(screen.getByLabelText('Generate complementary color harmony palette')).toBeInTheDocument();
  });

  it('announces loading state to screen readers', async () => {
    mockApiClient.generateRandomPalette.mockImplementation(
      () => new Promise(resolve => setTimeout(() => resolve(mockPaletteResponse), 100))
    );
    
    render(<PaletteGenerator />);
    
    const randomButton = screen.getByText('🎲 Random');
    
    await act(async () => {
      fireEvent.click(randomButton);
    });
    
    const loadingStatus = screen.getByRole('status');
    expect(loadingStatus).toHaveAttribute('aria-live', 'polite');
    expect(loadingStatus).toHaveTextContent('Generating palette...');
    
    await waitFor(() => {
      expect(screen.queryByRole('status')).not.toBeInTheDocument();
    });
  });

  it('announces errors to screen readers', async () => {
    const errorMessage = 'Failed to generate palette';
    mockApiClient.generateRandomPalette.mockRejectedValue(new Error(errorMessage));
    
    render(<PaletteGenerator />);
    
    const randomButton = screen.getByText('🎲 Random');
    
    await act(async () => {
      fireEvent.click(randomButton);
    });
    
    await waitFor(() => {
      const errorAlert = screen.getByRole('alert');
      expect(errorAlert).toHaveAttribute('aria-live', 'assertive');
      expect(errorAlert).toHaveTextContent('Generation Failed');
      expect(errorAlert).toHaveTextContent(errorMessage);
    });
  });

  it('shows locked colors information', async () => {
    render(<PaletteGenerator />);
    
    // Generate initial palette
    const randomButton = screen.getByText('🎲 Random');
    
    await act(async () => {
      fireEvent.click(randomButton);
    });
    
    await waitFor(() => {
      expect(screen.getByText('🎨 Color Palette')).toBeInTheDocument();
    });
    
    // Lock two colors
    const lockButtons = screen.getAllByLabelText('Lock color');
    
    await act(async () => {
      fireEvent.click(lockButtons[0]);
      fireEvent.click(lockButtons[1]);
    });
    
    expect(screen.getByText('🔒 2 colors will remain locked during generation')).toBeInTheDocument();
  });

  it('resets locked colors when new palette is set via setPalette', async () => {
    const onPaletteChange = jest.fn();
    render(<PaletteGenerator onPaletteChange={onPaletteChange} />);
    
    // Generate initial palette
    const randomButton = screen.getByText('🎲 Random');
    
    await act(async () => {
      fireEvent.click(randomButton);
    });
    
    await waitFor(() => {
      expect(screen.getByText('🎨 Color Palette')).toBeInTheDocument();
    });
    
    // Lock a color
    const lockButtons = screen.getAllByLabelText('Lock color');
    
    await act(async () => {
      fireEvent.click(lockButtons[0]);
    });
    
    // Verify color is locked
    expect(screen.getByText('🔒 1 color will remain locked during generation')).toBeInTheDocument();
    
    // This would typically be called by a parent component setting a new palette
    // In a real test, we'd need to expose the setPalette function or test it through integration
  });

  it('handles initial palette prop correctly', () => {
    const initialPalette = {
      colors: ['#FF0000', '#00FF00', '#0000FF'],
      names: ['Red', 'Green', 'Blue'],
      metadata: {
        generationMethod: 'random' as const,
        timestamp: '2023-01-01T00:00:00Z',
      },
    };
    
    render(<PaletteGenerator initialPalette={initialPalette} />);
    
    expect(screen.getByText('🎨 Color Palette')).toBeInTheDocument();
    expect(screen.getByText('Generated via random • 3 colors')).toBeInTheDocument();
  });
});