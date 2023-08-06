"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const PROCESS = require("process");
const child_process_1 = require("child_process");
function openBrowser(url) {
    url = encodeURI(url);
    let command;
    if (PROCESS.platform === 'darwin') {
        command = 'open';
    }
    else if (PROCESS.platform === 'linux') {
        command = 'xdg-open';
    }
    const subprocess = child_process_1.spawn(command, [url]);
    subprocess.unref();
    return subprocess;
}
exports.openBrowser = openBrowser;
