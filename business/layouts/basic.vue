<template>
    <div class="w-full h-full flex bg-tertiary-light align-center justify-center">
        <div class="w-full absolute space-x-* flex flex-row align-end justify-end py-2 px-8 z-10">
            <TopbarLanguageSelector />
        </div>
        <slot />
    </div>
</template>