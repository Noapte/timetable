import template from './home.html';
import controller from './home.controller';
import './home.scss';

let homeComponent = {
    restrict: 'E',
    bindings: {},
    template,
    controller: ['$scope', '$http', 'FileSaver', controller]
};

export default homeComponent;
