<template>
  <div class="flex flex-col w-full mx-2 my-10">
    <div class="text-center">
      <div class="flex items-center cursor-pointer p-4 rounded-full overflow-hidden w-64 mx-auto bg-gray-200"
        ref="contentBlock"
        @mousedown="isClickingOnContent = true"
        @mousemove="isClickingOnContent = false"
        @mouseup="handleMouseEventOnContentBlock">

        <!-- Avatar Block -->
        <div class="w-12 h-12 mr-4">
          <router-link :to="`/hrm/employees/${dataRef.manager_id}`" tag="span">
            <el-avatar
              v-if="dataRef.manager"
              :src="dataRef.manager.avatar"
              />
            <el-avatar v-else :icon="UserFilled"/>
          </router-link>
        </div>

        <!-- Name Block -->
        <div class="flex flex-col w-full">
          <div class="text-sm font-medium">
            <span v-if="dataRef.type">{{ `[${dataRef.type.name}]` }}</span>
            {{ dataRef.name }}
          </div>
          <hr class="my-2" />
          <router-link v-if="dataRef.manager_id" :to="`/hrm/employees/${dataRef.manager_id}`" tag="span">
            <div class="text-lg font-bold">
              {{ dataRef.manager ? dataRef.manager.name : "TBD" }}
            </div>
          </router-link>
          <div v-else class="text-lg font-bold">
            {{ dataRef.manager ? dataRef.manager.name : "TBD" }}
          </div>
        </div>
      </div>
    </div>

    <!-- Children Container -->
    <template v-if="isShowChildren">
      <div class="flex justify-center">
        <Members
          v-if="dataRef.members && dataRef.members.length > 0"
          :members="dataRef.members"
          ref="members">
          <template v-slot:header>Members</template>
        </Members>
        <Unit
          v-for="unit in dataRef.units"
          :key="unit.id"
          :data="unit"
          :renderCallback="renderCallback"
        />
      </div>
    </template>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { UserFilled } from '@element-plus/icons-vue';
import { overrideFieldIfNullOrEmpty } from "@/utils/obj";

// Define props
interface Manager {
  name: string;
  avatar: string;
}

interface Unit {
  id: number;
  name: string;
  type: { name: string };
  manager: Manager;
  manager_id: number;
  members: any[];
  units: Unit[];
}

interface Props {
  data: Unit;
  renderCallback: () => void;
}

const props = defineProps<Props>();

// Use a ref to handle props.data
const dataRef = ref<Unit>(overrideFieldIfNullOrEmpty(props.data));

// Control the state of children visibility
const isShowChildren = ref(true);
const isClickingOnContent = ref(false);

// Handle rendering check for members and units
const isRenderingFinished = (showChildren: boolean): boolean => {
  if (dataRef.value.members && dataRef.value.members.length > 0) {
    // Check member rendering
  }
  if (dataRef.value.units && dataRef.value.units.length > 0) {
    for (const unit of dataRef.value.units) {
      if (showChildren && !document.querySelector(`[ref="unit-${unit.id}"]`)) {
        return false;
      }
    }
  }
  return true;
};

// Wait for rendering completion
const waitForRendering = (showChildren: boolean, timeout: number): Promise<void> => {
  return new Promise((resolve) => {
    const checkRendering = () => {
      if (!isRenderingFinished(showChildren) && timeout > 0) {
        setTimeout(() => {
          waitForRendering(showChildren, timeout - 100).then(resolve);
        }, 100);
      } else {
        resolve();
      }
    };
    checkRendering();
  });
};

// Switch the state for showing children
const switchShowingChildrenState = (): void => {
  isShowChildren.value = !isShowChildren.value;
  waitForRendering(isShowChildren.value, 3000).then(() => {
    props.renderCallback();
  });
};

// Handle mouse event
const handleMouseEventOnContentBlock = (): void => {
  if (isClickingOnContent.value) {
    switchShowingChildrenState();
  }
  isClickingOnContent.value = false;
};

// On component mount
onMounted(() => {

});
</script>
