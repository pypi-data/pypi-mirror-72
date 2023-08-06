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
const sqlite3 = require("sqlite3");
const experiments_1 = require("../common/experiments");
const PATH = require("path");
const YAML = require("yaml");
const consts_1 = require("./consts");
const util_1 = require("./util");
const cache_1 = require("./experiments/cache");
const UPDATABLE_KEYS = new Set(['comment', 'notes', 'tags']);
const USE_CACHE = true;
const USE_VALUES_CACHE = false;
class RunNodeJS {
    constructor(run) {
        this.run = run;
    }
    static create(run) {
        return new RunNodeJS(run);
    }
    loadDatabase() {
        if (this.db != null) {
            return new Promise(resolve => {
                resolve();
            });
        }
        let path = PATH.join(consts_1.LAB.experiments, this.run.name, this.run.uuid, 'sqlite.db');
        return new Promise((resolve, reject) => {
            util_1.exists(path).then((isExists) => {
                if (!isExists) {
                    this.db = null;
                    return reject(false);
                }
                this.db = new sqlite3.Database(path, sqlite3.OPEN_READONLY, (err) => {
                    if (err) {
                        console.log(`SQLite connect failed ${this.run.name} : ${this.run.uuid}`, err);
                        this.db = null;
                        reject(err);
                    }
                    else {
                        resolve();
                    }
                });
            });
        });
    }
    collectLastValue(to_collect) {
        for (let i = 0; i < to_collect.length; ++i) {
            to_collect[i] = `"${to_collect[i]}"`;
        }
        let sql = `SELECT a.* FROM scalars AS a
            INNER JOIN (
                SELECT indicator, MAX(step) AS step 
                FROM scalars
                WHERE indicator IN (${to_collect.join(',')})
                GROUP BY indicator
            ) b ON a.indicator = b.indicator AND a.step = b.step`;
        return new Promise((resolve, reject) => {
            this.db.all(sql, (err, rows) => {
                if (err) {
                    reject(err);
                }
                else {
                    let values = {};
                    for (let row of rows) {
                        values[row.indicator] = row;
                    }
                    resolve(values);
                }
            });
        });
    }
    getLastStep() {
        let sql = `SELECT MAX(step) as step FROM scalars`;
        return new Promise((resolve, reject) => {
            this.db.all(sql, (err, rows) => {
                if (err) {
                    reject(err);
                }
                else {
                    let step = 0;
                    for (let row of rows) {
                        step = row.step;
                    }
                    resolve(step);
                }
            });
        });
    }
    migrateIndicatorsToSingleFile() {
        return __awaiter(this, void 0, void 0, function* () {
            console.log("Migrating indicators to a single file: ", this.run.name, this.run.uuid);
            let indicatorsFile = PATH.join(consts_1.LAB.experiments, this.run.name, this.run.uuid, 'indicators.yaml');
            let artifactsFile = PATH.join(consts_1.LAB.experiments, this.run.name, this.run.uuid, 'artifacts.yaml');
            let indicators;
            try {
                indicators = YAML.parse(yield util_1.readFile(indicatorsFile));
            }
            catch (e) {
                indicators = {};
            }
            let artifacts;
            try {
                artifacts = YAML.parse(yield util_1.readFile(artifactsFile));
            }
            catch (e) {
                artifacts = {};
            }
            for (let [k, v] of Object.entries(artifacts)) {
                indicators[k] = v;
            }
            yield util_1.writeFile(indicatorsFile, YAML.stringify({ 'indicators': indicators }));
            yield util_1.safeRemove(artifactsFile);
        });
    }
    getIndicators() {
        return __awaiter(this, void 0, void 0, function* () {
            // TODO: Caching
            if (!USE_CACHE || this.indicators == null) {
                let contents = YAML.parse(yield util_1.readFile(PATH.join(consts_1.LAB.experiments, this.run.name, this.run.uuid, 'indicators.yaml')));
                if (contents['indicators'] == null) {
                    yield this.migrateIndicatorsToSingleFile();
                    try {
                        return this.getIndicators();
                    }
                    catch (e) {
                        this.indicators = new experiments_1.Indicators({});
                        return this.indicators;
                    }
                }
                this.indicators = new experiments_1.Indicators(contents['indicators']);
            }
            return this.indicators;
        });
    }
    getConfigs() {
        return __awaiter(this, void 0, void 0, function* () {
            if (!USE_CACHE || this.configs == null) {
                try {
                    let contents = yield util_1.readFile(PATH.join(consts_1.LAB.experiments, this.run.name, this.run.uuid, 'configs.yaml'));
                    const doc = YAML.parseDocument(contents);
                    if (doc.errors.length > 0) {
                        throw doc.errors[0];
                    }
                    let configs = doc.toJSON();
                    this.configs = new experiments_1.Configs(doc.toJSON());
                    // this.configs = new Configs(YAML.parse(contents))
                }
                catch (e) {
                    return new experiments_1.Configs({});
                }
            }
            return this.configs;
        });
    }
    getDiff() {
        return __awaiter(this, void 0, void 0, function* () {
            return yield util_1.readFile(PATH.join(consts_1.LAB.experiments, this.run.name, this.run.uuid, 'source.diff'));
        });
    }
    getCode() {
        return __awaiter(this, void 0, void 0, function* () {
            try {
                return yield util_1.readFile(this.run.python_file);
            }
            catch (e) {
                return '# File missing';
            }
        });
    }
    getValues() {
        return __awaiter(this, void 0, void 0, function* () {
            if (USE_VALUES_CACHE && this.values != null) {
                return this.values;
            }
            // console.log("loading values")
            let empty = { step: { indicator: 'step', value: 0, step: 0 } };
            try {
                yield this.loadDatabase();
            }
            catch (e) {
                return empty;
            }
            let indicators = yield this.getIndicators();
            let to_collect = [];
            for (let ind of Object.values(indicators.indicators)) {
                if (ind.class_name == null) {
                    continue;
                }
                let key = ind.class_name.indexOf('Scalar') !== -1
                    ? ind.name
                    : `${ind.name}.mean`;
                if (ind.is_print) {
                    to_collect.push(key);
                }
            }
            let values = empty;
            try {
                values = yield this.collectLastValue(to_collect);
            }
            catch (e) {
                console.log('Could not read from SQLite db', this.run.name, this.run.uuid, e);
                return empty;
            }
            values['step'] = { indicator: 'step', value: 0, step: yield this.getLastStep() };
            this.values = values;
            return values;
        });
    }
    getLab() {
        return __awaiter(this, void 0, void 0, function* () {
            return consts_1.LAB;
        });
    }
    remove() {
        return __awaiter(this, void 0, void 0, function* () {
            let path = PATH.join(consts_1.LAB.experiments, this.run.name, this.run.uuid);
            yield util_1.rmtree(path);
            let analytics = PATH.join(consts_1.LAB.analytics, this.run.name, this.run.uuid);
            yield util_1.rmtree(analytics);
        });
    }
    update(data) {
        return __awaiter(this, void 0, void 0, function* () {
            let name = null;
            if (data['name'] != null) {
                name = data['name'];
            }
            let path = PATH.join(consts_1.LAB.experiments, this.run.name, this.run.uuid, 'run.yaml');
            let contents = yield util_1.readFile(path);
            let run = YAML.parse(contents);
            for (let k in data) {
                if (UPDATABLE_KEYS.has(k)) {
                    run[k] = data[k];
                }
            }
            yield util_1.writeFile(path, YAML.stringify(run));
            if (name != null) {
                yield this.rename(name);
            }
        });
    }
    rename(name) {
        return __awaiter(this, void 0, void 0, function* () {
            let oldPath = PATH.join(consts_1.LAB.experiments, this.run.name, this.run.uuid);
            let folder = PATH.join(consts_1.LAB.experiments, name);
            let newPath = PATH.join(consts_1.LAB.experiments, name, this.run.uuid);
            if (!(yield util_1.exists(folder))) {
                yield util_1.mkdir(folder, { recursive: true });
            }
            yield util_1.rename(oldPath, newPath);
            cache_1.ExperimentsFactory.cacheReset(this.run.uuid);
        });
    }
    cleanupCheckpoints() {
        return __awaiter(this, void 0, void 0, function* () {
            let path = PATH.join(consts_1.LAB.experiments, this.run.name, this.run.uuid, 'checkpoints');
            if (!(yield util_1.exists(path))) {
                return;
            }
            let checkpoints = yield util_1.readdir(path);
            if (checkpoints.length == 0) {
                return;
            }
            let last = parseInt(checkpoints[0]);
            for (let c of checkpoints) {
                if (last < parseInt(c)) {
                    last = parseInt(c);
                }
            }
            for (let c of checkpoints) {
                if (last !== parseInt(c)) {
                    yield util_1.rmtree(PATH.join(path, c));
                }
            }
        });
    }
    getArtifactFiles() {
        let sql = 'SELECT indicator, step, filename FROM tensors';
        return new Promise((resolve, reject) => {
            this.db.all(sql, (err, rows) => {
                if (err) {
                    reject(err);
                }
                else {
                    let files = {};
                    for (let row of rows) {
                        if (files[row.indicator] == null) {
                            files[row.indicator] = [];
                        }
                        files[row.indicator].push({
                            step: row.step,
                            filename: row.filename
                        });
                    }
                    resolve(files);
                }
            });
        });
    }
    cleanupArtifacts() {
        return __awaiter(this, void 0, void 0, function* () {
            try {
                yield this.loadDatabase();
            }
            catch (e) {
                return;
            }
            let files = yield this.getArtifactFiles();
            let stepsCount = {};
            let indicatorsCount = 0;
            for (let fileList of Object.values(files)) {
                for (let file of fileList) {
                    if (stepsCount[file.step] == null) {
                        stepsCount[file.step] = 0;
                    }
                    stepsCount[file.step]++;
                }
                indicatorsCount++;
            }
            let steps = [];
            for (let [s, c] of Object.entries(stepsCount)) {
                if (c === indicatorsCount) {
                    steps.push(parseInt(s));
                }
            }
            steps.sort((a, b) => {
                return a - b;
            });
            if (steps.length == 0) {
                return yield this.removeArtifactsExcept(files, steps);
            }
            let last = steps[steps.length - 1];
            let interval = Math.max(1, Math.floor(last / 99));
            let condensed = [steps[0]];
            for (let i = 1; i < steps.length; ++i) {
                let s = steps[i];
                if (s - condensed[condensed.length - 1] >= interval) {
                    condensed.push(s);
                }
            }
            if (last != condensed[condensed.length - 1]) {
                condensed.push(last);
            }
            return yield this.removeArtifactsExcept(files, condensed);
        });
    }
    removeArtifactsExcept(files, steps) {
        return __awaiter(this, void 0, void 0, function* () {
            let stepSet = new Set();
            for (let s of steps) {
                stepSet.add(s);
            }
            let path = PATH.join(consts_1.LAB.experiments, this.run.name, this.run.uuid, 'sqlite.db');
            let db = yield new Promise(((resolve, reject) => {
                let db = new sqlite3.Database(path, sqlite3.OPEN_READWRITE, (err) => {
                    if (err) {
                        console.log(`SQLite connect failed ${this.run.name} : ${this.run.uuid}`, err);
                        this.db = null;
                        reject(err);
                    }
                    else {
                        resolve(db);
                    }
                });
            }));
            console.log('Cleaning up artifacts', (new Date()).getTime());
            db.run('BEGIN TRANSACTION');
            let promises = [];
            for (let [name, fileList] of Object.entries(files)) {
                for (let file of fileList) {
                    if (stepSet.has(file.step)) {
                        continue;
                    }
                    let path = PATH.join(consts_1.LAB.experiments, this.run.name, this.run.uuid, 'artifacts', file.filename);
                    promises.push(util_1.safeRemove(path));
                    let sql = 'DELETE FROM tensors WHERE indicator = ? AND step = ?';
                    db.run(sql, name, file.step);
                }
            }
            console.log('Committing', (new Date()).getTime());
            yield util_1.sqliteRun(db, 'COMMIT');
            console.log("Closing db", (new Date()).getTime());
            try {
                yield util_1.sqliteClose(db);
            }
            catch (err) {
                console.log('Error closing db', this.run.uuid);
            }
            console.log('Deleting files', promises.length, (new Date()).getTime());
            yield Promise.all(promises);
            console.log('Deleted files', (new Date()).getTime());
        });
    }
}
exports.RunNodeJS = RunNodeJS;
