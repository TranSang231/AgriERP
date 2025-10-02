<template>
    <div class="relative">
        <div v-if="icon" class="m-3">
            <el-avatar
                v-if="icon.uri"
                :src="icon.uri" 
                :size="size? size : 'large'"
                fit="fill"
                shape="square"
            />
            <component v-else :is="icon.svg" class="text-primary" :style="{width: iconSize, height: iconSize}"></component>
        </div>
        <Remove v-if="editable"
            @click="remove"
            class="absolute bg-on-primary rounded-full text-primary hover:text-pink-600 justify-center top-1 end-1 w-6 h-6 z-20"
        />
    </div>
</template>

<script setup lang="ts">
import { Remove, VideoPlay } from '@element-plus/icons-vue';
import Image from "@/assets/icons/image.svg";
import FileIcon from "@/assets/icons/file.svg";
import Zip from "@/assets/icons/zip.svg";
import Json from "@/assets/icons/json.svg";
import Pdf from "@/assets/icons/pdf.svg";
const mineTypesMap = [
    {
        type: "image",
        icon: Image
    },
    {
        type: "video",
        icon: VideoPlay
    },
    {
        type: "application",
        subtypes: [
            {
                type: "zip",
                icon: Zip
            },
            {
                type: "json",
                icon: Json
            },
            {
                type: "pdf",
                icon: Pdf
            }
        ],
        icon: FileIcon
    }
]

const props = defineProps({
    uri: {
        type: [String, null],
        default: null
    },
    mimeType: {
        type: String,
        default: 'image/*',
    },
    editable: {
        type: Boolean,
        default: false
    },
    size: {
        type: [String, Number, null],
        default: 80
    },
});

const emit = defineEmits(['remove']);
const remove = () => {
    emit('remove', props.uri);
}

const icon = computed(() => {
    const mimeTypeParts = props.mimeType.split("/");
    const type = mimeTypeParts[0];
    const subtype = mimeTypeParts.length > 1 ? mimeTypeParts[1]: null
    const mineType = mineTypesMap.find((o) => o.type===type);
    if (!mineType) {
        return null;
    }
    let mineTypeIcon = mineType.icon;
    if (subtype && mineType.subtypes && mineType.subtypes.length > 0) {
        let subMineType = mineType.subtypes.find((o) => o.type ===subtype)
        if (subMineType) {
            mineTypeIcon = subMineType.icon;
        }
    }
    if (type === "image" && props.uri && props.uri.length > 0) {
        return {
            uri: props.uri
        }
    }
    return {
        svg: mineTypeIcon
    }
});

const iconSize = computed(() => {
    const map = {
        small: 24,
        default: 40,
        large: 56
    }

    if (props.size && typeof props.size === 'string') {
        const mapValue =  map[props.size];
        return mapValue ? mapValue : props.size;
    }
    return props.size;
});
</script>