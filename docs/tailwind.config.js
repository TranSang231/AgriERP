/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
    "./error.vue",
  ],
  theme: {
    extend: {
      fontFamily: {
        'heading1': "Poppins, Arial, sans-serif",
        'paragraph': "Poppins, Arial, sans-serif",
      },
      fontSize: {
        'heading1': "48px",
        'paragraph': "16px"
      },
      colors: {
        'primary': '#B62132',
        'secondary': '#FFFFFF',
        'heading1': '#000000',
        'paragraph': '#000000'
      },
      boxShadow: {
        'custom-shadow': '0 20px 30px -10px rgba(29, 1, 80, .1)',
      }
    }
  },
  darkMode: ['class', '[data-theme="dark"]'],
  plugins: [],
}

