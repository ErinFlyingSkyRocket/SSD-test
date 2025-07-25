// test/search.test.js
const { performSearch } = require('../assets/search');

global.fetch = jest.fn();

describe('performSearch()', () => {
  beforeEach(() => fetch.mockClear());

  it('throws error for empty input', async () => {
    await expect(performSearch('')).rejects.toThrow('Empty input');
  });

  it('returns filtered results', async () => {
    fetch.mockResolvedValue({
      ok: true,
      json: async () => ['Flask']
    });

    const result = await performSearch('fl');
    expect(result).toEqual(['Flask']);
  });

  it('throws error if backend rejects input', async () => {
    fetch.mockResolvedValue({
      ok: false,
      json: async () => ({ error: 'Potential SQL injection detected' })
    });

    await expect(performSearch('DROP')).rejects.toThrow('Potential SQL injection detected');
  });
});
