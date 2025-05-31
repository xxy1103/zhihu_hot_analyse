import './css/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#667eea',
          secondary: '#f093fb',
          accent: '#4ecdc4',
          error: '#ff6b6b',
          warning: '#feca57',
          info: '#48cae4',
          success: '#06ffa5',
          surface: '#ffffff',
          background: '#f8fbff',
          'surface-variant': '#f1f5f9',
          'on-surface-variant': '#64748b',
          'primary-container': '#e0e7ff',
          'secondary-container': '#fce7f3',
          'accent-container': '#ccf7f0',
        }
      },
      dark: {
        colors: {
          primary: '#818cf8',
          secondary: '#a78bfa',
          accent: '#22d3ee',
          error: '#f87171',
          warning: '#fbbf24',
          info: '#60a5fa',
          success: '#34d399',
          surface: '#1e293b',
          background: '#0f172a',
          'surface-variant': '#334155',
          'on-surface-variant': '#94a3b8',
          'primary-container': '#312e81',
          'secondary-container': '#581c87',
          'accent-container': '#155e75',
        }
      }
    }
  }
})

const app = createApp(App)

app.use(router)
app.use(vuetify)

app.mount('#app')
