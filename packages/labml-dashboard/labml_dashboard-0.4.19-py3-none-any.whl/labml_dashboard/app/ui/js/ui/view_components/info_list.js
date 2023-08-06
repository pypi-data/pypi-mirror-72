define(["require", "exports"], function (require, exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    class InfoList {
        constructor(items, classes = '') {
            this.items = items;
            this.classes = classes;
        }
        render($) {
            $(`div.info_list${this.classes}`, $ => {
                for (let item of this.items) {
                    let classes = '';
                    let text;
                    if (typeof item === 'object' &&
                        'length' in item && item.length == 2) {
                        classes = item[0];
                        text = item[1];
                    }
                    else {
                        text = item;
                    }
                    if (classes === '.key') {
                        text = text.trimRight() + ' ';
                    }
                    $(`span${classes}`, text);
                }
            });
        }
    }
    exports.InfoList = InfoList;
});
