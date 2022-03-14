function comma(str) {
    var str = String(str);
    return str.replace(/(\d)(?=(?:\d{3})+(?!\d))/g, '$1,');
}
function uncomma(str) {
    var str = String(str);
    var str = str.replace(/(^0+)/, '');
    return str.replace(/[^\d]+/g, '');
}
function inputNumberFormat(obj) {
    obj.value = comma(uncomma(obj.value));
}

for (const i in filtersList) {
    var filterName = filtersList[i] // eps, per, bps, pbr, dps, dvd_yld    
    var filters = $(`[data-id^=${filterName}]`) // objects
    
    const setLeftSlider = e => {
        const _this = e.target;
        const { value, min, max } = _this;
        if (filters[3].value - +value < 0.1) {
            _this.value = +filters[3].value - 0.1;
        }
        const percent = ((+_this.value - +min) / (+max - +min)) * 100;
        filters[4].style.left = `${percent}%`;
        filters[5].style.left = `${percent * .95}%`;
        filters[7].value = _this.value;
    };
    
    const setRightSlider = e => {
        const _this = e.target;
        const { value, min, max } = _this;
        if (+value - +filters[2].value < 0.1) {
            _this.value = +filters[2].value + 0.1;
        }
        const percent = ((+_this.value - +min) / (+max - +min)) * 100;
        filters[4].style.right = `${100 - percent}%`;
        filters[6].style.right = `${(100 - percent) * .95}%`;
        filters[8].value = _this.value;
    };
    
    const setLeftBox = e => {
        const _this = Number(e.target.value);
        const { min, max } = filters[2]
        if ((_this >= min) && (_this < filters[3].value)) {
            const percent = ((+_this - +min) / (+max - +min)) * 100;
            filters[2].value = percent;
            filters[4].style.left = `${percent}%`;
            filters[5].style.left = `${percent *.95}%`;
        }
        else {

        }
    }

    const setRightBox = e => {
        const _this = Number(e.target.value);
        const { min, max } = filters[3]
        if ((_this <= max) && (_this > filters[2].value)) {
            const percent = ((+_this - +min) / (+max - +min)) * 100;
            console.log(comma(percent))
            filters[3].value = percent;
            filters[4].style.right = `${100 - percent}%`;
            filters[6].style.right = `${(100 - percent) *.95}%`;
        }
    }

    // slider 동작 및 input text-box 값 수정
    if (filters[2] && filters[3]) {
        filters[2].addEventListener("input", setLeftSlider);
        filters[3].addEventListener("input", setRightSlider);
    };
    
    // input text-box 값 수정 시 slider 동작
    if (filters[7] && filters[8]) {
        filters[7].addEventListener("change", setLeftBox)
        filters[8].addEventListener("change", setRightBox)
    };
};

// resultTable 출력 함수
function setTable(result) {
    const table = document.getElementById("tableOutput").getElementsByTagName('tbody')[0];
    table.innerHTML = '';
    for (let i = 1; i < result.length; i++) {
        var row = `
        <tr>
        <td>${result[i].stcd}</td>
        <td>${result[i].stnm}</td>
        <td>${result[i].eps}</td>
        <td>${result[i].per}</td>
        <td>${result[i].bps}</td>
        <td>${result[i].pbr}</td>
        <td>${result[i].dps}</td>
        <td>${result[i].dvd_yld}</td>
        </tr>
        `
        var newRow = table.insertRow(table.rows.length);
        newRow.innerHTML = row;
    }
}