<template>
    <div class="flex flex-col space-x-2 justify-around 
        sticky top-0 bg-black border-gray-800 border-t border-b">
      <div class="xl:block flex justify-end font-sans text-md font-normal text-white">
        <button @click="logout" class="text-lg px-4 py-2 hover:bg-slate-700 rounded-sm">Logout</button>
      </div>
    </div>
  </template>
  
<script setup lang="ts">
import { onMounted, defineComponent, computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
const router = useRouter()
const toast = useToast()

const logout = () => {
    // TODO: Add logout logic and make a universal logout function
    toast.success('Logout successful')
    // Remove token
    localStorage.removeItem('auth-token');
    // Sleep for 2 seconds
    setTimeout(() => {
        router.push('/accounts/login')
    }, 2000)

}
  </script>
  