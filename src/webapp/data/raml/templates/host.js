module.exports = {
	id: faker.random.number(),
	name: faker.name.firstName() + 'PC',
	measurements: tmplUtils.multiCollection(3, 6)( i => {
		return {
			id: faker.random.number(),
			description: faker.lorem.sentences()
		}
	}),
	metadata: tmplUtils.multiCollection(3, 6)( i => {
		return {
			key: tmplUtils.stringId(),
			value: faker.random.number()
		}
	})
};