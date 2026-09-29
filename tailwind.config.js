/** Сборка CSS вместо Tailwind CDN — см. README-НАСТРОЙКА.md, раздел «Ускорение сайта» */
module.exports = {
  content: ['./index.html'],
  theme: {
    extend: {
      colors: {
        brand: {
          primary: '#1D4ED8',
          primaryHover: '#1E40AF',
          primaryLight: '#EFF6FF',
          dark: '#0F172A',
          bgLight: '#F8FAFC',
          card: '#FFFFFF',
          border: '#E2E8F0',
          borderDark: '#CBD5E1',
          muted: '#64748B'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'Segoe UI', 'Roboto', 'Arial', 'sans-serif']
      }
    }
  }
};
