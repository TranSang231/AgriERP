<template>
    <div class="el-input">
        <div class="el-input__wrapper" tabindex="-1">
            <div
                ref="inputDom"
                v-html="inputHtml"
                @input="onInput"
                @compositionstart="onCompositionStart"
                @compositionend="onCompositionEnd"
                contenteditable="true"
                class="el-input__inner"
                @keydown.enter="onEnterDown"
                @mouseup="onMouseUp"
            />
        </div>
    </div>
</template>

<script setup lang="ts">
import debounce from 'lodash/debounce'
import IntervalTree from 'node-interval-tree';

const props = defineProps({
	highlight: {
		type: Array,
		default: []
	},
    highlightEnabled: {
        type: Boolean,
        default: false
    },
    highlightStyle: {
      type : [String, Object],
      default:  'text-primary'
    },
    highlightDelay: {
      type: Number,
      default: 500 //This is milliseconds
    },
    caseSensitive: {
      type: Boolean,
      default: false
    }
});

const { t } = useI18n();
const inputDom = ref()
const model = defineModel();
const internal = ref<string>(model.value? model.value as string: '');
const inputHtml = ref(model.value ? model.value: '');
const lock = ref(false);
const cursorOffset = ref(0);
const emit = defineEmits(['selectText']);


const normalizedHighlights  = () => {
    if (!props.highlight || props.highlight.length === 0) {
        return null;
    }
    

    if (
        Object.prototype.toString.call(props.highlight) === '[object RegExp]' ||
        typeof(props.highlight) == "string"
    ) {
        return [{text: props.highlight}]
    }
    
    if (
        Object.prototype.toString.call(props.highlight) === '[object Array]' &&
        props.highlight.length > 0
    ){
        let globalDefaultStyle = typeof(props.highlightStyle) == 'string'
            ? props.highlightStyle
            : (Object.keys(props.highlightStyle).map(
                    key => key + ':' + (props.highlightStyle as any)[key]
                ).join(';') + ';');
    
        let regExpHighlights = props.highlight.filter(
            x => Object.prototype.toString.call(x) === '[object RegExp]'
        );
        let nonRegExpHighlights = props.highlight.filter(
            x => Object.prototype.toString.call(x) !== '[object RegExp]'
        );
        nonRegExpHighlights =  nonRegExpHighlights.map((h: any) => {
            if (h.text || typeof(h) == "string") {
                return {
                    text:   h.text || h,
                    style:  h.style || globalDefaultStyle,
                    caseSensitive: h.caseSensitive
                } as {text?: any, style?: any, caseSensitive?: any, start?:any, end?: any}
            } else if (h.start && h.end) {
                return {
                    style:  h.style || globalDefaultStyle,
                    start: h.start,
                    end:   h.end,
                    caseSensitive: h.caseSensitive
                } as {text?: any, style?: any, caseSensitive?: any, start?:any, end?: any}
            }
            else {
                console.error("Please provide a valid highlight object or string")
                return null;
            }
        }).filter((o) => !!o)
        .sort(
            (a, b) => (a.text && b.text)
                ? a.text.localeCompare(b.text)
                : (a.start == b.start
                    ? (a.end < b.end ? 1 : a.end == b.end ? 0 : -1) 
                    : (a.start < b.start ? 1: -1)
                )
        );
        // We sort here in ascending order because we want to find highlights for the smaller strings first
        // and then override them later with any overlapping larger strings. So for example:
        // if we have highlights: g and gg and the string "sup gg" should have only "gg" highlighted.
        // RegExp highlights are not sorted and simply concated (this could be done better  in the future)
        return nonRegExpHighlights.concat(regExpHighlights);     
    }
    console.error("Expected a string or an array of strings");
    return null;
};

const getIndicesOf = (searchStr:string, str:string, caseSensitive:boolean = false) => {
    const searchStrLen = searchStr.length;
    if (searchStrLen == 0) {
        return [];
    }
    let startIndex = 0, index=0, indices = [];
    if (!caseSensitive) {
        str = str.toLowerCase();
        searchStr = searchStr.toLowerCase();
    }
    while ((index = str.indexOf(searchStr, startIndex)) > -1) {
        indices.push(index);
        startIndex = index + searchStrLen;
    }
    return indices;
};

const insertRange = (start: number, end: number, highlightObj: any, intervalTree: any) => {
    let overlap = intervalTree.search(start, end);
    var maxLengthOverlap = overlap.reduce((max: any, o:any) => { return Math.max(o.end-o.start, max) }, 0)
    if (overlap.length == 0){
        intervalTree.insert(start, end, { start: start, end: end, style: highlightObj.style} )
    }
    else if ((end - start) > maxLengthOverlap)
    {
        overlap.forEach((o: any) => {
            intervalTree.remove(o.start, o.end, o)
        })
        intervalTree.insert(start, end, { start: start, end: end, style: highlightObj.style} )
    }
};

const getRegexIndices = (regex: any, str: string) => {
    if (!regex.global){
        console.error("Expected " + regex + " to be global")
        return []
    }
    
    regex = RegExp(regex)
    var indices = [];
    var match = null;
    while ((match = regex.exec(str)) != null) {
        indices.push({start:match.index, end: match.index + match[0].length - 1});
    }
    return indices;
}

const tagsToReplace = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;'
};

const replaceTag = (tag: string)  => {
    return tagsToReplace[tag] || tag;
};

const safeTagsReplace = (str: string)  => {
    return str.replace(/[&<>]/g, replaceTag);
};

const processHighlights = async () => {
    if (!props.highlightEnabled)
    {
        inputHtml.value = internal.value;
        model.value = internal.value;
        return;
    }

    let pos = getCursorPosition(inputDom.value) + cursorOffset.value;
    let intervalTree = new IntervalTree()
    // Find the position ranges of the text to highlight
    let highlightPositions: Array<any> = [];
    let sortedHighlights = normalizedHighlights();
    if (!sortedHighlights) {
        model.value = internal.value;
        return;
    }
        
    for (var i = 0; i < sortedHighlights.length; i++){
        let highlightObj = sortedHighlights[i] as any;

        let indices = [];
        if (highlightObj.text)
        {
            if (typeof(highlightObj.text) == "string"){
                indices = getIndicesOf(highlightObj.text, internal.value as string, !highlightObj.caseSensitive? props.caseSensitive : highlightObj.caseSensitive);
                indices.forEach(start => {
                    let end = start+highlightObj.text.length - 1;
                    insertRange(start, end, highlightObj, intervalTree);
                });
            }

            if (Object.prototype.toString.call(highlightObj.text) === '[object RegExp]'){
                indices = getRegexIndices(highlightObj.text, internal.value as string);
                indices.forEach(pair => 
                {
                    insertRange(pair.start, pair.end, highlightObj, intervalTree);
                });
            }
        }


        if (highlightObj.start && highlightObj.end && highlightObj.start < highlightObj.end){
            const start = highlightObj.start;
            const end = highlightObj.end - 1;
            insertRange(start, end, highlightObj, intervalTree);
        }
    }
    
    highlightPositions = intervalTree.search(0, (internal.value as string).length);
    highlightPositions = highlightPositions.sort((a: any,b: any) => a.start-b.start);

    // Construct the output with styled spans around the highlight text
    let result = '';
    let startingPosition = 0;
    for (let k = 0; k < highlightPositions.length; k++){
        let position = highlightPositions[k] as any;
        result += safeTagsReplace(internal.value.substring(startingPosition, position.start));
        result += "<span style='" + highlightPositions[k].style + "'>" + safeTagsReplace(internal.value.substring(position.start, position.end + 1)) + "</span>";
        startingPosition = position.end + 1;
    }

    // In case we exited the loop early
    if (startingPosition < internal.value.length) {
        result += safeTagsReplace(internal.value.substring(startingPosition, internal.value.length));
    }

    // Stupid firefox bug
    if (result[result.length-1] == ' '){
        result = result.substring(0, result.length-1);
        result += '&nbsp;'
    }

    inputHtml.value = result;
    model.value = internal.value;
    await nextTick()
    setCursorPosition(inputDom.value, pos)
    cursorOffset.value = 0;
}

const handleInputChange = (e: Event) => {
    const debouncedHandler = debounce(
        function(){
            if(!lock.value) {
                let text = (e.target as HTMLElement).innerText
                if (internal.value !== text){
                    internal.value = text;
                    processHighlights();
                }
            }
        },
        props.highlightDelay
    );
    debouncedHandler();
};


//Get the cursor offset, including line breaks
const getCursorPosition = (el: HTMLInputElement) => {
    el.focus()
    let range = document.getSelection()?.getRangeAt(0) as Range
    let rangeClone = range?.cloneRange()
    rangeClone?.selectNodeContents(el)
    rangeClone?.setEnd(range?.endContainer, range?.endOffset)
    // return rangeClone?.toString().length
    return countDocumentFragment(rangeClone.cloneContents())
}

// Calculate the number of characters in all child nodes of range
const countDocumentFragment = (fragment: DocumentFragment) => {
    let text = '';
    let childNodes = fragment.childNodes;
    for (let i = 0; i < childNodes.length; i++) {
        let node = childNodes[i];
        if (node.nodeType === Node.TEXT_NODE) {
            text += node.textContent;
        } else if (node.nodeType === Node.ELEMENT_NODE) {
            text += countCharacterElement(node);
        }
    }
    return text.length;
};
// Element Node
const countCharacterElement = (element: Node) => {
    var text = '';
    if (element.nodeName === 'BR') {
    return text + ' '
    }
    var childNodes = element.childNodes;
    for (var i = 0; i < childNodes.length; i++) {
    var node = childNodes[i];
    if (node.nodeType === Node.TEXT_NODE) {
        text += node.textContent;
    } else if (node.nodeType === Node.ELEMENT_NODE) {
        if (node.nodeName === 'BR') {
        text += ' '
        } else {
        text += countCharacterElement(node);
        }
    }
    }
    return text;
};

// Restore cursor position
const setCursorPosition = (el: HTMLElement, pos: number) => {
    let selection = getSelection();
    let range = createRange(inputDom.value, { pos })
    if (range) {
        range.collapse(false)
        selection?.removeAllRanges()
        selection?.addRange(range)
    }
}

const createRange = (node: Node, obj: { pos: number }, range?: Range): Range => {
    if (!range) {
        range = document.createRange();
        range.selectNode(node);
        range.setStart(node, 0);
    }
    if (obj.pos === 0) {
        range.setEnd(node, obj.pos);
    } else if (node && obj.pos > 0) {
        if (node.nodeType === Node.TEXT_NODE) {
            let text = node.textContent || ''
            if (text.length < obj.pos) {
                obj.pos -= text.length;
            } else {
                range.setEnd(node, obj.pos);
                obj.pos = 0;
            }
        } else {
            if (node.nodeName === 'BR') {
                obj.pos -= 1;
                if (obj.pos === 0) {
                    range.setEnd(node.nextSibling || node, 0);
                }
            } else {
            for (var lp = 0; lp < node.childNodes.length; lp++) {
                range = createRange(node.childNodes[lp], obj, range);
                if (obj.pos === 0) {
                    break;
                }
            }
            }
        }
    }
    return range;
}


const onCompositionStart = () => {
    lock.value = true
}
const onCompositionEnd = (e: Event) => {
    lock.value = false
    handleInputChange(e);
}

const onInput = (e: Event) => {
    handleInputChange(e);
}

const onMouseUp = (e: Event) => {
    console.log('e:', e);
    let selection = window.getSelection() as Selection;
    if (selection.rangeCount > 0) {
        const text = selection.toString();
        if (text && text.length > 0) {
            const range = selection.getRangeAt(0);
            const rangeClone = range?.cloneRange()
            rangeClone?.selectNodeContents(inputDom.value);
            rangeClone?.setEnd(range?.endContainer, range?.endOffset)
            const content = rangeClone.cloneContents();
            const end = countDocumentFragment(content);
            const start = end - text.length;
            emit('selectText', {text, start, end});
        }
    }
}

const onEnterDown = (event: KeyboardEvent) => {
  // Enter and shift+enter have different performances, and need to handle line break logic separately
  if (!event.shiftKey) {
    event.preventDefault()
    let selection = window.getSelection() as Selection;
    let range = selection.getRangeAt(0);
    let endContainer = range.endContainer;
    let parentNode = endContainer.parentNode || inputDom.value;
    let pos = getCursorPosition(inputDom.value);
    if (pos === inputDom.value.innerText.length) {
      let br1 = document.createElement("br");
      let br2 = document.createElement("br");
      if (endContainer.nodeName === 'BR') {
        parentNode.insertBefore(br1, endContainer.nextSibling)
        parentNode.insertBefore(br2, endContainer.nextSibling)
        range.setStartBefore(br2)
        range.setEndBefore(br2)
      } else {
        range.insertNode(br1);
        range.insertNode(br2);
        range.setStartAfter(br2);
        range.setEndAfter(br2);
      }
    } else {
      let br1 = document.createElement("br");
      if (endContainer.nodeName === 'BR') {
        parentNode.insertBefore(br1, endContainer.nextSibling);
        range.setStartBefore(br1);
        range.setEndBefore(br1);
      } else {
        range.insertNode(br1);
        range.setStartAfter(br1);
        range.setEndAfter(br1);
      }
    }
  }
}

watch(props,
    () => {
        processHighlights();
    }
);

onMounted(() => {
    processHighlights();
    inputDom.value.addEventListener("paste", (e: ClipboardEvent) => {
        e.preventDefault()
        if(!e.clipboardData)
        {
            return;
        }
        const text = e.clipboardData.getData('text')
        const cleanedText = text.replace(/\r/g, '')
        let position = getCursorPosition(inputDom.value)
        let innerText = inputDom.value.innerText
        let inputText = innerText.substr(0, position) + cleanedText + innerText.substr(position);
        cursorOffset.value = cleanedText.length;
        internal.value = inputText;
        processHighlights();
    });
})

</script>
