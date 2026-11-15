<script setup>
import {
    NPageHeader,
    NFlex,
    NAvatar,
    NSpace,
    NButton,
    NDropdown,
    useMessage,
    NTabs,
    NTabPane,
    NUpload,
    NUploadDragger,
    NIcon,
    NText,
    NP,
    NImage,
    NGrid,
    NGridItem,
    NCard,
} from "naive-ui";
import { ResizeImage24Regular, ResizeVideo24Regular, Settings32Regular } from "@vicons/fluent";
import { API_URL } from "@/config";
import StreamView from "./StreamView.vue";
import LOGO from "@/assets/LOGO.jpg";

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
// 以下是图片、视频处理逻辑，目前不可用
async function handlePictureUploaded({ file, onFinish, onError }) {
    const formData = new FormData();
    formData.append("file", file.file);
    try {
        // TODO 后端地址待填
        const response = await fetch("", {
            method: "POST",
            body: formData,
        });
        if (!response.ok) {
            message.error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        onFinish();
    } catch (error) {
        message.error("无法上传！" + String(error));
        onError();
    }
}
async function handleVideoUploaded({ file, onFinish, onError }) {
    const formData = new FormData();
    formData.append("file", file.file);
    try {
        // TODO 后端地址待填
        const response = await fetch("", {
            method: "POST",
            body: formData,
        });
        if (!response.ok) {
            message.error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        onFinish();
    } catch (error) {
        message.error("无法上传！" + String(error));
        onError();
    }
}
</script>

<template>
    <n-flex vertical align="center" style="padding: 20px min(80px, 10vw)">
        <n-page-header subtitle="2026 SRTP Project" style="width: 100%">
            <template #title>
                <a style="text-decoration: none; color: inherit">行人摔倒智能识别与报警系统</a>
            </template>
            <template #header> </template>
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
        <n-tabs type="segment" animated @before-leave="handleBeforeLeaveTab">
            <n-tab-pane name="use-stream" tab="摄像头流输入">
                <StreamView />
            </n-tab-pane>
            <!-- 我是傻杯，我当时为什么要把两个视图全塞这里？？？ -->
            <!-- TODO 拆分视图到多个文件，同时配置子路由 -->
            <n-tab-pane name="use-picture" tab="图片输入">
                <n-upload directory-dnd accept="image/*" :custom-request="handlePictureUploaded">
                    <n-upload-dragger>
                        <div style="margin-bottom: 12px">
                            <n-icon size="48" :depth="3">
                                <ResizeImage24Regular />
                            </n-icon>
                        </div>
                        <n-text style="font-size: 16px"> 点击或者拖动文件到该区域来上传图片 </n-text>
                        <n-p depth="3" style="margin: 8px 0 0 0"> 支持上传单张任意图片类型 </n-p>
                    </n-upload-dragger>
                </n-upload>
                <n-grid cols="1 500:2" x-gap="12px" y-gap="12px" style="margin-top: 12px">
                    <n-grid-item>
                        <n-card title="输入">
                            <n-image width="100%" src="/src/assets/example/cxk-org.png" />
                        </n-card>
                    </n-grid-item>
                    <n-grid-item>
                        <n-card title="输出">
                            <n-image width="100%" src="/src/assets/example/cxk-pdd.jpg" />
                        </n-card>
                    </n-grid-item>
                </n-grid>
            </n-tab-pane>
            <n-tab-pane name="use-video" tab="视频输入"
                ><n-upload directory-dnd accept="video/*" :custom-request="handleVideoUploaded">
                    <n-upload-dragger>
                        <div style="margin-bottom: 12px">
                            <n-icon size="48" :depth="3">
                                <ResizeVideo24Regular />
                            </n-icon>
                        </div>
                        <n-text style="font-size: 16px"> 点击或者拖动文件到该区域来上传视频 </n-text>
                        <n-p depth="3" style="margin: 8px 0 0 0"> 支持上传单个任意视频类型 </n-p>
                    </n-upload-dragger>
                </n-upload>
                <n-grid cols="1 500:2" x-gap="12px" y-gap="12px" style="margin-top: 12px">
                    <n-grid-item>
                        <n-card title="输入">
                            <n-image width="100%" src="/src/assets/example/cxk-org.png" />
                        </n-card>
                    </n-grid-item>
                    <n-grid-item>
                        <n-card title="输出">
                            <n-image width="100%" src="/src/assets/example/cxk-pdd.jpg" />
                        </n-card>
                    </n-grid-item>
                </n-grid>
            </n-tab-pane>
        </n-tabs>
    </n-flex>
</template>
