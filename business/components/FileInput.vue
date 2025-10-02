<template>
    <el-upload class="cursor-pointer relative overflow-hidden transition duration-150 hover:border-blue-500"
        :show-file-list="false" :on-success="handleAvatarSuccess" :before-upload="beforeAvatarUpload"
        list-type="picture-card" :disabled="!canEdit">
        <div v-if="imageUrl" class="p-5 group">
            <img :src="imageUrl" class="block w-full h-full object-cover transition duration-150 group-hover:blur-sm" />
            <div v-if="canEdit"
                class="absolute inset-0 flex items-center justify-center space-x-2 opacity-0 group-hover:opacity-100 transition duration-150 bg-black bg-opacity-50">
                <span class="text-white" @click.stop="handlePictureCardPreview">
                    <el-icon><zoom-in /></el-icon>
                </span>
                <span class="text-white" @click.stop="handleRemove">
                    <el-icon>
                        <Delete />
                    </el-icon>
                </span>
            </div>
            <div class="mt-2 text-center text-sm text-gray-600 truncate mb-2 max-w-[96px]">{{ fileName }}</div>
        </div>

        <el-icon v-else class="text-primary align-middle">
            <AddFileIcon />
        </el-icon>
        <span v-if="!imageUrl" class="absolute mt-12 text-primary">{{ label }}</span>
    </el-upload>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import AddFileIcon from '~/assets/icons/add-file.svg'
import { Delete, Download, ZoomIn } from '@element-plus/icons-vue'

import type { UploadProps, UploadFile } from 'element-plus'

// Props
const props = defineProps({
    modelValue: {
        type: File,
        default: null,
    },
    label: {
        type: String,
        default: 'Add file',
    },
    multiple: {
        type: Boolean,
        default: false,
    },
    accept: {
        type: String,
        default: '*/*',
    }, canEdit: {
        type: Boolean,
        default: true,
    },
});
const emit = defineEmits(['update:modelValue']);
const fileName = ref('');

const imageUrl = ref('')
const dialogImageUrl = ref('')
const dialogVisible = ref(false)

const handleAvatarSuccess: UploadProps['onSuccess'] = (
    response,
    uploadFile
) => {
    imageUrl.value = URL.createObjectURL(uploadFile.raw!)
    fileName.value = uploadFile.name;
    emit('update:modelValue', uploadFile);
}

const beforeAvatarUpload: UploadProps['beforeUpload'] = (rawFile) => {
    if (rawFile.type !== 'image/jpeg') {
        ElMessage.error('Avatar picture must be JPG format!')
        return false
    } else if (rawFile.size / 1024 / 1024 > 2) {
        ElMessage.error('Avatar picture size can not exceed 2MB!')
        return false
    }
    return true
}

const handleRemove = () => {
    imageUrl.value = '';
    fileName.value = '';
    emit('update:modelValue', null);
};

const handlePictureCardPreview = () => {
    const link = document.createElement('a');
    link.href = imageUrl.value;
    link.target = '_blank';
    link.click();
};
</script>
