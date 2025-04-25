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
  <div v-if="searchMessage" class="pl-2 pr-2 text-yellow-400 font-bold">
  {{ searchMessage }}
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
  Conversation,
  Friend
} from '@/common/models'
import axios from 'axios'
import { AxiosError } from 'axios';
import { ref } from 'vue'
import jwt_decode from 'jwt-decode';

import { 
	useRouter 
} from 'vue-router'

const props = defineProps({
  conversations: {
        type: Object as() => Conversation[] | undefined,
        required: true
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


const emit = defineEmits(['update-invitations', 'update-conversations'])

const router = useRouter()
const searchQuery = ref('')
const searchMessage = ref('');
const token = localStorage.getItem('auth-token');
if (!token) {
  console.log("No auth token found, redirecting to login...");
  router.push('/auth/login');
}

const userId = ref<string | null>(null);


if (token) {
  try {
    const decodedToken = jwt_decode<{ user_id: string }>(token); 
    userId.value = decodedToken.user_id;
  } catch (error) {
    console.error("Error decoding token:", error);
  }
}

const searchFriend = () => {
  if (!searchQuery.value.trim()) {
    console.log('Please enter a search term.')
    searchMessage.value = '請輸入有效的 Email 或 username 來搜尋好友';
    return
  }

  searchMessage.value = `正在搜尋: ${searchQuery.value}...`;

  axios.get('friends/search', {
    headers: {
                "Authorization":`Bearer ${token}`
            },
    params: {
      username:searchQuery.value
    }
  })
  .then(async response => {
    const friend: Friend = response.data;
    if (friend) {
      console.log('Found friend:', friend);
    }

    // 1. 如果搜尋結果是自己，顯示提示
    if (friend.user_id === userId.value) {
      searchMessage.value = '你不能搜尋自己!';
      return;
    }

    // 2. 檢查該朋友是否已經在好友列表中
    const isAlreadyFriend = props.conversations?.some(f => {
      return f.user.id === friend.user_id;
    });
    if (isAlreadyFriend) {
      searchMessage.value = '你們早就是好友啦～快去聊天吧!';
      return;
    }
    // 3. 如果已經發送過好友邀請，顯示已經發送過
    const isRequestAlreadySent = await checkIfRequestSent(friend);
    if (isRequestAlreadySent) {
      searchMessage.value = '邀請已經送過囉～等對方回應中!';
      return;
    }
    // 4. 如果不是好友，發送好友邀請
    await sendFriendRequest(friend);
    searchMessage.value = `已發送好友邀請給 ${friend.username}!`;

  })
  .catch(error => {
    if (error.response && error.response.status == 404) {
      searchMessage.value = '找不到這個人，是不是打錯啦~';
    } else {
      searchMessage.value = '搜尋出了點小差錯，請稍後再試!';
    }

  });
}

const checkIfRequestSent = async(friend: Friend) => {
  try {

    const response = await axios.get('friends/requests/sent',{
      headers: {
       "Authorization": `Bearer ${token}`,
     },
    });
    
    const sentRequests: Friend[] = response.data;
    
    const isRequestSent = sentRequests.some((sentFriend) => sentFriend.user_id === friend.user_id);
    
    return isRequestSent
  } catch (error) {
    console.error('Error fetching sent requests:', error);
    return 0;
  }
}

/**
 * Send friend request
 */
const sendFriendRequest = async (friend: Friend) => {
 // Log the action for debugging purposes
 console.log(`Sending friend request to ${friend.username}...`);

 try {
   // Make a POST request to the API to send a friend request
   const response = await axios.post('/friends/request', null, {
     headers: {
       "Authorization": `Bearer ${token}`,
     },
     params: {
       friend_id: friend.user_id,
     },
   });

   console.log(`Friend request sent to ${friend.username}`);
 } catch (error: unknown) {
    if (error instanceof AxiosError) {

      if (error.response) {
        if (error.response.status === 400) {
          console.error('Error sending friend request:', error.response.data.detail);
        } else {
          console.error('Error sending friend request:', error.response.data);
        }
      } else {
        console.error('No response received:', error.message);
      }
    } else {
      console.error('Unexpected error occurred:', error);
    }
  }
 }

/**
 * Accept friend request
 */
 const acceptFriendRequest = async (invit: Invitation) => {
  console.log(`Friend request accepted for ${invit.user.userName}`)

  try {
    const response = await axios.post('friends/requests/accepted', null, {
      headers: {
        "Authorization": `Bearer ${token}`,
      },
      params: {
        friend_id: invit.user.id, // 發送的好友 ID
      },
    })
    if (response.status === 200) {

      // Update conversations list by adding the accepted user
      if (Array.isArray(props.conversations)) {
        if (userId.value){
          createFriendChatroom(userId.value, invit);
        } else {
        console.log('User ID is not available');
        }
        const updatedConversations = [...props.conversations, { user: invit.user }];
        emit('update-conversations', updatedConversations);
      }

      // Remove the accepted invitation from the invitations list
      if (Array.isArray(props.invitations)) {
        const updatedInvitations = props.invitations.filter(inv => inv.uuid !== invit.uuid);
        emit('update-invitations', updatedInvitations);
      }

      console.log(`Successfully accepted the friend request for ${invit.user.userName}`);
    } else {
      console.error("Failed to accept the friend request", response.data);
    }
  } catch (error) {
    if (error instanceof AxiosError) {
      console.error('Error accepting friend request:', error.response?.data || error.message);
    } else {
      console.error('Unexpected error occurred:', error);
    }
  }
};

/**
 * Create New Chatroom with friend
 */

const createFriendChatroom = async(user_id: string, invit: Invitation) => {
  console.log(`create Friend Chatroom for ${invit.user.userName}`)
  try {
    const chatroomName = "Default Chatroom";
    const members_id = [invit.user.id, user_id]
    const response = await axios.post('chatrooms/', {
      members_id: members_id,
      chatroom_name: chatroomName,
    }, {
      headers: {
        "Authorization": `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    console.log("Chatroom created:", response.data);

  } catch (error) {
    if (error instanceof AxiosError) {
      console.error('Error creating Friend Chatroom:', error.response?.data || error.message);
    } else {
      console.error('Unexpected error occurred:', error);
    }
  }
}

/**
 * Reject friend request
 */
 const rejectFriendRequest = async (invit: Invitation) => {
  console.log(`Friend request rejected for ${invit.user.userName}`)

  try {
    const response = await axios.delete('friends/requests/reject', {
      headers: {
        "Authorization": `Bearer ${token}`,
      },
      params: {
        friend_id: invit.user.id,
      },
    })

    // 從邀請列表中移除該請求
    if (props.invitations && Array.isArray(props.invitations)) {
      const updatedInvitations = [...props.invitations.filter(inv => inv.uuid !== invit.uuid)];
      emit('update-invitations', updatedInvitations)
    }

  } catch (error) {
    if (error instanceof AxiosError) {
      console.error('Error rejecting friend request:', error.response?.data || error.message)
    } else {
      console.error('Unexpected error occurred:', error)
    }
  }
}





</script>