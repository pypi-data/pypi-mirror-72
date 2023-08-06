var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
define(["require", "exports", "../../lib/weya/weya", "../codemirror", "../cache", "../app"], function (require, exports, weya_1, codemirror_1, cache_1, app_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    class ControlsView {
        constructor(format, syncListeners) {
            this.onSearchKeyUp = (e) => __awaiter(this, void 0, void 0, function* () {
                // if (e.key === 'Enter') {
                //     this.saveComment(this.commentInput.value)
                // }
                let search = this.searchInput.value;
                let terms = [];
                for (let t of search.split(' ')) {
                    t = t.trim();
                    if (t !== '') {
                        terms.push(t);
                    }
                }
                this.resetSelection();
                this.syncListeners.setFilter(terms);
            });
            this.onTensorboard = () => __awaiter(this, void 0, void 0, function* () {
                let runs = [];
                for (let r in this.selectedRuns) {
                    let run = this.selectedRuns[r].run;
                    runs.push(run.uuid);
                }
                let url = yield app_1.API.launchTensorboards(runs);
                if (url === '') {
                    alert("Couldn't start Tensorboard");
                }
                else {
                    window.open(url, '_blank');
                }
            });
            this.onRemove = (e) => __awaiter(this, void 0, void 0, function* () {
                let count = this.getSelectedRunsCount();
                if (confirm(`Do you want to remove ${count} runs?`)) {
                    this.syncListeners.onChanging();
                    for (let run of Object.values(this.selectedRuns)) {
                        yield run.remove();
                    }
                    this.resetSelection();
                    cache_1.clearCache();
                    this.syncListeners.onReload();
                }
            });
            this.onCleanupCheckpoints = (e) => __awaiter(this, void 0, void 0, function* () {
                this.syncListeners.onChanging();
                for (let r in this.selectedRuns) {
                    let run = this.selectedRuns[r];
                    yield run.cleanupCheckpoints();
                }
                this.resetSelection();
                cache_1.clearCache();
                this.syncListeners.onReload();
            });
            this.onCleanupArtifacts = (e) => __awaiter(this, void 0, void 0, function* () {
                this.syncListeners.onChanging();
                for (let r in this.selectedRuns) {
                    let run = this.selectedRuns[r];
                    yield run.cleanupArtifacts();
                }
                this.resetSelection();
                cache_1.clearCache();
                this.syncListeners.onReload();
            });
            this.onSync = (e) => {
                e.preventDefault();
                e.stopPropagation();
                console.log("Sync");
                this.format.update(this.codemirror.getValue());
                this.syncListeners.onSync(this.format.dashboard);
            };
            this.onEdit = (e) => {
                e.preventDefault();
                e.stopPropagation();
                if (this.codemirrorDiv.style.display === 'none') {
                    this.syncControls.style.display = null;
                    this.codemirrorDiv.style.display = null;
                    this.editorControls.style.float = null;
                    this.codemirror.setValue(this.format.toYAML());
                    this.codemirror.focus();
                }
                else {
                    this.syncControls.style.display = 'none';
                    this.codemirrorDiv.style.display = 'none';
                    this.editorControls.style.float = 'right';
                }
            };
            this.onSave = (e) => {
                e.preventDefault();
                e.stopPropagation();
                console.log("Sync");
                this.format.update(this.codemirror.getValue());
                this.syncListeners.onSync(this.format.dashboard);
                this.format.save().then();
            };
            this.format = format;
            this.syncListeners = syncListeners;
            this.selectedRuns = {};
        }
        onSelect(run) {
            this.selectedRuns[run.run.hash()] = run;
            this.updateSelectedRunsCount();
        }
        onUnSelect(run) {
            delete this.selectedRuns[run.run.hash()];
            this.updateSelectedRunsCount();
        }
        render() {
            this.elem = weya_1.Weya('div.control_panel', $ => {
                this.editorControls = $('div.editor_controls', $ => {
                    $('i.fa.fa-edit', { on: { click: this.onEdit } });
                    this.syncControls = $('span', $ => {
                        $('i.fa.fa-sync', { on: { click: this.onSync } });
                        $('i.fa.fa-save', { on: { click: this.onSave } });
                    });
                });
                this.codemirrorDiv = $('div.editor');
                $('div.search', $ => {
                    $('div.input-container', $ => {
                        $('i.input-icon.fa.fa-search');
                        this.searchInput = $('input', {
                            type: 'text',
                            on: {
                                keyup: this.onSearchKeyUp
                            }
                        });
                    });
                });
                this.actionsContainer = $('div.actions-container', $ => {
                    this.actionsElem = $('div.actions', $ => {
                        this.tensorboardBtn = ($('button', { on: { click: this.onTensorboard } }, $ => {
                            $('i.fa.fa-chart-bar');
                            $('span', ' Launch Tensorboard');
                        }));
                        this.removeBtn = $('button.danger', { on: { click: this.onRemove } }, $ => {
                            $('i.fa.fa-trash');
                            $('span', ' Remove');
                        });
                        this.cleanupCheckpointsBtn = $('button.danger', { on: { click: this.onCleanupCheckpoints } }, $ => {
                            $('i.fa.fa-trash');
                            $('span', ' Cleanup Checkpoints');
                        });
                        this.cleanupArtifactsBtn = $('button.danger', { on: { click: this.onCleanupArtifacts } }, $ => {
                            $('i.fa.fa-trash');
                            $('span', ' Cleanup Artifacts');
                        });
                    });
                    this.selectedCountElem = $('div.selected_count', 'No runs selected');
                });
            });
            this.codemirror = codemirror_1.CodeMirror(this.codemirrorDiv, {
                mode: "yaml",
                theme: "darcula"
            });
            this.codemirrorDiv.style.display = 'none';
            this.syncControls.style.display = 'none';
            this.editorControls.style.float = 'right';
            this.updateSelectedRunsCount();
            return this.elem;
        }
        setSearch(search) {
            this.searchInput.value = search;
        }
        updateFormat() {
            this.codemirror.setValue(this.format.toYAML());
        }
        getSelectedRunsCount() {
            let count = 0;
            for (let r of Object.keys(this.selectedRuns)) {
                count++;
            }
            return count;
        }
        updateSelectedRunsCount() {
            let count = this.getSelectedRunsCount();
            if (count === 0) {
                this.tensorboardBtn.disabled = true;
                this.cleanupCheckpointsBtn.disabled = true;
                this.cleanupArtifactsBtn.disabled = true;
                this.removeBtn.disabled = true;
                this.selectedCountElem.classList.remove('items-selected');
            }
            else {
                this.tensorboardBtn.disabled = false;
                this.cleanupCheckpointsBtn.disabled = false;
                this.cleanupArtifactsBtn.disabled = false;
                this.removeBtn.disabled = false;
                this.selectedCountElem.classList.add('items-selected');
            }
            if (count === 0) {
                this.selectedCountElem.textContent = `No runs selected`;
            }
            else if (count == 1) {
                this.selectedCountElem.textContent = `One run selected`;
            }
            else {
                this.selectedCountElem.textContent = `${count} runs selected`;
            }
        }
        resetSelection() {
            this.selectedRuns = {};
            this.updateSelectedRunsCount();
        }
    }
    exports.ControlsView = ControlsView;
});
