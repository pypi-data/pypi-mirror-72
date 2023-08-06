var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
define(["require", "exports", "../common/experiments", "./app", "./cache"], function (require, exports, experiments_1, app_1, cache_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    class RunUI {
        constructor(run) {
            this.generations = 0;
            this.children = 0;
            this.run = run;
        }
        static create(run) {
            if (!(run.hash() in RunUI.cache)) {
                RunUI.cache[run.hash()] = new RunUI(run);
            }
            return RunUI.cache[run.hash()];
        }
        static clearCache() {
            this.cache = {};
        }
        loadIndicators() {
            return __awaiter(this, void 0, void 0, function* () {
                if (this.indicators != null) {
                    return this.indicators;
                }
                if (this.run.indicators != null) {
                    this.indicators = new experiments_1.Indicators(this.run.indicators);
                    return this.indicators;
                }
                this.indicators = new experiments_1.Indicators(yield app_1.API.getIndicators(this.run.uuid));
                return this.indicators;
            });
        }
        loadConfigs() {
            return __awaiter(this, void 0, void 0, function* () {
                if (this.configs != null) {
                    return this.configs;
                }
                if (this.run.configs != null) {
                    this.configs = new experiments_1.Configs(this.run.configs);
                    return this.configs;
                }
                this.configs = new experiments_1.Configs(yield app_1.API.getConfigs(this.run.uuid));
                return this.configs;
            });
        }
        loadDiff() {
            return __awaiter(this, void 0, void 0, function* () {
                if (this.diff == null) {
                    this.diff = yield app_1.API.getDiff(this.run.uuid);
                }
                return this.diff;
            });
        }
        loadCode() {
            return __awaiter(this, void 0, void 0, function* () {
                if (this.code == null) {
                    this.code = yield app_1.API.getCode(this.run.uuid);
                }
                return this.code;
            });
        }
        loadValues() {
            return __awaiter(this, void 0, void 0, function* () {
                if (this.values != null) {
                    return this.values;
                }
                if (this.run.values != null) {
                    this.values = this.run.values;
                    return this.values;
                }
                this.values = yield app_1.API.getValues(this.run.uuid);
                return this.values;
            });
        }
        launchTensorboard() {
            return __awaiter(this, void 0, void 0, function* () {
                return yield app_1.API.launchTensorboard(this.run.uuid);
            });
        }
        launchJupyter(templateName) {
            return __awaiter(this, void 0, void 0, function* () {
                return yield app_1.API.launchJupyter(this.run.uuid, templateName);
            });
        }
        getAnalyticsTemplates() {
            return __awaiter(this, void 0, void 0, function* () {
                return yield app_1.API.getAnalyticsTemplates(this.run.uuid);
            });
        }
        remove() {
            return __awaiter(this, void 0, void 0, function* () {
                return yield app_1.API.removeRun(this.run.uuid);
            });
        }
        cleanupCheckpoints() {
            return __awaiter(this, void 0, void 0, function* () {
                return yield app_1.API.cleanupCheckpoints(this.run.uuid);
            });
        }
        cleanupArtifacts() {
            return __awaiter(this, void 0, void 0, function* () {
                return yield app_1.API.cleanupArtifacts(this.run.uuid);
            });
        }
        update(data) {
            return __awaiter(this, void 0, void 0, function* () {
                cache_1.clearCache();
                this.run.update(data);
                return yield app_1.API.updateRun(this.run.uuid, data);
            });
        }
    }
    exports.RunUI = RunUI;
    RunUI.cache = {};
});
