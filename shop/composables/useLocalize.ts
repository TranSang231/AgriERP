import { useLocaleStore } from '~/stores/locale'

export const useLocalize = () => {
  const localeStore = useLocaleStore()
  
  return {
    localize: localeStore.localize,
    currentLanguage: localeStore.currentLangue,
    supportedLanguages: localeStore.supportedLanguages,
    setLanguage: localeStore.setCurrentLangue
  }
}
