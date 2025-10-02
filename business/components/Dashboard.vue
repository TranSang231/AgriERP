<template>
    <div class=" flex flex-col w-full p-3 justify-center left-0 mt-10 items-center">
        <span class="my-5">{{ t('Service_to_manage') }}</span>
        <div class=" self-center grid grid-cols-3 gap-2 text-sm mt-12">
            <el-card>
                <NuxtLink to="/websites" class="flex flex-col items-center align-top text-center">
                    <IconWebsite width="28" height="28" class="text-primary"/>
                    <span>{{ t('Website') }}</span>
                </NuxtLink>
            </el-card>
            <el-card>
                <NuxtLink to="/e-commerce" class="flex flex-col items-center align-top text-center">
                    <IconEComerce width="28" height="28" class="text-primary"/>
                    <span>{{ t('E_commerce') }}</span>
                </NuxtLink>
            </el-card>
            <el-card>
                <NuxtLink to="/hrm" class="flex flex-col items-center align-top text-center">
                    <IconHumanResource width="28" height="28" class="text-primary"/>
                    <span>{{ t('Human_resources') }}</span>
                </NuxtLink>
            </el-card>
            <el-card>
                <NuxtLink to="/va" class="flex flex-col items-center align-top text-center">
                    <IconCRM width="28" height="28" class="text-primary"/>
                    <span>{{ t('Virtual_assistants') }}</span>
                </NuxtLink>
            </el-card>
            <el-card>
                <NuxtLink to="/knowledge" class="flex flex-col items-center align-top text-center">
                    <IconCafe width="28" height="28" class="text-primary"/>
                    <span>{{ t('Knowledge')}}</span>
                </NuxtLink>
            </el-card>
        </div>
    </div>
</template>
<script setup>
import IconWebsite from '@/assets/icons/website.svg';
import IconEComerce from '@/assets/icons/e-commerce.svg';
import IconHumanResource from '@/assets/icons/human-resource.svg';
import IconCRM from '@/assets/icons/crm.svg';
import IconCafe from '@/assets/icons/cafe.svg';

const { t } = useI18n();

</script>