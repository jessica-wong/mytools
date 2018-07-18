module.exports = {

    formatDate(date,formatStr){
    if (Object.prototype.toString.call(new Date()).toLowerCase() !== "[object date]"){
        throw new Error("请传入时间格式")
    }

    var tempStr = formatStr,
        date = new Date(date),
        year = date.getFullYear(),//年份
        month = date.getMonth()+1,//月份 从0开始取
        date1 = date.getDate(), //日期
        hour = date.getHours(),
        minutes = date.getMinutes(),
        second = date.getSeconds();

    /YYYY/gi.test(formatStr) && (tempStr = tempStr.replace(/YYYY/gi, year));
    /MM/g.test(formatStr) && (tempStr = tempStr.replace(/MM/g, month.toString().length == 1 ? "0"+month: month));
    /M/g.test(formatStr) && (tempStr = tempStr.replace(/M/g, month));
    /DD/g.test(formatStr) && (tempStr = tempStr.replace(/DD/g, date1.toString().length == 1 ? "0"+date1: date1));
    /D/g.test(formatStr) && (tempStr = tempStr.replace(/D/g, date1));
    /HH/g.test(formatStr) && (tempStr = tempStr.replace(/HH/g, hour.toString().length == 1 ? "0"+hour: hour));
    /H/g.test(formatStr) && (tempStr = tempStr.replace(/H/g, hour));
    /hh/g.test(formatStr) && (tempStr = tempStr.replace(/hh/g, hour > 12 ? (hour - 12).length == 1 ? "0"+ (hour - 12): hour-12 : hour));
    /h/g.test(formatStr) && (tempStr = tempStr.replace(/h/g, hour > 12 ? hour - 12 : hour));
    /mm/g.test(formatStr) && (tempStr = tempStr.replace(/mm/g, minutes.toString().length == 1 ? "0"+minutes: minutes));
    /m/g.test(formatStr) && (tempStr = tempStr.replace(/m/g, minutes));
    /ss/g.test(formatStr) && (tempStr = tempStr.replace(/ss/g, second.toString().length == 1 ? "0"+second: second));
    /s/g.test(formatStr) && (tempStr = tempStr.replace(/s/g, second));

    return tempStr;
    }
}