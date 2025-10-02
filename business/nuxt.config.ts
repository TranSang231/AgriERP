// https://nuxt.com/docs/api/configuration/nuxt-config
// https://nuxt.com/docs/api/nuxt-config

export default defineNuxtConfig({
  // Server Side Rendering(SSR): true;  Client Side Rendering (Single Page Applications(SPA)): false
  ssr: false,

  devtools: { enabled: true },

  css: [
    '~/assets/scss/element/index.scss',
    '~/assets/css/main.css',
  ],

  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {}
    }
  },

  app: {
    buildAssetsDir: "/business/",
  },

  experimental: {
    appManifest: false,
  },

  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8008/api/v1',
      defaultHost: 'http://localhost:8008'
    }
  },

  vite: {
    build: {
      manifest: "business.manifest.json"
    },
  },

  modules: [
    '@nuxtjs/i18n',
    '@pinia/nuxt',
    '@pinia-plugin-persistedstate/nuxt',
    '@nuxtjs/color-mode',
    '@element-plus/nuxt',
    'nuxt-svgo',
    'nuxt-lodash',
  ],

  i18n: {
    strategy: 'no_prefix',
    defaultLocale: 'en',
    vueI18n: './i18n.config.ts'
  },

  pinia: {
    storesDirs: ['./stores/**', './stores/oauth/**'],
  },

  piniaPersistedstate: {
    storage: 'localStorage'
  },

  elementPlus: {
    importStyle: false
  },

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