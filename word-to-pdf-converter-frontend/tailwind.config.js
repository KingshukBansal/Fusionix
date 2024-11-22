module.exports = {
  darkMode: 'class', // Enables dark mode based on a class toggle
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'indigo': {
          600: '#4F46E5',
          700: '#4338CA',
        },
        'gray': {
          800: '#1F2937',
          700: '#374151',
        },
      },
    },
  },
  plugins: [],
};
