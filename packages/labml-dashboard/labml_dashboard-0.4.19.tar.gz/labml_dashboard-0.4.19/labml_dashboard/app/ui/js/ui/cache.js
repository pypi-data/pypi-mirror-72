var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
define(["require", "exports", "./app", "../common/experiments", "./run_ui"], function (require, exports, app_1, experiments_1, run_ui_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    function getRuns() {
        return __awaiter(this, void 0, void 0, function* () {
            console.log("Reloading all");
            return new experiments_1.RunCollection(yield app_1.API.getRuns());
        });
    }
    exports.getRuns = getRuns;
    function clearCache() {
        run_ui_1.RunUI.clearCache();
    }
    exports.clearCache = clearCache;
});
