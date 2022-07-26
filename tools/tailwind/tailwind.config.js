/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['tailwind.html', 'prose.html'],
  theme: {
    extend: {
      typography: (theme) => ({
        DEFAULT: {
          css: {
            /* Adjustments for Inter */
            'h1, h2, h3': {
              letterSpacing: '-0.025em',
            },
          }
        }
      })
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    // TODO
    // require('@tailwindcss/line-clamp'),
    // TODO
    // require('@tailwindcss/aspect-ratio'),
  ]
}
