define(["require", "exports", "../../lib/weya/weya"], function (require, exports, weya_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    class ControlsView {
        constructor(container, listener) {
            this.container = container;
            this.listener = listener;
        }
        render() {
            this.elem = weya_1.Weya('div.header_controls', this.container, $ => {
                $('i.fa.fa-sort-amount-down', { on: { click: this.listener.onSortDescending } });
                $('i.fa.fa-sort-amount-up-alt', { on: { click: this.listener.onSortAscending } });
                $('i.fa.fa-arrow-left', { on: { click: this.listener.onMoveLeft } });
                $('i.fa.fa-arrow-right', { on: { click: this.listener.onMoveRight } });
                // $('i.fa.fa-compress')
                // $('i.fa.fa-expand')
            });
        }
        show(x, y) {
            this.elem.style.display = 'block';
            let width = this.elem.offsetWidth;
            this.elem.style.top = `${y}px`;
            this.elem.style.left = `${x - width / 2}px`;
        }
        hide() {
            this.elem.style.display = null;
        }
    }
    class BackgroundView {
        constructor(container, listener) {
            this.onClick = (e) => {
                e.stopPropagation();
                e.preventDefault();
                this.listener.onHide();
            };
            this.container = container;
            this.listener = listener;
        }
        render() {
            this.elem = weya_1.Weya('div.header_controls_background', this.container, { on: { click: this.onClick } });
        }
        show(x, y) {
            this.elem.style.display = 'block';
        }
        hide() {
            this.elem.style.display = null;
        }
    }
    class HeaderCell {
        constructor(index, elem, listener) {
            this.onClick = (e) => {
                e.preventDefault();
                e.stopPropagation();
                if (this.controls != null) {
                    return;
                }
                this.listener.onClickHeader(this.index);
            };
            this.elem = elem;
            this.index = index;
            this.listener = listener;
            if (elem != null) {
                this.elem.addEventListener('click', this.onClick);
            }
        }
        getXY(container) {
            let x = 0, y = 0;
            let node = this.elem;
            while (node != container) {
                y += node.offsetTop;
                x += node.offsetLeft;
                node = node.offsetParent;
            }
            x += this.elem.offsetWidth / 2;
            y += this.elem.offsetHeight;
            return [x, y];
        }
    }
    class HeaderControls {
        constructor(container, format, listener) {
            this.onSortAscending = () => {
                this.format.sortAscending(this.selected);
                this.listener.onFormatUpdated();
            };
            this.onSortDescending = () => {
                this.format.sortDescending(this.selected);
                this.listener.onFormatUpdated();
            };
            this.onMoveLeft = () => {
                this.format.moveLeft(this.selected);
                this.listener.onFormatUpdated();
            };
            this.onMoveRight = () => {
                this.format.moveRight(this.selected);
                this.listener.onFormatUpdated();
            };
            this.container = container;
            this.format = format;
            this.listener = listener;
            this.controls = new ControlsView(this.container, this);
            this.controls.render();
            this.background = new BackgroundView(this.container, this);
            this.background.render();
            this.headers = [];
        }
        addCell(cell, elem) {
            this.headers.push(new HeaderCell(this.headers.length, elem, this));
        }
        onClickHeader(index) {
            this.selected = index;
            let [x, y] = this.headers[index].getXY(this.container);
            this.controls.show(x, y);
            this.background.show(x, y);
        }
        reset() {
            this.controls.hide();
            this.background.hide();
            this.headers = [];
        }
        onHide() {
            this.controls.hide();
            this.background.hide();
        }
    }
    exports.HeaderControls = HeaderControls;
});
