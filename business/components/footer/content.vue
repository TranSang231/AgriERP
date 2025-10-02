<template>
    <div class="w-full">
        <div class="w-full grid grid-cols-4 gap-4 px-5 py-2 bg-gray-50 text-sm">
            <div class="flex flex-col items-center">
                <AmozIcon class="w-20 h-20" />
                <p>{{ t('Footer_company_name') }}</p>
                <p class="text-center font-light text-sm">{{ t('Footer_compay_address') }}</p>
            </div>
            <div class="flex flex-col items-center">
                <h3 class="font-semibold mb-3">{{ t('About_us') }}</h3>
                <NuxtLink to="https://pandosima.com/about" class="block mb-2 text-gray-700 hover:underline text-left">
                    {{ t('About_the_company') }}
                </NuxtLink>
                <NuxtLink href="https://pandosima.com/#portfolio" class="block mb-2 text-gray-700 hover:underline">
                    {{ t('Portfolio') }}
                </NuxtLink>
            </div>
            <div class="flex flex-col items-center">
                <h3 class="font-semibold mb-3"> {{ t('Policies') }}</h3>
                <NuxtLink href="/policies/privacy_policy" class="block mb-2 text-gray-700 hover:underline">
                    {{ t('Privacy_policy') }}
                </NuxtLink>
                <NuxtLink href="/policies/terms-of-service" class="block mb-2 text-gray-700 hover:underline">
                    {{ t('Terms_of_Service') }}
                </NuxtLink>
                <NuxtLink href="/policies/content-policy" class="block mb-2 text-gray-700 hover:underline">
                    {{  t('Content_Policy') }}
                </NuxtLink>
            </div>
            <div class="flex flex-col items-center">
                <h3 class="font-semibold mb-3">{{ t('Follow_us') }}</h3>
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
        <div class="w-full text-center p-3 inset-x-0 bottom-0 bg-primary text-white">
            <span class="font-light text-sm italic">{{ t('Copyright') }}</span>
        </div>
    </div>
</template>
<script setup>
import AmozIcon from '~/assets/icons/BigLogo.svg'
import { mdiFacebook, mdiTwitter, mdiLinkedin, mdiYoutube } from '@mdi/js';

const size = 32; // Icon size in pixels
const { t } = useI18n();

const icons = [
    {
        name: 'Facebook',
        link: 'https://www.facebook.com/pandosima',
        path: mdiFacebook,
    },
    {
        name: 'Twitter',
        link: 'https://x.com/pandosima',
        path: mdiTwitter,
    },
    {
        name: 'LinkedIn',
        link: 'https://linkedin.com/company/pandosima',
        path: mdiLinkedin,
    },
    {
        name: 'Youtube',
        link: 'https://www.youtube.com/@pandosima',
        path: mdiYoutube,
    },
];
</script>
