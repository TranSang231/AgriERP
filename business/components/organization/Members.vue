<template>
    <div class="org-container">
        <div class="content-container">
            <div class="content-block" ref="content-block">
                <div class="name-block">
                    <div class="org-name">
                        <h3>
                            <slot name="header">Members</slot>
                        </h3>
                    </div>
                    <hr />
                    <div class="member-block" v-for="member in members" :key="member.email">
                        <div class="avatar-block">
                            <img :src="member.profile && member.profile.image
                                    ? `${API_IMAGE_SRC}/${member.profile.image}`
                                    : user_icon
                                " width="50px" height="50px" class="avatar-img" />
                        </div>
                        <router-link v-if="member.id" :to="`/users/${member.id}`" tag="span">
                            <div class="manager-name">
                                {{ member.name }}
                            </div>
                        </router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>


interface MemberType {
    email: string,
    id: string,
    name: string,
    profile: {
        image: string
    }
}
const props = defineProps({
    members: Array<MemberType>
})
// const members = ref([])
const API_IMAGE_SRC = ref("");
const user_icon = ref("");
const isShowChildren = ref(true);
const isClickingOnContent = ref(false)
</script>
<style scoped>
.member-block {
    display: flex;
    padding-top: 10px;
    align-items: center;

    .manager-name {
        padding-left: 10px;
    }
}
</style>