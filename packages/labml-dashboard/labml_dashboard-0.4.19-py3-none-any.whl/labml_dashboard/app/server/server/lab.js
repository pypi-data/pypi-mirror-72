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
const PATH = require("path");
const YAML = require("yaml");
const util_1 = require("./util");
const CONFIG_FILE_NAME = '.labml.yaml';
class Lab {
    constructor(path) {
        this.currentPath = path;
    }
    load() {
        return __awaiter(this, void 0, void 0, function* () {
            let configsList = yield getConfigFiles(this.currentPath);
            if (configsList.length == 0) {
                throw Error(`No .labml.yaml files found: ${this.currentPath}`);
            }
            let configs = mergeConfig(configsList);
            this.path = configs.path;
            this.experiments = PATH.join(this.path, configs.experiments_path);
            this.analytics = PATH.join(this.path, configs.analytics_path);
            this.analyticsPath = configs.analytics_path;
            this.analyticsTemplates = configs.analytics_templates;
            this.tensorboardLogDir = PATH.join(this.experiments, '_tensorboard');
        });
    }
}
exports.Lab = Lab;
function mergeConfig(configs) {
    let config = {
        path: null,
        check_repo_dirty: true,
        is_log_python_file: true,
        config_file_path: null,
        data_path: 'data',
        experiments_path: 'logs',
        analytics_path: 'analytics',
        analytics_templates: {}
    };
    for (let i = configs.length - 1; i >= 0; --i) {
        let c = configs[i];
        if (config['path'] == null) {
            config.path = c.config_file_path;
        }
        if ('path' in c) {
            throw Error('Path in configs: ' + c.config_file_path);
        }
        if (i > 0 && 'experiments_path' in c) {
            throw Error('Experiment path in configs: ' + c.config_file_path);
        }
        if (i > 0 && 'analytics_path' in c) {
            throw Error('Analyitics path in configs: ' + c.config_file_path);
        }
        for (let [k, v] of Object.entries(c)) {
            if (!(k in config)) {
                throw Error('Unknown configs: ' + c.config_file_path);
            }
            if (k === 'analytics_templates') {
                for (let [name, template] of Object.entries(v)) {
                    config.analytics_templates[name] = PATH.resolve(c.config_file_path, template);
                }
            }
            else {
                config[k] = v;
            }
        }
    }
    return config;
}
function getConfigFiles(path) {
    return __awaiter(this, void 0, void 0, function* () {
        path = PATH.resolve(path);
        let configsList = [];
        while (yield util_1.exists(path)) {
            let stats = yield util_1.lstat(path);
            if (stats.isDirectory()) {
                let config_file = PATH.join(path, CONFIG_FILE_NAME);
                if (yield util_1.exists(config_file)) {
                    let contents = yield util_1.readFile(config_file);
                    let configs = YAML.parse(contents);
                    if (configs == null) {
                        configs = {};
                    }
                    configs.config_file_path = path;
                    configsList.push(configs);
                }
            }
            if (path === PATH.resolve(path, '..')) {
                break;
            }
            path = PATH.resolve(path, '..');
        }
        return configsList;
    });
}
