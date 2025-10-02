<template>
    <div class="flex flex-col items-center justify-center font-sans min-h-screen">
        <main class="grid my-5 flex-col items-center mb-8">
            <div class="min-w-280 sm:w-full h-full flex flex-col justify-items-start items-center text-center px-6">
                <h1 class="text-3xl font-bold mb-4">{{ $t('start_using_amoz') }}</h1>
                <p class="text-lg mb-5">
                    {{ $t('Login_to_start_using')}}
                </p>
                <LoginForm />
            </div>
        </main>
    </div>
</template>

<script setup>
import AmozLogo from '~/assets/icons/Logo.svg'
</script>
