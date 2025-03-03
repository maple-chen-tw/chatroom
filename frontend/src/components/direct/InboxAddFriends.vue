<template>
  <div>
    <!-- 搜尋欄 + 搜尋圖標 -->
    <div class="flex items-center p-3 rounded-lg">
      <input 
        v-model="searchQuery" 
        type="text" 
        placeholder="輸入Email搜尋好友"
        class="flex-1 p-2 bg-black text-white rounded-lg focus:ring-2 focus:ring-white"
      />
      <button @click="searchFriend" class="ml-2 text-white">
        <!-- 使用 Font Awesome 的搜尋圖標 -->
        <i class="fas fa-search"></i>
      </button>
    </div>
  </div>

  <div class="flex flex-col pl-2 pr-2 text-white font-bold">
    待確認好友邀請
  </div>
	<div 
    v-if="invitations"
		v-for="(invit, index) of invitations"
		:key="index"
		class="flex flex-col md:block pl-2 pr-2">
		<div 
			:class="{ 'bg-slate-1100': invit.uuid === activeInvitationId }"
			class="flex justify-between p-3 space-x-3 sm:hover:bg-slate-1100 w-full cursor-pointer">

      <div class="flex items-center space-x-3">
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
      </div>
      <div class="flex space-x-2 items-center">
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
	</div>
</template>

<script setup lang="ts">
import type {
  Invitation
} from '@/common/models'
import { ref } from 'vue'

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

const searchQuery = ref('')

const searchFriend = () => {
  if (!searchQuery.value.trim()) {
    console.log('Please enter a search term.')
    return
  }
  console.log(`Searching for: ${searchQuery.value}`)
  // 在這裡可以添加處理搜尋邏輯的程式碼
  // 比如過濾邀請資料
  // 例如篩選出符合搜尋關鍵字的邀請:
  // const filteredInvitations = invitations.filter(invit => invit.user.userName.includes(searchQuery.value))
  // console.log(filteredInvitations)
}
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