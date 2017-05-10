module.exports = {
    measurements_id: faker.random.number(),
    "time-from": faker.date.past(),
	"time-to": faker.date.past(),
	jwt: tmplUtils.stringId()
};