<template>
  <div class="login">
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <input v-model="username" placeholder="Username" required />
      <input type="password" v-model="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
    <RouterLink to="/register">Register</RouterLink>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '../stores/userStore'
import { useRouter } from 'vue-router'
import '../assets/Login.css' 

const username = ref('')
const password = ref('')
const error = ref(null)
const userStore = useUserStore()
const router = useRouter()

const handleLogin = async () => {
  try {
    error.value = null

    const tokenData = await userStore.login(username.value, password.value)
    userStore.token = tokenData.access_token
    localStorage.setItem('token', tokenData.access_token)

    const user = await userStore.fetchCurrentUser()

    if (user.is_admin) {
      router.push('/admin/dashboard')
    } else {
      router.push('/user/dashboard')
    }
  } catch (err) {
    error.value = 'Error al iniciar sesión. Verifica tus credenciales.'
    console.error(err)
  }
}
</script>
