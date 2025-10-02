<template>
    <div>
        <div class="flex flex-col items-start justify-end my-1 mx-2">
            <div v-if="multiple" class="flex flex-row gap-2 items-center">
                <FileThumbnail
                    v-for="p in previewURIs"
                    :uri="p._fileURI"
                    :mimeType="accept"
                    :size="size"
                    :editable="editable"
                    @remove="onRemove"
                />
                <div v-if="editable" class="flex flex-col align-middle justify-center items-center content-center">
                    <AddFileIcon class="text-primary hover:text-pink-600 w-8 h-8" @click="pickFile()" />
                    <span  v-if="placeholder" class="text-wrap text-primary self-center px-2">{{placeholder}}</span>
                </div>
            </div>
            <div v-else class="flex flex-row gap-2 items-center">
                <FileThumbnail
                    v-if="previewURI"
                    :uri="previewURI"
                    :mimeType="accept"
                    :size="size"
                    :editable="editable"
                    @remove="onRemove"
                />
                <div v-if="editable && !previewURI" class="flex flex-col align-middle justify-center items-center content-center">
                    <AddFileIcon  class="text-primary hover:text-pink-600 w-8 h-8" @click="pickFile()" />
                    <span  v-if="placeholder" class="text-wrap text-primary self-center px-2">{{placeholder}}</span>
                </div>
            </div>
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
import AddFileIcon from '@/assets/icons/add-file.svg'
import FileThumbnail from './FileThumbnail.vue';

const props = defineProps({
    placeholder: {
        type: [String, null],
        default: 'default'
    },
    editable: {
        type: Boolean,
        default: false
    },
    size: {
        type: [String, Number, null],
        default: 'default'
    },
    fileField: {
        type: [String, null],
        default: null
    },
    itemTemplate: {
        type: [Object, null],
        default: null
    },
    accept: {
        type: String,
        default: 'image/*',
    },
});

const model = defineModel();
const emit = defineEmits(['change']);
const fileRef = ref(null);
const multiple = model.value && Array.isArray(model.value);
const previewURI = computed(() => {
    const value = model.value;
    if (value && !Array.isArray(value)) {
        if(typeof value === 'string' && value.length > 6) {
            return value;
        }
        if(value instanceof Blob) {
            return URL.createObjectURL(value);
        }
    }
    return null;
});

const previewURIs = computed(() => {
    const { fileField } = props;
    if (!fileField) {
        return null;
    }
    const value = model.value;
    if (value && Array.isArray(value)) {
        return value.map((i) => {
            const file = i[fileField];
            return (file && file instanceof Blob)
                ? { i, _fileURI: URL.createObjectURL(file) }
                : { i, _fileURI: file };
        });
    }
    return null;
});

const pickFile = () => {
    if (fileRef.value) {
        fileRef.value.click();
    }   
}

const onRemove = (u: any) => {
    if (model.value && Array.isArray(model.value)) {
        const item = previewURIs.value?.find((o) => o._fileURI === u);
        console.log(item);
        if (item) {
            const { i } = item;
            console.log('i',i);
            if (i) {
                const newValue = model.value.filter((o: any) => o !== i);
                console.log('newValue',newValue);
                model.value = newValue;
                emit('change', newValue);
            }
        }
    } else {
        model.value = null;
        emit('change', null);
    }
};

const onFileChange = (event: { target: { files: any; }; }) => {
    const files = event.target.files;
    const file = files && files.length > 0 ? files[0] : null;
    if (!file) {
        return;
    }
    if (model.value && Array.isArray(model.value)) {
        const { fileField, itemTemplate } = props
        if (!fileField) {
            return;
        }
        const newItem = itemTemplate
            ? {
                ..._cloneDeep(itemTemplate),
                [fileField]: file
            }
            : {
                [fileField]: file
            }
        const newValue = model.value && Array.isArray(model.value)
            ? [
                ...model.value,
                newItem
            ]
            : [newItem];
        console.log(newValue);
        model.value = newValue;
        emit('change', newValue);
    } else {
        model.value = file;
        emit('change', file);
    }
};
</script>