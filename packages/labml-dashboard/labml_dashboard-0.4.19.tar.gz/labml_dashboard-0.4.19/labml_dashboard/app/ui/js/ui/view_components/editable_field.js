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
    class EditableField {
        constructor(value, onUpdate, empty = '') {
            this.onEdit = (e) => __awaiter(this, void 0, void 0, function* () {
                e.preventDefault();
                e.stopPropagation();
                this.span.style.display = 'none';
                this.inputContainer.style.display = null;
                this.input.value = this.value;
                this.input.focus();
            });
            this.onSave = (e) => __awaiter(this, void 0, void 0, function* () {
                e.preventDefault();
                e.stopPropagation();
                this.update();
            });
            this.onKeyDown = (e) => __awaiter(this, void 0, void 0, function* () {
                if (e.key === 'Enter') {
                    this.update();
                }
            });
            this.value = value;
            this.onUpdate = onUpdate;
            this.empty = empty;
        }
        render($) {
            this.span = $('span', {
                on: { click: this.onEdit }
            });
            this.inputContainer = $('div.input-container', $ => {
                $('i.input-icon.fa.fa-edit');
                this.input = $('input', {
                    type: 'text',
                    on: {
                        blur: this.onSave,
                        keydown: this.onKeyDown
                    }
                });
            });
            this.inputContainer.style.display = 'none';
            this.change(this.value);
        }
        update(trigger = true) {
            this.span.style.display = null;
            this.inputContainer.style.display = 'none';
            this.value = this.input.value;
            if (this.value.trim() !== '') {
                this.span.textContent = this.value;
            }
            else {
                this.span.textContent = this.empty;
            }
            if (trigger) {
                this.onUpdate(this.value);
            }
        }
        change(value) {
            this.input.value = value;
            this.update(false);
        }
    }
    exports.EditableField = EditableField;
});
