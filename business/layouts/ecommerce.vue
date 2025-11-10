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
                            <IconEcommerce class="w-20 h-20 text-white" />
                            <h5>{{ t('E_commerce') }}</h5>
                        </template>
                        <el-menu-item index="/e-commerce">
                            <IconDashboard class="el-icon" />
                            <span>{{ t('Dashboard') }}</span>
                        </el-menu-item>
                        <el-menu-item index="/e-commerce/products">
                            <IconProduct class="el-icon" />
                            <span>{{ t('Products') }}</span>
                        </el-menu-item>
                        <el-menu-item index="/e-commerce/categories">
                            <Folder class="el-icon" />
                            <span>{{ t('Categories') }}</span>
                        </el-menu-item>
                        <el-menu-item index="/e-commerce/promotions">
                            <IconPromotion class="el-icon" />
                            <span>{{ t('Promotions') }}</span>
                        </el-menu-item>
                        <el-menu-item index="/e-commerce/orders">
                            <Document class="el-icon" />
                            <span>{{ t('Orders') }}</span>
                        </el-menu-item>
                        <el-menu-item index="/e-commerce/goods-receipts">
                            <Document class="el-icon" />
                            <span>{{ t('Goods_receipts') }}</span>
                        </el-menu-item>
                        <el-menu-item index="/e-commerce/inventory">
                            <Box class="el-icon" />
                            <span>{{ t('Inventory') }}</span>
                        </el-menu-item>
                        <RestrictedView :oneOfScopes="['ecommerce:customers:view', 'ecommerce:customers:edit']">
                            <el-menu-item index="/e-commerce/customers">
                                <IconUsers class="el-icon" />
                                <span>{{ t('Customers') }}</span>
                            </el-menu-item>
                        </RestrictedView>
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
import AmozLogo from '/assets/icons/Logo.svg';
import IconEcommerce from '~/assets/icons/e-commerce.svg';
import IconDashboard from '~/assets/icons/dashboard.svg';
import IconProduct from '~/assets/icons/product.svg';
import IconPromotion from '~/assets/icons/promotion.svg';
import IconUsers from '~/assets/icons/users.svg';
import { Document, Folder, Box } from '@element-plus/icons-vue';
import { useOauthStore } from '@/stores/oauth';
import RestrictedView from '@/components/RestrictedView.vue';

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
