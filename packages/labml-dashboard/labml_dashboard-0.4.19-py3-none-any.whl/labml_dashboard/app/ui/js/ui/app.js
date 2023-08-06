define(["require", "exports", "./screen", "../lib/weya/router", "../lib/io/ajax", "../common/api_handler", "../common/api"], function (require, exports, screen_1, router_1, ajax_1, api_handler_1, api_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.ROUTER = new router_1.Router({
        emulateState: false,
        hashChange: false,
        pushState: true,
        root: '/',
        onerror: e => {
            console.error('Error', e);
        }
    });
    exports.SCREEN = new screen_1.ScreenContainer();
    const protocol = window.location.protocol === 'http:' ? 'http' : 'https';
    exports.PORT = new ajax_1.AjaxHttpPort(protocol, window.location.hostname, parseInt(window.location.port), '/api');
    api_handler_1.wrapAPI(exports.PORT, api_1.API_SPEC);
    exports.API = api_1.API_SPEC;
});
