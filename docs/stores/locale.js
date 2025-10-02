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
        }
    },
    actions: {
        setCurrentLangue(language) {
            this.current_langue = language;
        }
    },
})