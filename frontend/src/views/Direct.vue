<template>
    <div class="flex md:flex-row flex-col h-screen">
        <div class="md:flex md:flex-row md:p-0 md:place-self-center md:max-w-4xl m-auto items-center
            sm:p-2 border-[#363636] border-2 w-full h-4/5">
            <!-- Navigation and Messages overview -->
            <div class="flex flex-col h-full w-2/5 overflow-hidden">
                <!-- activePanel -->
                <InboxPanel
                  v-if="activePanel === 'user'"
                  :chatroomWithFriends="chatroomWithFriends"
                  :conversations="conversations"
                  :invitations=undefined
                  :active-panel="activePanel"
                  :activeConversation=undefined
                  :current-user="user!"
                  @on-select-conversation="selectConversation"

                />

                <InboxPanel
                  v-else-if="activePanel === 'plus'"
                  :conversations=conversations
                  :invitations="invitations"
                  :active-panel="activePanel"
                  :activeConversation=undefined
                  :current-user="user!"
                  @update-invitations="updatedInvitations"
                  @update-conversations="updatedConversations"
                  @update-chatrooms="updateChatrooms"
                />
              
                <InboxPanel
                  v-else
                  :conversations="conversations"
                  :invitations=undefined
                  :active-panel="activePanel"
                  :activeConversation=undefined
                  :current-user="user!"
                  @on-select-conversation="selectConversation"
                />
            
                <InboxBottom class="mt-auto" @icon-click="changePanel"/>
            </div>

            <!-- Chat input and Dialogs -->
            <ActiveInfo
                v-if="activePanel === 'options'"
                :current-user="user!"
                @updateUser="updateUserData"
                />
            <ActiveChat 
                v-else-if="activeConversation"
                :active-conversation="activeConversation"
                v-model="chatMessageInput"
                :current-user="user"
                :is-chat-loading="isChatLoading"
                :is-chat-empty="true"
                @on-chat-back="leaveChat"
                @on-file-upload="triggerFileUpload"
                @on-send-message="sendMessage"
                @on-like-icon="sendHeartEmoji"
                />


            <!-- Chat intro -->
            <ChatIntroMessage 
                v-else
                @on-send-message-modal="openSendMessageModal" />


        </div>
    </div>
    <!-- File Uploading -->
    <input
        ref="fileUpload"
        accept="image/*"
        type="file"
        hidden
        @change="onFileUpload" /> 
</template>

<script setup lang="ts">
import {
    computed,
    ref,
    watch
} from 'vue'

import {
    useToast
} from 'vue-toastification'

import {
    ChatIntroMessage,
	ActiveChat,
	InboxPanel,
    InboxBottom,
    ActiveInfo
} from '@/components'

import type {
    Sender,
    ChatDialog,
    HTMLInputElementRef,
    PhotoModalImage,
    Conversation,
    ChatroomWithFriend,
    Friend,
    Invitation,
    Viewer
} from '@/common'

import {
    getCurrentTimestamp
} from '@/common/helpers'


import { 
	useRouter 
} from 'vue-router'
import { onMounted, onUnmounted } from 'vue';
import axios, { AxiosError } from "axios";
import type { User } from '@/common'

import io from 'socket.io-client'
const socket = io(import.meta.env.VITE_SOCKET_URL, {
    path: "/ws/socket.io/",
    transports: ['websocket'],
    autoConnect: true,
    reconnection: true,
    reconnectionAttempts: 5,
    reconnectionDelay: 1000,
});

const token: string | null = localStorage.getItem('auth-token');
const user = ref<Viewer | null>(null);
const chatroomWithFriends = ref<ChatroomWithFriend[]>([]);
const conversations = ref<Conversation[]>([]);
const invitations = ref<Invitation[]>([]);
const activeConversation = ref<Conversation | undefined>(undefined)

const fetchUserInfo = async (token: string) => {
    try {
        const response = await axios.get("/user/me", {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });
        return {
            id: response.data.user_id,
            userName: response.data.username,
            profilePictureUrl: response.data.avatar_url,
            email: response.data.email,
            status: response.data.status,
            nickname: response.data.nickname,
            dateJoined: response.data.created_at,
            lastModifiedAt: response.data.updated_at,
        };
    } catch (error) {
        console.error("Error fetching user info:", error);
        throw error;
    }
};

const fetchFriendsList = async (token: string) => {
    try {
        const response = await axios.get("/friends/", {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });
        return response.data;
    } catch (error) {
        console.error("Error fetching friends list:", error);
        throw error;
    }
};



const createConversations = async (chatroomWithFriends: ChatroomWithFriend[], user_id: number, token: string) => {
  const convoPromises = chatroomWithFriends.map(async (friend) => {
    let lastMessage = '';
    let timeSinceLastMessage = '';

    try {
      const response = await axios.get(`/chatrooms/${friend.chatroom_id}/messages`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        params: {
          limit: 1,
        },
      });

      if (response.data.length > 0) {
        const msg = response.data[0];
        lastMessage = msg.content || '[No text]';
        timeSinceLastMessage = msg.timestamp;
      }
    } catch (error) {
      console.error(`Failed to fetch last message for chatroom ${friend.chatroom_id}`, error);
    }

    return {
      uuid: friend.chatroom_id,
      user: {
        id: friend.user_id,
        userName: friend.username,
        nickname: friend.nickname ?? undefined,
        profilePictureUrl: friend.avatar_url ?? undefined,
      },
      lastMessage,
      timeSinceLastMessage,
      dialogs: [] as ChatDialog[],
      isActive: true,
    };
  });

  return await Promise.all(convoPromises);
};

const fetchChatroomWithFriendsList = async (token: string) => {
    try {
        const response = await axios.get("/chatrooms/", {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });
        return response.data;
    } catch (error) {
        console.error("Error fetching friends list:", error);
        throw error;
    }
}

const fetchMessages = async (chatroomId: string, token: string, limit = 50, before?: string) => {
  try {
    const params: any = { limit };
    if (before) params.before = before;

    const response = await axios.get(`/chatrooms/${chatroomId}/messages`, {
      headers: {
        "Authorization": `Bearer ${token}`
      },
      params
    });

    return response.data;
  } catch (error) {
    console.error("Error fetching messages:", error);
    return [];
  }
};

const fetchInvitationList = async (token: string) => {
    try {
        const response = await axios.get("/friends/requests/pending", {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });
        return response.data;
    } catch (error) {
        console.error("Error fetching invitation list:", error);
        throw error;
    }
}

const createInvitations = (friends: Friend[]) => {
    const newInvitations = friends.map(friend => {
        return {
            uuid: `invi-${friend.user_id}`,
            user: {
                id: friend.user_id,
                userName: friend.username,
                nickname: friend.nickname ?? undefined,
                profilePictureUrl: friend.avatar_url ?? undefined,
            },
            status: 'pending' as 'pending'
        };
    });
    return newInvitations;

};

const addMessageToDB = async (token:string, messageData: ChatDialog) => {
  if (!activeConversation.value || !activeConversation.value.uuid) return;

  try {
    const response = await axios.post(
      `/chatrooms/${activeConversation.value.uuid}/message`, 
      {
        "chatroom_id": messageData.chatroom_id,
        "sender_id": messageData.user?.id,
        "content": messageData.content,
        "message_type": messageData.message_type,
        "read_status": "unread",
        "timestamp": messageData.timestamp,
      },
      {
        headers: {
          "Authorization": `Bearer ${token}`
        }
      }
    );
    console.log('Successfully add message to db.')
    } catch (error) {
        if (error instanceof AxiosError){
            console.error('Failed to add message:', error.response?.data || error.message);
        } else {
            console.error('Unexpected error occurred when add message:', error);
        }

  }
};

onMounted(async () => {
    const router = useRouter();
    if (!token) {
        router.push('/accounts/login');
        return;
    }

    try {

        user.value = await fetchUserInfo(token);
        chatroomWithFriends.value = await fetchChatroomWithFriendsList(token);
        console.log("ChatroomWithFriend:", chatroomWithFriends.value)
        conversations.value = await createConversations(chatroomWithFriends.value, user.value?.id, token);
        const invits = await fetchInvitationList(token);
        invitations.value = createInvitations(invits);

        socket.on('connect', () => {
            console.log("✅ Connected to WebSocket server");
            if (user.value?.id) {
                socket.emit('set_user_id', user.value.id); // Send the user ID to the server
            }
        });
    } catch (error) {
        console.error("Error fetching user info:", error);
    }
        socket.on('connect_error', (err: Error) => {
            console.error("❌ WebSocket connection error:", err);
        });

        // ✅ 重新連線成功
        socket.on('reconnect', (attempt: number) => {
            console.log(`🔄 WebSocket reconnected (attempt ${attempt})`);
        });

        // ✅ 伺服器傳來的訊息
    socket.on("receive_message", (messageData: ChatDialog) => {
    try {
        // Check if there's an active conversation and if it has a uuid
        if (activeConversation.value && activeConversation.value.uuid) {
          console.log('Message received');
          const isSentByViewer = messageData.user?.id === user.value?.id;
          messageData.isSentByViewer = isSentByViewer;
          if(isSentByViewer === false){
            activeConversation.value.dialogs.push(messageData);
            
          };
          updateConversationPreview(messageData);
          

      }
    } catch (error) {
      // Log the error if something goes wrong during the process
      console.error("Error while processing received message:", error);
    }
    });
});

onUnmounted(() => {
    socket.off("receive_message");
    socket.off("connect");
});


const updateUserData = (updatedUser: User) => {
  user.value = updatedUser; // 更新用戶資料
};

const updatedConversations = (newConversations: Conversation[]) => {
  conversations.value = newConversations
}

const updatedInvitations = (newInvitations: Invitation[]) => {
  invitations.value = newInvitations
}

const updateConversationPreview = (messageData: ChatDialog) => {
  const chatroomId = messageData.chatroom_id;
  const targetIndex = conversations.value.findIndex((c: Conversation) => c.uuid === chatroomId);

  if (targetIndex !== -1) {
    const old = conversations.value[targetIndex];
    const timestamp = messageData.timestamp ? new Date(messageData.timestamp) : new Date();

    const updated = {
      ...old,
      lastMessage: messageData.content ?? '[No text]',
      timeSinceLastMessage: timestamp.toLocaleString('zh-TW', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false,
      })
    };

    conversations.value.splice(targetIndex, 1, updated); 
  }
};

const updateChatrooms = async () => {

    console.log("emit update-chatrooms in Direct");

    try {
        if (!token) {
      console.warn("Token is null, cannot fetch chatrooms.");
      return;
    }
        const updatedChatrooms = await fetchChatroomWithFriendsList(token);
        chatroomWithFriends.value = updatedChatrooms;
    } catch (error) {
        console.error("Error updating chatrooms:", error);
    }
}


// References to DOM element
const fileUpload = ref<HTMLInputElementRef | null>()

// Form data
const attachmentImage = ref<PhotoModalImage>(null)
const chatMessageInput = ref<string | null>(null)

// Flags for tracking state
const isFileUploaded = ref<boolean>(false)
const isFileValid = ref<boolean>(false)
const isChatLoading = ref<boolean>(false)

// Active Chat Message
const chatMessage = ref<ChatDialog>({
    message_id: undefined,
    chatroom_id: undefined,
    user: undefined,
    timestamp: undefined,
    message_type: undefined,
    isSentByViewer: undefined,
    content: undefined,
    
})

// Change InboxPanel
const activePanel = ref('chat')
const changePanel = (panel: string) => {
  activePanel.value = panel
  activeConversation.value = undefined
}

// Services
const toast = useToast()

// Methods
const sendMessage = (payload: Event) => {
    chatMessageInput.value = '' // Clear message area
    const message = payload?.target as HTMLInputElement
    // Prevent spacing values
    if (message.value.trim() != '') {
        if (!user.value) {
            console.error('User is null, cannot send message');
            return;
        }
        const messageData = {

            chatroom_id: activeConversation.value?.uuid,
            user: user.value,
            timestamp:  getCurrentTimestamp(),
            message_type: "text" as "text",
            isSentByViewer: true,
            content: message.value,
        }

        chatMessage.value = messageData
        // console.log("messageData: ", messageData);
        socket.emit('send_message', messageData)
        message.value = ''
    }
}

/**
 * Trigger DOM file upload event
 */
const triggerFileUpload = () => {
    fileUpload.value?.click()
}

/**
 * Push message to inbox
 * @param message Message to be added
 */
const addToChat = (message: ChatDialog) => {
    if (activeConversation.value) {
        activeConversation.value.dialogs.push(message);
    }
}

 /**
 * 判斷檔案對應的 message_type
 */
 const getMessageTypeFromFile = (file: File): 'image' | 'video' | 'audio' | 'file' => {
    const type = file.type

    if (type.startsWith('image/')) {
        return 'image'
    } else if (type.startsWith('video/')) {
        return 'video'
    } else if (type.startsWith('audio/')) {
        return 'audio'
    } else {
        return 'file'
    }
}

/**
 * 處理檔案上傳事件
 * - 檢查檔案格式與大小
 * - 讀取檔案並轉成 Base64 預覽
 * - 建立聊天訊息物件
 * @param {Object} event - The event object
 */


const onFileUpload = async (event: Event) => {
    const targetEvent = event.target as HTMLInputElement
    const file = targetEvent?.files?.item(0) as File

    if (!file) return

    // 檔案格式與大小驗證
    const allowedTypes = [
        'image/jpeg',
        'image/png',
        'image/gif',
        'video/mp4',
        'audio/mpeg',
        'audio/mp3',
        'application/pdf'
    ]
    if (!allowedTypes.includes(file.type)) {
        isFileValid.value = false
        alert('只支援上傳圖片、影片、音訊 或 PDF 文件喔～')
        return
    }
    const maxSizeInMB = 10
    const fileSizeInMB = file.size / (1024 * 1024)
    if (fileSizeInMB > maxSizeInMB) {
        isFileValid.value = false
        alert(`檔案太大囉～請上傳小於 ${maxSizeInMB}MB 的檔案`)
        return
    }

    // 前端即時預覽(Base64)
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = async (event) => {
        attachmentImage.value = event.target?.result as string
        isFileValid.value = true
        isFileUploaded.value = true
        if (!user.value) {
            alert("User is not logged in, please login first.");
            return;
        }
        const formData = new FormData()
        formData.append('file', file)
        try {
            const { data } = await axios.post('/upload/upload-message-file', formData)

            chatMessage.value = {
                user: user.value,
                message_type: data.message_type,
                chatroom_id:activeConversation.value?.uuid,
                isSentByViewer: true,
                content: data.url,
                timestamp: getCurrentTimestamp()
            }
        } catch (err) {
            console.error(err)
            alert('檔案上傳失敗，請稍後再試')
        }
    }

}



/**
 * Select conversation from inbox list
 * @param convo - Conversation to be selected
 */
const selectConversation = async (convo: Conversation) => {
    
    activeConversation.value = convo
    if (activeConversation.value) {
        console.log(" join room:", activeConversation.value.uuid);
        socket.emit('join_room', activeConversation.value.uuid)

        // 從後端拉歷史訊息
        if (token) {
          const messages = await fetchMessages(activeConversation.value.uuid, token);
          //console.log("Fetched messages:", messages);
          //console.log("Current user:", user);

          activeConversation.value.dialogs = messages.map((msg: ChatDialog) => {
            //console.log("msg.user:", msg.user);
            //console.log("Compare msg.user?.id vs currentUser.id:", msg.user?.id, user.value?.id);
                  
            return {
              ...msg,
              isSentByViewer: msg.user?.id === user.value?.id
            };
          });

        }
    }
}

/**
 * Go back to conversation list
 */
const leaveChat = () => {
    activeConversation.value = undefined
}

/**
 * Show toast message on unsupported feature click
 */
const onUnsupportedFeatureClick = () => {
    toast.info('The following feature, is not supported yet.')
}

/**
 * Reset chat message object
 */
const resetChatMessage = () => {
    chatMessage.value = {
        message_id: undefined,
        chatroom_id: undefined,
        user: undefined,
        timestamp: undefined,
        message_type: undefined,
        isSentByViewer: undefined,
        content: undefined,
        }
}

/**
 * TODO
 */
const openSendMessageModal = () => {
    onUnsupportedFeatureClick()
}

/**
 * TODO
 */
const sendHeartEmoji = () => {
    chatMessage.value = {
        content: undefined
    }
}

/**
 * Scroll to latest message in the conversation
 */
const scrollToTheLatestMessage = () => {
    const target = document.querySelector('#last-element')
    if (target) {
        target.scrollIntoView({
            behavior: 'smooth'
        })
    }
}

/**
 * Dynamically check whether inbox should updated
 */
const shouldUpdateInbox = () => {
    const message = chatMessage.value
    return (message.content != undefined || message.img != undefined)
}


// Watchers
/**
 * Update inbox with latest message
 */
watch(chatMessage, () => {
    if (shouldUpdateInbox()) {
        addToChat(chatMessage.value)
        if(token){
          addMessageToDB(token, chatMessage.value)
        }
        resetChatMessage()
        scrollToTheLatestMessage()
    }
})

/**
 * Scroll to latest message on conversation change
 */
watch(activeConversation, () => {
    const WAITING_TIME = 1500
    isChatLoading.value = true
    setTimeout(() => {
        isChatLoading.value = false
        scrollToTheLatestMessage()
    }, WAITING_TIME)
})

</script>