var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
define(["require", "exports", "../jsyaml", "./cell", "../app"], function (require, exports, jsyaml_1, cell_1, app_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    class Format {
        constructor(dashboard) {
            this.dashboard = dashboard;
            this.cells = [];
        }
        defaults(cells) {
            let has = new Set();
            for (let c of this.cells) {
                has.add(Format.hashCell(c));
            }
            for (let c of cells) {
                if (!has.has(Format.hashCell(c))) {
                    this.cells.push(c);
                }
            }
        }
        update(yaml) {
            let data = jsyaml_1.jsyaml.load(yaml);
            this.dashboard = data.dashboard;
            this.cells = data.cells;
        }
        createCells() {
            let res = [];
            for (let opt of this.cells) {
                res.push(cell_1.CellFactory.create(opt));
            }
            return res;
        }
        toYAML() {
            return jsyaml_1.jsyaml.dump({ dashboard: this.dashboard, cells: this.cells });
        }
        save() {
            return __awaiter(this, void 0, void 0, function* () {
                yield app_1.API.saveDashboard(this.dashboard, this.cells);
            });
        }
        load() {
            return __awaiter(this, void 0, void 0, function* () {
                let dashboards = yield app_1.API.loadDashboards();
                console.log(dashboards, this.dashboard);
                if (dashboards[this.dashboard] != null) {
                    this.cells = dashboards[this.dashboard];
                }
            });
        }
        static hashCell(cell) {
            return `${cell.type}-${cell.key}`;
        }
        sortAscending(index) {
            for (let c of this.cells) {
                c.sortRank = null;
            }
            this.cells[index].sortRank = 1;
        }
        sortDescending(index) {
            for (let c of this.cells) {
                c.sortRank = null;
            }
            this.cells[index].sortRank = -1;
        }
        moveLeft(index) {
            if (index <= 0) {
                return;
            }
            let temp = this.cells[index];
            this.cells[index] = this.cells[index - 1];
            this.cells[index - 1] = temp;
        }
        moveRight(index) {
            if (index >= this.cells.length - 1) {
                return;
            }
            let temp = this.cells[index];
            this.cells[index] = this.cells[index + 1];
            this.cells[index + 1] = temp;
        }
    }
    exports.Format = Format;
});
