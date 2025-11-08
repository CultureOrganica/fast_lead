import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  build: {
    lib: {
      entry: resolve(__dirname, 'src/index.ts'),
      name: 'FastLeadWidget',
      formats: ['es', 'umd'],
      fileName: (format) => `fast-lead-widget.${format}.js`,
    },
    rollupOptions: {
      output: {
        // Inline all assets to create a single file
        inlineDynamicImports: true,
        assetFileNames: 'fast-lead-widget.[ext]',
      },
    },
    // Minimize for production
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
      },
    },
    // Output to dist/
    outDir: 'dist',
    emptyOutDir: true,
  },
  define: {
    'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'production'),
  },
});
