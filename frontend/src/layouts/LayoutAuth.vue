<template>
	<div class="flex flex-col h-dynamic-screen sm:h-screen">
        <RouterView />
        <footer class="block text-sm text-gray-500 text-center dark:text-gray-400 m-4">
        </footer>
	</div>
</template>

<script lang="ts">
import { onMounted, defineComponent } from 'vue'

export default defineComponent({
    name: 'LayoutAuth',
    setup() {
        onMounted(() => {
        })

        return {}
    }
})
</script>