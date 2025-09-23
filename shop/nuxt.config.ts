// https://nuxt.com/docs/api/configuration/nuxt-config
// https://nuxt.com/docs/api/nuxt-config
import { defineNuxtConfig } from 'nuxt/config'

export default defineNuxtConfig({
  ssr: false,

  devtools: { enabled: true },

  css: [
    '~/assets/css/main.css',
  ],

  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {}
    }
  },

  app: {
    buildAssetsDir: "/shop/",
  },

  experimental: {
    appManifest: false,
  },

  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8008/api/v1/ecommerce',
      defaultHost: 'http://localhost:8008'
    }
  },

  vite: {
    build: {
      manifest: "shop.manifest.json",
    },
  },

  modules: [
    ['@nuxtjs/i18n', {
      strategy: 'no_prefix',
      defaultLocale: 'en',
      vueI18n: './i18n.config.ts',
      bundle: { optimizeTranslationDirective: false },
    }],
    ['@pinia/nuxt', { storesDirs: ['./stores/**'] }],
    ['@pinia-plugin-persistedstate/nuxt', { storage: 'localStorage' }],
    'nuxt-svgo',
    'nuxt-lodash',
  ],


  svgo: {
    defaultImport: 'component',
    global: false,
  },

  lodash: {
    prefix: "_",
    prefixSkip: false,
    upperAfterPrefix: false,
  },

  compatibilityDate: '2025-02-19'
})


