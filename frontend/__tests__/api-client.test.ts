/**
 * Contract tests: the API client must send payloads in the shape the
 * FastAPI backend (backend/models, backend/routes) expects.
 */

import { APIClient } from '@/lib/api-client';

type MockResponseInit = { contentType: string; body: unknown };

function mockResponse({ contentType, body }: MockResponseInit) {
  return {
    ok: true,
    status: 200,
    headers: { get: () => contentType },
    json: async () => body,
    blob: async () => body,
    text: async () => String(body),
  };
}

describe('APIClient request formats', () => {
  const fetchMock = jest.fn();
  const client = new APIClient('http://api.test/');

  beforeEach(() => {
    fetchMock.mockReset();
    global.fetch = fetchMock as unknown as typeof fetch;
  });

  it('sends snake_case fields to /generate/random', async () => {
    fetchMock.mockResolvedValue(
      mockResponse({
        contentType: 'application/json',
        body: { colors: [], names: [], harmony_info: {} },
      })
    );

    await client.generateRandomPalette({
      locked_colors: ['#FF5733'],
      harmony_type: 'split_complementary',
    });

    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toBe('http://api.test/generate/random');
    expect(init.method).toBe('POST');
    expect(JSON.parse(init.body)).toEqual({
      locked_colors: ['#FF5733'],
      harmony_type: 'split_complementary',
    });
  });

  it('sends one "colors" form field per color to /export-png', async () => {
    fetchMock.mockResolvedValue(
      mockResponse({ contentType: 'image/png', body: 'png-bytes' })
    );

    await client.exportPNG({ colors: ['#FF0000', '#00FF00', '#0000FF'] });

    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toBe('http://api.test/export-png');
    expect(init.body).toBeInstanceOf(FormData);
    expect((init.body as FormData).getAll('colors')).toEqual([
      '#FF0000',
      '#00FF00',
      '#0000FF',
    ]);
    // The browser must set the multipart boundary itself.
    expect(init.headers['Content-Type']).toBeUndefined();
  });

  it('only exposes methods for implemented backend routes', () => {
    const methods = Object.getOwnPropertyNames(APIClient.prototype);
    expect(methods).not.toContain('editPalette');
    expect(methods).not.toContain('validateAccessibility');
    expect(methods).not.toContain('exportJSON');
    expect(methods).not.toContain('exportASE');
  });
});
