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
      locales: [
        {
          code: 'en',
          name: 'English'
        },
        {
          code: 'vi',
          name: 'Tiếng Việt'
        }
      ],
      defaultLocale: 'en',
      vueI18n: '~/i18n.config.ts',  // Giữ nguyên: Load config từ file
      // THÊM: Các options bổ sung cho SPA và persist
      lazyMessages: false,  // Load messages ngay (không lazy để tránh delay)
      // Sửa lỗi cảnh báo bundle.optimizeTranslationDirective:
      bundle: {
        optimizeTranslationDirective: false
      },
      // THÊM: Lang detection từ cookie (hỗ trợ detectBrowserLanguage trong config)
      langDetectionRedirect: false  // Không redirect, chỉ switch locale
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

  compatibilityDate: '2025-02-19',

  hooks: {
    'modules:done'() {
      console.log('i18n module configuration applied:', {
        locales: [
          { code: 'en', name: 'English' },
          { code: 'vi', name: 'Tiếng Việt' }
        ],
        defaultLocale: 'en',
        vueI18n: '~/i18n.config.ts'
      });
    }
  }
})