var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
define(["require", "exports"], function (require, exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    function getParameters(func) {
        let code = func.toString().replace(/\n/g, '');
        let argumentList = new RegExp('(?:' + func.name + '\\s*|^)\\s*\\((.*?)\\)').exec(code)[1];
        // remove comments
        argumentList = argumentList.replace(/\/\*.*?\*\//g, '');
        // remove spaces
        argumentList = argumentList.replace(/ /g, '');
        if (argumentList === '') {
            return [];
        }
        return argumentList.split(',');
    }
    function createCaller(port, name, args) {
        function caller() {
            let params = {};
            if (arguments.length !== args.length) {
                throw Error('Invalid call' + name + args + arguments);
            }
            for (let i = 0; i < args.length; ++i) {
                params[args[i]] = arguments[i];
            }
            return new Promise((resolve, reject) => {
                port.send(name, params, (data, options) => {
                    resolve(data);
                });
            });
        }
        return caller;
    }
    function wrapAPI(port, api) {
        let proto = api['__proto__'];
        let wrappers = {};
        for (let k of Object.getOwnPropertyNames(proto)) {
            if (k === 'constructor') {
                continue;
            }
            let func = proto[k];
            let args = getParameters(func);
            wrappers[k] = createCaller(port, k, args);
        }
        for (let k in wrappers) {
            proto[k] = wrappers[k];
        }
    }
    exports.wrapAPI = wrapAPI;
    function createListener(port, name, api, func, args) {
        function listener(data, packet, response) {
            return __awaiter(this, void 0, void 0, function* () {
                let params = [];
                for (let i = 0; i < args.length; ++i) {
                    params.push(data[args[i]]);
                }
                let result = yield func.apply(api, params);
                response.success(result);
            });
        }
        port.on(name, listener);
    }
    function listenAPI(port, api) {
        let proto = api['__proto__'];
        for (let k of Object.getOwnPropertyNames(proto)) {
            if (k === 'constructor') {
                continue;
            }
            let func = proto[k];
            let args = getParameters(func);
            createListener(port, k, api, func, args);
        }
    }
    exports.listenAPI = listenAPI;
});
