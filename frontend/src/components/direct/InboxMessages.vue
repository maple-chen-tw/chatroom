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


			<!-- Username / Chat / Date -->
			<div class="flex flex-col self-center space-y-2 pb-3">
				<span class="font-sans text-xs sm:text-sm font-semibold text-white self-start">
					{{ convo.user.userName }}
				</span>

				<div class="flex flex-row space-x-1">
					<span class="font-sans text-xs font-semibold text-gray-400 truncate max-w-xs">
						{{ convo.lastMessage }}
					</span>

					<div class="font-sans text-xs font-semibold text-gray-500">
						•
					</div>

					<div class="font-sans font-semibold text-xs text-gray-500 justify-self-end">
						{{ formatedDate(convo.timeSinceLastMessage) }}
					</div>
				</div>
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

const getTimeSince = (timestamp: string) => {
  const now = new Date();
  const messageTime = new Date(timestamp);
  const diff = Math.floor((now.getTime() - messageTime.getTime()) / 1000); // in seconds

  if (diff < 60) return `Just now`; // 當差距不到 1 分鐘時
  if (diff < 3600) return `${Math.floor(diff / 60)} mins ago`; // 當差距不到 1 小時時
  if (diff < 86400) return `${Math.floor(diff / 3600)} hrs ago`; // 當差距不到 1 天時
  if (diff < 2592000) return `${Math.floor(diff / 86400)} days ago`; // 當差距不到 30 天時
  if (diff < 31536000) return `${Math.floor(diff / 2592000)} months ago`; // 當差距不到 1 年時
  return `${Math.floor(diff / 31536000)} years ago`; // 超過 1 年
};

const formatedDate = (date: string) => {
	if (!date) return ''
	//return getTimeSince(date)
	return new Date(date).toLocaleString('zh-TW', {  
	year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  });

}

</script>

<style scoped>

.truncate {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.max-w-xs {
    max-width: 200px;
}
</style>