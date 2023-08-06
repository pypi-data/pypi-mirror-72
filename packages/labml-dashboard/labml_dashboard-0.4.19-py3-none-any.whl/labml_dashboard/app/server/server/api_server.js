"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const api_1 = require("../common/api");
const cache_1 = require("./experiments/cache");
const run_nodejs_1 = require("./run_nodejs");
const tensorboard_1 = require("./tensorboard");
const jupyter_1 = require("./jupyter");
const PATH = require("path");
const consts_1 = require("./consts");
const util_1 = require("./util");
const YAML = require("yaml");
let TENSORBOARD = null;
let JUPYTER = null;
function getRun(runUuid) {
    return __awaiter(this, void 0, void 0, function* () {
        let runs = yield cache_1.ExperimentsFactory.load();
        return run_nodejs_1.RunNodeJS.create(runs.getRun(runUuid));
    });
}
class ApiServer extends api_1.Api {
    getRuns() {
        return __awaiter(this, void 0, void 0, function* () {
            let runs = yield cache_1.ExperimentsFactory.load();
            return runs.toJSON();
        });
    }
    getIndicators(uuid) {
        return __awaiter(this, void 0, void 0, function* () {
            let run = yield getRun(uuid);
            let indicators = yield run.getIndicators();
            return indicators.toJSON();
        });
    }
    getConfigs(uuid) {
        return __awaiter(this, void 0, void 0, function* () {
            let run = yield getRun(uuid);
            let configs = yield run.getConfigs();
            return configs.toJSON();
        });
    }
    getDiff(uuid) {
        return __awaiter(this, void 0, void 0, function* () {
            let run = yield getRun(uuid);
            return yield run.getDiff();
        });
    }
    getCode(uuid) {
        return __awaiter(this, void 0, void 0, function* () {
            let run = yield getRun(uuid);
            return yield run.getCode();
        });
    }
    getValues(uuid) {
        return __awaiter(this, void 0, void 0, function* () {
            let run = yield getRun(uuid);
            return yield run.getValues();
        });
    }
    launchTensorboard(uuid) {
        return __awaiter(this, void 0, void 0, function* () {
            let runs = yield cache_1.ExperimentsFactory.load();
            let run = runs.getRun(uuid);
            if (TENSORBOARD != null) {
                TENSORBOARD.stop();
            }
            TENSORBOARD = new tensorboard_1.Tensorboard([run]);
            try {
                yield TENSORBOARD.start();
                return 'http://localhost:6006';
            }
            catch (e) {
                console.log(e);
                TENSORBOARD = null;
                return '';
            }
        });
    }
    launchTensorboards(uuids) {
        return __awaiter(this, void 0, void 0, function* () {
            let runsList = [];
            for (let r of uuids) {
                let runs = yield cache_1.ExperimentsFactory.load();
                runsList.push(runs.getRun(r));
            }
            if (TENSORBOARD != null) {
                TENSORBOARD.stop();
            }
            TENSORBOARD = new tensorboard_1.Tensorboard(runsList);
            try {
                yield TENSORBOARD.start();
                return 'http://localhost:6006';
            }
            catch (e) {
                TENSORBOARD = null;
                return '';
            }
        });
    }
    launchJupyter(uuid, analyticsTemplate) {
        return __awaiter(this, void 0, void 0, function* () {
            let runs = yield cache_1.ExperimentsFactory.load();
            let run = runs.getRun(uuid);
            if (JUPYTER == null) {
                JUPYTER = new jupyter_1.Jupyter();
                try {
                    yield JUPYTER.start();
                }
                catch (e) {
                    JUPYTER = null;
                    return '';
                }
            }
            return yield JUPYTER.setupTemplate(run, analyticsTemplate);
        });
    }
    getAnalyticsTemplates(uuid) {
        return __awaiter(this, void 0, void 0, function* () {
            let run = yield getRun(uuid);
            let templateNames = [];
            let lab = yield run.getLab();
            for (let k in lab.analyticsTemplates) {
                templateNames.push(k);
            }
            return templateNames;
        });
    }
    removeRun(uuid) {
        return __awaiter(this, void 0, void 0, function* () {
            try {
                let run = yield getRun(uuid);
                yield run.remove();
                cache_1.ExperimentsFactory.cacheReset(uuid);
            }
            catch (e) {
            }
        });
    }
    cleanupCheckpoints(uuid) {
        return __awaiter(this, void 0, void 0, function* () {
            let run = yield getRun(uuid);
            yield run.cleanupCheckpoints();
            cache_1.ExperimentsFactory.cacheReset(uuid);
        });
    }
    cleanupArtifacts(uuid) {
        return __awaiter(this, void 0, void 0, function* () {
            let run = yield getRun(uuid);
            yield run.cleanupArtifacts();
            cache_1.ExperimentsFactory.cacheReset(uuid);
        });
    }
    updateRun(uuid, data) {
        return __awaiter(this, void 0, void 0, function* () {
            let run = yield getRun(uuid);
            yield run.update(data);
            cache_1.ExperimentsFactory.cacheReset(uuid);
        });
    }
    saveDashboard(name, cells) {
        return __awaiter(this, void 0, void 0, function* () {
            let path = PATH.join(consts_1.LAB.path, ".labml_dashboard.yaml");
            let dashboards;
            try {
                let contents = yield util_1.readFile(path);
                dashboards = YAML.parse(contents);
            }
            catch (e) {
                dashboards = {};
            }
            dashboards[name] = cells;
            yield util_1.writeFile(path, YAML.stringify(dashboards));
        });
    }
    loadDashboards() {
        return __awaiter(this, void 0, void 0, function* () {
            let path = PATH.join(consts_1.LAB.path, ".labml_dashboard.yaml");
            let dashboards;
            try {
                let contents = yield util_1.readFile(path);
                dashboards = YAML.parse(contents);
            }
            catch (e) {
                dashboards = {};
            }
            return dashboards;
        });
    }
}
exports.API = new ApiServer();
