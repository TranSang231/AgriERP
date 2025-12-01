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
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8008/api/v1/ecommerce',
      defaultHost: process.env.NUXT_PUBLIC_DEFAULT_HOST || 'http://localhost:8008'
    }
  },

  vite: {
    build: {
      manifest: "shop.manifest.json",
    },
    server: {
      // Allow Cloudflare tunnel host
      allowedHosts: [
        'guide-courage-headquarters-photography.trycloudflare.com',
        'assign-knowing-minds-whatever.trycloudflare.com',
        '.trycloudflare.com', // Allow all Cloudflare tunnel domains
        'localhost'
      ],
      // Disable HMR when accessed via HTTPS (Cloudflare tunnel)
      hmr: false
    }
  },

  // Allow Cloudflare tunnel host for dev server
  devServer: {
    host: '0.0.0.0', // Listen on all interfaces
    port: 3011
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

  // @ts-expect-error Provided via nuxt-svgo module runtime hooks
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