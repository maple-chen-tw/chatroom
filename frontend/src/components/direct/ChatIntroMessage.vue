<template>
    <div
        class="md:grid place-content-center bg-black border-l border-slate-800
        lg:basis-9/12 w-full md:h-full h-screen hidden text-center">
        <div class="flex flex-col space-y-1 text-center">
                <img 
                src="@/assets/images/404chat_white.png" style="width:50%;display:block;margin:auto;"/>

            <div class="text-white md:text-xl text-xs pt-3 ">
                Your messages
            </div>

            <div class="text-[#a8a8a8] lg:text-sm text-xs pb-3">
                Send private photos and messages to a friend or group.
            </div>

        </div>
    </div>

</template>

<script setup lang="ts">
import {
    SVGLoader
} from '@/components'
defineEmits(['onSendMessageModal'])
</script>