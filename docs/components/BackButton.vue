<template>
    <el-button :icon="Back" class="self-start" @click="back()">{{ $t('back') }}</el-button>
</template>

<script setup lang="ts">
import { Back } from '@element-plus/icons-vue'
const route = useRoute();
const router = useRouter()

const back = () => {
    const path = route.path;
    if (!path || path.trim().length === 0) {
        return;
    }
    const { id } = route.params;
    if (id && path.endsWith(`/${id}`)) {
        const n = path.lastIndexOf(id);
        const to = path.slice(0, n-1);
        navigateTo(to);
    } else if(path.endsWith('/new')) {
        const n = path.lastIndexOf('/new');
        const to = path.slice(0, n);
        navigateTo(to)
    } else {
        router.back();
    }
}

</script>
