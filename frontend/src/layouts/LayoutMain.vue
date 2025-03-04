<template>
    <div class="sm:min-h-screen h-screen min-w-screen bg-black md:max-w-full mx-auto sm:h-screen scrollbar scrollbar-thumb-gray-900">
        <TopLogoutBar
            v-if="!isTopLogoutBarHidden"/>
        
        <TopNavBar 
            v-if="!isTopNavBarHidden" />

        <div class="flex" :class=isModalToggledClass>
            <div    
                v-if="!isSideNavBarHidden"
                class="md:block hidden space-y-12 sticky top-0 border-r border-gray-900"
                :class="isNavBarCollapsed">
                <SideNavBar />
            </div>

            <div class="basis-full">
                <RouterView  />
            </div>
        </div>
    </div>
    
    <BottomNavBar 
        v-if="!isBottomNavBarHidden" />

    <Modals />
</template>

<script setup lang="ts">
import {
    computed,
} from 'vue'

import {
    useRoute
} from 'vue-router'

import {
    TopNavBar,
    BottomNavBar,
    SideNavBar,
    TopLogoutBar,
    Modals
} from '@/components'


import { 
    useModalManagerStore
} from '@/stores'

// Routes without no top/bottom navbars
const topNavBarHiddenRoutes = ['style', 'stories', 'reels', 'explore','direct']
const bottomNavBarHiddenRoutes = ['stories', 'style', 'direct']
const sideNavBarHiddenRoutes = ['stories', 'direct']
const collapsedHiddenRoutes = ['direct']

const topLogoutBarHiddenRoutes = ['style', 'stories', 'reels', 'explore']

// Services
const route = useRoute()
const modalStoreManager = useModalManagerStore()

// Computed
const routeName = computed(() => {
    return route.name ? route.name.toString() : ''
})


const isModalToggledClass = computed(() => {
    return modalStoreManager.isAnyModalOpen && modalStoreManager.shouldBlur ? 'lights-off' : ''
})

const isNavBarCollapsed = computed(() => {
    return collapsedHiddenRoutes.includes(routeName.value)  ? 'sm:w-20' : 'basis-1/6'
})

const isSideNavBarHidden = computed(() => {
    return sideNavBarHiddenRoutes.includes(routeName.value)
})

const isBottomNavBarHidden = computed(() => {
    return bottomNavBarHiddenRoutes.includes(routeName.value)
})

const isTopNavBarHidden = computed(() => {
    return topNavBarHiddenRoutes.includes(routeName.value)
})

const isTopLogoutBarHidden = computed(() => {
    return topLogoutBarHiddenRoutes.includes(routeName.value)
})
</script>