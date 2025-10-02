<template>
    <div class="w-full h-full flex bg-tertiary-light align-center justify-center">
        <div v-if="!authenticated" class="lg:py-20 py-6">
            <LoginForm>
                <div class="flex text-center justify-center">
                    <AmozLogo class="h-20" />
                </div>
                <div class="my-5">
                    <p class="lg:text-l text-center font-bold">
                        {{ $t('welcome_to_amoz') }}
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
                            <IconUsers class="w-20 h-20" />
                            <h5>{{$t('Human_resources')}}</h5>
                        </template>
                        <el-menu-item index="/hrm">
                            <IconDashboard class="el-icon" />
                            <span>{{$t('Dashboard')}}</span>
                        </el-menu-item>
                        <el-menu-item index="/hrm/roles">
                            <IconRoles class="el-icon" />
                            <span>{{$t('Roles')}}</span>
                        </el-menu-item>
                        <el-sub-menu index="/hrm/employees">
                            <template #title>
                                <IconUsers class="el-icon" />
                                <span>{{$t('employees')}}</span>
                            </template>
                            <RestrictedView :oneOfScopes="['employees:edit']">
                                <el-menu-item index="/hrm/employees/custom-fields">{{$t('custom_fields')}}</el-menu-item>
                            </RestrictedView>
                            <el-menu-item index="/hrm/employees">{{$t('employees')}}</el-menu-item>
                            <el-menu-item index="/hrm/contracts">{{$t('contracts')}}</el-menu-item>
                        </el-sub-menu>
                        <el-menu-item index="/hrm/offices">
                            <IconOffices class="el-icon" />
                            <span>{{$t('offices')}}</span>
                        </el-menu-item>
                        <el-sub-menu index="/hrm/organization">
                            <template #title>
                                <IconOffices class="el-icon" />
                                <span>{{$t('organization')}}</span>
                            </template>
                            <el-menu-item index="/hrm/organization/tree">{{$t('organization_tree')}}</el-menu-item>
                            <el-menu-item index="/hrm/organization/chart">{{$t('organization_chart')}}</el-menu-item>
                            <el-menu-item index="/hrm/organization/unit-type">{{$t('unit_types')}}</el-menu-item>
                        </el-sub-menu>
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
import AmozLogo from '~/assets/icons/Logo.svg'
import IconUsers from '~/assets/icons/users.svg'
import IconDashboard from '~/assets/icons/dashboard.svg'
import IconRoles from '~/assets/icons/roles.svg'
import IconOffices from '~/assets/icons/businesses.svg'
import { useOauthStore } from '@/stores/oauth';
import OAuthService from '@/services/oauth';

const oauthStore = useOauthStore()
const authenticated = computed(() => {
    const { tokenInfo } = oauthStore;
    if (!tokenInfo) return false;
    const { access_token } = tokenInfo;
    if (!access_token) return false;
    return access_token.length > 0;
})

onMounted(() => {
    OAuthService.fetchScopes();
})
</script>