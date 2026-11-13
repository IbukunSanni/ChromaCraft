/**
 * Helpers for keeping locked colors in place across regeneration.
 *
 * POST /generate/random does not know palette positions: it returns the
 * locked colors (in the order they were sent) in the first N slots, followed
 * by newly generated colors. The UI tracks locks by position, so the client
 * restores each locked color to the slot the user locked it in.
 */

export interface PaletteColors {
  colors: string[];
  names: string[];
}

export interface RestoredPalette extends PaletteColors {
  /** Positions of the locked colors in the restored palette. */
  lockedIndices: number[];
}

/**
 * Indices of locked colors that exist in the palette, in ascending order.
 * This is also the order in which locked colors are sent to the backend.
 */
export function getSortedLockedIndices(
  lockedIndices: Iterable<number>,
  palette: PaletteColors | null | undefined
): number[] {
  if (!palette) return [];
  return Array.from(lockedIndices)
    .filter((index) => index >= 0 && index < palette.colors.length)
    .sort((a, b) => a - b);
}

/**
 * Place locked colors back at their original positions and fill the
 * remaining positions with the newly generated colors.
 *
 * @param generated Backend response: locked colors first, then new colors.
 * @param lockedIndices Ascending positions of the locked colors in `previous`.
 * @param previous The palette shown before regeneration.
 */
export function restoreLockedPositions(
  generated: PaletteColors,
  lockedIndices: number[],
  previous: PaletteColors
): RestoredPalette {
  if (lockedIndices.length === 0) {
    return {
      colors: [...generated.colors],
      names: [...generated.names],
      lockedIndices: [],
    };
  }

  const lockedOrder = new Map(lockedIndices.map((index, order) => [index, order]));
  const freeColors = generated.colors.slice(lockedIndices.length);
  const freeNames = generated.names.slice(lockedIndices.length);
  const slotCount = Math.max(
    generated.colors.length,
    lockedIndices[lockedIndices.length - 1] + 1
  );

  const colors: string[] = [];
  const names: string[] = [];
  const restoredLocked: number[] = [];

  for (let slot = 0; slot < slotCount; slot++) {
    const order = lockedOrder.get(slot);
    if (order !== undefined) {
      restoredLocked.push(colors.length);
      colors.push(previous.colors[slot]);
      names.push(generated.names[order] ?? previous.names[slot] ?? '');
    } else if (freeColors.length > 0) {
      colors.push(freeColors.shift() as string);
      names.push(freeNames.shift() ?? '');
    }
  }

  return { colors, names, lockedIndices: restoredLocked };
}
