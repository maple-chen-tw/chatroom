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
                    <!-- 頭像區塊 -->
                    <div class="flex flex-col items-center space-y-2 w-[150px]">
                      <div class="relative w-[150px] h-[150px]">
                        <img 
                          :src="previewImage || currentUser?.profilePictureUrl || defaultAvatar"
                          class="cursor-pointer rounded-full shadow-lg w-full h-full object-cover"
                          alt="頭像預覽"
                        />
                      
                        <!-- 小圓形按鈕（右下角） -->
                        <button
                          @click="triggerFileInput"
                          class="absolute bottom-1 right-1 bg-slate-700 hover:bg-slate-600 text-white rounded-full p-1 shadow-md"
                          title="上傳新頭像"
                        >
                          <i class="fas fa-camera text-xs"></i>
                        </button>
                      
                        <!-- 隱藏的 input -->
                        <input 
                          type="file" 
                          ref="fileInput"
                          accept="image/*"
                          @change="handleImageUpload"
                          class="hidden"
                        />
                      </div>
                    
                      <!-- 按鈕在下方 -->
                      <div v-if="selectedImage" class="flex justify-center space-x-2">
                        <button 
                          @click="uploadAvatarToServer"
                          class="text-white text-xs sm:text-sm hover:bg-slate-700 p-1 rounded"
                        >
                          上傳頭像
                        </button>
                        <button 
                          @click="cancelUpload"
                          class="text-red-400 text-xs sm:text-sm hover:bg-slate-800 p-1 rounded"
                        >
                          取消上傳
                        </button>
                      </div>
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

import defaultAvatar from '@/assets/images/chatify_user.png';

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

  } catch (error) {
    console.error("Error updating Nickname:", error);
  }
};


const selectedImage = ref<File | null>(null);
const previewImage = ref<string | null>(null);

const MAX_WIDTH = 500; // 限制最大寬度 (像素)
const MAX_HEIGHT = 500; // 限制最大高度 (像素)

const handleImageUpload = (event: Event) => {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (file) {
        // 檢查圖片的尺寸
        const image = new Image();
        const objectURL = URL.createObjectURL(file);

        image.onload = () => {
            // 獲取圖片的寬度和高度
            const width = image.width;
            const height = image.height;

            // 判斷圖片是否超過最大寬度和高度
            if (width > MAX_WIDTH || height > MAX_HEIGHT) {
                alert(`圖片大小限制為最大 ${MAX_WIDTH}x${MAX_HEIGHT} 像素，請選擇一張更小的圖片。`);
                selectedImage.value = null;
                previewImage.value = null;
                return;
            }

            // 圖片尺寸符合限制，更新預覽和檔案
            selectedImage.value = file;
            previewImage.value = objectURL;
        };

        image.src = objectURL;
    }
};

// 上傳到後端，並更新資料庫
const uploadAvatarToServer = async () => {
  if (!selectedImage.value) return;

  const formData = new FormData();
  formData.append("file", selectedImage.value);

  try {
    // 1. 上傳圖片取得 URL
    const uploadResponse = await axios.post("/upload/upload-avatar", formData);
    const imageUrl = uploadResponse.data.url;

    // 2. 更新使用者 avatar_url 到資料庫
    const patchResponse = await axios.patch(`/user/${props.currentUser.id}`, {
      avatar_url: imageUrl
    }, {
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("auth-token")}`
      }
    });

    // 3. 更新前端畫面
    emit("updateUser", {
      ...props.currentUser,
      profilePictureUrl: imageUrl
    });

    selectedImage.value = null;
    previewImage.value = null;

    console.log("上傳成功", imageUrl);
  } catch (error) {
    console.error("上傳或更新失敗", error);
  }
};

const cancelUpload = () => {
    selectedImage.value = null;
    previewImage.value = null;
    if (fileInput.value) {
    fileInput.value.value = '';
  }
};

// Services
const router = useRouter() 


const onPageBack = () => {
    router.back()
}

const fileInput = ref<HTMLInputElement | null>(null);

const triggerFileInput = () => {
  fileInput.value?.click();
};

</script>