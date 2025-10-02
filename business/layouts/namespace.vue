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
            <TopbarNav>
                <template #right>
                    <el-button
                        v-if="showCreatePage"
                        type="primary"
                        :icon="Plus"
                        @click="createPage"
                        class="mr-2 px-2"
                    >
                        {{ $t('Create_page') }}
                    </el-button>
                </template>
            </TopbarNav>
            <div class="flex flex-row">
                <aside>
                    <Sidebar>
                        <template #header>
                            <IconWebsite class="w-20 h-20 text-white" />
                            <h5>{{ t('Knowledge') }}</h5>
                        </template>
                        <el-menu-item index="/knowledge">
                            <IconDashboard class="el-icon" />
                            <span>{{ t('Dashboard') }}</span>
                        </el-menu-item>
                        <el-menu-item index="/knowledge/namespaces">
                            <IconWebsite class="el-icon" />
                            <span>{{ t('Namespaces') }}</span>
                        </el-menu-item>
                        <el-divider class="my-4"/>
                        <KnowledgePageTree ref="pageTreeRef"/>
                        <el-divider v-if="route.params && route.params.namespaceId" class="my-4"/>
                        <el-menu-item
                            v-if="route.params && route.params.namespaceId"
                            :index="`/knowledge/namespaces/${route.params.namespaceId}/settings`"
                        >
                            <IconWebsite class="el-icon" />
                            <span>{{ t('Namespace_settings') }}</span>
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
import { Plus } from '@element-plus/icons-vue';
import AmozLogo from "/assets/icons/Logo.svg";
import IconWebsite from "~/assets/icons/website.svg";
import IconDashboard from "~/assets/icons/dashboard.svg";
import { useOauthStore } from "@/stores/oauth";

const { t } = useI18n();
const route = useRoute();

const oauthStore = useOauthStore();
const pageTreeRef = ref(null);
provide('pageTreeRef', pageTreeRef);

const authenticated = computed(() => {
    const { tokenInfo } = oauthStore;
    if (!tokenInfo) return false;
    const { access_token } = tokenInfo;
    if (!access_token) return false;
    return access_token.length > 0;
});

const showCreatePage = computed(() => {
    const canEdit = oauthStore.hasOneOfScopes(["knowledge:pages:edit"]);
    if (!canEdit) {
        return false;
    }
    return route.path.lastIndexOf('pages/new') === -1;
});

const createPage = () => {
    if (!route.params) {
        return;
    }
    const { namespaceId, id } = route.params;
    if (!namespaceId) {
        return
    }
    let to = `/knowledge/namespaces/${namespaceId}/pages/new`
    if(id) {
        to = `${to}?parentId=${id}`;
    }
    navigateTo(to);
};

</script>
