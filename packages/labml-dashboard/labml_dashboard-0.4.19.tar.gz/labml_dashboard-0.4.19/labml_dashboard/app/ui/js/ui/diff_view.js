var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
define(["require", "exports", "./app", "../lib/weya/weya", "./cache", "./run_ui", "./hljs"], function (require, exports, app_1, weya_1, cache_1, run_ui_1, hljs_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    class DiffView {
        constructor(uuid) {
            this.uuid = uuid;
        }
        render() {
            this.elem = weya_1.Weya('div.container', $ => {
                this.diffView = $('div.diff', '');
            });
            this.renderRun().then();
            return this.elem;
        }
        renderRun() {
            return __awaiter(this, void 0, void 0, function* () {
                this.run = (yield cache_1.getRuns()).getRun(this.uuid);
                this.runUI = run_ui_1.RunUI.create(this.run);
                this.diff = yield this.runUI.loadDiff();
                let h = hljs_1.highlight('diff', this.diff, true, null);
                let diffPre;
                weya_1.Weya(this.diffView, $ => {
                    diffPre = $('pre');
                });
                diffPre.innerHTML = h.value;
            });
        }
    }
    class CodeView {
        constructor(uuid) {
            this.uuid = uuid;
        }
        render() {
            this.elem = weya_1.Weya('div.container', $ => {
                this.diffView = $('div.diff', '');
            });
            this.renderRun().then();
            return this.elem;
        }
        renderRun() {
            return __awaiter(this, void 0, void 0, function* () {
                this.run = (yield cache_1.getRuns()).getRun(this.uuid);
                this.runUI = run_ui_1.RunUI.create(this.run);
                this.diff = yield this.runUI.loadCode();
                let h = hljs_1.highlight('python', this.diff, true, null);
                let diffPre;
                weya_1.Weya(this.diffView, $ => {
                    diffPre = $('pre');
                });
                diffPre.innerHTML = h.value;
            });
        }
    }
    class DiffHandler {
        constructor() {
            this.handleRun = (uuid) => {
                app_1.SCREEN.setView(new DiffView(uuid));
            };
            this.handleRunCode = (uuid) => {
                app_1.SCREEN.setView(new CodeView(uuid));
            };
            app_1.ROUTER.route('run/:uuid/diff', [this.handleRun]);
            app_1.ROUTER.route('run/:uuid/code', [this.handleRunCode]);
        }
    }
    exports.DiffHandler = DiffHandler;
});
