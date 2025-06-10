<template>
    <div
        class="md:grid place-content-center bg-black border-l border-slate-800
        lg:basis-9/12 w-full md:h-full h-screen hidden text-center">
        <div class="flex flex-col space-y-1 text-center">
                <img 
                src="@/assets/images/chatify_w.png" style="width:50%;display:block;margin:auto;"/>

            <div class="text-white md:text-xl text-xs pt-3 ">
                朋友 404 Not Found？
            </div>

            <div class="text-[#a8a8a8] lg:text-sm text-xs pb-3">
                聊天要緣分，朋友要自己加，<br>
                緣分還沒來？那就主動一點，去找人聊聊吧～ 
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