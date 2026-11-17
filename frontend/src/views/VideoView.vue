<script setup>
import { NUpload, NUploadDragger, NIcon, NText, NP, NGrid, NGridItem, NCard, NImage } from "naive-ui";
import { ResizeVideo24Regular } from "@vicons/fluent";

// TODO
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
    <n-upload directory-dnd accept="video/*" :custom-request="handleVideoUploaded">
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
</template>
