<script setup>
import { darkTheme, NGlobalStyle, useOsTheme, zhCN, dateZhCN, NDialogProvider, NConfigProvider, NMessageProvider, NLoadingBarProvider } from "naive-ui";
import { useThemeStore } from "@/stores/theme";
import { RouterView } from "vue-router";
import { computed } from "vue";
import { storeToRefs } from "pinia";

// 主题相关
const osTheme = useOsTheme();
const theme = computed(() => (osTheme.value === "dark" ? darkTheme : null));
const themeStore = useThemeStore();
const { themeColor } = storeToRefs(themeStore);
const themeOverrides = computed(() => ({
    common: {
        borderRadius: "8px",
    },
    Input: {
        borderFocus: "1px solid" + themeColor.value,
        borderHover: "1px solid" + themeColor.value,
        caretColor: themeColor.value,
        loadingColor: themeColor.value,
    },
    LoadingBar: {
        colorLoading: themeColor.value,
    },
    Dialog: {
        borderRadius: "12px",
    },
}));
</script>

<template>
    <n-config-provider :theme-overrides="themeOverrides" :theme :locale="zhCN" :date-locale="dateZhCN">
        <n-global-style />
        <n-dialog-provider>
            <n-message-provider>
                <n-loading-bar-provider>
                    <RouterView />
                </n-loading-bar-provider>
            </n-message-provider>
        </n-dialog-provider>
    </n-config-provider>
</template>

<style scoped></style>
