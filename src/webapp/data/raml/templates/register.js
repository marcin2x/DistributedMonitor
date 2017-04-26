module.exports = {
	login: faker.internet.email(),
	password: tmplUtils.stringId(),
    password_confirmation: tmplUtils.stringId()
};