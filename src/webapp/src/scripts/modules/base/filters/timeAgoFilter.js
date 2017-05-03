base.filter('timeago', () => {
    return function (date) {
        const msec = new Date() - new Date(date);
        let amount;

        if (msec < 60000) {
            return 'a moment ago';
        } else if (msec < 3600000) {
            amount = Math.floor(msec / 60000);

            if (amount == 1) {
                return 'a minute ago';
            } else {
                return amount + ' minutes ago';
            }
        } else if (msec < 86400000) {
            amount = Math.floor(msec / 3600000);

            if (amount == 1) {
                return 'an hour ago';
            } else {
                return amount + ' hours ago';
            }

        } else if (msec < 604800000) {
            amount = Math.floor(msec / 86400000);

            if (amount == 1) {
                return 'yesterday';
            } else {
                return amount + ' days ago';
            }

        } else if (msec < 2592000000) {
            amount = Math.floor(msec / 604800000);

            if (amount == 1) {
                return 'a week ago';
            } else {
                return amount + ' weeks ago';
            }

        } else if (msec < 946080000000) {
            amount = Math.floor(msec / 2592000000);

            if (amount == 1) {
                return 'a month ago';
            } else {
                return amount + ' months ago';
            }

        } else {
            return 'a long time ago';
        }
    };
});