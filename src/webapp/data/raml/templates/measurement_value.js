module.exports = {
    measurment_id: faker.random.number(),
    host_name: faker.name.firstName() + 'PC',
    value:  faker.random.number(100),
    date: faker.date.past()
};