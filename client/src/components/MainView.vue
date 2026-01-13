<script setup lang="ts">
import { useRoute } from 'vue-router';

const route = useRoute()
</script>

<template>
  <ElContainer>
    <ElAside>
      <ElMenu router :default-active="route.path">
        <ElMenuItem index="/main/home">
          <ElIcon>
            <IElMenu />
          </ElIcon>
          <span>Home</span>
        </ElMenuItem>
      </ElMenu>
    </ElAside>
    <ElContainer>
      <ElHeader>Header</ElHeader>
      <ElMain>
        <RouterView></RouterView>
      </ElMain>
      <ElFooter>Footer</ElFooter>
    </ElContainer>
  </ElContainer>
</template>

<style scoped>
.el-container {
  height: 100%;
}
</style>
