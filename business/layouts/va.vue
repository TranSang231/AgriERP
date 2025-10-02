<template>
    <div class="w-full h-full flex bg-tertiary-light align-center justify-center">
        <div v-if="!authenticated" class="lg:py-20 py-6">
            <LoginForm>
                <div class="flex text-center justify-center">
                    <AmozLogo class="h-20" />
                </div>
                <div class="my-5">
                    <p class="lg:text-l text-center font-bold">
                        {{ $t("welcome_to_amoz") }}
                    </p>
                </div>
            </LoginForm>
        </div>
        <div v-else class="absolute w-full">
            <TopbarNav />
            <div class="flex flex-row">
                <aside>
                    <Sidebar>
                        <template #header>
                            <IconWebsite class="w-20 h-20 text-white" />
                            <h5>{{ t('Virtual_assistants') }}</h5>
                        </template>
                        <el-menu-item index="/va">
                            <IconDashboard class="el-icon" />
                            <span>{{ t('Dashboard') }}</span>
                        </el-menu-item>
                        <el-menu-item index="/va/bots">
                            <IconWebsite class="el-icon" />
                            <span>{{ t('Bots') }}</span>
                        </el-menu-item>
                        <el-menu-item index="/va/training">
                            <Folder class="el-icon" />
                            <span>{{ t('Training') }}</span>
                        </el-menu-item>
                        <el-menu-item index="/va/models">
                            <Folder class="el-icon" />
                            <span>{{ t('Models') }}</span>
                        </el-menu-item>
                    </Sidebar>
                </aside>
                <div class="flex-auto">
                    <slot />
                </div>
            </div>
            <footer class="w-full bg-gray-100 flex justify-center">
                <FooterContent />
            </footer>
        </div>
    </div>
</template>

<script setup>
import AmozLogo from "/assets/icons/Logo.svg";
import IconWebsite from "~/assets/icons/website.svg";
import IconDashboard from "~/assets/icons/dashboard.svg";
import { Document, Folder } from '@element-plus/icons-vue';
import { useOauthStore } from "@/stores/oauth";

const { t } = useI18n();

const oauthStore = useOauthStore();
const authenticated = computed(() => {
    const { tokenInfo } = oauthStore;
    if (!tokenInfo) return false;
    const { access_token } = tokenInfo;
    if (!access_token) return false;
    return access_token.length > 0;
});
</script>

<style scoped></style>
