<template>
    <div class="py-12">
        <h1 class="text-3xl mb-3 font-bold">User List</h1>
        <p>It's the user page</p>
        <div class="table">
            <div class="flex flex-row" v-for="user in users.data.users" :key="users.id">
                <p class="text-lg mt-3">
                    {{ user.first_name }}
                </p>
            </div>
        </div>
    </div>
</template>
<script setup>
const { pending, data: users } = await useFetch("/api/v1/users", { lazy: true })
</script>