import * as _ from 'lodash';
import * as dataHelpers from './utils/dataHelper';
import Employee from './utils/employeeCreator';

class HomeController {

    constructor($scope, $http, $httpParamSerializerJQLike, fileSaver) {

        var vm = this;
        vm.currentShop = '';
        vm.availableShops = [];
        vm.employees = [];

        $http.get('http://localhost:5000/admin/table/get')
            .then((resp) => {
                console.log(resp.data)
                vm.currentShop = resp.data.currentShop.name;
                vm.employees = _.map(resp.data.employees, employee => {
                    return new Employee(employee.id, employee.name);
                });
                vm.availableShops = _.map(resp.data.availableShops, shop => {
                    return shop.name;
                });
            })
            .catch(err => {
                vm.currentShop = 'Wroclaw Bielany';
                vm.employees = [
                    new Employee('1', 'ble'),
                    new Employee('2', 'blaaah'),
                    new Employee('3', 'Jan'),
                    new Employee('4', 'ble'),
                    new Employee('5', 'ble'),
                    new Employee('6', 'ble')
                ];
                vm.availableShops = ['Wroclaw Bielany', 'Wroclaw Oławska'];
            });

        vm.save = save;

        function save() {
            $http({
                url: 'http://localhost:5000/admin/table/update',
                method: "POST",
                data: $httpParamSerializerJQLike({
                    'json': '{a: 2}',
                    'year': vm.year,
                    'month': _.indexOf(vm.months, vm.selected),
                    'shop': 1
                }),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function (resp) {
                console.log(vm.employees)
                console.log(resp)
            });
        }

        vm.months = dataHelpers.months;
        vm.daysOfWeek = dataHelpers.daysOfWeek;
        vm.numberOfDays = [];
        vm.print = true;
        vm.printStyle = {'border': '0.1pt  solid #808080', 'padding': '0px', 'margin': '0px', 'text-align': 'middle'};

        vm.selected = vm.months[new Date().getMonth()];
        vm.year = new Date().getFullYear();
        setDateMap();
        vm.hoursPerMonth = dataHelpers.countWorkdays(vm.numberOfDays) * 8;
        vm.countSum = countSum;
        vm.exportExcel = exportExcel;
        vm.printFile = printFile;
        vm.changeMonth = changeMonth;
        vm.changeShop = changeShop;
        vm.changeYear = changeYear;
        vm.setRowStyle = setRowStyle;
        vm.setHoliday = setHoliday;


        function setHoliday(index) {
            vm.numberOfDays[index].isHoliday = !vm.numberOfDays[index].isHoliday;
            vm.hoursPerMonth = (dataHelpers.countWorkdays(vm.numberOfDays) - dataHelpers.countHolidays(vm.numberOfDays)) * 8;
        }

        function setRowStyle(i) {
            if (i.isHoliday)
                return {'background-color': 'red'};
            if (dataHelpers.isWeekend(i.day))
                return {'background-color': '#D3D3D3'};
        }

        function changeMonth(name) {
            vm.selected = name;
            cleanUp();
            setDateMap();
            vm.hoursPerMonth = dataHelpers.countWorkdays(vm.numberOfDays) * 8;
        }

        function changeShop(name) {
            vm.currentShop = name;
            cleanUp();
            setDateMap();
        }

        function daysInMonth(month, year) {
            return new Date(year, month, 0).getDate();
        }

        function exportExcel() {
            var tab = document.getElementById('toPrint').innerHTML;
            var blob = new Blob(['\uFEFF' + tab], {
                type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=windows-1252s'
            });
            fileSaver.saveAs(blob, 'report.xls');
        }

        function printFile() {
            var html = '<html>';
            html += document.getElementById('toPrint').innerHTML;
            html += '</html>';
            var printWin = window.open('', '', 'left=0,top=0,width=1,height=1,toolbar=0,scrollbars=0,status  =0');
            printWin.document.write(html);
            printWin.document.close();
            printWin.focus();
            printWin.print();
            printWin.close();
        }

        function countSum(emp, index) {
            const to = emp.to && emp.to[index] ? emp.to[index] : 0;
            const from = emp.from && emp.from[index] ? emp.from[index] : 0;
            emp.sum[index] = to - from;
            emp.totalSum = emp.sum.reduce((a, b)=> {
                return a + b;
            })
        }

        function setDateMap() {
            const month = vm.months.indexOf(vm.selected);
            vm.numberOfDays = [];
            const daysNumber = daysInMonth(month + 1, vm.year);
            const firstDay = new Date(vm.year, month).getDay();

            for (let i = 0; i < daysNumber; i++) {
                vm.numberOfDays.push({day: `${vm.daysOfWeek[(firstDay + i) % 7]}`, isHoliday: false});
            }
        }

        function changeYear() {
            cleanUp();
            setDateMap();
            vm.hoursPerMonth = dataHelpers.countWorkdays(vm.numberOfDays) * 8;
        }

        function cleanUp() {
            _.each(vm.employees, employee => {
                employee.from = null;
                employee.to = null;
                employee.sum = [];
                employee.totalSum = 0;
            })
        }
    }
}

export default HomeController;

