/** @type {import('tailwindcss').Config} */

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",]
  ,
  theme: {
    extend: {
      gridTemplateRows: {
        '12': 'repeat(12, minmax(0, 1fr))',
      },

      fontFamily: {
        title: ["Fredoka", "sans-serif"],
        subtitle: ["Bubblegum Sans", "sans-serif"],
        
      },
      backgroundImage: {
        "lang-bg": "url('./src/assets/background.png')",
      },
      colors: {
        "pink": "#f5224c",
        "orange": "#fd5600",
        "purple": "#7d42fd",
        "pink-500": "#ec4899",
        "purple-500": "#a855f7",
        "rose-500": "#f43f5e",
        "indigo-500": "#6366f1",
      }

    },
  },
  plugins: [],
}

