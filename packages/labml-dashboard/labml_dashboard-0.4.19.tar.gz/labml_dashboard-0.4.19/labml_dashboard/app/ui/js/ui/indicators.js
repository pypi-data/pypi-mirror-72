define(["require", "exports", "../lib/weya/weya", "./view_components/info_list", "./view_components/format"], function (require, exports, weya_1, info_list_1, format_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    function renderValues(elem, values) {
        weya_1.Weya(elem, $ => {
            let maxStep = 0;
            for (let [k, v] of Object.entries(values)) {
                new info_list_1.InfoList([
                    ['.key', k],
                    ['.value', format_1.formatScalar(v.value)]
                ], '.mono').render($);
                maxStep = Math.max(v.step, maxStep);
            }
            new info_list_1.InfoList([
                ['.key', 'step'],
                ['.value', format_1.formatInt(maxStep)]
            ], '.mono').render($);
        });
    }
    exports.renderValues = renderValues;
    function renderIndicators(elem, indicators) {
        let inds = indicators.indicators;
        weya_1.Weya(elem, $ => {
            for (let [k, ind] of Object.entries(inds)) {
                new info_list_1.InfoList([
                    ['.key', k],
                    ['.value', `${ind.class_name}`]
                ]).render($);
            }
        });
    }
    exports.renderIndicators = renderIndicators;
});
