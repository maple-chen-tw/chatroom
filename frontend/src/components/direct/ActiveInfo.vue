<template>
    <div class="md:grid bg-black border-l border-slate-800
    lg:basis-9/12 w-full md:h-full h-screen hidden">
        <div>
            <div class="flex flex-col pl-2 pr-2 text-white font-bold">
                會員資料設定
            </div>

            <div 
	    		class="grid grid-cols-[auto,1fr] p-3 space-x-3 w-full mr-4">
                <div class="flex items-center space-x-3">
                    <div>
	            	    <img 
	            	      	:src="currentUser?.profilePictureUrl"
	            	      	class="cursor-pointer rounded-full shadow-lg max-w-[150px] h-auto"/>
                    </div>
                    <div class="flex flex-col space-y-2">
                        <!-- Username with Edit icon -->
                        <div class="flex items-center space-x-2">
                            <span class="font-sans text-xs sm:text-sm font-semibold text-white self-start">
                                暱稱  
                            </span>
                            <span class="font-sans text-xs sm:text-sm font-semibold text-white self-start">
                                {{ currentUser?.userName }}
                            </span>
                            <button class="text-white text-xs sm:text-sm hover:bg-slate-700 p-1 rounded">
                                <i class="fas fa-pencil-alt"></i>
                            </button>
                        </div>

                        <div class="flex items-center space-x-2">
                            <span class="font-sans text-xs sm:text-sm font-semibold text-white self-start">
                                狀態  
                            </span>
                            <span class="font-sans sm:text-sm font-semibold text-white self-start overflow-hidden">
                                {{ currentUser?.status }}
                            </span>
                            <button class="text-white text-xs sm:text-sm hover:bg-slate-700 p-1 rounded">
                                <i class="fas fa-pencil-alt"></i>
                            </button>
                        </div>

                        <!-- Email -->
                        <div class="flex items-center space-x-2">
                            <span class="font-sans text-xs sm:text-sm font-semibold text-white self-start">
                                Email  
                            </span>
                            <span class="font-sans text-xs sm:text-sm font-semibold text-white self-start">
                                {{ currentUser?.email }}
                            </span>
                        </div>
                    </div>
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