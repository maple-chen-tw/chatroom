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
                  :activeConversation="activeConversation"
                  :current-user="currentUser"
                  @on-select-conversation="selectConversation"
                />
              
                <InboxPanel
                  v-if="activePanel === 'chat'"
                  :conversations="conversations"
                  :invitations=undefined
                  :active-panel="activePanel"
                  :activeConversation="activeConversation"
                  :current-user="currentUser"
                  @on-select-conversation="selectConversation"
                />
            
                <InboxPanel
                  v-if="activePanel === 'plus'"
                  :conversations=undefined
                  :invitations="invitations"
                  :active-panel="activePanel"
                  :activeConversation=undefined
                  :current-user="currentUser"
                />

                <InboxPanel
                  v-if="activePanel === 'options'"
                  :active-panel="activePanel"
                  :active-conversation=undefined
                  :conversations=undefined
                  :current-user="currentUser"
                />

                <InboxBottom class="mt-auto" @icon-click="changePanel"/>
            </div>

            <!-- Chat input and Dialogs -->

            <ActiveChat 
                v-if="activeConversation"
                :active-conversation="activeConversation"
                v-model="chatMessageInput"
                :current-user="currentUser"
                :is-chat-loading="isChatLoading"
                :is-chat-empty="true"
                @on-chat-back="leaveChat"
                @on-file-upload="triggerFileUpload"
                @on-send-message="sendMessage"
                @on-like-icon="sendHeartEmoji" />

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
} from '@/components'

import type {
    Sender,
    ChatDialog,
    HTMLInputElementRef,
    PhotoModalImage,
    Conversation
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
import { Invitation } from '../common'

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

const conversationSampleA = new ConversationSample()
const conversationSampleB = new ConversationSample()
const conversationSampleC = new ConversationSample()

const invitationSampleA = new InvitationSample()
const invitationSampleB = new InvitationSample()
const invitationSampleC = new InvitationSample()

const currentUser: Sender = sender

// List of all conversations in the inbox
const conversations = ref<Conversation[]>([
    conversationSampleA,
    conversationSampleB,
    conversationSampleC
])

// List of all invitations in the inbox
const invitations = ref<Invitation[]>([
    invitationSampleA,
    invitationSampleB,
    invitationSampleC
])
console.log(invitations.value);



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