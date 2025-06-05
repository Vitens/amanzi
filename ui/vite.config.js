import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

import fs from 'fs'

let version = fs.readFileSync('../VERSION', 'utf8')

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  esbuild: {
    supported: {
      'top-level-await': true
    }
  },
  define: {
    '__VERSION__': JSON.stringify(version)
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '@@': fileURLToPath(new URL('../', import.meta.url))
    }
  },
})