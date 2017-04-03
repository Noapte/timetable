import * as _ from 'lodash';
import * as dataHelpers from './utils/dataHelper';
import Employee from './utils/employeeCreator';

class HomeController {
    constructor($scope, $http, $httpParamSerializerJQLike, fileSaver) {
        var vm = this;
        vm.currentShop = null;
        vm.availableShops = [];
        vm.employees = [];
        vm.availableSchedules = {};
        vm.months = dataHelpers.months;
        vm.selected = vm.months[new Date().getMonth()];
        vm.year = new Date().getFullYear();
        vm.daysOfWeek = dataHelpers.daysOfWeek;
        vm.numberOfDays = [];
        vm.print = true;
        vm.printStyle = {'border': '0.1pt  solid #808080', 'padding': '0px', 'margin': '0px', 'text-align': 'middle'};
        vm.hoursPerMonth = dataHelpers.countWorkdays(vm.numberOfDays) * 8 - dataHelpers.countHolidays(vm.numberOfDays) * 8;

        setDateMap();
        loadCurrentTimetableData('');

        vm.save = save;
        vm.radomize = randomize;
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
            if (scheduleExist()) {
                const schedule = vm.availableSchedules[vm.year][_.indexOf(vm.months, vm.selected)];
                vm.employees = _.isString(schedule) ? JSON.parse(schedule) : schedule;
            }
            else {
                cleanUp();
            }
            setDateMap();
            vm.hoursPerMonth = dataHelpers.countWorkdays(vm.numberOfDays) * 8;
        }
        function randomize(){
            _.each(vm.employees, employee => {

                console.log("A")
            } )
            
        }

        function changeShop(shop) {
            loadCurrentTimetableData(shop.id);
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

        function loadCurrentTimetableData(shopId) {

            $http({
                url: 'admin/table/get',
                method: "POST",
                data: $httpParamSerializerJQLike({
                    'shop': shopId
                }),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function (resp) {
                vm.currentShop = resp.data.currentShop;
                vm.availableSchedules = resp.data.schedule;
                vm.availableShops = resp.data.availableShops;
                if (vm.availableSchedules && vm.availableSchedules[vm.year] && vm.availableSchedules[vm.year][_.indexOf(vm.months, vm.selected)])

                    vm.employees = JSON.parse(vm.availableSchedules[vm.year][_.indexOf(vm.months, vm.selected)]);
                else
                    vm.employees = _.map(resp.data.employees, employee => {
                        return new Employee(employee.id, employee.name);
                    });
            })
                .catch(err => {
                    //just for testing without database
                    setMockedObjects();
                    console.log(err);
                });
        }

        function setMockedObjects() {
            vm.currentShop = {name: 'Bielany Wroclaw', id: 1};
            const data = [{
                "id": 1,
                "name": "fkiepski",
                "from": {"0": 1, "1": 1},
                "to": {"0": 13, "1": 13},
                "sum": [12, 12],
                "totalSum": 24
            }, {"id": 2, "name": "mpaździoch", "from": null, "to": null, "sum": [], "totalSum": 0}, {
                "id": 3,
                "name": "aboczek",
                "from": null,
                "to": null,
                "sum": [],
                "totalSum": 0
            }, {"id": 4, "name": "wkiepski", "from": null, "to": null, "sum": [], "totalSum": 0}, {
                "id": 5,
                "name": "jsocha",
                "from": null,
                "to": null,
                "sum": [],
                "totalSum": 0
            }, {"id": 11, "name": "admin", "from": null, "to": null, "sum": [], "totalSum": 0}];
            vm.employees = _.map(data, employee => {
                return new Employee(employee.id, employee.name);
            });
            vm.availableShops = [{name: 'Bielany Wroclaw', id: 1}, {name: 'Bielany2 Wroclaw', id: 1}];
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

            if (scheduleExist()) {
                const schedule = vm.availableSchedules[vm.year][_.indexOf(vm.months, vm.selected)];
                vm.employees = _.isString(schedule) ? JSON.parse(schedule) : schedule;
            }
            else {
                cleanUp();
            }

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

        function scheduleExist() {
            vm.availableSchedules = vm.availableSchedules || {};
            if (vm.availableSchedules[vm.year] && vm.availableSchedules[vm.year][_.indexOf(vm.months, vm.selected)]) {
                return true;
            }
            return false;
        }

        function save() {
            vm.availableSchedules = vm.availableSchedules || {};
            if (vm.availableSchedules[vm.year] && vm.availableSchedules[vm.year][_.indexOf(vm.months, vm.selected)]) {
                vm.availableSchedules[vm.year][_.indexOf(vm.months, vm.selected)] = vm.employees;
            }

            else {
                if (vm.availableSchedules[vm.year]) {
                    vm.availableSchedules[vm.year][_.indexOf(vm.months, vm.selected)] = vm.employees;
                }
                else {
                    vm.availableSchedules[vm.year] = {};
                    vm.availableSchedules[vm.year][_.indexOf(vm.months, vm.selected)] = vm.employees;
                }
            }
            $http({
                url: 'admin/table/update',
                method: "POST",
                data: $httpParamSerializerJQLike({
                    'json': JSON.stringify(vm.employees),
                    'year': vm.year,
                    'month': _.indexOf(vm.months, vm.selected),
                    'shop': vm.currentShop.id
                }),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function (resp) {
                console.log(resp)
            });
        }
    }
}

export default HomeController;

