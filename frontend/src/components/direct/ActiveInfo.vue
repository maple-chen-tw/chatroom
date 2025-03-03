<template>
	<div>
        會員資料設定
    </div>

	<div class="flex flex-col md:block pl-2 pr-2">
	    <div class="flex justify-between p-3 space-x-3 sm:hover:bg-slate-1100 w-full cursor-pointer">
          <div class="flex items-center space-x-3">
	    		  <!-- Profile Image -->
	    		  <img 
	    		  	:src="currentUser?.profilePictureUrl"
	    		  	class="cursor-pointer h-14 w-14 rounded-full shadow-lg" />

	    		  <!-- Username -->
	    		  <div class="flex flex-col self-center space-y-2 pb-3">
	    		  	<span class="font-sans text-xs sm:text-sm font-semibold text-white self-start">
	    		  		{{ currentUser?.userName }}
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


// Services
const router = useRouter() 


const onPageBack = () => {
    router.back()
}
</script>