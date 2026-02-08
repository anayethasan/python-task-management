/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // Templates at the project level
    "./**/templates/**/*.html", // Templates inside apps
    "./user/templates/**/*.html",      // User app templates (নতুন)
    "./**/templates/**/*.html",        // All app templates
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};