import { defineStore } from 'pinia'
import api from '../api/axios'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    token: null,
  }),
  actions: {
    async login(username, password) {
      const formData = new FormData()
      formData.append("username", username)
      formData.append("password", password)

      const response = await api.post("http://localhost:8000/auth/login", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })

      // Guardamos token
      this.token = response.data.access_token
      api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`

      // Obtenemos info del usuario
      await this.fetchCurrentUser()

      return this.user
    },

    async fetchCurrentUser() {
      try {
        const response = await api.get("http://localhost:8000/auth/me")
        this.user = response.data  // ahora tu backend devuelve el user directamente
        return this.user
      } catch (error) {
        console.error('Error obteniendo el usuario actual:', error)
        throw error
      }
    },

    logout() {
      this.user = null
      this.token = null
      delete api.defaults.headers.common['Authorization']
    },

    async register(username, email, password, isAdmin = false) {
      try {
        await api.post('/auth/', { username, email, password, is_admin: isAdmin })
      } catch (error) {
        throw error.response?.data?.detail || error.message
      }
    }
  }
})
