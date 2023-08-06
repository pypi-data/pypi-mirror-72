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
const consts_1 = require("./consts");
const PATH = require("path");
const child_process_1 = require("child_process");
const PROCESS = require("process");
const run_nodejs_1 = require("./run_nodejs");
const util_1 = require("./util");
class Jupyter {
    constructor(port = 6006) {
        this.port = port;
        this.proc = null;
    }
    start() {
        return __awaiter(this, void 0, void 0, function* () {
            let env = JSON.parse(JSON.stringify(PROCESS.env));
            if (!('PYTHONPATH' in env)) {
                env['PYTHONPATH'] = env['PWD'];
            }
            else {
                env['PYTHONPATH'] += ':' + env['PWD'];
            }
            let args = ['notebook', '--no-browser'];
            console.log('jupyter', args);
            this.proc = child_process_1.spawn('jupyter', args, { env: env });
            let isClosed = false;
            this.proc.on('close', (code, signal) => {
                isClosed = true;
                console.log('Close', code, signal);
            });
            this.proc.stdout.on('data', (data) => {
                console.log('TB out', data.toString());
            });
            this.proc.stderr.on('data', (data) => {
                console.log('TB err', data.toString());
            });
            return new Promise((resolve, reject) => {
                setTimeout(() => {
                    console.log('isClosed', isClosed);
                    if (isClosed) {
                        reject();
                    }
                    else {
                        resolve();
                    }
                }, 2500);
            });
        });
    }
    stop() {
        if (this.proc == null) {
            return;
        }
        else {
            this.proc.kill('SIGINT');
        }
    }
    setupTemplate(run, templateName) {
        return __awaiter(this, void 0, void 0, function* () {
            let runNodeJs = run_nodejs_1.RunNodeJS.create(run);
            let lab = yield runNodeJs.getLab();
            let template = lab.analyticsTemplates[templateName];
            let destinationPath = PATH.join(consts_1.LAB.analytics, run.name, run.uuid);
            let destination = PATH.join(destinationPath, `${templateName}.ipynb`);
            let url = `http://localhost:8888/notebooks/${lab.analyticsPath}/${run.uuid}/${templateName}.ipynb`;
            console.log(url);
            if (yield util_1.exists(destination)) {
                return url;
            }
            yield util_1.mkdir(destinationPath, { recursive: true });
            console.log(template, destination);
            yield util_1.copyFile(template, destination);
            return url;
        });
    }
}
exports.Jupyter = Jupyter;
