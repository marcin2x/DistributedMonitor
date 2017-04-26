module.exports = {
    measurment_id: faker.random.number(),
    measurment_name: faker.name.firstName(),
    values:  tmplUtils.multiCollection(2, 5)(function (i) {
        return {
            value: tmplUtils.stringId(),
            data: tmplUtils.stringId()
        }
    })
};