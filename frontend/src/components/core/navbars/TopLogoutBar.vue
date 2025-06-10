<template>
    <div class="flex flex-col space-x-2 justify-around 
        sticky top-0 bg-black border-gray-800 border-t border-b">
      <div class="draggable no-draggable-children sticky top-0 p-3 flex items-center justify-between z-20 h-header-height
      font-semibold bg-token-main-surface-primary [view-transition-name:var(--vt-page-header)] select-none *:pointer-events-auto motion-safe:transition max-md:hidden @[84rem]/thread:absolute @[84rem]/thread:start-0 @[84rem]/thread:end-0 @[84rem]/thread:bg-transparent @[84rem]/thread:shadow-none! [box-shadow:var(--sharp-edge-top-shadow-placeholder)]">
        <div class="xl:block flex font-sans text-md font-normal text-white">
          <img 
              class="w-35 h-10"
              src="@/assets/images/chatify_w.png" />
        </div>

        <div class="xl:block flex justify-end font-sans text-md font-normal text-white">
          <button @click="logout" class="text-lg px-4 py-2 hover:bg-slate-700 rounded-sm z-30">Logout</button>
        </div>
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
  