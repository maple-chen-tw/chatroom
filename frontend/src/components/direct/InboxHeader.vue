<template>
	<div class="flex flex-col md:block pl-2 pr-2 border border-[#363636]">
		<div class="flex p-3 space-x-3 sm:hover:bg-slate-1100 w-full">
				<!-- Profile Image -->
				<img 
					:src="currentUser?.profilePictureUrl"
					class="cursor-pointer h-14 w-14 rounded-full shadow-lg" />

				<div class="flex flex-col self-center space-y-2 pb-3">
					<span class="font-sans text-xs sm:text-sm font-semibold text-white self-start">
						{{ currentUser?.userName }}
					</span>
					<div class="flex flex-row space-x-1">
						<span class="font-sans text-xs font-semibold text-gray-400">
							Status - gogogo
						</span>
					</div>
				</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { 
    useRouter
} from 'vue-router'

import {
    SVGLoader
} from '@/components'

import type { 
    Viewer 
} from '@/common'

defineProps({
    currentUser: {
        type: Object as () => Viewer,
        required: true
    }
})

const emit = defineEmits(["onNewMessage"])

// Services
const router = useRouter() 

/**
 * Emit new message
 */
const emitNewMessage = () => {
    emit("onNewMessage")
}

const onPageBack = () => {
    router.back()
}
</script>