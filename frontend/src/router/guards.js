export default function setupRouterGuards(router) {
    router.beforeEach(async (to) => {
        // 设置页面标题
        if (to.meta.title) document.title = to.meta.title;
    });
}
