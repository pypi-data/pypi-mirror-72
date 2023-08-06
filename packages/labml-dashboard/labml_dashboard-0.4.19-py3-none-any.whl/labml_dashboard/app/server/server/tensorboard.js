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
const util_1 = require("./util");
class Tensorboard {
    constructor(runs, port = 6006) {
        this.runs = runs;
        this.port = port;
        this.proc = null;
    }
    start() {
        return __awaiter(this, void 0, void 0, function* () {
            let path = consts_1.LAB.tensorboardLogDir;
            yield util_1.rmtree(path);
            yield util_1.mkdir(path, { recursive: true });
            for (let r of this.runs) {
                try {
                    yield util_1.symlink(PATH.join(consts_1.LAB.experiments, r.name, r.uuid, 'tensorboard'), PATH.join(path, `${r.uuid}`));
                }
                catch (e) {
                    console.log(e);
                }
            }
            let args = [
                `--logdir=${path}`,
                '--port',
                `${this.port}`
            ];
            console.log('tensorboard', args);
            this.proc = child_process_1.spawn('tensorboard', args);
            return new Promise((resolve, reject) => {
                this.proc.on('close', (code, signal) => {
                    console.log('Close', code, signal);
                    reject();
                });
                this.proc.stdout.on('data', (data) => {
                    console.log('TB out', data.toString());
                });
                this.proc.stderr.on('data', (data) => {
                    console.log('TB err', data.toString());
                    if (data.toString().indexOf('Press CTRL+C to quit') !== -1) {
                        resolve();
                    }
                });
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
}
exports.Tensorboard = Tensorboard;
