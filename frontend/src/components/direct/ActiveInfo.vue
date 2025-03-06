<template>
    <div class="md:grid bg-black border-l border-slate-800
    lg:basis-9/12 w-full md:h-full h-screen hidden">
        <div>
            <div class="flex flex-col pl-2 pr-2 text-white font-bold">
                會員資料設定
            </div>

            <div 
	    		class="grid grid-cols-[auto,1fr] p-3 space-x-3 w-full mr-4">
                <div class="flex items-center space-x-3">
                    <div>
	            	    <img 
	            	      	:src="currentUser?.profilePictureUrl"
	            	      	class="cursor-pointer rounded-full shadow-lg max-w-[150px] h-auto"/>
                    </div>
                    <div class="flex flex-col space-y-2">
                        <!-- Username with Edit icon -->
                        <div class="flex items-center space-x-2">
                            <span class="font-sans text-xs sm:text-sm font-semibold text-white self-start">
                                暱稱  
                            </span>
                            <span v-if="!isEditingNickname" class="font-sans sm:text-sm font-semibold text-white self-start overflow-hidden">
                                {{ currentUser?.nickname }}
                            </span>
                            <input
                                v-else
                                v-model="editedNickname"
                                class=" px-1 py-0 font-sans sm:text-sm font-semibold text-white bg-black border border-white rounded"
                                style="width: auto;"
                              />
                            <button @click="toggleEditedNickname" class="text-white text-xs sm:text-sm hover:bg-slate-700 p-1 rounded">
                                <i v-if="!isEditingNickname" class="fas fa-pencil-alt"></i>
                                <i v-else class="fas fa-save"></i>
                            </button>
                        </div>

                        <div class="flex items-center space-x-2">
                            <span class="font-sans text-xs sm:text-sm font-semibold text-white self-start">
                                狀態  
                            </span>
                            <span v-if="!isEditingStatus" class="font-sans sm:text-sm font-semibold text-white self-start overflow-hidden">
                                {{ currentUser?.status }}
                            </span>
                            <input
                                v-else
                                v-model="editedStatus"
                                class=" px-1 py-0 font-sans sm:text-sm font-semibold text-white bg-black border border-white rounded"
                                style="width: auto;"
                              />
                            <button @click="toggleEditStatus" class="text-white text-xs sm:text-sm hover:bg-slate-700 p-1 rounded">
                                <i v-if="!isEditingStatus" class="fas fa-pencil-alt"></i>
                                <i v-else class="fas fa-save"></i>
                            </button>
                        </div>

                        <!-- Email -->
                        <div class="flex items-center space-x-2">
                            <span class="font-sans text-xs sm:text-sm font-semibold text-white self-start">
                                Email  
                            </span>
                            <span class="font-sans text-xs sm:text-sm font-semibold text-white self-start">
                                {{ currentUser?.email }}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>



<script setup lang="ts">
import { 
    useRouter
} from 'vue-router'

import {
    SVGLoader
} from '@/components'

import type { 
    Viewer 
} from '@/common'

import {
    ref,
} from 'vue'
import axios from "axios";

const props = defineProps({
    currentUser: {
        type: Object as () => Viewer,
        required: true
    }
})
const isEditingStatus = ref(false);
const editedStatus = ref("");
const emit = defineEmits(["updateUser"]);

const isEditingNickname = ref(false);
const editedNickname = ref("");

const toggleEditStatus = async () => {
  if (isEditingStatus.value) {
    await saveStatus();
  } else {
    editedStatus.value = props.currentUser?.status || "尚未設定狀態";
    isEditingStatus.value = true;
  }
};
const saveStatus = async () => {
  try {
    const response = await axios.patch(`/user/${props.currentUser.id}`, {
      status: editedStatus.value,
    },{
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("auth-token")}`
        }
    });
    emit("updateUser", { ...props.currentUser, status: editedStatus.value });
    isEditingStatus.value = false;

    //console.log("Status updated:", response.data);
  } catch (error) {
    console.error("Error updating status:", error);
  }
};

const toggleEditedNickname = async () => {
  if (isEditingNickname.value) {
    await saveNickname();
  } else {
    editedNickname.value = props.currentUser?.nickname || "尚未設定暱稱";
    isEditingNickname.value = true;
  }
};
const saveNickname = async () => {
  try {
    const response = await axios.patch(`/user/${props.currentUser.id}`, {
        nickname: editedNickname.value,
    },{
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("auth-token")}`
        }
    });

    emit("updateUser", { ...props.currentUser, nickname: editedNickname.value });
    isEditingNickname.value = false;

    //console.log("Nickname updated:", response.data);
  } catch (error) {
    console.error("Error updating Nickname:", error);
  }
};


// Services
const router = useRouter() 


const onPageBack = () => {
    router.back()
}
</script>