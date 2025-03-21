<template>
    <div class="flex md:flex-row flex-col h-screen">
        <div class="md:flex md:flex-row md:p-0 md:place-self-center md:max-w-4xl m-auto items-center
            sm:p-2 border-[#363636] border-2 w-full h-4/5">
            <!-- Navigation and Messages overview -->
            <div class="flex flex-col h-full w-2/5">
                <!-- activePanel -->
                <InboxPanel
                  v-if="activePanel === 'user'"
                  :conversations="conversations"
                  :invitations=undefined
                  :active-panel="activePanel"
                  :activeConversation=undefined
                  :current-user="currentUser"
                  @on-select-conversation="selectConversation"
                />

                <InboxPanel
                  v-else-if="activePanel === 'plus'"
                  :conversations=conversations
                  :invitations="invitations"
                  :active-panel="activePanel"
                  :activeConversation=undefined
                  :current-user="currentUser"
                  @update-invitations="updateInvitations"
                />
              
                <InboxPanel
                  v-else
                  :conversations="conversations"
                  :invitations=undefined
                  :active-panel="activePanel"
                  :activeConversation=undefined
                  :current-user="currentUser"
                  @on-select-conversation="selectConversation"
                />
            
                <InboxBottom class="mt-auto" @icon-click="changePanel"/>
            </div>

            <!-- Chat input and Dialogs -->
            <ActiveInfo
                v-if="activePanel === 'options'"
                :current-user="currentUser"
                @updateUser="updateUserData"
                />
            <ActiveChat 
                v-else-if="activeConversation"
                :active-conversation="activeConversation"
                v-model="chatMessageInput"
                :current-user="currentUser"
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
    Friend,
    Invitation
} from '@/common'

import {
    getCurrentTimestamp
} from '@/common/helpers'

// Demo data
import {
    ChatDialogSample,
    ConversationSample, 
    UserSample,
    InvitationSample
} from '@/data'

import { 
	useRouter 
} from 'vue-router'
import { onMounted } from 'vue';
import axios from "axios";
import { User } from '@/common'

const router = useRouter()

const token: string | null = localStorage.getItem('auth-token');
const user = ref<User | null>(null);
const conversations = ref<Conversation[]>([]);
const invitations = ref<Invitation[]>([]);

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

const createConversations = (friends: Friend[]) => {
    const newConversations = friends.map(friend => {
        return {
            uuid: `conv-${friend.user_id}`,
            user: {
                id: friend.user_id,
                userName: friend.username,
                nickname: friend.nickname || null,
                profilePictureUrl: friend.avatar_url
            },
            lastMessage: 'No messages yet',
            timeSinceLastMessage: '0 mins ago',
            dialogs: [],
            isActive: true
        };
    });
    return newConversations;
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
                nickname: friend.nickname || null,
                profilePictureUrl: friend.avatar_url
            },
            status: 'pending'
        };
    });
    return newInvitations;

};

onMounted(async () => {
    const router = useRouter();

    if (!token) {
        router.push('/accounts/login');
        return;
    }

    try {

        user.value = await fetchUserInfo(token);
        const friends = await fetchFriendsList(token);
        conversations.value = createConversations(friends);
        const invits = await fetchInvitationList(token);
        invitations.value = createInvitations(invits);
        

    } catch (error) {
        console.error("Error in onMounted:", error);
    }
});

const updateUserData = (updatedUser) => {
  user.value = updatedUser; // 更新用戶資料
};

const updateInvitations = (newInvitations: Invitation[]) => {
  invitations.value = newInvitations
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

// Others
const activeConversation = ref<Conversation | undefined>(undefined)

// Sample data
const viewer = new UserSample()
const sender = new UserSample()

// const conversationSampleA = new ConversationSample()
// const conversationSampleB = new ConversationSample()
// const conversationSampleC = new ConversationSample()

// const invitationSampleA = new InvitationSample()
// const invitationSampleB = new InvitationSample()
// const invitationSampleC = new InvitationSample()

//const currentUser: Sender = sender
const currentUser: Sender = user

// List of all conversations in the inbox
//const conversations = ref<Conversation[]>([
//    conversationSampleA,
//    conversationSampleB,
//    conversationSampleC
//])

// List of all invitations in the inbox
//const invitations = ref<Invitation[]>([
//    invitationSampleA,
//    invitationSampleB,
//    invitationSampleC
//])
//console.log(invitations.value);



// Active Chat Message
const chatMessage = ref<ChatDialog>({
    user: undefined,
    uqSeqId: undefined,
    itemType: undefined,
    isSentByViewer: undefined,
    text: undefined,
    timestamp: undefined
})

// Change InboxPanel
const activePanel = ref('chat')
const changePanel = (panel: string) => {
  activePanel.value = panel
  activeConversation.value = undefined
}
watch(activePanel, (newValue) => {
  console.log("activePanel changed:", newValue);
});

// Services
const toast = useToast()

// Methods
const sendMessage = (payload: Event) => {
    chatMessageInput.value = '' // Clear message area
    const message = payload?.target as HTMLInputElement
    // Prevent spacing values
    if (message.value.trim() != '') {
        chatMessage.value = {
            user: sender,
            itemType: '',
            isSentByViewer: true,
            text: message.value,
            timestamp: getCurrentTimestamp()
        }
        // Reset message
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
    activeConversation.value?.dialogs.push(message)
}

/**
 * TODO: Add validation
 * Handle file uploaded event
 * @param {Object} event - The event object
 */
const onFileUpload = async (event: Event) => {
    const targetEvent = event.target as HTMLInputElement
    const file = targetEvent?.files?.item(0) as Blob

    // Read the file as data URL to show preview
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = (event) => {
        attachmentImage.value = event.target?.result as string
        isFileValid.value = true
        isFileUploaded.value = true

        chatMessage.value = {
            user: sender,
            itemType: 'image',
            isSentByViewer: true,
            img: attachmentImage.value as string,
            timestamp: getCurrentTimestamp()
        }
    }
}



/**
 * Select conversation from inbox list
 * @param convo - Conversation to be selected
 */
const selectConversation = (convo: Conversation) => {
    const dialogA = new ChatDialogSample(sender)
    const dialogB = new ChatDialogSample(viewer)
    convo.dialogs.push(dialogA, dialogB)
    activeConversation.value = convo
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
        text: undefined
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
        text: undefined
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
    return (message.text != undefined || message.img != undefined)
}


// Watchers
/**
 * Update inbox with latest message
 */
watch(chatMessage, () => {
    if (shouldUpdateInbox()) {
        addToChat(chatMessage.value)
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