<script setup>
import {
    darkTheme,
    NGlobalStyle,
    useOsTheme,
    zhCN,
    dateZhCN,
    NDialogProvider,
    NConfigProvider,
    NMessageProvider,
    NLoadingBarProvider,
} from "naive-ui";
import { useThemeStore } from "@/stores/theme";
import { RouterView } from "vue-router";
import { computed } from "vue";
import { storeToRefs } from "pinia";
import { scaleColor } from "seemly";

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
        colorFocus: themeColor.value + "1a",
    },
    LoadingBar: {
        colorLoading: themeColor.value,
    },
    Dialog: {
        borderRadius: "12px",
    },
    Button: {
        textColorTextHover: themeColor.value,
        textColorTextPressed: scaleColor(themeColor.value, { lightness: 0.73 }),
        textColorTextFocus: themeColor.value,
        colorPrimary: themeColor.value,
        colorDisabledPrimary: themeColor.value,
        rippleColorPrimary: themeColor.value,
        colorHoverPrimary: scaleColor(themeColor.value, { lightness: 1.23 }),
        colorFocusPrimary: scaleColor(themeColor.value, { lightness: 1.23 }),
        colorPressedPrimary: scaleColor(themeColor.value, { lightness: 0.73 }),
        textColorGhostHover: themeColor.value,
        borderHover: "1px solid " + themeColor.value,
        borderFocus: "1px solid " + themeColor.value,
        textColorGhostPressed: scaleColor(themeColor.value, { lightness: 0.73 }),
        borderPressed: "1px solid " + scaleColor(themeColor.value, { lightness: 0.73 }),
        rippleColor: themeColor.value,
        textColorHover: themeColor.value,
        textColorFocus: themeColor.value,
        textColorPressed: scaleColor(themeColor.value, { lightness: 0.73 }),
    },
    Menu: {
        itemTextColorActive: themeColor.value,
        itemTextColorActiveHover: themeColor.value,
        itemIconColorActive: themeColor.value,
        itemIconColorActiveHover: themeColor.value,
        itemColorActive: themeColor.value + "26",
        itemColorActiveHover: themeColor.value + "26",
        itemColorActiveCollapsed: themeColor.value + "26",
    },
    Card: {
        borderRadius: "12px",
    },
    Radio: {
        dotColorActive: themeColor.value,
        boxShadowActive: "inset 0 0 0 1px " + themeColor.value,
        boxShadowHover: "inset 0 0 0 1px " + themeColor.value,
        boxShadowFocus: "inset 0 0 0 1px " + themeColor.value + ", 0 0 0 2px " + themeColor.value + "33",
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
