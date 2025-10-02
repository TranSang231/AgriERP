import 'pinia'

declare module 'pinia' {
  export interface DefineStoreOptionsBase<S, Store> {
    persist?: boolean | import('pinia-plugin-persistedstate').PersistOptions
  }
}


