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
const YAML = require("yaml");
const PATH = require("path");
const experiments_1 = require("../../common/experiments");
const consts_1 = require("../consts");
const util_1 = require("../util");
const run_nodejs_1 = require("../run_nodejs");
class CacheEntry {
    constructor() {
        this.minDelay = 5 * 1000; // 5 seconds
        this.maxDelay = 2 * 60 * 60 * 1000; // 2 hours
        this.exponentialFactor = 1.5;
        this.lastLoaded = 0;
        this.delay = this.minDelay;
    }
    get() {
        return __awaiter(this, void 0, void 0, function* () {
            let now = (new Date()).getTime();
            if (this.cached == null || this.lastLoaded + this.delay < now) {
                let updated = yield this.loadIfUpdated(this.cached);
                if (updated != null) {
                    this.cached = updated;
                    this.delay = Math.max(this.minDelay, this.delay / this.exponentialFactor);
                    // console.log("Reduced checking time to ", this.delay)
                }
                else {
                    let delay = now - this.lastLoaded;
                    this.delay = Math.min(this.maxDelay, delay * this.exponentialFactor);
                    // console.log("Extended checking time to ", this.delay)
                }
                this.lastLoaded = now;
            }
            return this.cached;
        });
    }
    reset() {
        this.cached = null;
    }
}
class RunModelCacheEntry extends CacheEntry {
    constructor(name, uuid) {
        super();
        this.name = name;
        this.uuid = uuid;
    }
    static getMaxStep(values) {
        let maxStep = 0;
        for (let value of Object.values(values)) {
            maxStep = Math.max(maxStep, value.step);
        }
        return maxStep;
    }
    loadIfUpdated(original) {
        return __awaiter(this, void 0, void 0, function* () {
            if (original == null) {
                return yield this.watchedLoad();
            }
            let run = run_nodejs_1.RunNodeJS.create(new experiments_1.Run(original));
            let values = yield run.getValues();
            if (RunModelCacheEntry.getMaxStep(original.values) !==
                RunModelCacheEntry.getMaxStep(values)) {
                return yield this.watchedLoad();
            }
            // console.log('cached', this.uuid)
            return null;
        });
    }
    watchedLoad() {
        return __awaiter(this, void 0, void 0, function* () {
            // console.log(`Loading run ${this.name} ${this.uuid}`)
            let start = (new Date()).getTime();
            let loaded = yield this.load();
            let end = (new Date()).getTime();
            if (end - start > 100) {
                console.log(`Loaded run ${this.name} ${this.uuid} in ${(end - start)} ms`);
            }
            return loaded;
        });
    }
    load() {
        return __awaiter(this, void 0, void 0, function* () {
            let contents;
            try {
                contents = yield util_1.readFile(PATH.join(consts_1.LAB.experiments, this.name, this.uuid, 'run.yaml'));
            }
            catch (e) {
                console.log(`Failed to read run ${this.name} - ${this.uuid}`);
                return null;
            }
            let res = YAML.parse(contents);
            res = experiments_1.Run.fixRunModel(this.name, res);
            res.uuid = this.uuid;
            res.total_size = yield util_1.getDiskUsage(PATH.join(consts_1.LAB.experiments, this.name, this.uuid));
            res.artifacts_size = yield util_1.getDiskUsage(PATH.join(consts_1.LAB.experiments, this.name, this.uuid, 'artifacts'));
            res.checkpoints_size = yield util_1.getDiskUsage(PATH.join(consts_1.LAB.experiments, this.name, this.uuid, 'checkpoints'));
            res.tensorboard_size = yield util_1.getDiskUsage(PATH.join(consts_1.LAB.experiments, this.name, this.uuid, 'tensorboard'));
            res.sqlite_size = yield util_1.getDiskUsage(PATH.join(consts_1.LAB.experiments, this.name, this.uuid, 'sqlite.db'));
            res.analytics_size = yield util_1.getDiskUsage(PATH.join(consts_1.LAB.analytics, this.name, this.uuid));
            let run = run_nodejs_1.RunNodeJS.create(new experiments_1.Run(res));
            res.values = yield run.getValues();
            res.configs = (yield run.getConfigs()).configs;
            return res;
        });
    }
}
class ExperimentRunsSetCacheEntry extends CacheEntry {
    constructor() {
        super();
        this.maxDelay = 30 * 1000;
    }
    loadIfUpdated(original) {
        return __awaiter(this, void 0, void 0, function* () {
            let loaded = yield ExperimentRunsSetCacheEntry.load();
            if (ExperimentRunsSetCacheEntry.isUpdated(original, loaded)) {
                let count = 0;
                for (let runs of Object.values(loaded)) {
                    for (let r of runs.keys()) {
                        count++;
                    }
                }
                console.log(`Found ${count} runs`);
                return loaded;
            }
            return null;
        });
    }
    static isUpdated(original, loaded) {
        if (original == null) {
            return true;
        }
        for (let [e, runs] of Object.entries(loaded)) {
            if (runs == null) {
                return true;
            }
            if (original[e] == null) {
                return true;
            }
            for (let r of runs.keys()) {
                if (!original[e].has(r)) {
                    return true;
                }
            }
        }
        return false;
    }
    static load() {
        return __awaiter(this, void 0, void 0, function* () {
            let experiments = yield util_1.readdir(consts_1.LAB.experiments);
            let res = {};
            for (let e of experiments) {
                if (!e.startsWith('_')) {
                    res[e] = new Set(yield util_1.readdir(PATH.join(consts_1.LAB.experiments, e)));
                }
            }
            return res;
        });
    }
}
class Cache {
    constructor() {
        this.experimentRunsSet = new ExperimentRunsSetCacheEntry();
        this.runs = {};
    }
    getRun(uuid) {
        return __awaiter(this, void 0, void 0, function* () {
            if (this.runs[uuid] == null) {
                let expSet = yield this.experimentRunsSet.get();
                for (let [expName, runs] of Object.entries(expSet)) {
                    if (runs.has(uuid)) {
                        if (this.runs[uuid] != null) {
                            if (this.runs[uuid].name != expName) {
                                this.runs[uuid] = new RunModelCacheEntry(expName, uuid);
                            }
                        }
                        else {
                            this.runs[uuid] = new RunModelCacheEntry(expName, uuid);
                        }
                    }
                }
            }
            return yield this.runs[uuid].get();
        });
    }
    getExperiment(name) {
        return __awaiter(this, void 0, void 0, function* () {
            let runs = [];
            for (let r of (yield this.experimentRunsSet.get())[name].keys()) {
                runs.push(yield this.getRun(r));
            }
            return runs;
        });
    }
    getExperimentAsync(name) {
        return __awaiter(this, void 0, void 0, function* () {
            let promises = [];
            for (let r of (yield this.experimentRunsSet.get())[name].keys()) {
                promises.push(this.getRun(r));
            }
            return promises;
        });
    }
    getAllAsync() {
        return __awaiter(this, void 0, void 0, function* () {
            let promises = [];
            for (let e of Object.keys(yield this.experimentRunsSet.get())) {
                promises = promises.concat(yield this.getExperimentAsync(e));
            }
            let runs = yield Promise.all(promises);
            let filteredRuns = [];
            for (let r of runs) {
                if (r != null) {
                    filteredRuns.push(r);
                }
            }
            return new experiments_1.RunCollection(filteredRuns);
        });
    }
    getAll() {
        return __awaiter(this, void 0, void 0, function* () {
            let runs = [];
            for (let e of Object.keys(yield this.experimentRunsSet.get())) {
                runs = runs.concat(yield this.getExperiment(e));
            }
            let filteredRuns = [];
            for (let r of runs) {
                if (r != null) {
                    filteredRuns.push(r);
                }
            }
            return new experiments_1.RunCollection(filteredRuns);
        });
    }
    resetRun(uuid) {
        // console.log('resetCache', uuid)
        if (this.runs[uuid] != null) {
            delete this.runs[uuid];
        }
        this.experimentRunsSet.reset();
    }
}
const _CACHE = new Cache();
class ExperimentsFactory {
    static load() {
        return __awaiter(this, void 0, void 0, function* () {
            let start = (new Date()).getTime();
            let all = yield _CACHE.getAll();
            let end = (new Date()).getTime();
            console.log(`Loaded runs in ${(end - start)} ms`);
            return all;
        });
    }
    static cacheReset(uuid) {
        // console.log('reset', experimentName, runUuid)
        _CACHE.resetRun(uuid);
    }
}
exports.ExperimentsFactory = ExperimentsFactory;
