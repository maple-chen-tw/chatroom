import type { BaseUser, User } from "./user.model"

/**
 * Represents an emoji reaction.
//  */
// export interface Emoji {
//     /** Timestamp of the emoji reaction */
//     timeStamp: number

//     /** ID of the sender */
//     senderId: string

//     /** Emoji value */
//     emoji: string
// }

/**
 * Represents reactions associated with a chat item.
 */
export interface Reactions {
    /** Array of liked items */
    likes: any[]

    /** Number of likes */
    likesCount: number

    /** Array of emoji reactions */
    // Emojis: Emoji[]
}

/**
 * Represents a chat item.
 */
export interface ChatDialog {
    /** ID of the chat item */
    message_id?: number

    /** The ID of the chatroom this message belongs to */
    chatroom_id?: string  // UUID string of the chatroom

    /** A simple instance of the user */
    user?: Sender | Viewer

    /** Timestamp of the chat item */
    timestamp?: number | string

    /** Type of the chat item */
    message_type?: 'text' | 'image' | 'audio' | 'file' | 'video' // Type of message

    /** Indicates if the chat item is sent by the viewer */
    isSentByViewer?: boolean


    /** Text content of the chat item */
    content?: string

    /** Image as a data URI scheme of the chat item*/
    img?: string
}

/**
 * Represent a single conversation instance between two users.
 */
export interface Conversation {
    /** Unique identifier for the conversation */
    uuid: string

    /** User who initiated the conversation */
    user: Sender

    /** Last message in the conversation */
    lastMessage: string

    /** Time elapsed since the last message */
    timeSinceLastMessage: string

    /** Dialogs (messages) in the conversation */
    dialogs: ChatDialog[]

    /** Indicates if the conversation is currently active */
    isActive: boolean
}

export interface ChatroomWithFriend {
    chatroom_id: string;
    chatroom_name: string;
    user_id: number;
    username: string;
    nickname: string | null;
    avatar_url: string | null;
    status: string | null;
}


export interface Friend {
    user_id: number;
    username: string;
    nickname: string | null;
    avatar_url: string | null;
}

/**
 * Represents an inbox containing chat threads.
 */
export interface Inbox {
    /** List of chat threads */
    threads: Conversation[]

    /** Number of unseen chats */
    unseenCount: number

    /** Timestamp of the last update to the unseen count */
    unseenCountTimeStamp: number
}

/**
 * Represents the viewer (current user) of the application.
 */
export interface Viewer extends User {

}

/**
 * Represents the Sender (chatting to) of the application.
 */
export interface Sender extends User {

}

/**
 * Represent a Friend Invitation instance between two users.
 */
export interface Invitation {
    /** Unique identifier for the Invitation */
    uuid: string
    user: User
    status?: 'pending' | 'accepted' | 'rejected' | 'deleted';

}
