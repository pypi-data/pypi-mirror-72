var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
define(["require", "exports", "./app", "../lib/weya/weya", "./cache", "./run_ui", "./configs", "./indicators", "./view_components/info_list", "./view_components/format", "./view_components/editable_field"], function (require, exports, app_1, weya_1, cache_1, run_ui_1, configs_1, indicators_1, info_list_1, format_1, editable_field_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    function wrapEvent(eventName, func) {
        function wrapper() {
            let e = arguments[arguments.length - 1];
            if (eventName[eventName.length - 1] !== '_') {
                e.preventDefault();
                e.stopPropagation();
            }
            func.apply(null, arguments);
        }
        return wrapper;
    }
    class RunView {
        constructor(uuid) {
            this.events = {
                tag: (tag) => {
                    app_1.ROUTER.navigate(`/table/default/${tag}`);
                },
                tensorboard: () => __awaiter(this, void 0, void 0, function* () {
                    let url = yield this.runUI.launchTensorboard();
                    if (url === '') {
                        alert("Couldn't start Tensorboard");
                    }
                    else {
                        window.open(url, '_blank');
                    }
                }),
                dirty: () => {
                    app_1.ROUTER.navigate(`/run/${this.run.uuid}/diff`);
                },
                code: () => {
                    app_1.ROUTER.navigate(`/run/${this.run.uuid}/code`);
                },
                loadRun: () => {
                    app_1.ROUTER.navigate(`/run/${this.run.load_run}`);
                },
                remove: (e) => __awaiter(this, void 0, void 0, function* () {
                    if (confirm('Are you sure')) {
                        yield this.runUI.remove();
                        cache_1.clearCache();
                        app_1.ROUTER.back();
                    }
                }),
                cleanupCheckpoints: (e) => __awaiter(this, void 0, void 0, function* () {
                    yield this.runUI.cleanupCheckpoints();
                    cache_1.clearCache();
                    app_1.ROUTER.back();
                }),
                cleanupArtifacts: (e) => __awaiter(this, void 0, void 0, function* () {
                    yield this.runUI.cleanupArtifacts();
                    cache_1.clearCache();
                    app_1.ROUTER.back();
                }),
                jupyter: (e) => __awaiter(this, void 0, void 0, function* () {
                    let target = e.currentTarget;
                    let url = yield this.runUI.launchJupyter(target.template);
                    if (url === '') {
                        alert("Couldn't start Jupyter");
                    }
                    else {
                        window.open(url, '_blank');
                    }
                }),
                editTags: (e) => __awaiter(this, void 0, void 0, function* () {
                    this.tagsList.style.display = 'none';
                    this.tagEditBtn.style.display = 'none';
                    this.tagsInputContainer.style.display = null;
                    this.tagsInput.value = this.run.tags.join(', ');
                    this.tagsInput.focus();
                }),
                saveTags: (e) => __awaiter(this, void 0, void 0, function* () {
                    this.saveTags(this.tagsInput.value).then();
                }),
                onTagsKeyDown_: (e) => __awaiter(this, void 0, void 0, function* () {
                    if (e.key === 'Enter') {
                        this.saveTags(this.tagsInput.value).then();
                    }
                })
            };
            this.saveComment = (comment) => __awaiter(this, void 0, void 0, function* () {
                if (this.run.comment === comment) {
                    return;
                }
                yield this.runUI.update({ comment: comment });
            });
            this.saveName = (name) => __awaiter(this, void 0, void 0, function* () {
                if (this.run.name === name) {
                    return;
                }
                if (name.trim() === '') {
                    this.nameField.change(this.run.name);
                    return;
                }
                yield this.runUI.update({ name: name });
            });
            this.uuid = uuid;
            let events = [];
            for (let k in this.events) {
                events.push(k);
            }
            for (let k of events) {
                let func = this.events[k];
                this.events[k] = wrapEvent(k, func);
            }
        }
        render() {
            this.elem = weya_1.Weya('div.container', $ => {
                this.runView = $('div.run_single', '');
            });
            this.renderRun().then();
            return this.elem;
        }
        renderRun() {
            return __awaiter(this, void 0, void 0, function* () {
                this.run = (yield cache_1.getRuns()).getRun(this.uuid);
                this.runUI = run_ui_1.RunUI.create(this.run);
                let comment = this.run.comment.trim() === '' ? '[comment]' : this.run.comment;
                weya_1.Weya(this.runView, $ => {
                    $('h1', $ => {
                        $('span', $ => {
                            this.nameField = new editable_field_1.EditableField(this.run.name, this.saveName, '[name]');
                            this.nameField.render($);
                        });
                        $('span', ":" + ' ');
                        $('span', $ => {
                            this.commentField = new editable_field_1.EditableField(this.run.comment, this.saveComment, '[comment]');
                            this.commentField.render($);
                        });
                    });
                    $('div.controls', $ => {
                        this.tensorboardBtn = ($('button', { on: { click: this.events.tensorboard } }, $ => {
                            $('i.fa.fa-chart-bar');
                            $('span', ' Launch Tensorboard');
                        }));
                        this.analyticsBtns = $('span.analytics_buttons');
                        $('button.danger', { on: { click: this.events.remove } }, $ => {
                            $('i.fa.fa-trash');
                            $('span', ' Remove');
                        });
                        $('button.danger', { on: { click: this.events.cleanupCheckpoints } }, $ => {
                            $('i.fa.fa-trash');
                            $('span', ' Cleanup Checkpoints');
                        });
                        $('button.danger', { on: { click: this.events.cleanupArtifacts } }, $ => {
                            $('i.fa.fa-trash');
                            $('span', ' Cleanup Artifacts');
                        });
                    });
                    $('div.block', $ => {
                        new info_list_1.InfoList([
                            ['.key', 'UUID'],
                            ['.value', this.run.uuid]
                        ], '').render($);
                        new info_list_1.InfoList([
                            ['.key', 'Date & Time'],
                            ['.value', `${this.run.trial_date} ${this.run.trial_time}`]
                        ], '').render($);
                    });
                    if (this.run.load_run != null) {
                        $('div.block', $ => {
                            let load_info = [
                                ['.key', 'Loaded run']
                            ];
                            load_info.push([
                                '.link',
                                $ => {
                                    $('span', ' ');
                                    $('button.inline', `${this.run.load_run}`, {
                                        on: { click: this.events.loadRun }
                                    });
                                }
                            ]);
                            new info_list_1.InfoList(load_info, '.mono').render($);
                            new info_list_1.InfoList([
                                ['.key', 'Starting step'],
                                ['.value', `${this.run.start_step}`]
                            ], '').render($);
                        });
                    }
                    $('div.block', $ => {
                        let commit_info = [
                            ['.key', 'Commit'],
                            ['.value', this.run.commit]
                        ];
                        if (this.run.is_dirty) {
                            commit_info.push([
                                '.link',
                                $ => {
                                    $('span', ' ');
                                    $('button.inline', '[dirty]', {
                                        on: { click: this.events.dirty }
                                    });
                                }
                            ]);
                        }
                        new info_list_1.InfoList(commit_info, '.mono').render($);
                        new info_list_1.InfoList([
                            ['.key', 'Commit message'],
                            ['.value', this.run.commit_message]
                        ], '').render($);
                        let python_file = [
                            ['.key', 'Python File'],
                            ['.value', this.run.python_file]
                        ];
                        python_file.push([
                            '.link',
                            $ => {
                                $('span', ' ');
                                $('button.inline', '[view]', {
                                    on: { click: this.events.code }
                                });
                            }
                        ]);
                        new info_list_1.InfoList(python_file, '.mono').render($);
                    });
                    $('div.block', $ => {
                        $('div.info_list', $ => {
                            $('span.key', 'Tags');
                            this.tagsList = $('span.tags');
                            this.renderTagList();
                            $('span', $ => {
                                this.tagEditBtn = $('button.inline', { on: { click: this.events.editTags } }, $ => {
                                    $('i.fa.fa-edit');
                                });
                                this.tagsInputContainer = $('div.input-container', $ => {
                                    $('i.input-icon.fa.fa-edit');
                                    this.tagsInput = $('input', {
                                        type: 'text',
                                        on: {
                                            blur: this.events.saveTags,
                                            keydown: this.events.onTagsKeyDown_
                                        }
                                    });
                                });
                            });
                            this.tagsInputContainer.style.display = 'none';
                        });
                    });
                    $('div.block', $ => {
                        $('h3', 'Storage space');
                        new info_list_1.InfoList([
                            ['.key', 'Total size'],
                            ['.value', format_1.formatSize(this.run.total_size)]
                        ], '.mono').render($);
                        new info_list_1.InfoList([
                            ['.key', 'Checkpoints'],
                            ['.value', format_1.formatSize(this.run.checkpoints_size)]
                        ], '.mono').render($);
                        new info_list_1.InfoList([
                            ['.key', 'Artifacts'],
                            ['.value', format_1.formatSize(this.run.artifacts_size)]
                        ], '.mono').render($);
                        new info_list_1.InfoList([
                            ['.key', 'SQLite'],
                            ['.value', format_1.formatSize(this.run.sqlite_size)]
                        ], '.mono').render($);
                        new info_list_1.InfoList([
                            ['.key', 'Analytics'],
                            ['.value', format_1.formatSize(this.run.analytics_size)]
                        ], '.mono').render($);
                        new info_list_1.InfoList([
                            ['.key', 'TensorBoard'],
                            ['.value', format_1.formatSize(this.run.tensorboard_size)]
                        ], '.mono').render($);
                    });
                    this.indicatorsView = $('div.indicators.block', $ => {
                        $('h3', 'Indicators');
                    });
                    this.configsView = $('div.configs.block', $ => {
                        $('h3', 'Configurations');
                    });
                });
                this.renderIndicators().then();
                this.renderConfigs().then();
                this.renderAnalyticsBtns().then();
                return this.elem;
            });
        }
        renderTagList() {
            this.tagsList.innerHTML = '';
            weya_1.Weya(this.tagsList, $ => {
                for (let tag of this.run.tags) {
                    $('button.inline', tag, { on: { click: this.events.tag.bind(this, tag) } });
                }
            });
        }
        saveTags(tags) {
            return __awaiter(this, void 0, void 0, function* () {
                let tagList = [];
                for (let tag of tags.split(',')) {
                    tag = tag.trim();
                    if (tag !== '') {
                        tagList.push(tag);
                    }
                }
                yield this.runUI.update({ tags: tagList });
                this.tagsList.style.display = null;
                this.tagEditBtn.style.display = null;
                this.tagsInputContainer.style.display = 'none';
                this.renderTagList();
            });
        }
        renderAnalyticsBtns() {
            return __awaiter(this, void 0, void 0, function* () {
                let templates = yield this.runUI.getAnalyticsTemplates();
                for (let t of templates) {
                    weya_1.Weya(this.analyticsBtns, $ => {
                        $('button', {
                            on: { click: this.events.jupyter },
                            data: { template: t }
                        }, $ => {
                            $('i.fa.fa-chart-line');
                            $('span', ` ${t}`);
                        });
                    });
                }
            });
        }
        renderIndicators() {
            return __awaiter(this, void 0, void 0, function* () {
                // let indicators: Indicators = await this.runUI.getIndicators()
                let values = yield this.runUI.loadValues();
                indicators_1.renderValues(this.indicatorsView, values);
            });
        }
        renderConfigs() {
            return __awaiter(this, void 0, void 0, function* () {
                let configs = yield this.runUI.loadConfigs();
                configs_1.renderConfigs(this.configsView, configs);
            });
        }
    }
    class RunHandler {
        constructor() {
            this.handleRun = (uuid) => {
                app_1.SCREEN.setView(new RunView(uuid));
            };
            app_1.ROUTER.route('run/:uuid', [this.handleRun]);
        }
    }
    exports.RunHandler = RunHandler;
});
