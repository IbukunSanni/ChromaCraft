/**
 * Tests for ColorSwatch component
 */

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ColorSwatch from '@/components/ColorSwatch';

// Mock the clipboard API
Object.assign(navigator, {
  clipboard: {
    writeText: jest.fn(() => Promise.resolve()),
  },
});

describe('ColorSwatch', () => {
  const defaultProps = {
    color: '#FF5733',
    name: 'Red Orange',
    locked: false,
    index: 0,
    onToggleLock: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders color swatch with correct color and name', () => {
    render(<ColorSwatch {...defaultProps} />);
    
    expect(screen.getByText('#FF5733')).toBeInTheDocument();
    expect(screen.getByText('Red Orange')).toBeInTheDocument();
  });

  it('displays unlock icon when not locked', () => {
    render(<ColorSwatch {...defaultProps} />);
    
    const lockButton = screen.getByLabelText('Lock color');
    expect(lockButton).toBeInTheDocument();
    expect(lockButton).toHaveTextContent('🔓');
  });

  it('displays lock icon when locked', () => {
    render(<ColorSwatch {...defaultProps} locked={true} />);
    
    const lockButton = screen.getByLabelText('Unlock color');
    expect(lockButton).toBeInTheDocument();
    expect(lockButton).toHaveTextContent('🔒');
  });

  it('calls onToggleLock when lock button is clicked', () => {
    const onToggleLock = jest.fn();
    render(<ColorSwatch {...defaultProps} onToggleLock={onToggleLock} />);
    
    const lockButton = screen.getByLabelText('Lock color');
    fireEvent.click(lockButton);
    
    expect(onToggleLock).toHaveBeenCalledWith(0);
  });

  it('copies color to clipboard when color area is clicked', async () => {
    render(<ColorSwatch {...defaultProps} />);
    
    const colorArea = screen.getByTitle('Click to copy #FF5733');
    fireEvent.click(colorArea);
    
    await waitFor(() => {
      expect(navigator.clipboard.writeText).toHaveBeenCalledWith('#FF5733');
    });
  });

  it('shows copied feedback after copying', async () => {
    render(<ColorSwatch {...defaultProps} />);
    
    const colorArea = screen.getByTitle('Click to copy #FF5733');
    fireEvent.click(colorArea);
    
    await waitFor(() => {
      expect(screen.getByText('Copied!')).toBeInTheDocument();
    });
  });

  it('shows locked indicator when color is locked', () => {
    render(<ColorSwatch {...defaultProps} locked={true} />);
    
    // The locked indicator should be visible
    const lockedIndicators = screen.getAllByText('🔒');
    expect(lockedIndicators.length).toBeGreaterThan(0);
  });

  it('displays accessibility information when provided', () => {
    const accessibilityInfo = {
      contrastRatio: 4.5,
      wcagLevel: 'AA' as const,
    };
    
    render(
      <ColorSwatch 
        {...defaultProps} 
        showAccessibility={true}
        accessibilityInfo={accessibilityInfo}
      />
    );
    
    expect(screen.getByText('Contrast: 4.50')).toBeInTheDocument();
    expect(screen.getByText('WCAG AA')).toBeInTheDocument();
  });

  it('applies correct styling for different WCAG levels', () => {
    const testCases = [
      { wcagLevel: 'fail' as const, expectedClass: 'text-red-500' },
      { wcagLevel: 'AA' as const, expectedClass: 'text-yellow-500' },
      { wcagLevel: 'AAA' as const, expectedClass: 'text-green-500' },
    ];

    testCases.forEach(({ wcagLevel, expectedClass }) => {
      const { rerender } = render(
        <ColorSwatch 
          {...defaultProps} 
          showAccessibility={true}
          accessibilityInfo={{ contrastRatio: 4.5, wcagLevel }}
        />
      );
      
      const wcagElement = screen.getByText(`WCAG ${wcagLevel}`);
      expect(wcagElement).toHaveClass(expectedClass);
      
      rerender(<div />); // Clear for next test
    });
  });

  it('handles missing color name gracefully', () => {
    render(<ColorSwatch {...defaultProps} name="" />);
    
    expect(screen.getByText('Unnamed')).toBeInTheDocument();
  });

  it('prevents event propagation when lock button is clicked', () => {
    const onToggleLock = jest.fn();
    const onColorClick = jest.fn();
    
    render(
      <div onClick={onColorClick}>
        <ColorSwatch {...defaultProps} onToggleLock={onToggleLock} />
      </div>
    );
    
    const lockButton = screen.getByLabelText('Lock color');
    fireEvent.click(lockButton);
    
    expect(onToggleLock).toHaveBeenCalledWith(0);
    expect(onColorClick).not.toHaveBeenCalled();
  });

  it('applies correct background color to color display', () => {
    render(<ColorSwatch {...defaultProps} />);
    
    const colorArea = screen.getByTitle('Click to copy #FF5733');
    expect(colorArea).toHaveStyle('background-color: #FF5733');
  });

  it('has proper accessibility attributes', () => {
    render(<ColorSwatch {...defaultProps} />);
    
    const swatch = screen.getByTestId('color-swatch-0');
    expect(swatch).toHaveAttribute('tabIndex', '0');
    expect(swatch).toHaveAttribute('data-swatch-index', '0');
    expect(swatch).toHaveAttribute('aria-label');
    expect(swatch.getAttribute('aria-label')).toContain('#FF5733');
    expect(swatch.getAttribute('aria-label')).toContain('Red Orange');
    expect(swatch.getAttribute('aria-label')).toContain('Unlocked');
  });

  it('updates aria-label when locked state changes', () => {
    const { rerender } = render(<ColorSwatch {...defaultProps} />);
    
    let swatch = screen.getByTestId('color-swatch-0');
    expect(swatch.getAttribute('aria-label')).toContain('Unlocked');
    
    rerender(<ColorSwatch {...defaultProps} locked={true} />);
    
    swatch = screen.getByTestId('color-swatch-0');
    expect(swatch.getAttribute('aria-label')).toContain('Locked');
  });

  it('handles keyboard navigation - Enter key copies color', async () => {
    render(<ColorSwatch {...defaultProps} />);
    
    const swatch = screen.getByTestId('color-swatch-0');
    fireEvent.keyDown(swatch, { key: 'Enter' });
    
    await waitFor(() => {
      expect(navigator.clipboard.writeText).toHaveBeenCalledWith('#FF5733');
    });
  });

  it('handles keyboard navigation - Space key copies color', async () => {
    render(<ColorSwatch {...defaultProps} />);
    
    const swatch = screen.getByTestId('color-swatch-0');
    fireEvent.keyDown(swatch, { key: ' ' });
    
    await waitFor(() => {
      expect(navigator.clipboard.writeText).toHaveBeenCalledWith('#FF5733');
    });
  });

  it('handles keyboard navigation - L key toggles lock', () => {
    const onToggleLock = jest.fn();
    render(<ColorSwatch {...defaultProps} onToggleLock={onToggleLock} />);
    
    const swatch = screen.getByTestId('color-swatch-0');
    fireEvent.keyDown(swatch, { key: 'l' });
    
    expect(onToggleLock).toHaveBeenCalledWith(0);
  });

  it('handles keyboard navigation - L key (uppercase) toggles lock', () => {
    const onToggleLock = jest.fn();
    render(<ColorSwatch {...defaultProps} onToggleLock={onToggleLock} />);
    
    const swatch = screen.getByTestId('color-swatch-0');
    fireEvent.keyDown(swatch, { key: 'L' });
    
    expect(onToggleLock).toHaveBeenCalledWith(0);
  });

  it('lock button responds to keyboard activation', () => {
    const onToggleLock = jest.fn();
    render(<ColorSwatch {...defaultProps} onToggleLock={onToggleLock} />);
    
    const lockButton = screen.getByLabelText('Lock color');
    fireEvent.keyDown(lockButton, { key: 'Enter' });
    
    expect(onToggleLock).toHaveBeenCalledWith(0);
  });

  it('lock button responds to space key', () => {
    const onToggleLock = jest.fn();
    render(<ColorSwatch {...defaultProps} onToggleLock={onToggleLock} />);
    
    const lockButton = screen.getByLabelText('Lock color');
    fireEvent.keyDown(lockButton, { key: ' ' });
    
    expect(onToggleLock).toHaveBeenCalledWith(0);
  });

  it('has focus styles for accessibility', () => {
    render(<ColorSwatch {...defaultProps} />);
    
    const swatch = screen.getByTestId('color-swatch-0');
    expect(swatch).toHaveClass('focus:outline-none', 'focus:ring-2', 'focus:ring-blue-500');
    
    const lockButton = screen.getByLabelText('Lock color');
    expect(lockButton).toHaveClass('focus:outline-none', 'focus:ring-2', 'focus:ring-blue-500');
  });
});