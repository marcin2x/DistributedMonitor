module.exports = {
	id: faker.random.number(),
	name: faker.name.firstName() + 'PC',
	measurements: tmplUtils.multiCollection(3, 6)( i => {
		return {
			id: faker.random.number(),
			description: faker.lorem.words(1) + '_usage'
		}
	}),
	metadata: tmplUtils.multiCollection(3, 6)( i => {
		return {
			key: tmplUtils.stringId(),
			value: faker.random.number()
		}
	})
};