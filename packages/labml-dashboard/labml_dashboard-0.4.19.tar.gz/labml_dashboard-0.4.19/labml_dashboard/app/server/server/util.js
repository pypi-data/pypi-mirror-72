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
const UTIL = require("util");
const FS = require("fs");
const PATH = require("path");
exports.readdir = UTIL.promisify(FS.readdir);
function readFile(path) {
    return new Promise((resolve, reject) => {
        FS.readFile(path, { flag: 'r', encoding: 'utf-8' }, (err, contents) => {
            if (err != null) {
                reject(err);
            }
            else {
                resolve(contents);
            }
        });
    });
}
exports.readFile = readFile;
function writeFile(path, content) {
    return new Promise((resolve, reject) => {
        FS.writeFile(path, content, { flag: 'w', encoding: 'utf-8' }, () => {
            resolve();
        });
    });
}
exports.writeFile = writeFile;
exports.lstat = UTIL.promisify(FS.lstat);
let unlink = UTIL.promisify(FS.unlink);
let rmdir = UTIL.promisify(FS.rmdir);
function mkdir(path, options = null) {
    return new Promise((resolve, reject) => {
        FS.mkdir(path, options, (err) => {
            if (err != null) {
                reject(err);
            }
            else {
                resolve();
            }
        });
    });
}
exports.mkdir = mkdir;
exports.copyFile = UTIL.promisify(FS.copyFile);
exports.symlink = UTIL.promisify(FS.symlink);
function rename(oldPath, newPath) {
    return __awaiter(this, void 0, void 0, function* () {
        return new Promise(((resolve, reject) => {
            FS.rename(oldPath, newPath, (err) => {
                if (err != null) {
                    reject(err);
                }
                else {
                    resolve();
                }
            });
        }));
    });
}
exports.rename = rename;
function exists(path) {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            yield exports.lstat(path);
        }
        catch (e) {
            return false;
        }
        return true;
    });
}
exports.exists = exists;
function safeRemove(path) {
    return __awaiter(this, void 0, void 0, function* () {
        if (!(yield exists(path))) {
            return;
        }
        yield unlink(path);
    });
}
exports.safeRemove = safeRemove;
function rmtree(path) {
    return __awaiter(this, void 0, void 0, function* () {
        let stats;
        try {
            stats = yield exports.lstat(path);
        }
        catch (e) {
            return;
        }
        if (stats.isDirectory()) {
            let files = yield exports.readdir(path);
            for (let f of files) {
                yield rmtree(PATH.join(path, f));
            }
            yield rmdir(path);
        }
        else {
            yield unlink(path);
        }
    });
}
exports.rmtree = rmtree;
function getDiskUsage(path) {
    return __awaiter(this, void 0, void 0, function* () {
        let stats;
        try {
            stats = yield exports.lstat(path);
        }
        catch (e) {
            return 0;
        }
        if (stats.isDirectory()) {
            let files = yield exports.readdir(path);
            let size = 0;
            for (let f of files) {
                size += yield getDiskUsage(PATH.join(path, f));
            }
            return size;
        }
        else {
            return stats.size;
        }
    });
}
exports.getDiskUsage = getDiskUsage;
function sqliteRun(db, sql) {
    return __awaiter(this, void 0, void 0, function* () {
        return new Promise(((resolve, reject) => {
            db.run(sql, (res, err) => {
                if (err) {
                    reject(err);
                }
                else {
                    resolve(res);
                }
            });
        }));
    });
}
exports.sqliteRun = sqliteRun;
function sqliteClose(db) {
    return __awaiter(this, void 0, void 0, function* () {
        return new Promise(((resolve, reject) => {
            db.close(err => {
                if (err) {
                    reject(err);
                }
                else {
                    resolve();
                }
            });
        }));
    });
}
exports.sqliteClose = sqliteClose;
