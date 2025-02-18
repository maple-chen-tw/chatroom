<template>
	<div 
        v-if="conversations"
		v-for="(convo, index) of conversations"
		:key="index"
		class="flex flex-col md:block pl-2 pr-2"
		@click="emitSelectConversation(convo)">
		<div 
			:class="{ 'bg-slate-1100': convo.uuid === activeConversationId }"
			class="flex p-3 space-x-3 sm:hover:bg-slate-1100 w-full cursor-pointer">
			<!-- Profile Image -->
			<img 
				:src="convo.user.profilePictureUrl"
				class="cursor-pointer h-14 w-14 rounded-full shadow-lg" />


			<!-- Username -->
			<div class="flex flex-col self-center space-y-2 pb-3">
				<span class="font-sans text-xs sm:text-sm font-semibold text-white self-start">
					{{ convo.user.userName }}
				</span>
			</div>

            <!-- V and X buttons -->
            <div class="flex space-x-2">
              <!-- V Button (Accept) -->
              <button 
                @click.stop="acceptFriendRequest(convo)"
                class="text-green-500 hover:text-green-700 text-sm font-semibold">
                [V]
              </button>

              <!-- X Button (Reject) -->
              <button 
                @click.stop="rejectFriendRequest(convo)"
                class="text-red-500 hover:text-red-700 text-sm font-semibold">
                [X]
              </button>
            </div>
		</div>
	</div>
</template>

<script setup lang="ts">
import type {
    Conversation
} from '@/common/models'

defineProps({
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
const emitSelectConversation = (conversation: Conversation) => {
    emit('onSelectConversation', conversation)
}

const formatedDate = (date: string) => {
	return new Date(date).toLocaleDateString()
}

/**
 * Accept friend request
 */
 const acceptFriendRequest = (convo: Conversation) => {
  console.log(`Friend request accepted for ${convo.user.userName}`)
  // Add logic to accept the friend request
}

/**
 * Reject friend request
 */
const rejectFriendRequest = (convo: Conversation) => {
  console.log(`Friend request rejected for ${convo.user.userName}`)
  // Add logic to reject the friend request
}


</script>