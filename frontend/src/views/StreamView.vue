<script setup>
import { NCard, NButton, NIcon, NGrid, NGi, NDescriptions, NDescriptionsItem, NEllipsis, NFlex, useMessage } from "naive-ui";
import { ref, onUnmounted, computed } from "vue";
import { Play16Regular, Settings16Regular, Pause16Regular, VideoOff32Regular } from "@vicons/fluent";
import { API_URL } from "@/config";

const message = useMessage();
const isStarted = ref(false);
const isStarting = ref(false);
const isPausing = ref(false);
const outputFrame = ref("");
let ws = null;
let currentObjectURL = null;
const wsStartAt = ref(0);
const now = ref(0);
const wsDuration = computed(() => {
    const total = Math.floor(Math.max(0, now.value - wsStartAt.value) / 1000);
    return [total / 3600, (total % 3600) / 60, total % 60].map((n) => String(Math.floor(n)).padStart(2, "0")).join(":");
});
const fps = ref(0);
let fpsTimer = null;
let frameCount = 0;

async function handleStartBtnClicked() {
    isStarting.value = true;
    ws = new WebSocket(`${API_URL}/stream/ws`);
    ws.onopen = () => {
        wsStartAt.value = Date.now();
        now.value = wsStartAt.value;
        isStarting.value = false;
        isStarted.value = true;
    };
    ws.onmessage = (event) => {
        if (currentObjectURL) URL.revokeObjectURL(currentObjectURL);
        currentObjectURL = URL.createObjectURL(event.data);
        outputFrame.value = currentObjectURL;
        frameCount++;
    };
    ws.onclose = () => {
        message.info("WebSocket连接断开");
        clearInterval(fpsTimer);
        fps.value = 0;
        frameCount = 0;
        isStarting.value = false;
        isStarted.value = false;
        isPausing.value = false;
    };
    ws.onerror = (e) => {
        message.warn("WebSocket发生错误！" + e);
        isStarting.value = false;
        isStarted.value = false;
    };
    fpsTimer = setInterval(() => {
        fps.value = frameCount;
        frameCount = 0;
        now.value = Date.now();
    }, 1000);
}
async function handlePauseBtnClicked() {
    isPausing.value = true;
    ws?.close();
    isPausing.value = false;
    isStarted.value = false;
}

onUnmounted(() => {
    ws?.close();
    if (currentObjectURL) {
        URL.revokeObjectURL(currentObjectURL);
        currentObjectURL = null;
    }
    if (fpsTimer) clearInterval(fpsTimer);
});
</script>

<template>
    <div class="grid-layout">
        <n-card title="视频流">
            <n-flex v-if="!isStarted" align="center" justify="center" style="height: 80%">
                <n-icon :size="64" :component="VideoOff32Regular" />
            </n-flex>
            <img v-else :src="outputFrame" alt="输出画面" style="width: 100%" />
        </n-card>
        <n-card title="控制台">
            <n-grid x-gap="12" :cols="2">
                <n-gi>
                    <n-button
                        type="primary"
                        :bordered="false"
                        style="width: 100%"
                        v-if="!isStarted"
                        :disabled="isStarting"
                        @click="handleStartBtnClicked">
                        <template #icon>
                            <n-icon>
                                <Play16Regular />
                            </n-icon>
                        </template>
                        开始
                    </n-button>
                    <n-button strong secondary style="width: 100%" v-else :disabled="isPausing" @click="handlePauseBtnClicked">
                        <template #icon>
                            <n-icon>
                                <Pause16Regular />
                            </n-icon>
                        </template>
                        停止
                    </n-button>
                </n-gi>
                <n-gi>
                    <n-button style="width: 100%">
                        <template #icon>
                            <n-icon>
                                <Settings16Regular />
                            </n-icon>
                        </template>
                        设置
                    </n-button>
                </n-gi>
            </n-grid>
            <n-descriptions
                label-placement="top"
                :column="1"
                label-style="font-size: 12px;color: #888888;"
                content-style="font-size: 16px;font-weight: bold;"
                style="margin-top: 20px">
                <n-descriptions-item label="帧率">
                    <n-ellipsis line-clamp="1"> {{ fps || "--" }} FPS </n-ellipsis>
                </n-descriptions-item>
                <n-descriptions-item label="持续时间">
                    <n-ellipsis line-clamp="1"> {{ isStarted ? wsDuration : "--" }}</n-ellipsis>
                </n-descriptions-item>
                <n-descriptions-item label="不知道写什么">
                    <n-ellipsis line-clamp="1"> 114514 </n-ellipsis>
                </n-descriptions-item>
                <n-descriptions-item label="只因你太美">
                    <n-ellipsis line-clamp="1"> 2778 </n-ellipsis>
                </n-descriptions-item>
            </n-descriptions>
        </n-card>
    </div>
</template>

<style scoped>
.grid-layout {
    display: grid;
    grid-template-columns: minmax(0, 1fr) min(300px, calc((100% - 12px) / 2));
    gap: 12px;
    margin-top: 12px;
}
@media (max-width: 500px) {
    .grid-layout {
        grid-template-columns: 1fr;
    }
}
:deep(.n-descriptions-table) {
    table-layout: fixed;
}
</style>
