let date =  new Date();
date.setSeconds(date.getSeconds() - faker.random.number(60));

module.exports = {
    value:  faker.random.number(100),
    date
};