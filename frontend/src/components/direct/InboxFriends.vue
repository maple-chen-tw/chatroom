<template>
	<div 
        v-if="chatroomWithFriends"
		v-for="(convo, index) of chatroomWithFriends"
		:key="index"
		class="flex flex-col md:block pl-2 pr-2"
		@click="emitSelectConversation(convo)">
		<div 
			:class="{ 'bg-slate-1100': convo.chatroom_id === activeConversationId }"
			class="flex p-3 space-x-3 sm:hover:bg-slate-1100 w-full cursor-pointer">
			<!-- Profile Image -->
			<img 
				:src="convo.avatar_url || defaultAvatar"
				class="cursor-pointer h-14 w-14 rounded-full shadow-lg" />


			<!-- Username / Chat / Date -->
			<div class="flex flex-col self-center space-y-2 pb-3">
				<span class="font-sans text-xs sm:text-sm font-semibold text-white self-start">
					{{ convo.username }}
				</span>

				<div class="flex flex-row space-x-1">
					<span class="font-sans text-xs font-semibold text-gray-400">
						{{ convo.status }}
					</span>

				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import defaultAvatar from '@/assets/images/404ghost.png';

import type {
    Conversation,
	ChatroomWithFriend,
} from '@/common/models'

const props = defineProps({
	chatroomWithFriends: {
        type: Array as() => ChatroomWithFriend[] | undefined,
        required: true
    },
    conversations: {
        type: Object as() => Conversation[] | undefined,
        required: true
    },
    activeConversationId: {
        type: String as() => Conversation['uuid'] | undefined,
        default: undefined
    }
})

const emit = defineEmits(['onSelectConversation'])

/**
 * Emit new message
 */
const emitSelectConversation = (chatroomWithFriend: ChatroomWithFriend) => {
	const uuid = chatroomWithFriend.chatroom_id;
	const conversation = props.conversations?.find(
		(c) => c.uuid == uuid
	);

    if (conversation) {
		emit('onSelectConversation', conversation);
	} else {
		console.warn(`No conversation found with uuid: ${uuid}`);
	};
}

const formatedDate = (date: string) => {
	return new Date(date).toLocaleDateString()
}
</script>