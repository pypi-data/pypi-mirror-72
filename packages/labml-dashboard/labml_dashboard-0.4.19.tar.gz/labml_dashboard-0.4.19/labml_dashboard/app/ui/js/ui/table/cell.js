define(["require", "exports", "../view_components/format"], function (require, exports, format_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    class Cell {
        constructor(opt) {
            this.isEmpty = false;
            this.isSame = false;
            this.sortRank = null;
            this.defaultWidth = '10em';
            this.align = 'left';
            this.cssClasses = '';
            this.options = opt;
            this.name = opt.name;
            this.key = opt.key;
            this.type = opt.type;
            this.sortRank = opt.sortRank;
            this.visible = !(opt.visible === false);
            this.specifiedWidth = opt.width;
        }
        get width() {
            if (this.specifiedWidth == null) {
                return this.defaultWidth;
            }
            else {
                return this.specifiedWidth;
            }
        }
        get isHidden() {
            return !this.visible || this.isEmpty;
        }
        renderHeader($) {
            if (this.isHidden) {
                return;
            }
            let tag = 'div.cell';
            tag += this.cssClasses;
            if (this.isSame) {
                tag += '.same';
            }
            let elem = $(tag, $ => {
                if (this.name != null) {
                    if (this.name.trim() !== '') {
                        $('span', this.name, { title: this.name });
                    }
                }
                else {
                    this.renderHeaderContent($);
                }
            });
            if (elem.childElementCount === 0) {
                elem.innerHTML = '&nbsp;';
            }
            elem.style.width = this.width;
            return elem;
        }
        renderHeaderContent($) {
        }
        renderCellContent($, run) {
        }
        getString(run) {
            return null;
        }
        renderCell($, run) {
            if (this.isHidden) {
                return null;
            }
            let tag = 'div.cell';
            if (this.isSame) {
                tag += '.same';
            }
            tag += this.cssClasses;
            tag += `.${this.align}`;
            let elem = $(tag, $ => {
                let value = this.getString(run);
                if (value != null) {
                    if (value.trim() !== '') {
                        $('span', value, { title: value });
                    }
                }
                else {
                    this.renderCellContent($, run);
                }
            });
            if (elem.childElementCount === 0) {
                elem.innerHTML = '&nbsp;';
            }
            elem.style.width = this.width;
            return elem;
        }
        updateCellState(runs) {
            if (!this.visible) {
                return;
            }
            this.update(runs);
        }
        update(runs) {
        }
        compare(a, b) {
            if (this.sortRank == null) {
                return 0;
            }
            else {
                return this.compareDirection(this.sortRank, a, b);
            }
        }
        compareDirection(rank, a, b) {
            let av = this.getValue(a);
            let bv = this.getValue(b);
            if (av === '') {
                av = null;
            }
            if (bv === '') {
                bv = null;
            }
            if (av == null && bv == null) {
                return 0;
            }
            else if (av == null && bv != null) {
                return Math.abs(rank);
            }
            else if (av != null && bv == null) {
                return -Math.abs(rank);
            }
            else if (av < bv) {
                return -rank;
            }
            else if (av > bv) {
                return +rank;
            }
            else {
                return 0;
            }
        }
        getValue(run) {
            return this.getString(run);
        }
        isFiltered(run, t) {
            let s = this.getString(run);
            if (s == null) {
                return false;
            }
            return s.includes(t);
        }
    }
    exports.Cell = Cell;
    class InfoCell extends Cell {
        constructor(opt) {
            super(opt);
            this.cssClasses = '.info';
            if (opt.key === 'is_dirty') {
                this.defaultWidth = '3em';
            }
        }
        getString(run) {
            return `${run.run.get(this.key)}`;
        }
        getValue(run) {
            return run.run.get(this.key);
        }
    }
    exports.InfoCell = InfoCell;
    class ValueCell extends Cell {
        constructor() {
            super(...arguments);
            this.cssClasses = '.value';
            this.decimals = 7;
            this.align = 'right';
        }
        renderCellContent($, run) {
            if (!this.isNull(run)) {
                $('span', format_1.formatFixed(run.values[this.key].value, this.decimals));
            }
        }
        isNull(run) {
            return run.values[this.key] == null || run.values[this.key].value == null;
        }
        getValue(run) {
            if (!this.isNull(run)) {
                return run.values[this.key].value;
            }
            else {
                return null;
            }
        }
        update(runs) {
            let min = null;
            let max = null;
            let count = 0;
            for (let r of runs) {
                let v = this.getValue(r);
                if (v == null) {
                    continue;
                }
                count++;
                if (min == null) {
                    min = max = v;
                }
                if (v < min) {
                    min = v;
                }
                if (v > max) {
                    max = v;
                }
            }
            this.isEmpty = count <= 0;
            let estimate = Math.max(Math.abs(max), Math.abs(min));
            let lg;
            if (estimate < 1e-9) {
                lg = 0;
            }
            else {
                lg = Math.ceil(Math.log10(estimate)) + 1;
            }
            let decimals = 7 - lg;
            decimals = Math.max(1, decimals);
            decimals = Math.min(6, decimals);
            this.decimals = decimals;
        }
    }
    exports.ValueCell = ValueCell;
    class ConfigComputedCell extends Cell {
        renderCellContent($, run) {
            if (run.configs.configs[this.key] == null) {
                return;
            }
            let conf = run.configs.configs[this.key];
            if (conf.order < 0) {
                $('span.ignored', `ignored`);
                return;
            }
            if (typeof (conf.computed) === "string") {
                let computed = conf.computed;
                computed = computed.replace('\n', '');
                $('span', computed, { title: computed });
            }
            else {
                $('span', { title: `${conf.computed}` }, format_1.formatValue(conf.computed));
            }
        }
        getValue(run) {
            if (run.configs.configs[this.key] == null) {
                return null;
            }
            let conf = run.configs.configs[this.key];
            if (conf.order < 0) {
                return null;
            }
            return conf.computed;
        }
        update(runs) {
            this.isSame = true;
            this.isEmpty = true;
            if (runs.length === 0) {
                return;
            }
            let value = this.getValue(runs[0]);
            for (let run of runs) {
                let v = this.getValue(run);
                if (v !== value) {
                    this.isSame = false;
                }
                if (v != null) {
                    this.isEmpty = false;
                }
            }
        }
    }
    exports.ConfigComputedCell = ConfigComputedCell;
    class ConfigOptionCell extends Cell {
        renderCellContent($, run) {
            if (run.configs.configs[this.key] == null) {
                return;
            }
            let conf = run.configs.configs[this.key];
            if (conf.order < 0) {
                return;
            }
            let options = new Set();
            for (let opt of conf.options) {
                options.add(opt);
            }
            if (options.has(conf.value)) {
                options.delete(conf.value);
                if (options.size === 0) {
                    $('span.only_option', conf.value);
                }
                else {
                    $('span.picked', conf.value);
                }
            }
            else {
                $('span.custom', '-');
            }
            if (options.size > 0) {
                $('span.options', $ => {
                    for (let opt of options.keys()) {
                        if (typeof opt !== 'string') {
                            continue;
                        }
                        $('span', opt);
                    }
                });
            }
        }
        update(runs) {
            this.isEmpty = true;
            this.isSame = true;
            if (runs.length === 0) {
                return;
            }
            for (let run of runs) {
                if (run.configs.configs[this.key] == null) {
                    continue;
                }
                let conf = run.configs.configs[this.key];
                if (conf.order < 0) {
                    continue;
                }
                let options = new Set();
                for (let opt of conf.options) {
                    options.add(opt);
                }
                if (options.size === 0) {
                    continue;
                }
                this.isEmpty = false;
            }
            let value = this.getValue(runs[0]);
            for (let run of runs) {
                let v = this.getValue(run);
                if (v !== value) {
                    this.isSame = false;
                }
            }
        }
        getValue(run) {
            if (run.configs.configs[this.key] == null) {
                return null;
            }
            let conf = run.configs.configs[this.key];
            if (conf.order < 0) {
                return null;
            }
            return conf.value;
        }
    }
    exports.ConfigOptionCell = ConfigOptionCell;
    class ConfigCalculatedCell extends Cell {
        constructor() {
            super(...arguments);
            this.cssClasses = '.config';
        }
        renderCellContent($, run) {
            if (run.configs.configs[this.key] == null) {
                return;
            }
            let conf = run.configs.configs[this.key];
            if (conf.order < 0) {
                $('span.ignored', `ignored`);
                return;
            }
            let options = new Set();
            for (let opt of conf.options) {
                options.add(opt);
            }
            if (options.has(conf.value)) {
                options.delete(conf.value);
                if (options.size === 0) {
                    $('span.only_option', conf.value);
                }
                else {
                    $('span.picked', conf.value);
                }
            }
            else {
                if (typeof (conf.computed) === "string") {
                    let computed = conf.computed;
                    computed = computed.replace('\n', '');
                    $('span.computed', computed, { title: computed });
                }
                else {
                    $('span.computed', { title: `${conf.computed}` }, format_1.formatValue(conf.computed));
                }
            }
        }
        getValue(run) {
            if (run.configs.configs[this.key] == null) {
                return null;
            }
            let conf = run.configs.configs[this.key];
            if (conf.order < 0) {
                return null;
            }
            let options = new Set();
            for (let opt of conf.options) {
                options.add(opt);
            }
            if (options.has(conf.value)) {
                return conf.value;
            }
            return conf.computed;
        }
        update(runs) {
            this.isSame = true;
            this.isEmpty = true;
            if (runs.length === 0) {
                return;
            }
            let value = this.getValue(runs[0]);
            for (let run of runs) {
                let v = this.getValue(run);
                // if (value == null) {
                //     value = v
                // }
                if (v != value) {
                    this.isSame = false;
                }
                if (v != null) {
                    this.isEmpty = false;
                }
            }
        }
    }
    exports.ConfigCalculatedCell = ConfigCalculatedCell;
    class StepCell extends Cell {
        constructor() {
            super(...arguments);
            this.cssClasses = '.step';
            this.defaultWidth = '6em';
            this.align = 'right';
        }
        renderCellContent($, run) {
            $('span', format_1.formatInt(run.values['step'].step));
        }
        getValue(run) {
            return run.values['step'].step;
        }
    }
    exports.StepCell = StepCell;
    class DateTimeCell extends Cell {
        constructor() {
            super(...arguments);
            this.cssClasses = '.date-time';
        }
        getString(run) {
            return `${run.run.trial_date} ${run.run.trial_time}`;
        }
    }
    exports.DateTimeCell = DateTimeCell;
    class CommentCell extends Cell {
        constructor() {
            super(...arguments);
            this.cssClasses = '.comment';
        }
        getString(run) {
            return run.run.comment;
        }
    }
    exports.CommentCell = CommentCell;
    class SizeCell extends Cell {
        constructor() {
            super(...arguments);
            this.cssClasses = '.size';
            this.defaultWidth = '5em';
            this.align = 'right';
        }
        getSize(run) {
            let size = run.run.get(this.key);
            return size;
        }
        renderCellContent($, run) {
            let size = this.getSize(run);
            $('span', format_1.formatSize(size));
        }
        getValue(run) {
            return this.getSize(run);
        }
    }
    exports.SizeCell = SizeCell;
    class ExperimentNameCell extends Cell {
        constructor() {
            super(...arguments);
            this.cssClasses = '.experiment-name';
        }
        getString(run) {
            return run.run.name;
        }
    }
    exports.ExperimentNameCell = ExperimentNameCell;
    class ControlsCell extends Cell {
        constructor() {
            super(...arguments);
            this.cssClasses = '.controls';
            this.defaultWidth = '3em';
        }
        getString(run) {
            return "";
        }
    }
    exports.ControlsCell = ControlsCell;
    class GenerationsCell extends Cell {
        constructor() {
            super(...arguments);
            this.defaultWidth = '3em';
        }
        renderCellContent($, run) {
            for (let i = 0; i < run.generations; ++i) {
                $('i.generation.fas.fa-circle');
            }
            if (run.children > 0) {
                $('i.generation.fas.fa-circle');
            }
            else {
                $('i.generation.far.fa-circle');
            }
        }
    }
    exports.GenerationsCell = GenerationsCell;
    class CellFactory {
        static create(opt) {
            switch (opt.type) {
                case "controls":
                    return new ControlsCell(opt);
                case "generations":
                    return new GenerationsCell(opt);
                case "experiment_name":
                    return new ExperimentNameCell(opt);
                case "comment":
                    return new CommentCell(opt);
                case "date_time":
                    return new DateTimeCell(opt);
                case "info":
                    return new InfoCell(opt);
                case "size":
                    return new SizeCell(opt);
                case "step":
                    return new StepCell(opt);
                case "value":
                    return new ValueCell(opt);
                case "config_computed":
                    return new ConfigComputedCell(opt);
                case "config_options":
                    return new ConfigOptionCell(opt);
                case "config_calculated":
                    return new ConfigCalculatedCell(opt);
                default:
                    throw new Error("Unknown Cell Type" + opt.type);
            }
        }
    }
    exports.CellFactory = CellFactory;
});
