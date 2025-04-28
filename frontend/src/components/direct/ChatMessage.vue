<template>
	<div
		v-if="activeConversation && !isChatLoading"
		v-for="(dialog, index) of activeConversation?.dialogs"
		:key="index"
		class="flex pt-5 space-x-2 m-2"
		:class="{
			'justify-end': dialog.isSentByViewer,
		}"
		id="index === activeConversation.dialogs.length - 1 ? 'last-element' : null"
		>
		<img 
			v-if="!dialog.isSentByViewer"
			:src="dialog.user.profilePictureUrl || defaultAvatar"
			class="cursor-pointer h-6 w-6 rounded-full shadow-lg self-end" />
			<!-- TODO: Change to active user img based on user store -->

		<p 
			v-if="dialog.content && dialog.message_type === 'text'"
			class="break-words p-3 border border-[#1f1f1f] rounded-lg text-white lg:text-sm text-xs max-w-xs"
			:class="{ 
				'm-2 bg-gray-1100 md:bg-sky-1100': dialog.isSentByViewer, 
				'md:bg-[#262626]': !dialog.isSentByViewer 
			}">
			{{ dialog.content }}
		</p>
		<img 
			v-else-if="dialog.message_type === 'image'"
			:src="dialog.content"
			class="cursor-pointer rounded-lg" />
		<audio 
			v-else-if="dialog.message_type === 'audio'"
			:src="dialog.content"
			controls
			class="w-full mt-2 rounded-lg"
		>
			Your browser does not support the audio element.
		</audio>

		<video 
			v-else-if="dialog.message_type === 'video'"
			:src="dialog.content"
			controls
			class="w-60 h-40 rounded-lg mt-2"
		>
			Your browser does not support the video tag.
		</video>

		<a 
			v-else-if="dialog.message_type === 'file'"
			:href="dialog.content"
			class="text-blue-500 underline"
			target="_blank"
		>
			Download File
		</a>

		<div
			v-if="index === activeConversation.dialogs.length - 1" 
			id="last-element">
		</div>
	</div>
</template>

<script setup lang="ts">
import defaultAvatar from '@/assets/images/404ghost.png';
import type {
    Conversation
} from '@/common'
import { onUpdated } from 'vue'

defineProps({
    activeConversation: {
        type: Object as() => Conversation,
        required: true
    },
	isChatLoading: {
		type: Boolean,
		required: true
	},
})


onUpdated(() => {
	const el = document.querySelector('#last-element')
	if (el) {
		el.scrollIntoView({ behavior: 'smooth' })
	}
})
</script>