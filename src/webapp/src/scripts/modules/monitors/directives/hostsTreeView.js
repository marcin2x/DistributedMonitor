monitors.directive('hostsTreeView', () => {
    const link = (scope, element) => {
        const $tree = $(element).find('#tree');

        const checkAllUncheckedNodes = nodes => {
            let nodesToCheck = [];

            nodes.map((childNode) => {
                if (!childNode.state.checked) {
                    $tree.treeview('checkNode', [childNode.nodeId, {silent: true}]);
                    nodesToCheck.push(childNode.measurement);
                }
            });

            nodesToCheck.length && scope.selectMeasurements(nodesToCheck);
        };

        const uncheckAllCheckedNodes = nodes => {
            let nodesToUncheck = [];

            nodes.map((childNode) => {
                if (childNode.state.checked) {
                    $tree.treeview('uncheckNode', [childNode.nodeId, {silent: true}]);
                    nodesToUncheck.push(childNode.measurement);
                }
            });

            nodesToUncheck.length && scope.deselectMeasurements(nodesToUncheck);
        };

        const treeData = scope.hosts.map((host) => ({
            text: host.name,
            selectable: false,
            state: {
                expanded: false
            },
            nodes: host.measurements.map((measurement) => ({
                text: measurement.description,
                selectable: false,
                measurement: {
                    id: measurement.id,
                    description: measurement.description,
                    hostName: host.name
                }
            }))
        }));

        $tree.treeview({
            data: treeData,
            showCheckbox: true
        });

        $tree.on('nodeChecked', (event, node) => {
            typeof node.nodes !== 'undefined'
                ? checkAllUncheckedNodes(node.nodes)
                : scope.selectMeasurements([node.measurement]);
        });

        $tree.on('nodeUnchecked', (event, node) => {
            typeof node.nodes !== 'undefined'
                ? uncheckAllCheckedNodes(node.nodes)
                : scope.deselectMeasurements([node.measurement]);
        });
    };

    return {
        restrict: 'E',
        template: '<div id="tree"></div>',
        scope: {
            hosts: '=ngModel',
            selectMeasurements: '=selectMeasurements',
            deselectMeasurements: '=deselectMeasurements'
        },
        link: link
    };
});
