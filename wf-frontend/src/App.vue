<template>
  <div id="app">
    <nav>
      <template v-if="!userStore.user">
        <RouterLink to="/login">Login</RouterLink>
        
      </template>

      <template v-else>
        <span>Hola, {{ userStore.user.username }}</span>
        <button @click="logout">Cerrar sesión</button>
      </template>
    </nav>

    <main>
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { useUserStore } from './stores/userStore'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const logout = () => {
  userStore.logout()
  router.push('/login')
}
</script>
