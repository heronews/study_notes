<script setup lang="ts">

</script>

<template>
    <ElCarousel height="500px" :interval="5000">
        <ElCarouselItem v-for="v in 3" :key="v">
            <div class="flex-container">
                <h1>{{ v }}</h1>
            </div>
        </ElCarouselItem>
    </ElCarousel>
</template>

<style scoped>
.flex-container {
    background-color: aqua;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

h1 {
    text-align: center;
}
</style>