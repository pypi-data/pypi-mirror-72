var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
define(["require", "exports"], function (require, exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    class Api {
        getRuns() {
            return __awaiter(this, void 0, void 0, function* () {
                return null;
            });
        }
        getIndicators(uuid) {
            return __awaiter(this, void 0, void 0, function* () {
                return null;
            });
        }
        getConfigs(uuid) {
            return __awaiter(this, void 0, void 0, function* () {
                return null;
            });
        }
        getDiff(uuid) {
            return __awaiter(this, void 0, void 0, function* () {
                return null;
            });
        }
        getCode(uuid) {
            return __awaiter(this, void 0, void 0, function* () {
                return null;
            });
        }
        getValues(uuid) {
            return __awaiter(this, void 0, void 0, function* () {
                return null;
            });
        }
        launchTensorboard(uuid) {
            return __awaiter(this, void 0, void 0, function* () {
                return null;
            });
        }
        launchTensorboards(uuids) {
            return __awaiter(this, void 0, void 0, function* () {
                return null;
            });
        }
        launchJupyter(uuid, analyticsTemplate) {
            return __awaiter(this, void 0, void 0, function* () {
                return null;
            });
        }
        getAnalyticsTemplates(uuid) {
            return __awaiter(this, void 0, void 0, function* () {
                return null;
            });
        }
        removeRun(uuid) {
            return __awaiter(this, void 0, void 0, function* () {
                return null;
            });
        }
        cleanupCheckpoints(uuid) {
            return __awaiter(this, void 0, void 0, function* () {
                return null;
            });
        }
        cleanupArtifacts(uuid) {
            return __awaiter(this, void 0, void 0, function* () {
                return null;
            });
        }
        updateRun(uuid, data) {
            return __awaiter(this, void 0, void 0, function* () {
                return null;
            });
        }
        saveDashboard(name, cells) {
            return __awaiter(this, void 0, void 0, function* () {
                return null;
            });
        }
        loadDashboards() {
            return __awaiter(this, void 0, void 0, function* () {
                return null;
            });
        }
    }
    exports.Api = Api;
    exports.API_SPEC = new Api();
});
