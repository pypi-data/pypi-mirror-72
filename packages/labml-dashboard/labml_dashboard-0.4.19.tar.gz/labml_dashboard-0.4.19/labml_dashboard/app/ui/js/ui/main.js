define(["require", "exports", "./app", "./run_view", "./diff_view", "./table/table_view"], function (require, exports, app_1, run_view_1, diff_view_1, table_view_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    new run_view_1.RunHandler();
    new diff_view_1.DiffHandler();
    new table_view_1.TableHandler();
    if (document.readyState === 'complete' ||
        document.readyState === 'interactive') {
        app_1.ROUTER.start(null, false);
    }
    else {
        document.addEventListener('DOMContentLoaded', () => {
            app_1.ROUTER.start(null, false);
        });
    }
});
