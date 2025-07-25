// assets/search.js
async function performSearch(term) {
  const trimmed = term.trim();
  if (!trimmed) throw new Error('Empty input');

  const res = await fetch(`/api/search?term=${encodeURIComponent(trimmed)}`);
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.error || 'Server error');
  }

  return await res.json();
}

module.exports = { performSearch };
