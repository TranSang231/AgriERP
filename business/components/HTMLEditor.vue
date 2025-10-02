<template>
    <QuillEditor
        ref="editorRef" 
        v-model:content="model"
        contentType="html"
        :theme="theme"
        :enable="enable"
        :placeholder="placeholder"
        toolbar="#editor-toolbar"
        :modules="modules"
        class="w-full"
    >
        <template #toolbar>
            <div id="editor-toolbar" class="w-full">
                <!-- Common format -->
                <span class="ql-formats">
                    <select class="ql-header">
                        <option value="1">H1</option>
                        <option value="2">H2</option>
                        <option value="3">H3</option>
                        <option value="4">H4</option>
                        <option value="5">H5</option>
                        <option value="0">Normal</option>
                    </select>
                    <select class="ql-font">
                        <option selected>Sans Serif</option>
                        <option value="time-new-roman">Times New Roman</option>
                        <option value="arial">Arial</option>
                        <option value="inconsolata">Inconsolata</option>
                        <option value="mirza">Mirza</option>
                    </select>
                    <select class="ql-size">
                        <option selected="selected">Default</option>
                        <option value="5pt">5</option>
                        <option value="6pt">6</option>
                        <option value="8pt">8</option>
                        <option value="9pt">9</option>
                        <option value="10pt">10</option>
                        <option value="11pt">11</option>
                        <option value="12pt">12</option>
                        <option value="13pt">13</option>
                        <option value="14pt">14</option>
                        <option value="16pt">16</option>
                        <option value="18pt">18</option>
                        <option value="20pt">20</option>
                        <option value="22pt">22</option>
                        <option value="24pt">24</option>
                        <option value="26pt">26</option>
                        <option value="28pt">28</option>
                        <option value="32pt">32</option>
                        <option value="36pt">36</option>
                        <option value="48pt">48</option>
                        <option value="72pt">72</option>
                    </select>
                </span>
                
                <span class="ql-formats">
                    <button class="ql-bold"></button>
                    <button class="ql-italic"></button>
                    <button class="ql-underline"></button>
                    <button class="ql-strike"></button>
                    <select class="ql-align"></select>
                </span>

                <span class="ql-formats">
                    <select class="ql-color"></select>
                    <select class="ql-background"></select>
                </span>

                <!-- Subscript and superscript buttons -->
                <span class="ql-formats">
                    <button class="ql-script" value="sub"></button>
                    <button class="ql-script" value="super"></button>
                </span>

                <!-- List -->
                <span class="ql-formats">
                    <button class="ql-list" value="ordered"></button>
                    <button class="ql-list" value="bullet"></button>
                    <button class="ql-list" value="check"></button>
                </span>

                <!-- media -->
                <span class="ql-formats">
                    <button class="ql-link"></button>
                    <button class="ql-image"></button>
                    <button class="ql-video"></button>
                    <button class="ql-formula"></button>
                    <button class="ql-blockquote"></button>
                    <button class="ql-code-block"></button>
                </span>
            </div>
        </template>
    </QuillEditor>
</template>


<script setup>
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css';
import { onMounted, getCurrentInstance } from 'vue'
import Quill from 'quill';
let Font = Quill.import('formats/font')
// We do not add Sans Serif since it is the default
Font.whitelist = ['time-new-roman', 'arial', 'mirza', 'inconsolata']
Quill.register(Font, true)

var Size = Quill.import('attributors/style/size');
Size.whitelist = [
    '5pt',
    '6pt',
    '8pt',
    '9pt',
    '10pt',
    '11pt',
    '12pt',
    '14pt',
    '16pt',
    '18pt',
    '20pt',
    '22pt',
    '24pt',
    '28px',
    '32pt',
    '36pt',
    '48pt',
    '72pt'
];
Quill.register(Size, true);
import Mention from "quill-mention";
import 'quill-mention/dist/quill.mention.css';
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css';
import ImageUploader from 'quill-image-uploader';
import BlotFormatter from 'quill-blot-formatter';

const props = defineProps({
    theme: {
        type: String,
        default: "snow"
    },
    enable: {
        type: Boolean,
        default: true
    },
    readOnly: {
        type: Boolean,
        default: false,
    },
    placeholder: {
        type: String,
        default: ''
    },
    mentions: {
        type: Object,
        default: {},
        requied: false
    },
    hashtags: {
        type: Object,
        default: {},
        requied: false
    },
    upload: {
        type: Function,
        default: (file) => {
            return URL.createObjectURL(file);
        },
        requied: false
    }
})

const model = defineModel();
const editorRef = ref(null);

const options = {
    readOnly: props.readOnly ? props.readOnly : false
}

const base_modules = [
    {
        name: 'imageUploader',
        module: ImageUploader,
        options: {
            upload: props.upload,
        }
    },
    {
        name: 'blotFormatter',
        module: BlotFormatter
    },
];

const mentions_array = computed(() => {
    return props.mentions
        ? Object.entries(props.mentions).map(([key,value]) => ({id: value, value: key}))
        : [];
});

const hashtags_array = computed(() => {
    return props.hashtags
        ? Object.entries(props.hashtags).map(([key,value]) => ({id: value, value: key}))
        : [];
});

const mention_module = {
    name: 'mention',
    module: Mention,
    options: {
        allowedChars: /^[A-Za-z\sÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ]*$/,
        mentionDenotationChars: ["@", "#"],
        source: function (searchTerm, renderList, mentionChar) {
            let values;

            if (mentionChar === "@") {
                values = mentions_array.value;
            } else {
                values = hashtags_array.value;
            }

            if (searchTerm.length === 0) {
                renderList(values, searchTerm);
            } else {
                const matches = [];
                for (let i = 0; i < values.length; i++) {
                    if (values[i].value.toLowerCase().includes(searchTerm.toLowerCase())) {
                        matches.push(values[i]);
                    }
                }
                renderList(matches, searchTerm);
            }
        }
    }
};

const modules = [...base_modules, mention_module];
</script>