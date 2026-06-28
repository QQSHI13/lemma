/**
 * Theme preference fix for DocsForge / MkDocs Material.
 *
 * Problem: Material's matchMedia listeners override manual theme toggle
 * when system theme changes. This is annoying for users who prefer a
 * fixed theme.
 *
 * Solution:
 * 1. No media queries in palette config (no matchMedia listeners).
 * 2. On first visit, detect system preference and store it.
 * 3. Manual toggles update the stored preference.
 * 4. Stored preference persists across sessions.
 */
(function () {
  const STORAGE_KEY = "__palette";

  // First visit: no stored preference yet
  if (!localStorage.getItem(STORAGE_KEY)) {
    var prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    var palette = { index: prefersDark ? 1 : 0 };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(palette));
  }
})();
