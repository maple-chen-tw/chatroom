<template>
	<form 
		class="flex flex-col sm:w-80 w-full border rounded-sm p-8 m-auto"
		@submit.prevent>

        <SignUpHeader />
		<!-- Input: Email -->
		<div class="mb-2">
			<TheInput
				v-model="signupForm.email"
				type="email" 
				placeholder="Email" 
				:class="{
					'border-red-400': v$.email.$dirty && v$.email.$invalid 
                }"
				@blur="v$.email.$touch" />

			<p
				v-for="error of v$.email.$errors"
				:key="error.$uid"
				class="mt-2 text-xs text-red-600 dark:text-red-500">
				{{ error.$message }}
			</p>
		</div>

		<!-- Input: Username -->
		<div class="mb-2">
			<TheInput
				v-model="signupForm.username" 
				placeholder="Username" 
				:class="{
					'border-red-400': v$.username.$dirty &&
						v$.username.$invalid 
                }"
				@blur="v$.username.$touch" />

			<p
				v-for="error of v$.username.$errors"
				:key="error.$uid"
				class="mt-2 text-xs text-red-600 dark:text-red-500">
				{{ error.$message }}
			</p>
		</div>


		<!-- Input: Password -->
		<div class="mb-5">
			<TheInput
				v-model="signupForm.password"
				type="password" 
				placeholder="Password"
				:class="{
					'border-red-400': v$.password.$dirty &&
						v$.password.$invalid 
                }"
				@blur="v$.password.$touch" />
    
			<p
				v-for="error of v$.password.$errors"
				:key="error.$uid"
				class="mt-2 text-xs text-red-600 dark:text-red-500">
				{{ error.$message }}
			</p>
		</div>

		<!-- Button: Sign Up -->
		<TheButton
			:size="'sm'"
			:disabled="isLoading || v$.$invalid"
			@click="signup()">
			<i  
				v-if="isLoading"
				class="fa-sharp fa-solid fa-spinner animate-spin">
			</i>

			<div v-else>
				註冊
			</div>
		</TheButton>

		<SignUpFooter />
	</form>
</template>

<script setup lang="ts">
import axios from 'axios'
import {
    ref,
    computed
} from 'vue'

import { 
	useRouter 
} from 'vue-router'

import useVuelidate from '@vuelidate/core'
import {
    email,
    helpers,
    minLength,
    required
} from '@vuelidate/validators'

import {
    useToast
} from 'vue-toastification'

import {
    TheInput,
    TheButton,
    SignUpFooter,
	SignUpHeader
} from '@/components'

// Form
const signupForm = ref({
    email: null,
    firstName: null,
	lastName: null,
    username: null,
    password: null
})

// Checkers
const isLoading = ref<boolean>(false)

const validation = computed(() => ({
    email: {
        required: helpers.withMessage(
            'Email is required',
            required
        ),
        email: helpers.withMessage(
            'Valid email is required',
            email
        )
    },
    username: {
        required: helpers.withMessage(
            'Username is required',
            required
        )
    },
    password: {
        required: helpers.withMessage(
            'Password is required',
            required
        ),
        minLength: helpers.withMessage(
            'Min length is 8 characters',
            minLength(8)
        )
    }
}))

// Services
const toast = useToast()
const router = useRouter()
const v$ = useVuelidate(validation, signupForm.value)

// Methods
const signup = async () => {
    isLoading.value = true
	try {
		const response = await axios.post('/auth/register', {
			email: signupForm.value.email,
			username: signupForm.value.username,
			password: signupForm.value.password
		})

		toast.success('註冊成功！即將跳轉至登入頁面...')
		router.push({ name: 'login' })

	} catch (error: any) {
		const msg = error?.response?.data?.detail || '註冊失敗'
		toast.error(msg)
	} finally {
		isLoading.value = false
	}
}
</script>