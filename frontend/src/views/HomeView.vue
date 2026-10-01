<script setup>
import { NPageHeader, NFlex, NAvatar, NSpace, NButton, NDropdown, useMessage } from "naive-ui";

const message = useMessage();

const moreOptions = [
    {
        label: "更多选项",
        disabled: true,
    },
    {
        label: "史山是如何诞生的？",
        key: "1",
    },

    {
        label: "你还想要什么",
        key: "2",
    },
];
function handleMoreOptionSelected(key) {
    switch (key) {
        case "1":
            message.info("阿巴 阿巴阿巴");
            break;
        case "2":
            message.info("所以你还想要什么啊？");
            break;
    }
}
</script>

<template>
    <n-flex vertical align="center" style="width: 100%">
        <n-page-header subtitle="2026 SRTP Project" style="width: 90vw; margin: 10px auto">
            <template #title>
                <a style="text-decoration: none; color: inherit">行人摔倒智能识别与报警系统</a>
            </template>
            <template #header> </template>
            <template #avatar>
                <n-avatar src="/src/assets/LOGO.jpg" />
            </template>
            <template #extra>
                <n-space>
                    <n-dropdown :options="moreOptions" placement="bottom-end" style="border-radius: 10px" @select="handleMoreOptionSelected">
                        <n-button style="padding: 0 4px; width: 34px; height: 34px"> ··· </n-button>
                    </n-dropdown>
                </n-space>
            </template>
        </n-page-header>
    </n-flex>
</template>
