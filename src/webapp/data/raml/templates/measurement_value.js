module.exports = {
    measurment_id: faker.random.number(),
    host_name: faker.name.firstName() + 'PC',
    value:  faker.random.number(),
    date: faker.date.past()
};