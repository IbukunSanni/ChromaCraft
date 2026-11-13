import { getSortedLockedIndices, restoreLockedPositions } from '@/lib/palette-locks';

const previous = {
  colors: ['#111111', '#222222', '#333333', '#444444', '#555555'],
  names: ['one', 'two', 'three', 'four', 'five'],
};

describe('getSortedLockedIndices', () => {
  it('sorts indices and drops ones outside the palette', () => {
    expect(getSortedLockedIndices(new Set([3, 0, 9]), previous)).toEqual([0, 3]);
  });

  it('returns an empty list without a palette', () => {
    expect(getSortedLockedIndices(new Set([1]), null)).toEqual([]);
  });
});

describe('restoreLockedPositions', () => {
  it('returns the generated palette unchanged when nothing is locked', () => {
    const generated = { colors: ['#a', '#b'], names: ['a', 'b'] };
    expect(restoreLockedPositions(generated, [], previous)).toEqual({
      colors: ['#a', '#b'],
      names: ['a', 'b'],
      lockedIndices: [],
    });
  });

  it('keeps a locked color at its original position', () => {
    // Backend puts the locked color (#222222) first.
    const generated = {
      colors: ['#222222', '#aaaaaa', '#bbbbbb', '#cccccc', '#dddddd'],
      names: ['two (server)', 'a', 'b', 'c', 'd'],
    };

    expect(restoreLockedPositions(generated, [1], previous)).toEqual({
      colors: ['#aaaaaa', '#222222', '#bbbbbb', '#cccccc', '#dddddd'],
      names: ['a', 'two (server)', 'b', 'c', 'd'],
      lockedIndices: [1],
    });
  });

  it('keeps several locked colors in place', () => {
    const generated = {
      colors: ['#222222', '#555555', '#aaaaaa', '#bbbbbb', '#cccccc'],
      names: ['two', 'five', 'a', 'b', 'c'],
    };

    const restored = restoreLockedPositions(generated, [1, 4], previous);

    expect(restored.colors).toEqual(['#aaaaaa', '#222222', '#bbbbbb', '#cccccc', '#555555']);
    expect(restored.lockedIndices).toEqual([1, 4]);
  });

  it('keeps locked colors beyond the generated length without gaps', () => {
    const longPrevious = {
      colors: [...previous.colors, '#666666', '#777777'],
      names: [...previous.names, 'six', 'seven'],
    };
    const generated = {
      colors: ['#777777', '#aaaaaa', '#bbbbbb', '#cccccc', '#dddddd'],
      names: ['seven', 'a', 'b', 'c', 'd'],
    };

    const restored = restoreLockedPositions(generated, [6], longPrevious);

    expect(restored.colors).toEqual(['#aaaaaa', '#bbbbbb', '#cccccc', '#dddddd', '#777777']);
    expect(restored.lockedIndices).toEqual([4]);
    expect(restored.colors[restored.lockedIndices[0]]).toBe('#777777');
  });
});
