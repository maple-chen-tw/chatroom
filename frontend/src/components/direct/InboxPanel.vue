<template>
	<div 
		:class="{ 'hidden': activeConversation }"
		class="bg-black sm:basis-1/2 lg:basis-2/5 md:block h-full flex flex-col">
		<!-- Inbox Header  -->
		<InboxHeader 
			:current-user="currentUser" />

		<!-- Inbox Rendering -->
		<div class="overflow-auto lg:max-h-[850px]">

            <div v-if="activePanel === 'plus'">
			<!-- plus -->
            <InboxAddFriends
                :invitations="invitations"
                :conversations="conversations"
                @update-invitations="updateInvitations"
                />
            </div>
            <div v-else-if="activePanel === 'user'">
			<!-- user -->
			<InboxFriends 
				:active-conversation-id="activeConversation?.uuid"
				:conversations="conversations"
				@on-select-conversation="$emit('onSelectConversation', $event as Conversation)" />
            </div>

            <div v-else>
			<!-- chat -->
			<InboxMessages 
				:active-conversation-id="activeConversation?.uuid"
				:conversations="conversations"
				@on-select-conversation="$emit('onSelectConversation', $event as Conversation)" />
            </div>

		</div>

	</div>

</template>

<script setup lang="ts">
import {
    InboxMessages,
    InboxFriends,
    InboxHeader,
    InboxAddFriends,
    ActiveInfo
} from '@/components'

import type {
    Conversation,
    Invitation,
    Viewer
} from '@/common'

const props = defineProps({
    conversations: {
        type: Array as() => Conversation[] | undefined,
        required: false
    },
    invitations: {
        type: Array as() => Invitation[] | undefined,
        required: false
    },
    activeConversation: {
        type: Object as() => Conversation | undefined,
        required: false
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

const emit = defineEmits(['onSelectConversation', 'update-invitations'])
const updateInvitations = (newInvitations: Invitation[]) => {
    emit('update-invitations', newInvitations)
}

</script>