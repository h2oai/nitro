/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['tailwind.html', 'prose.html'],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/typography'),
    // TODO
    // require('@tailwindcss/line-clamp'),
    // TODO
    // require('@tailwindcss/aspect-ratio'),
  ]
}
