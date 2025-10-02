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
        'display': ["Poppins", " Arial", " sans-serif"],
        'body': ["Poppins", " Arial", " sans-serif"],
      },
      colors: {
        'gray-25': '#FFF',
        'gray-75': '#F3F3F3',
        'gray-100': '#E9E9E9',
        'gray-200': '#E1E1E1',
        'gray-400': '#C6C6C6',
        'primary': '#B62132',
        'on-primary': '#FFFFFF',
        'secondary': '#B61362',
        'surface': '#FAFFE5',
        'surface-dim': '#DED8E1',
        'tertiary-light': '#F6F6FF',
        'tertiary-60': '#4E57A9',
        'default-layout': '#E4ECF2'
      },
      opacity: {
        '50': '0.5',
      },
    }
  },
  plugins: [],
}

