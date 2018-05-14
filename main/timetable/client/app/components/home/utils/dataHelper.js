const months =
    ['styczeń',
        'luty',
        'marzec',
        'kwiecień',
        'maj',
        'czerwiec',
        'lipiec',
        'sierpień',
        'wrzesień',
        'październik',
        'listopad',
        'grudzień'];

const daysOfWeek =
    ['niedziela',
        'poniedziałek',
        'wtorek',
        'środa',
        'czwartek',
        'piątek',
        'sobota'];

function isWeekend(day) {
    return day === 'sobota' || day === 'niedziela';
}
function countHolidays(daysList) {
    return daysList.reduce((previousValue, currentValue)=> {
        const val = (currentValue.isHoliday && currentValue.day !== 'niedziela') ? previousValue + 1 : previousValue;
        return val;
    }, 0);
}

function countWorkdays(daysList) {
    return daysList.reduce((previousValue, currentValue)=> {
        const val = (!isWeekend(currentValue.day)) ? previousValue + 1 : previousValue;
        return val;
    }, 0);
}
export  {
    months,
    daysOfWeek,
    isWeekend,
    countHolidays,
    countWorkdays
};