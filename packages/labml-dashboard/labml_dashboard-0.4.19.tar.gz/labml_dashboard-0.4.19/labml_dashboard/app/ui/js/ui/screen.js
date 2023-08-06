define(["require", "exports"], function (require, exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    class ScreenContainer {
        setView(view) {
            document.body.innerHTML = '';
            document.body.append(view.render());
        }
    }
    exports.ScreenContainer = ScreenContainer;
});
