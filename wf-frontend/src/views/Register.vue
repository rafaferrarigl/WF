<template>
  <div class="register">
    <h1>Register</h1>
    <form @submit.prevent="handleRegister">
      <input v-model="username" placeholder="Username" required />
      <input v-model="email" placeholder="Email" type="email" required />
      <input type="password" v-model="password" placeholder="Password" required />
      <button type="submit">Register</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">User registered successfully!</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '../stores/userStore'

const username = ref('')
const email = ref('')
const password = ref('')
const error = ref(null)
const success = ref(false)
const userStore = useUserStore()

const handleRegister = async () => {
  try {
    error.value = null
    success.value = false
    await userStore.register(username.value, email.value, password.value)
    success.value = true
  } catch (err) {
    error.value = err
  }
}
</script>
