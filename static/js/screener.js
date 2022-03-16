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

var filterList = document.querySelectorAll("div.filter")

filterList.forEach(filter => {
    var filterName = filter.querySelector(".filter-name")
    var inputLeft = filter.querySelector(".left")
    var inputRight = filter.querySelector("input.right")
    var textLeft = filter.querySelector(".text.left")
    var textRight = filter.querySelector(".text.right")

    filterName.addEventListener("mouseover", e => {
        filterName.style.backgroundColor = "white";
    }, false);
    filterName.addEventListener("mouseout", function (e) {
        filterName.style.backgroundColor = "#e9ecef";
    }, false);
    filterName.addEventListener("click", filterNameClick, false);
    inputLeft.addEventListener("input", setLeftSlider, false)
    inputRight.addEventListener("input", setRightSlider, false)
    textLeft.addEventListener("change", setLeftBox, false)
    textRight.addEventListener("change", setRightBox, false)
})


function filterNameClick() {
    var filterMain = this.parentNode.querySelector(".filter-main")
    if (filterMain.style.display == "none") {
        filterMain.style.display = "block"
    }
    else {
        filterMain.style.display = "none"
    }
};

function setLeftSlider() {
    var parent = this.parentNode.parentNode;
    var range = parent.querySelector('div.range');
    var inputRight = parent.querySelector('input.right');
    var thumbLeft = parent.querySelector('.thumb.left');
    var textLeft = parent.querySelector('.text.left');

    const { value, min, max } = this;
    if (inputRight.value - value < 0.1) {
        this.value = inputRight.value - 0.1;
    }
    const percent = ((this.value - min) / (max - min)) * 100;
    range.style.left = `${percent}%`;
    thumbLeft.style.left = `${percent * .95}%`;
    textLeft.value = this.value;
};

function setRightSlider() {
    var parent = this.parentNode.parentNode;
    var range = parent.querySelector('div.range');
    var inputLeft = parent.querySelector('input.left');
    var thumbRight = parent.querySelector('.thumb.right');
    var textRight = parent.querySelector('.text.right');

    const { value, min, max } = this;
    if (value - inputLeft.value < 0.1) {
        this.value = inputLeft.value + 0.1;
    }
    const percent = ((this.value - min) / (max - min)) * 100;
    range.style.right = `${100 - percent}%`;
    thumbRight.style.right = `${(100 - percent) * .95}%`;
    textRight.value = this.value;
};

function setLeftBox() {
    var parent = this.parentNode.parentNode;
    var range = parent.querySelector('div.range');
    var inputLeft = parent.querySelector('input.left');
    var inputRight = parent.querySelector('input.right');
    var thumbLeft = parent.querySelector('.thumb.left');
    var textLeft = parent.querySelector('.text.left');

    var { min, max } = inputLeft;
    const value = Number(uncomma(textLeft.value));

    if ((value >= min) && (value < inputRight.value)) {
        const percent = ((value - min) / (max - min)) * 100;
        inputLeft.value = value;
        range.style.left = `${percent}%`;
        thumbLeft.style.left = `${percent * .95}%`;
    }
    else {
        textLeft.value = min;
        inputLeft.value = min;
        range.style.left = `0%`;
        thumbLeft.style.left = `0%`;
    }
};

function setRightBox() {
    var parent = this.parentNode.parentNode;
    var range = parent.querySelector('div.range');
    var inputLeft = parent.querySelector('input.left');
    var inputRight = parent.querySelector('input.right');
    var thumbRight = parent.querySelector('.thumb.right');
    var textRight = parent.querySelector('.text.right');

    var { min, max } = inputRight;
    const value = Number(uncomma(textRight.value));

    if ((value <= max) && (value > inputLeft.value)) {
        const percent = ((value - min) / (max - min)) * 100;
        inputRight.value = value;
        range.style.right = `${100 - percent}%`;
        thumbRight.style.right = `${(100 - percent) * .95}%`;
    }
    else {
        textRight.value = max;
        inputRight.value = max;
        range.style.right = `0%`;
        thumbRight.style.right = `0%`;
    }
};


// resultTable 출력 함수
function setTable(result) {
    const table = document.getElementById("tableOutput").getElementsByTagName('tbody')[0];
    // 테이블 초기화
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
