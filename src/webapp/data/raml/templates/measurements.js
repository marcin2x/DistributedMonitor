module.exports = tmplUtils.multiCollection(10, 20)(function (i) {
    return tmplUtils.getTemplate('measurement.js');
});