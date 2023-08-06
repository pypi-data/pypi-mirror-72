define(["require", "exports", "../../lib/weya/weya", "../app"], function (require, exports, weya_1, app_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    class RunRowView {
        constructor(r, index, selectListeners) {
            this.cells = [];
            this.onSelect = (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.setSelection(!this.isSelected);
            };
            this.onOpen = (e) => {
                e.preventDefault();
                e.stopPropagation();
                app_1.ROUTER.navigate(`/run/${this.run.run.uuid}`);
            };
            this.run = r;
            this.index = index;
            this.selectListeners = selectListeners;
            this.isSelected = false;
        }
        render(format) {
            let indexClass = this.index % 2 == 0 ? 'even' : 'odd';
            this.cells = [];
            this.elem = weya_1.Weya('div.row.' + indexClass, { on: { click: this.onSelect } }, $ => {
                for (let cell of format) {
                    let rendered = cell.renderCell($, this.run);
                    this.cells.push(rendered);
                    if (cell.type === 'controls') {
                        this.controls = rendered;
                    }
                }
            });
            this.controls.innerHTML = '';
            weya_1.Weya('span.controls', this.controls, $ => {
                this.selectIcon = $('i.fa.fa-square', { on: { click: this.onSelect } });
                $('a', {
                    on: { click: this.onOpen },
                    href: `/run/${this.run.run.name}/${this.run.run.uuid}`
                }, $ => {
                    $('i.fa.fa-file');
                });
            });
            return this.elem;
        }
        setSelection(isSelected) {
            this.isSelected = isSelected;
            this.selectIcon.classList.remove('fa-square');
            this.selectIcon.classList.remove('fa-check-square');
            if (this.isSelected) {
                this.elem.classList.add('selected');
                this.selectListeners.onSelect(this.run);
                this.selectIcon.classList.add('fa-check-square');
            }
            else {
                this.elem.classList.remove('selected');
                this.selectListeners.onUnSelect(this.run);
                this.selectIcon.classList.add('fa-square');
            }
        }
    }
    exports.RunRowView = RunRowView;
});
