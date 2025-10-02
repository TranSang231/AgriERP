<template>
    <div class="w-full h-full flex bg-tertiary-light align-center justify-center">
        <div class="absolute w-full">
            <TopbarNav />
            <div class="flex flex-row">
                <aside>
                    <Sidebar>
                        <template #header>
                            <IconCRM class="w-20 h-20 text-white" />
                            <h5>{{ t('Customer_support') }}</h5>
                        </template>
                        <el-input :placeholder="$t('Search')" v-model="keyword" class="p-2">
                            <template #append>
                                <el-button :icon="Search" />
                            </template>
                        </el-input>
                        <el-menu-item index="/">
                            <Folder class="el-icon" />
                            <span>{{ t('Namespaces') }}</span>
                        </el-menu-item>
                        <el-divider />
                        <KnowledgePageTree ref="pageTreeRef"/>
                    </Sidebar>
                </aside>
                <div class="flex-auto">
                    <slot />
                    <Chatbot/>
                </div>
            </div>
            <footer class="w-full bg-gray-100 flex justify-center">
                <FooterContent />
            </footer>
        </div>
    </div>
</template>

<script setup>
import IconCRM from "~/assets/icons/crm.svg";
import { Folder, Search } from '@element-plus/icons-vue';

const { t } = useI18n();
const keyword = ref("");

const pageTreeRef = ref(null);
provide('pageTreeRef', pageTreeRef);
</script>
