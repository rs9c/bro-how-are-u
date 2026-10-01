import { createRouter, createWebHistory } from "vue-router";
import setupRouterGuards from "@/router/guards";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            redirect: "/home",
        },
        {
            path: "/home",
            component: () => import("@/views/HomeView.vue"),
            meta: {
                title: "基于YOLOv8的摔倒检测与报警系统｜2026SRTP",
            },
        },
    ],
});

setupRouterGuards(router);

export default router;
