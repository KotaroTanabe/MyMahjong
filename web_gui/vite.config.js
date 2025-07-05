import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  root: '.',
  base: '/MyMahjong/',
  plugins: [react()],
  build: {
    outDir: 'dist',
  },
})
