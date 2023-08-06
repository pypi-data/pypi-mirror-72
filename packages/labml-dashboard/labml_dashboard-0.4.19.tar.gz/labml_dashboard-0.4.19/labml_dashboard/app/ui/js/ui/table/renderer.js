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
    const ADJUST_CELL_WIDTH_MARGIN = 2;
    class RunsRenderer {
        constructor(runsTable, runRows, headerCells, cells) {
            this.headerCells = headerCells;
            this.runRows = runRows;
            this.runsTable = runsTable;
            this.cells = cells;
            this.cancelled = false;
        }
        static getCellWidth(elem) {
            let children = elem.children;
            let width = 0;
            for (let x of children) {
                width += x.offsetWidth;
            }
            return width;
        }
        cancel() {
            this.cancelled = true;
        }
        render() {
            return __awaiter(this, void 0, void 0, function* () {
                let start = new Date().getTime();
                for (let j = 0; j < this.runRows.length;) {
                    j = yield this.renderRows(j, 5);
                    if (this.cancelled) {
                        return;
                    }
                }
                console.log("Render Rows", new Date().getTime() - start);
                start = new Date().getTime();
                for (let i = 0; i < this.cells.length; ++i) {
                    yield this.adjustCellWidth(i);
                    if (this.cancelled) {
                        return;
                    }
                }
                console.log("Adjust widths", new Date().getTime() - start);
            });
        }
        renderRows(offset, count) {
            return __awaiter(this, void 0, void 0, function* () {
                let to = Math.min(offset + count, this.runRows.length);
                for (let i = offset; i < to; ++i) {
                    let v = this.runRows[i];
                    this.runsTable.append(v.render(this.cells));
                }
                return new Promise((resolve => {
                    window.requestAnimationFrame(() => {
                        resolve(to);
                    });
                }));
            });
        }
        adjustCellWidth(i) {
            return __awaiter(this, void 0, void 0, function* () {
                let header = this.headerCells[i];
                if (header == null) {
                    return;
                }
                let defaultWidth = header.offsetWidth;
                let maxWidth = RunsRenderer.getCellWidth(header);
                if (defaultWidth <= maxWidth) {
                }
                if (this.cells[i].specifiedWidth != null) {
                    return;
                }
                for (let r of this.runRows) {
                    let c = r.cells[i];
                    if (c == null) {
                        continue;
                    }
                    maxWidth = Math.max(RunsRenderer.getCellWidth(c), maxWidth);
                    if (defaultWidth <= maxWidth) {
                        return;
                    }
                }
                maxWidth += ADJUST_CELL_WIDTH_MARGIN;
                header.style.width = `${maxWidth}px`;
                for (let r of this.runRows) {
                    let c = r.cells[i];
                    if (c == null) {
                        continue;
                    }
                    c.style.width = `${maxWidth}px`;
                }
                return new Promise((resolve) => {
                    window.requestAnimationFrame(() => {
                        resolve();
                    });
                });
            });
        }
    }
    exports.RunsRenderer = RunsRenderer;
});
