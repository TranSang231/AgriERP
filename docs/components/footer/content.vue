<template>
    <footer class="w-full">
        <div class="w-full grid grid-cols-4 gap-4 px-5 pt-5">
            <div class="flex flex-col items-center content-center">
	    	<AmozIcon class="w-32 h-32 text-primary" />
                <p>PANDOSIMA CO.,LTD
                </p>
                <p>46 Xuan Dan 2, Xuan Ha, Thanh Khe, Da Nang</p>
            </div>
            <div class="flex flex-col items-center">
                <h3 class="text-xl font-semibold mb-3">Giới thiệu công ty</h3>
                <NuxtLink to="/" class="block mb-2 text-gray-700 hover:underline text-left">Công ty của chúng tôi
                </NuxtLink>
                <NuxtLink href="#" class="block mb-2 text-gray-700 hover:underline">Liên hệ</NuxtLink>
                <NuxtLink href="#" class="block mb-2 text-gray-700 hover:underline">Khách hàng</NuxtLink>
                <NuxtLink href="#" class="block mb-2 text-gray-700 hover:underline">Pháp lý</NuxtLink>
            </div>
            <div class="flex flex-col items-center">
                <h3 class="text-xl font-semibold mb-3">Dịch vụ</h3>
                <NuxtLink href="#" class="block mb-2 text-gray-700 hover:underline">Hỗ trợ</NuxtLink>
                <NuxtLink href="#" class="block mb-2 text-gray-700 hover:underline">Nâng cấp</NuxtLink>
                <NuxtLink href="#" class="block mb-2 text-gray-700 hover:underline">Trở thành đối tác</NuxtLink>
                <NuxtLink href="#" class="block mb-2 text-gray-700 hover:underline">Phát triển tùy chỉnh</NuxtLink>
            </div>
            <div class="flex flex-col items-center">
                <h3 class="text-xl font-semibold mb-3">Kết nối với chúng tôi</h3>
                <div class="flex space-x-4">
                    <NuxtLink v-for="icon in icons" :key="icon.name" :to="icon.link"
                        class="text-primary hover:text-gray-800" target="_blank">
                        <svg :width="size" :height="size" viewBox="0 0 24 24" class="fill-current">
                            <path :d="icon.path" />
                        </svg>
                    </NuxtLink>
                </div>
            </div>
        </div>
        <!-- Copyright -->
        <div class="w-full text-center mt-3 p-3 inset-x-0 bottom-0" style="background-color: rgba(0, 0, 0, 0.2)">
            © 2024 Copyright: Website made with
            <a class="text-dark" href="https://amoz.com">Alpha</a>
        </div>
    </footer>
</template>
<script setup>
import AmozIcon from '~/assets/icons/BigLogo.svg'
import { mdiFacebook, mdiTwitter, mdiLinkedin, mdiInstagram } from '@mdi/js';

const size = 32; // Icon size in pixels

const icons = [
    {
        name: 'Facebook',
        link: 'https://www.facebook.com',
        path: mdiFacebook,
    },
    {
        name: 'Twitter',
        link: 'https://www.twitter.com',
        path: mdiTwitter,
    },
    {
        name: 'LinkedIn',
        link: 'https://www.linkedin.com',
        path: mdiLinkedin,
    },
    {
        name: 'Instagram',
        link: 'https://www.instagram.com',
        path: mdiInstagram,
    },
];
</script>
