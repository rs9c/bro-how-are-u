import { createRouter, createWebHistory } from "vue-router";
import setupRouterGuards from "@/router/guards";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            redirect: "/stream",
            component: () => import("@/views/HomeView.vue"),
            meta: {
                title: "基于YOLOv8的摔倒检测与报警系统｜2026SRTP",
            },
            children: [
                {
                    path: "stream",
                    component: () => import("@/views/StreamView.vue"),
                },
                {
                    path: "picture",
                    component: () => import("@/views/PictureView.vue"),
                },
                {
                    path: "video",
                    component: () => import("@/views/VideoView.vue"),
                },
            ],
        },
        {
            path: "/:otherPages(.*)*",
            redirect: "/stream",
        },
    ],
});

setupRouterGuards(router);

export default router;
