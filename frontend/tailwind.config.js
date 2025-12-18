/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        radar: {
          light: '#3b82f6',
          medium: '#2563eb',
          heavy: '#1d4ed8',
        }
      }
    },
  },
  plugins: [],
}

