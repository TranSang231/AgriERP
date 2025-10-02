import en from '../locales/en';
import vi from '../locales/vi';
export default defineI18nConfig(() => {
  return {
    legacy: false,
    locale: 'en',
    messages: {
      en,
      vi
    },
    langDir: './locales'
  };
});