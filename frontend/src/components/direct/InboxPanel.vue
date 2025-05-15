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
                @update-invitations="updatedInvitations"
                @update-conversations="updatedConversations"
                @update-chatrooms="updatedChatrooms"
                />
            </div>
            <div v-else-if="activePanel === 'user'">
			<!-- user -->
			<InboxFriends
				:active-conversation-id="activeConversation?.uuid"
                :chatroomWithFriends="chatroomWithFriends"
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
    Viewer,
    Friend,
    ChatroomWithFriend
} from '@/common'

const props = defineProps({
    chatroomWithFriends: {
        type: Array as() => ChatroomWithFriend[] | undefined,
        required: false
    },
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
        type: Object as() => Viewer | null,
        required: false,
        default: null
    },
    activePanel: {
        type: String,
        required: true
    }
})

const emit = defineEmits([
    'onSelectConversation', 
    'update-invitations', 
    'update-conversations', 
    'update-chatrooms'])
const updatedInvitations = (newInvitations: Invitation[]) => {
    emit('update-invitations', newInvitations)
}

const updatedConversations = (newConversations: Conversation[]) => {
    emit('update-conversations', newConversations)
}

const updatedChatrooms = () => {
    emit('update-chatrooms');
    console.log("emit update-chatrooms in Direct");
}

</script>