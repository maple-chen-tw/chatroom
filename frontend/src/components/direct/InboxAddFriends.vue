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
  Invitation,
  Conversation
} from '@/common/models'
import axios from 'axios'
import { ref } from 'vue'
import jwt_decode from 'jwt-decode';

import { 
	useRouter 
} from 'vue-router'

defineProps({
  conversations: {
        type: Object as() => Conversation[] | undefined,
        required: true
    },
    activeConversationId: {
        type: String as() => Conversation['uuid'] | undefined,
        default: undefined
    },
  invitations: {
        type: Object as() => Invitation[] | undefined,
        required: true
    },
    activeInvitationId: {
        type: String as() => Invitation['uuid'] | undefined,
        default: undefined
    }
})

const router = useRouter()
const searchQuery = ref('')
const token = localStorage.getItem('auth-token');
if (!token) {
  console.log("No auth token found, redirecting to login...");
  router.push('/auth/login');
}
interface DecodedToken {
  user_id: string;
}
if (token) {
  const decodedToken = jwt_decode<DecodedToken>(token); 
  const userId = decodedToken.user_id;
}

const searchFriend = () => {
  if (!searchQuery.value.trim()) {
    console.log('Please enter a search term.')
    return
  }
  console.log(`Searching for: ${searchQuery.value}`)

  axios.get('friends/search', {
    headers: {
                "Authorization":`Bearer ${token}`
            },
    params: {
      username:searchQuery.value
    }
  })
  .then(response => {
    const friend = response.data;
    if (friend) {
      console.log('Found friend:', friend);
    }

    // 1. 如果搜尋結果是自己，顯示提示
    //if (friend.user_id === userId) {
    //  console.log('You cannot search for yourself.');
    //  return;
    //}

    // 2. 檢查該朋友是否已經在好友列表中
    // 假設你有一個 `friends` 陣列，包含當前用戶的所有好友

    //const isAlreadyFriend = conversations.some(f => f.user_id === friend.user_id);
    //if (isAlreadyFriend) {
    //  console.log('You are already friends with this user.');
    //  return;
    //}

    // 3. 如果不是好友，發送好友邀請
    sendFriendRequest(friend.user_id);

  })
  .catch(error => {
    if (error.response && error.response.status == 404) {
      console.log('User with username not found');
    } else {
      console.error('Error searching for user:', error);
    }

  });
}

const sendFriendRequest = (friendId: number) => {

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