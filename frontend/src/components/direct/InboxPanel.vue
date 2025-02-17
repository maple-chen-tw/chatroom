<template>
	<div 
		:class="{ 'hidden': activeConversation }"
		class="bg-black sm:basis-1/2 lg:basis-2/5 md:block h-full flex flex-col">
		<!-- Inbox Header  -->
		<InboxHeader 
			:current-user="currentUser" />

		<!-- Inbox Rendering -->
		<div class="overflow-auto lg:max-h-[850px]">
            <div v-if="activePanel === 'user'">
			<!-- Inbox items-->
			<InboxFriends 
				:active-conversation-id="activeConversation?.uuid"
				:conversations="conversations"
				@on-select-conversation="$emit('onSelectConversation', $event as Conversation)" />
            </div>

            <div v-if="activePanel === 'chat'">
			<!-- Inbox items-->
			<InboxMessages 
				:active-conversation-id="activeConversation?.uuid"
				:conversations="conversations"
				@on-select-conversation="$emit('onSelectConversation', $event as Conversation)" />
            </div>

            <div v-if="activePanel === 'plus'">
			<!-- Inbox items-->
                <div>user-plus</div>
            </div>

            <div v-if="activePanel === 'options'">
			<!-- Inbox items-->
                <div>options</div>
            </div>

		</div>

	</div>

</template>

<script setup lang="ts">
import {
    InboxMessages,
    InboxFriends,
    InboxHeader
} from '@/components'

import type {
    Conversation,
    Viewer
} from '@/common'

defineProps({
    conversations: {
        type: Object as() => Conversation[] | undefined,
        required: true
    },
    activeConversation: {
        type: Object as() => Conversation | undefined,
        required: true
    },
    currentUser: {
        type: Object as() => Viewer,
        required: true
    },
    activePanel: {
        type: String,
        required: true
    }
})

const emit = defineEmits(['onSelectConversation'])
</script>