<template>
    <div>
        <div class="flex flex-row items-center justify-end">
            <el-avatar
                v-if="previewURI"
                :src="previewURI"
                :size="previewSize"
                :shape="shape"
                :fit="fit"
            />
            <el-avatar
                v-else
                :icon="icon"
                :size="previewSize"
                :shape="shape"
            />
            <el-button v-if="editable"
                circle
                :icon="Edit"
                @click="pickFile()"
                class="absolute self-end"
            />
            <input 
                type="file" 
                ref="fileRef" 
                class="hidden" 
                :multiple="false" 
                :accept="accept"
                @change="onFileChange"
            />
        </div>
    </div>
</template>

<script setup lang="ts">
import { UserFilled, Edit, PictureFilled } from '@element-plus/icons-vue'

const props = defineProps({
    editable: {
        type: Boolean,
        default: false
    },
    size: {
        type: [String, Number, null],
        default: 'default'
    },
    accept: {
        type: String,
        default: 'image/*', 
    },
    shape: {
        type: String,
        default: 'square'
    },
    fit: {
        type: String,
        default: 'fill',
    },
});

const model = defineModel();
const fileRef = ref(null);
const previewURI = computed(() => {
    const value = model.value;
    if (value ) {
        if(typeof value === 'string' && value.length > 6) {
            return value;
        }
        if(value instanceof Blob) {
            return URL.createObjectURL(value);
        }
    }
    return null;
});

const previewSize = computed(() => {
    return props.size? props.size : 'default';
});

const icon = computed(() => {
    return props.shape === 'square' ? PictureFilled : UserFilled;
});

const pickFile = () => {
    if (fileRef.value) {
        fileRef.value.click();
    }   
}

const onFileChange = (event: any) => {
    const files = event.target.files;
    if (files && files.length > 0) {
        model.value = files[0];
    }
};
</script>