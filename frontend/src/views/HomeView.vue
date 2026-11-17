<script setup>
import { NPageHeader, NFlex, NAvatar, NSpace, NButton, NDropdown, useMessage, NTabs, NTabPane, NIcon } from "naive-ui";
import { Settings32Regular } from "@vicons/fluent";
import { API_URL } from "@/config";
import LOGO from "@/assets/LOGO.jpg";
import { useRouter, RouterView, useRoute } from "vue-router";

const message = useMessage();
const route = useRoute();
const router = useRouter();

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
        label: "连通性测试",
        key: "2",
    },
];
function handleMoreOptionSelected(key) {
    switch (key) {
        case "1":
            window.open("https://github.com/rs9c/bro-how-are-u");
            break;
        case "2":
            handlePingTest();
            break;
    }
}
async function handlePingTest() {
    try {
        const resp1 = await fetch(`${API_URL}/ping`);
        const data1 = await resp1.json();
        message[resp1.ok ? "info" : "warning"](data1.msg);
        const resp2 = await fetch(`${API_URL}/ping`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                req: "Ping",
                repeat: 3,
            }),
        });
        const data2 = await resp2.json();
        message[resp2.ok ? "info" : "warning"](data2.msg);
    } catch (e) {
        message.error("无法连通后端服务！");
        console.error(API_URL);
    }
}
function handleBeforeLeaveTab(tabName) {
    if (tabName === route.path.match(/\/([^/]+)/)[1]) return false;
    router.push("/" + tabName);
    return true;
}
</script>

<template>
    <n-flex vertical align="center" style="padding: 20px min(80px, 10vw)">
        <n-page-header subtitle="2026 SRTP Project" style="width: 100%">
            <template #title>
                <a style="text-decoration: none; color: inherit">行人摔倒智能识别与报警系统</a>
            </template>
            <template #header></template>
            <template #avatar>
                <n-avatar :src="LOGO" />
            </template>
            <template #extra>
                <n-flex>
                    <n-button style="height: 34px">
                        <template #icon>
                            <n-icon>
                                <Settings32Regular />
                            </n-icon>
                        </template>
                        全局设置
                    </n-button>
                    <n-space>
                        <n-dropdown :options="moreOptions" placement="bottom-end" style="border-radius: 10px" @select="handleMoreOptionSelected">
                            <n-button style="padding: 0 4px; width: 34px; height: 34px"> ··· </n-button>
                        </n-dropdown>
                    </n-space>
                </n-flex>
            </template>
        </n-page-header>
        <n-tabs type="segment" animated @before-leave="handleBeforeLeaveTab" v-model:value="route.path.match(/\/([^/]+)/)[1]">
            <n-tab-pane name="stream" tab="摄像头流输入">
                <RouterView />
            </n-tab-pane>
            <n-tab-pane name="picture" tab="图片输入">
                <RouterView />
            </n-tab-pane>
            <n-tab-pane name="video" tab="视频输入">
                <RouterView />
            </n-tab-pane>
        </n-tabs>
    </n-flex>
</template>
