base.filter('timeago', () => {
    return function (date) {
       return moment(date).fromNow();
    };
});