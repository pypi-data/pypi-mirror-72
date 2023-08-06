"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
class Indicators {
    constructor(indicators) {
        this.indicators = indicators;
    }
    toJSON() {
        return this.indicators;
    }
}
exports.Indicators = Indicators;
class Configs {
    constructor(configs) {
        for (let [k, v] of Object.entries(configs)) {
            if (v.is_explicitly_specified == null) {
                v.is_explicitly_specified = false;
            }
        }
        this.configs = configs;
    }
    toJSON() {
        return this.configs;
    }
}
exports.Configs = Configs;
exports.DEFAULT_RUN_MODEL = {
    uuid: '',
    name: '',
    comment: '',
    tags: [],
    commit: '',
    commit_message: '',
    notes: '',
    is_dirty: false,
    python_file: '',
    start_step: 0,
    trial_date: '2000-01-01',
    trial_time: '00:00:00',
    tensorboard_size: 0,
    total_size: 0,
    artifacts_size: 0,
    checkpoints_size: 0,
    sqlite_size: 0,
    analytics_size: 0
};
class Run {
    constructor(info) {
        this.info = info;
    }
    get uuid() {
        return this.info.uuid;
    }
    get name() {
        return this.info.name;
    }
    get comment() {
        return this.info.comment;
    }
    get tags() {
        return this.info.tags;
    }
    get commit() {
        return this.info.commit;
    }
    get commit_message() {
        return this.info.commit_message;
    }
    get notes() {
        return this.info.notes;
    }
    get is_dirty() {
        return this.info.is_dirty;
    }
    get python_file() {
        return this.info.python_file;
    }
    get start_step() {
        return this.info.start_step;
    }
    get trial_date() {
        return this.info.trial_date;
    }
    get trial_time() {
        return this.info.trial_time;
    }
    get load_run() {
        return this.info.load_run;
    }
    get total_size() {
        return this.info.total_size;
    }
    get artifacts_size() {
        return this.info.artifacts_size;
    }
    get tensorboard_size() {
        return this.info.tensorboard_size;
    }
    get checkpoints_size() {
        return this.info.checkpoints_size;
    }
    get sqlite_size() {
        return this.info.sqlite_size;
    }
    get analytics_size() {
        return this.info.analytics_size;
    }
    get configs() {
        return this.info.configs;
    }
    get values() {
        return this.info.values;
    }
    get indicators() {
        return this.info.indicators;
    }
    get(key) {
        return this.info[key];
    }
    update(data) {
        for (let [k, v] of Object.entries(data)) {
            this.info[k] = v;
        }
    }
    toJSON() {
        return this.info;
    }
    hash() {
        return `${this.info.uuid}`;
    }
    static fixRunModel(name, run) {
        let copy = JSON.parse(JSON.stringify(exports.DEFAULT_RUN_MODEL));
        if (run == null) {
            return copy;
        }
        run.name = name;
        if (run.tags == null) {
            run.tags = run.name.split('_');
        }
        for (let k of Object.keys(exports.DEFAULT_RUN_MODEL)) {
            if (run[k] == null) {
                run[k] = copy[k];
            }
        }
        return run;
    }
}
exports.Run = Run;
class RunCollection {
    constructor(runs) {
        this.runs = runs.map(t => new Run(t));
        this.runs.sort((a, b) => {
            if (a.trial_date < b.trial_date) {
                return -1;
            }
            else if (a.trial_date > b.trial_date) {
                return +1;
            }
            else {
                if (a.trial_time < b.trial_time) {
                    return -1;
                }
                else if (a.trial_time > b.trial_time) {
                    return +1;
                }
                else {
                    return 0;
                }
            }
        });
    }
    get lastRun() {
        if (this.runs.length > 0) {
            return this.runs[this.runs.length - 1];
        }
        return null;
    }
    getRun(uuid) {
        for (let run of this.runs) {
            if (run.uuid === uuid) {
                return run;
            }
        }
        throw Error(`Unknown run ${uuid}`);
    }
    toJSON() {
        return this.runs.map(t => t.toJSON());
    }
}
exports.RunCollection = RunCollection;
