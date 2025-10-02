import { defineStore } from "pinia";

export const useLocaleStore = defineStore('locale', {
    state: () => ({
        current_langue: {
            code: 'en',
            name: 'English',
            flag: 'us'
        },
        supported_languages: [
            {
                code: 'en',
                name: 'English',
                flag: 'us'
            },
            {
                code: 'vi',
                name: 'Tiếng Việt',
                flag: 'vn'
            }
        ]
    }),
    persist: {
        storage: persistedState.localStorage,
    },
    getters: {
        currentLangue: (state) => {
            return state.current_langue;
        },
        supportedLanguages: (state) => {
            return state.supported_languages;
        },
        localize: (state) => {
            const language = state.current_langue ? state.current_langue.code : null
            return (obj) =>  {
                if (!obj) {
                    return '';
                }
                const { origin, translates } = obj;
                if (!language || !translates || translates.length == 0) {
                    return origin || '';
                }
                const translate = translates.find((t) => t.language === language);
                return translate.value || '';
            }
        }
    },
    actions: {
        setCurrentLangue(language) {
            this.current_langue = language;
        }
    },
})