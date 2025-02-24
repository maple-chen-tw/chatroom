<template>
	<div 
    v-if="invitations"
		v-for="(invit, index) of invitations"
		:key="index"
		class="flex flex-col md:block pl-2 pr-2">
		<div 
			:class="{ 'bg-slate-1100': invit.uuid === activeInvitationId }"
			class="flex p-3 space-x-3 sm:hover:bg-slate-1100 w-full cursor-pointer">
			<!-- Profile Image -->
			<img 
				:src="invit.user.profilePictureUrl"
				class="cursor-pointer h-14 w-14 rounded-full shadow-lg" />


			<!-- Username -->
			<div class="flex flex-col self-center space-y-2 pb-3">
				<span class="font-sans text-xs sm:text-sm font-semibold text-white self-start">
					{{ invit.user.userName }}
				</span>
			</div>

            <!-- V and X buttons -->
            <div class="flex space-x-2">
              <!-- V Button (Accept) -->
              <button 
                @click.stop="acceptFriendRequest(invit)"
                class="text-green-500 hover:text-green-700 text-sm font-semibold">
                [V]
              </button>

              <!-- X Button (Reject) -->
              <button 
                @click.stop="rejectFriendRequest(invit)"
                class="text-red-500 hover:text-red-700 text-sm font-semibold">
                [X]
              </button>
            </div>
		</div>
	</div>
</template>

<script setup lang="ts">
import type {
  Invitation
} from '@/common/models'

defineProps({
  invitations: {
        type: Object as() => Invitation[] | undefined,
        required: true
    },
    activeInvitationId: {
        type: String as() => Invitation['uuid'] | undefined,
        default: undefined
    }
})

/**
 * Accept friend request
 */
 const acceptFriendRequest = (invit: Invitation) => {
  console.log(`Friend request accepted for ${invit.user.userName}`)
  // Add logic to accept the friend request
}

/**
 * Reject friend request
 */
const rejectFriendRequest = (invit: Invitation) => {
  console.log(`Friend request rejected for ${invit.user.userName}`)
  // Add logic to reject the friend request
}


</script>