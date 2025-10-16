/**
 * Tests for PaletteDisplay component - focusing on accessibility and keyboard navigation
 */

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import PaletteDisplay from '@/components/PaletteDisplay';
import { ColorPalette } from '@/lib/types';

// Mock the clipboard API
Object.assign(navigator, {
  clipboard: {
    writeText: jest.fn(() => Promise.resolve()),
  },
});

describe('PaletteDisplay', () => {
  const mockPalette: ColorPalette = {
    colors: ['#FF5733', '#33FF57', '#3357FF', '#F333FF', '#33FFF3'],
    names: ['Red Orange', 'Green', 'Blue', 'Magenta', 'Cyan'],
    metadata: {
      generationMethod: 'random',
      timestamp: '2023-01-01T00:00:00Z',
      source: 'test',
    },
  };

  const defaultProps = {
    palette: mockPalette,
    lockedColors: new Set<number>(),
    onToggleLock: jest.fn(),
    showAccessibility: false,
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders palette with proper accessibility structure', () => {
    render(<PaletteDisplay {...defaultProps} />);
    
    expect(screen.getByRole('region', { name: /Color palette with 5 colors, 0 locked/ })).toBeInTheDocument();
    expect(screen.getByRole('grid', { name: 'Color swatches' })).toBeInTheDocument();
    expect(screen.getAllByRole('gridcell')).toHaveLength(5);
    expect(screen.getByRole('toolbar', { name: 'Palette actions' })).toBeInTheDocument();
  });

  it('displays keyboard shortcuts information', () => {
    render(<PaletteDisplay {...defaultProps} />);
    
    expect(screen.getByText(/Keyboard shortcuts:/)).toBeInTheDocument();
    expect(screen.getByText(/Arrow keys to navigate/)).toBeInTheDocument();
    expect(screen.getByText(/Enter\/Space to copy/)).toBeInTheDocument();
    expect(screen.getByText(/L to lock\/unlock/)).toBeInTheDocument();
    expect(screen.getByText(/Ctrl\+C to copy all/)).toBeInTheDocument();
    expect(screen.getByText(/Ctrl\+U to unlock all/)).toBeInTheDocument();
  });

  it('handles Ctrl+C keyboard shortcut to copy all colors', async () => {
    render(<PaletteDisplay {...defaultProps} />);
    
    const paletteRegion = screen.getByRole('region');
    fireEvent.keyDown(paletteRegion, { key: 'c', ctrlKey: true });
    
    await waitFor(() => {
      expect(navigator.clipboard.writeText).toHaveBeenCalledWith(
        '#FF5733\n#33FF57\n#3357FF\n#F333FF\n#33FFF3'
      );
    });
  });

  it('handles Cmd+C keyboard shortcut to copy all colors (Mac)', async () => {
    render(<PaletteDisplay {...defaultProps} />);
    
    const paletteRegion = screen.getByRole('region');
    fireEvent.keyDown(paletteRegion, { key: 'c', metaKey: true });
    
    await waitFor(() => {
      expect(navigator.clipboard.writeText).toHaveBeenCalledWith(
        '#FF5733\n#33FF57\n#3357FF\n#F333FF\n#33FFF3'
      );
    });
  });

  it('handles Ctrl+U keyboard shortcut to unlock all colors', () => {
    const onToggleLock = jest.fn();
    const lockedColors = new Set([0, 2, 4]);
    
    render(
      <PaletteDisplay 
        {...defaultProps} 
        lockedColors={lockedColors}
        onToggleLock={onToggleLock}
      />
    );
    
    const paletteRegion = screen.getByRole('region');
    fireEvent.keyDown(paletteRegion, { key: 'u', ctrlKey: true });
    
    expect(onToggleLock).toHaveBeenCalledTimes(3);
    expect(onToggleLock).toHaveBeenCalledWith(0);
    expect(onToggleLock).toHaveBeenCalledWith(2);
    expect(onToggleLock).toHaveBeenCalledWith(4);
  });

  it('copy all button has proper accessibility attributes', () => {
    render(<PaletteDisplay {...defaultProps} />);
    
    const copyButton = screen.getByLabelText('Copy all colors to clipboard (Ctrl+C)');
    expect(copyButton).toBeInTheDocument();
    expect(copyButton).toHaveClass('focus:outline-none', 'focus:ring-2', 'focus:ring-blue-500');
  });

  it('unlock all button appears when colors are locked', () => {
    const lockedColors = new Set([0, 2]);
    
    render(
      <PaletteDisplay 
        {...defaultProps} 
        lockedColors={lockedColors}
      />
    );
    
    const unlockButton = screen.getByLabelText('Unlock all 2 locked colors (Ctrl+U)');
    expect(unlockButton).toBeInTheDocument();
    expect(unlockButton).toHaveClass('focus:outline-none', 'focus:ring-2', 'focus:ring-yellow-500');
  });

  it('unlock all button is hidden when no colors are locked', () => {
    render(<PaletteDisplay {...defaultProps} />);
    
    expect(screen.queryByText('🔓 Unlock All')).not.toBeInTheDocument();
  });

  it('copy all button works when clicked', async () => {
    render(<PaletteDisplay {...defaultProps} />);
    
    const copyButton = screen.getByLabelText('Copy all colors to clipboard (Ctrl+C)');
    fireEvent.click(copyButton);
    
    await waitFor(() => {
      expect(navigator.clipboard.writeText).toHaveBeenCalledWith(
        '#FF5733\n#33FF57\n#3357FF\n#F333FF\n#33FFF3'
      );
    });
  });

  it('unlock all button works when clicked', () => {
    const onToggleLock = jest.fn();
    const lockedColors = new Set([1, 3]);
    
    render(
      <PaletteDisplay 
        {...defaultProps} 
        lockedColors={lockedColors}
        onToggleLock={onToggleLock}
      />
    );
    
    const unlockButton = screen.getByLabelText('Unlock all 2 locked colors (Ctrl+U)');
    fireEvent.click(unlockButton);
    
    expect(onToggleLock).toHaveBeenCalledTimes(2);
    expect(onToggleLock).toHaveBeenCalledWith(1);
    expect(onToggleLock).toHaveBeenCalledWith(3);
  });

  it('updates aria-label when locked colors change', () => {
    const { rerender } = render(<PaletteDisplay {...defaultProps} />);
    
    let paletteRegion = screen.getByRole('region');
    expect(paletteRegion).toHaveAttribute('aria-label', 'Color palette with 5 colors, 0 locked');
    
    rerender(
      <PaletteDisplay 
        {...defaultProps} 
        lockedColors={new Set([0, 2, 4])}
      />
    );
    
    paletteRegion = screen.getByRole('region');
    expect(paletteRegion).toHaveAttribute('aria-label', 'Color palette with 5 colors, 3 locked');
  });

  it('displays locked colors information', () => {
    const lockedColors = new Set([0, 2]);
    
    render(
      <PaletteDisplay 
        {...defaultProps} 
        lockedColors={lockedColors}
      />
    );
    
    expect(screen.getByText('🔒 2 colors locked')).toBeInTheDocument();
  });

  it('handles singular locked color text correctly', () => {
    const lockedColors = new Set([0]);
    
    render(
      <PaletteDisplay 
        {...defaultProps} 
        lockedColors={lockedColors}
      />
    );
    
    expect(screen.getByText('🔒 1 color locked')).toBeInTheDocument();
  });

  it('returns null when palette is empty', () => {
    const emptyPalette = {
      ...mockPalette,
      colors: [],
      names: [],
    };
    
    const { container } = render(
      <PaletteDisplay 
        {...defaultProps} 
        palette={emptyPalette}
      />
    );
    
    expect(container.firstChild).toBeNull();
  });

  it('returns null when palette is null', () => {
    const { container } = render(
      <PaletteDisplay 
        {...defaultProps} 
        palette={null as any}
      />
    );
    
    expect(container.firstChild).toBeNull();
  });

  it('has focus-within styles for keyboard navigation', () => {
    render(<PaletteDisplay {...defaultProps} />);
    
    const paletteRegion = screen.getByRole('region');
    expect(paletteRegion).toHaveClass('focus-within:ring-2', 'focus-within:ring-blue-500');
  });

  it('displays generation method and color count', () => {
    render(<PaletteDisplay {...defaultProps} />);
    
    expect(screen.getByText('Generated via random • 5 colors')).toBeInTheDocument();
  });

  it('handles different generation methods', () => {
    const conceptPalette = {
      ...mockPalette,
      metadata: {
        ...mockPalette.metadata,
        generationMethod: 'concept' as const,
      },
    };
    
    render(
      <PaletteDisplay 
        {...defaultProps} 
        palette={conceptPalette}
      />
    );
    
    expect(screen.getByText('Generated via concept • 5 colors')).toBeInTheDocument();
  });
});