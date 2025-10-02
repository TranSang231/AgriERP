<template>
    <el-button :icon="Back" class="self-start" @click="back()">{{ t('back') }}</el-button>
</template>

<script setup lang="ts">
import { Back } from '@element-plus/icons-vue'

const props = defineProps({
    prefix: {
        type: String,
        default: null
    },
    historyBack: {
        type: Boolean,
        default: false
    }
});

const { t } = useI18n();
const route = useRoute();
const router = useRouter()

const back = () => {
    const path = route.path;
    if (!path || path.trim().length === 0) {
        return;
    }
    if (props.historyBack) {
        router.back();
        console.log('router.back', router.back);
        return;
    }

    const { id } = route.params;
    let to = null;
    if (id && path.endsWith(`/${id}`)) {
        const n = path.lastIndexOf(id as string);
        to = path.slice(0, n-1);
        
    } else if(path.endsWith('/new')) {
        const n = path.lastIndexOf('/new');
        to = path.slice(0, n);
    }
    if (to && props.prefix) {
        const n = path.lastIndexOf(`/${props.prefix as string}`);
        to = path.slice(0, n);
    }
    if (to) {
        navigateTo(to);
    }
    else {
        router.back();
    }
}

</script>
