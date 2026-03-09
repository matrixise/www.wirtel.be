const purgeCSSPlugin = require('@fullhuman/postcss-purgecss').default;

const purgecss = purgeCSSPlugin({
  content: ["./hugo_stats.json"],
  defaultExtractor: (content) => {
    try {
      const els = JSON.parse(content).htmlElements;
      return [...(els.tags || []), ...(els.classes || []), ...(els.ids || [])];
    } catch (e) {
      return [];
    }
  },
  safelist: [],
});

module.exports = {
  plugins: [
    ...(process.env.HUGO_ENVIRONMENT === "production" ? [purgecss] : []),
  ],
};
