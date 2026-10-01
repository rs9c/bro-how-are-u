import { ref } from "vue";
import { defineStore } from "pinia";

// 主题相关配置
export const useThemeStore = defineStore("theme", () => {
    const themeColor = ref("#2080f0");
    // TODO 用户可以自定义主题色
    return { themeColor };
});
