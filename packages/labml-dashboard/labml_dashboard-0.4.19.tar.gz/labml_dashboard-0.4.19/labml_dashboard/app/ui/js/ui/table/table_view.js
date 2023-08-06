var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
define(["require", "exports", "../app", "../../lib/weya/weya", "../cache", "../run_ui", "./format", "./controls", "./run_row", "./tree", "./renderer", "./header_controls"], function (require, exports, app_1, weya_1, cache_1, run_ui_1, format_1, controls_1, run_row_1, tree_1, renderer_1, header_controls_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    class RunsView {
        constructor(dashboard, search) {
            this.isAllSelected = false;
            this.onSelectAll = (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.isAllSelected = !this.isAllSelected;
                this.selectAllIcon.classList.remove('fa-square');
                this.selectAllIcon.classList.remove('fa-check-square');
                if (this.isAllSelected) {
                    for (let r of this.runRows) {
                        r.setSelection(true);
                    }
                    this.selectAllIcon.classList.add('fa-check-square');
                }
                else {
                    for (let r of this.runRows) {
                        r.setSelection(false);
                    }
                    this.selectAllIcon.classList.add('fa-square');
                }
            };
            this.format = new format_1.Format(dashboard);
            this.filterTerms = [];
            for (let t of search.split(' ')) {
                t = t.trim();
                if (t !== '') {
                    this.filterTerms.push(t);
                }
            }
        }
        static getRuns(runs) {
            let runUIs = [];
            for (let r of runs.runs) {
                runUIs.push(run_ui_1.RunUI.create(r));
            }
            return runUIs;
        }
        render() {
            this.elem = weya_1.Weya('div.full_container', $ => {
                let controls = $('div.controls');
                this.controls = new controls_1.ControlsView(this.format, this);
                controls.appendChild(this.controls.render());
                this.tableContainer = $('div.table_container', $ => {
                    this.runsTable = $('div.table');
                });
            });
            this.headerControls = new header_controls_1.HeaderControls(this.tableContainer, this.format, this);
            this.controls.setSearch(this.filterTerms.join(' '));
            this.renderExperiments().then();
            return this.elem;
        }
        setFilter(filterTerms) {
            const isReplaceUrl = this.filterTerms.length === filterTerms.length;
            this.filterTerms = filterTerms;
            app_1.ROUTER.navigate(`table/${this.format.dashboard}/${this.filterTerms.join(' ')}`, { trigger: false, replace: isReplaceUrl });
            this.renderTable().then();
        }
        onSync(dashboard) {
            app_1.ROUTER.navigate(`table/${dashboard}`, { trigger: false });
            this.cells = this.format.createCells();
            this.renderTable().then();
        }
        onReload() {
            return __awaiter(this, void 0, void 0, function* () {
                this.runs = RunsView.getRuns(yield cache_1.getRuns());
                let promises = [];
                for (let r of this.runs) {
                    promises.push(r.loadConfigs());
                    promises.push(r.loadValues());
                }
                yield Promise.all(promises);
                this.cells = this.format.createCells();
                this.renderTable().then();
            });
        }
        onChanging() {
            this.runsTable.innerHTML = '';
        }
        getFormat() {
            let format = [
                { type: 'controls', name: '', key: '' },
                { type: 'generations', name: '', key: '' },
                { type: 'experiment_name', name: 'Experiment', key: '' },
                { type: 'comment', name: 'Comment', key: '' },
                { type: 'date_time', name: 'Date Time', key: '' },
                { type: 'info', name: 'Commit Message', key: 'commit_message', visible: false },
                { type: 'info', name: 'Dirty', key: 'is_dirty', visible: false },
                { type: 'info', name: 'Tags', key: 'tags', visible: false },
                { type: 'size', name: 'Size', key: 'total_size' },
                { type: 'size', name: 'Checkpoints', key: 'checkpoints_size', visible: false },
                { type: 'size', name: 'SQLite', key: 'sqlite_size', visible: false },
                { type: 'size', name: 'Analytics', key: 'analytics_size', visible: false },
                { type: 'size', name: 'Tensorboard', key: 'tensorboard_size', visible: false },
                { type: 'size', name: 'Artifacts', key: 'artifacts_size', visible: false },
            ];
            format.push({ type: 'step', name: 'Step', key: '' });
            let indicators = new Set();
            for (let r of this.runs) {
                for (let k of Object.keys(r.values)) {
                    if (k !== 'step') {
                        indicators.add(k);
                    }
                }
            }
            let indicator_count = 0;
            for (let k of indicators.keys()) {
                format.push({ type: 'value', name: k, key: k, visible: indicator_count < 10 });
                indicator_count++;
            }
            let configs = new Set();
            for (let r of this.runs) {
                for (let [k, conf] of Object.entries(r.configs.configs)) {
                    if (conf.is_hyperparam === true ||
                        (conf.is_hyperparam == null && conf.is_explicitly_specified)) {
                        configs.add(k);
                    }
                }
            }
            let configs_count = 0;
            for (let k of configs.keys()) {
                format.push({ type: 'config_calculated', name: k, key: k, visible: configs_count < 15 });
                // format.push({type: 'config_computed', name: k, 'key': k})
                // format.push({type: 'config_options', name: `${k} Options`, 'key': k})
                configs_count++;
            }
            return format;
        }
        renderExperiments() {
            return __awaiter(this, void 0, void 0, function* () {
                let start = new Date().getTime();
                yield this.format.load();
                this.runs = RunsView.getRuns(yield cache_1.getRuns());
                let promises = [];
                for (let r of this.runs) {
                    promises.push(r.loadConfigs());
                    promises.push(r.loadValues());
                }
                yield Promise.all(promises);
                this.format.defaults(this.getFormat());
                this.controls.updateFormat();
                this.cells = this.format.createCells();
                console.log('Get Experiments', new Date().getTime() - start);
                this.renderTable().then();
            });
        }
        sortRuns(runs) {
            runs.sort((a, b) => {
                let minRank = 1e6;
                let direction = 0;
                for (let c of this.cells) {
                    let s = c.compare(a, b);
                    if (s === 0) {
                        continue;
                    }
                    let r = Math.abs(s);
                    if (s < minRank) {
                        minRank = s;
                        direction = s / r;
                    }
                }
                return direction;
            });
        }
        isFiltered(run) {
            for (let t of this.filterTerms) {
                let matched = false;
                for (let c of this.cells) {
                    if (c.isFiltered(run, t)) {
                        matched = true;
                        break;
                    }
                }
                if (!matched) {
                    return false;
                }
            }
            return true;
        }
        filterRuns(runs) {
            let filtered = [];
            for (let r of runs) {
                if (this.isFiltered(r)) {
                    filtered.push(r);
                }
            }
            return filtered;
        }
        addParentRuns(runs) {
            let tree = new tree_1.RunsTree(this.runs, runs);
            return tree.getList();
        }
        renderControlsCell() {
            weya_1.Weya('span', this.controlsCell, $ => {
                this.selectAllIcon = $('i.fa.fa-square', { on: { click: this.onSelectAll } });
            });
        }
        renderTable() {
            return __awaiter(this, void 0, void 0, function* () {
                let start = new Date().getTime();
                this.runsTable.innerHTML = '';
                this.runRows = [];
                console.log("Render table");
                let runs = this.filterRuns(this.runs);
                console.log("Filter", new Date().getTime() - start);
                start = new Date().getTime();
                this.sortRuns(runs);
                console.log("Sort", new Date().getTime() - start);
                start = new Date().getTime();
                runs = this.addParentRuns(runs);
                console.log("Add parent", new Date().getTime() - start);
                start = new Date().getTime();
                for (let c of this.cells) {
                    c.updateCellState(runs);
                }
                console.log("Update cells", new Date().getTime() - start);
                start = new Date().getTime();
                for (let i = 0; i < runs.length; ++i) {
                    let r = runs[i];
                    this.runRows.push(new run_row_1.RunRowView(r, i, this.controls));
                }
                console.log("Create Views", new Date().getTime() - start);
                start = new Date().getTime();
                this.headerCells = [];
                this.headerControls.reset();
                weya_1.Weya('div.header', this.runsTable, $ => {
                    for (let c of this.cells) {
                        let rendered = c.renderHeader($);
                        this.headerControls.addCell(c, rendered);
                        this.headerCells.push(rendered);
                        if (c.type === 'controls') {
                            this.controlsCell = rendered;
                        }
                    }
                });
                this.renderControlsCell();
                console.log("Render Header", new Date().getTime() - start);
                if (this.renderer != null) {
                    this.renderer.cancel();
                }
                this.renderer = new renderer_1.RunsRenderer(this.runsTable, this.runRows, this.headerCells, this.cells);
                yield this.renderer.render();
            });
        }
        onFormatUpdated() {
            return __awaiter(this, void 0, void 0, function* () {
                this.cells = this.format.createCells();
                yield this.renderTable();
            });
        }
    }
    class TableHandler {
        constructor() {
            this.handleTableDefault = () => {
                app_1.ROUTER.navigate('table/default', { trigger: true, replace: true });
            };
            this.handleTable = (dashboard, search = '') => {
                app_1.SCREEN.setView(new RunsView(dashboard, search));
            };
            this.handleRoot = () => {
                app_1.ROUTER.navigate('table', { replace: true, trigger: true });
            };
            app_1.ROUTER.route('', [this.handleRoot]);
            app_1.ROUTER.route('table', [this.handleTableDefault]);
            app_1.ROUTER.route('table/:dashboard', [this.handleTable]);
            app_1.ROUTER.route('table/:dashboard/', [this.handleTable]);
            app_1.ROUTER.route('table/:dashboard/:search', [this.handleTable]);
        }
    }
    exports.TableHandler = TableHandler;
});
