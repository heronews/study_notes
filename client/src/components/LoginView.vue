<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()
const formData = ref({ username: "", password: "" })

const login = () => {
    router.push("/main/home")
}

</script>

<template>
    <div class="login-container">
        <ElForm label-width="auto">
            <ElRow justify="center" style="padding-bottom: 10px;">
                <h1>Welcome</h1>
            </ElRow>
            <ElFormItem label="用户名">
                <ElInput v-model="formData.username"></ElInput>
            </ElFormItem>
            <ElFormItem label="密码">
                <ElInput v-model="formData.password"></ElInput>
            </ElFormItem>
            <ElButton type="primary" @click="login">登录</ElButton>
        </ElForm>
    </div>
</template>

<style scoped>
.login-container {
    height: 100%;
}

.el-form {
    border: 2px solid var(--el-border-color);
    border-radius: 2px;
    box-shadow: var(--el-box-shadow);
    padding: 10px;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
}

.el-button {
    width: 100%;
    height: 100%;
}
</style>