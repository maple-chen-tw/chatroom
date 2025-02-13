<template>
    <div class="flex bottom-0 space-x-3">
        <div class="flex bg-black px-10 lg:h-16 w-full justify-between" >
            <div class="cursor-pointer flex items-center mx-3"
            @click="onIconClick('user')">
                <span class="relative">
                    <SVGLoader 
                    :icon="'user'"  
                    />
    			</span>
    		</div>
            <div class="cursor-pointer flex items-center mx-3"
            @click="onIconClick('chat')">
                <span class="relative">
                    <SVGLoader 
                    :icon="'chat'"  
                    />
    			</span>
    		</div> 
            <div class="cursor-pointer flex items-center mx-3"
                @click="onIconClick('plus')">
                <span class="relative">
                    <SVGLoader 
                    :icon="'user-plus'"  
                    />
    			</span>
    		</div> 
            <div class="cursor-pointer flex items-center mx-3"
                @click="onIconClick('options')">
    			<span class="relative">
                    <SVGLoader 
                    :icon="'profile-options'"  
                    />
    			</span>
    		</div> 
        </div>
    </div>
</template>

<script setup lang="ts">
import {
    ref
} from 'vue'

import {
    SVGLoader
} from '@/components'
const emit = defineEmits(['icon-click'])
const onIconClick = (panel: string) => {
  emit('icon-click', panel)
}

</script>