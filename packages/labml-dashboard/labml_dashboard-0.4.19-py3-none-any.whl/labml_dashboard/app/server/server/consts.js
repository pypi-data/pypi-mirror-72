"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const PROCESS = require("process");
const lab_1 = require("./lab");
const CWD = PROCESS.cwd();
exports.LAB = new lab_1.Lab(CWD);
