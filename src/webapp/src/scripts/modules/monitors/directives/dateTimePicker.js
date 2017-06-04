monitors.directive('dateTimePicker', () => {
    const FORMAT = 'YYYY-MM-DD HH:mm';

    const DATETIMEPICKER_OPTIONS = {
        format: FORMAT,
        sideBySide: true,
        toolbarPlacement: 'bottom',
        showClear: true,
        useCurrent: false,
        maxDate: moment().format(FORMAT),
    };

    const getDatetimepickerById = id => {
        return angular.element(`#${id}`);
    };

    const updateModel = (value, ngModel) => {
        ngModel.$setViewValue(value);
    };

    const link = (scope, element, attrs, ngModelCtrl) => {
        const dateTimePicker = element.find('#datetimepicker')
            .datetimepicker(DATETIMEPICKER_OPTIONS);

        if (scope.lowerThan) {
            const dateTimePickerTo = getDatetimepickerById(scope.lowerThan);

            dateTimePickerTo.on('dp.change', event => {
                event.date && dateTimePicker.data('DateTimePicker').maxDate(event.date);
            });
        } else if (scope.greaterThan) {
            const dateTimePickerFrom = getDatetimepickerById(scope.greaterThan);

            dateTimePickerFrom.on('dp.change', event => {
                event.date && dateTimePicker.data('DateTimePicker').minDate(event.date);
            });
        }

        dateTimePicker
            .on('dp.change', event => {
                updateModel(
                    event.date ? event.date.format(FORMAT) : null,
                    ngModelCtrl
                );
            })
            .on('dp.hide', scope.onHideCallback);
    };

    return {
        restrict: 'E',
        templateUrl: 'scripts/modules/monitors/views/directives/date-time-picker.html',
        scope: {
            date: '=ngModel',
            lowerThan: '@lowerThan',
            greaterThan: '@greaterThan',
            onHideCallback: '=onHide'
        },
        require: 'ngModel',
        link: link
    }
});
