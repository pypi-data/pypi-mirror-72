"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const server_1 = require("./server");
const consts_1 = require("./consts");
const api_handler_1 = require("../common/api_handler");
const api_server_1 = require("./api_server");
const browser_1 = require("./browser");
api_handler_1.listenAPI(server_1.SERVER, api_server_1.API);
consts_1.LAB.load().then(() => {
    let url = `http://localhost:${server_1.SERVER.port}`;
    console.log(`Server running at: ${url}`);
    console.log(`Analysing project: ${consts_1.LAB.path}`);
    server_1.SERVER.listen();
    browser_1.openBrowser(url);
});
