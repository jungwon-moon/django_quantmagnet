Color = [
    'rgb(255, 99, 132)',
    'rgb(54, 162, 235)',
    'rgb(255, 205, 86)',
]

function comma(str) {
    str = String(str);
    return str.replace(/(\d)(?=(?:\d{3})+(?!\d))/g, '$1,');
}
function uncomma(str) {
    str = String(str);
    return str.replace(/[^\d]+/g, '');
}
function inputNumberFormat(obj) {
    obj.value = comma(uncomma(obj.value));
}

//// cagr
function cagr() {
    console.log("cagr");
    var bv = document.getElementById('bv').value
    var ev = document.getElementById('ev').value
    var n = document.getElementById('n').value
    var result = ((ev / bv) ** (1 / n) - 1) * 100

    document.getElementById('result').textContent = result.toFixed(2) + ' %'
}

//// investment_inflation
function savingsgoalDetails() {
    $('#savingsgoal-detail-area').css('display', 'block')
    $('#savingsgoal-details').css('display', 'none')
}
function savingsgoalSimply() {
    $('#savingsgoal-detail-area').css('display', 'none')
    $('#savingsgoal-details').css('display', 'block')
}
function savingsestimatorDetails() {
    $('#savingsestimator-detail-area').css('display', 'block')
    $('#savingsestimator-details').css('display', 'none')
}
function savingsestimatorSimply() {
    $('#savingsestimator-detail-area').css('display', 'none')
    $('#savingsestimator-details').css('display', 'block')
}
function timetoachievegoalDetails() {
    $('#timetoachievegoal-detail-area').css('display', 'block')
    $('#timetoachievegoal-details').css('display', 'none')
}
function timetoachievegoalSimply() {
    $('#timetoachievegoal-detail-area').css('display', 'none')
    $('#timetoachievegoal-details').css('display', 'block')
}

function savingsgoalToggle() {
    $('#inputareasavingsgoal').css('display', 'block');
    $('#inputareasavingsestimator').css('display', 'none');
    $('#inputareatimetoachievegoal').css('display', 'none');

    $('#calculate').attr('onclick', '').unbind('click');
    $('#calculate').attr('onclick', '').click(savingsgoal);
}
function savingsestimatorToggle() {
    $('#inputareasavingsgoal').css('display', 'none');
    $('#inputareasavingsestimator').css('display', 'block');
    $('#inputareatimetoachievegoal').css('display', 'none');

    $('#calculate').attr('onclick', '').unbind('click');
    $('#calculate').attr('onclick', '').click(savingsestimator);
}
function timetoachievegoalToggle() {
    $('#inputareasavingsgoal').css('display', 'none');
    $('#inputareasavingsestimator').css('display', 'none');
    $('#inputareatimetoachievegoal').css('display', 'block');

    $('#calculate').attr('onclick', '').unbind('click');
    $('#calculate').attr('onclick', '').click(timetoachievegoal);
    //  compounding 계산 일단 보류
    $('#timetoachivegoal-compounding').css('display', 'none');
}


function savingsgoal() {
    $('#outputarea').css('display', 'block');
    $('#outputtablearea').css('display', 'block');
    $('#outputchart').remove();
    $('#outputtable').remove();
    $('#outputchartarea').append('<canvas id="outputchart"></canvas>');
    tableHtml = `
    <table id="outputtable" class="container table table-sm"">
    <thead>
    <tr class="text-center">
    <th>경과 개월</th>
    <th>누적 투자액</th>
    <th>누적 이자</th>
    <th>누적 총저축액</th>
    </tr>
    </thead>
    <tbody></tbody>
    </table>
    `
    $('#outputtablearea').append(tableHtml);
    
    $('#savingsgoal-output').css('display', 'block');
    $('#savingsestimator-output').css('display', 'none');
    $('#timetoachievegoal-output').css('display', 'none');
    
    // 복리 계산 
    // 월:1 분기:3 반기:6 연간:12
    const compounding = Number(document.getElementById('savingsgoal-compounding').value);
    // 목표 저축액 
    const goal = Number(uncomma(document.getElementById('savingsgoal-goal').value));
    // 현재 저축액
    const current = Number(uncomma(document.getElementById('savingsgoal-current').value));
    // 연이율
    const annualInterest = Number(document.getElementById('savingsgoal-annualinterest').value) / 1200 * compounding;
    // 연수
    const numberOfYear = Number(document.getElementById('savingsgoal-numberofyear').value) * 12;
    // 복리 승수
    const numberOfMul = Number(document.getElementById('savingsgoal-numberofyear').value) * 12 / compounding;
    
    // 월별 투자액
    const result1 = Number(Math.round(((goal - current * (1 + annualInterest) ** numberOfMul) / (((1 + annualInterest) ** numberOfMul - 1) / annualInterest)) / compounding))
    // 누적 투자액
    const result2 = Number(Math.round(result1 * numberOfYear + current))

    // 월별 투자액
    document.getElementById('savingsgoal-outputvalue0').textContent = comma(Math.round(result1))
    // 누적 이자
    document.getElementById('savingsgoal-outputvalue1').textContent = comma(Math.round(goal - result2))
    // 누적 투자액
    document.getElementById('savingsgoal-outputvalue2').textContent = comma(Math.round(result2))
    
    let sumInvestment = [0]
    let sumInterest = [0]
    let sumSavings = [current]
    
    let chartCurrent = []
    let chartInterest = []
    let chartSavings = []
    
    const ctx = document.getElementById('outputchart')
    
    const labels = [];
    for (let month = compounding; month <= numberOfYear; month+=compounding) {
        sumInvestment.push(Number(Math.round(sumInvestment.slice(-1)) + result1*compounding))
        currentInterest = (Number(sumSavings.slice(-1)) * annualInterest)
        sumInterest.push(Math.round(Number(sumInterest.slice(-1)) + currentInterest))
        sumSavings.push(Math.round(Number(sumSavings.slice(-1)) + result1*compounding + currentInterest))
        if (month % 12 == 0) {
            labels.push(month / 12 + '년')
            chartCurrent.push(current)
            chartInterest.push(sumInterest[sumInterest.length - 1])
            chartSavings.push(sumSavings[sumSavings.length - 1] - sumInterest[sumInterest.length - 1] - current)
        }
    }
    
    // 테이블
    for (let i = 1; i < sumSavings.length; i++) {
        var row = `
        <tr class="text-center">
        <td>${i*compounding}</td>
        <td>${comma(sumInvestment[i] + current)}</td>
        <td>${comma(sumInterest[i])}</td>
        <td>${comma(sumSavings[i])}</td>
        </tr>
        `
        $('#outputtable > tbody:last').append(row)
    }
    
    // 차트
    const data = {
        labels: labels,
        datasets: [
            {
                label: '현재 저축액',
                data: chartCurrent,
                backgroundColor: Color[0],
            },
            {
                label: '누적 투자액',
                data: chartSavings,
                backgroundColor: Color[1],
            },
            {
                label: '누적 이자',
                data: chartInterest,
                backgroundColor: Color[2],
            },
        ]
    }
    
    const config = {
        type: 'bar',
        data: data,
        options: {
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        boxWidth: 12,
                        boxHeight: 12,
                    }
                },
                title: {
                    display: false,
                    text: 'chchchchchch'
                },
            },
            maintainAspectRatio: false,
            responsive: true,
            scales: {
                x: {
                    stacked: true,
                },
                y: {
                    beginAtZero: true,
                    stacked: true,
                }
            }
        }
    }
    const myChart = new Chart(ctx, config);
    $('#outputtablearea').css('display', 'none');
}

function savingsestimator() {
    $('#outputarea').css('display', 'block');
    $('#outputtablearea').css('display', 'none');
    $('#outputchart').remove();
    $('#outputtable').remove();
    $('#outputchartarea').append('<canvas id="outputchart"></canvas>');
    tableHtml = `
    <table id="outputtable" class="container table"">
    <thead>
    <tr class="text-center">
    <th>경과 개월</th>
    <th>누적 투자액</th>
    <th>누적 이자</th>
    <th>누적 총저축액</th>
    </tr>
    </thead>
    <tbody></tbody>
    </table>
    `
    $('#outputtablearea').append(tableHtml);
    $('#outputview').append('<canvas id="outputchart"></canvas>');
    
    $('#savingsgoal-output').css('display', 'none');
    $('#savingsestimator-output').css('display', 'block');
    $('#timetoachievegoal-output').css('display', 'none');
    
    const compounding = Number(document.getElementById('savingsestimator-compounding').value);
    const current = Number(uncomma(document.getElementById('savingsestimator-current').value));
    const investment = Number(uncomma(document.getElementById('savingsestimator-investment').value)) * compounding;
    const annualInterest = Number(document.getElementById('savingsestimator-annualinterest').value) / 1200 * compounding;
    const numberOfYear = Number(document.getElementById('savingsestimator-numberofyear').value) * 12;
    const numberOfMul = Number(document.getElementById('savingsestimator-numberofyear').value) * 12 / compounding;
    
    // 누적 투자액
    const result1 = current + investment * numberOfMul;
    // 현재 저축액 이자
    const result2 = current * (1 + annualInterest) ** (numberOfMul);
    // 총 저축액
    const result3 = result2 + investment * ((1 + annualInterest) ** numberOfMul - 1) / annualInterest;
    
    document.getElementById('savingsestimator-outputvalue0').textContent = comma(Math.round(result3));
    document.getElementById('savingsestimator-outputvalue1').textContent = comma(Math.round(result3 - result1));
    document.getElementById('savingsestimator-outputvalue2').textContent = comma(Math.round(result1));
    
    let sumInvestment = [0]
    let sumInterest = [0]
    let sumSavings = [current]
    
    let chartCurrent = []
    let chartInterest = []
    let chartSavings = []
    
    const ctx = document.getElementById('outputchart');
    
    const labels = [];
    for (let month = compounding; month <= numberOfYear; month+=compounding) {
        sumInvestment.push(Number(Math.round(sumInvestment.slice(-1)) + investment))
        currentInterest = (Number(sumSavings.slice(-1)) * annualInterest)
        sumInterest.push(Math.round(Number(sumInterest.slice(-1)) + currentInterest))
        sumSavings.push(Math.round(Number(sumSavings.slice(-1)) + investment + currentInterest))
        if (month % 12 == 0) {
            labels.push(month / 12 + '년')
            chartCurrent.push(current)
            chartInterest.push(sumInterest[sumInterest.length - 1])
            chartSavings.push(sumSavings[sumSavings.length - 1] - sumInterest[sumInterest.length - 1] - current)
        }
    }
    
    for (let i = 1; i < sumSavings.length; i++) {
        var row = `
        <tr class="text-center">
        <td>${i * compounding}</td>
        <td>${comma(sumInvestment[i] + current)}</td>
        <td>${comma(sumInterest[i])}</td>
        <td>${comma(sumSavings[i])}</td>
        </tr>
        `
        $('#outputtable > tbody:last').append(row)
    }
    
    const data = {
        labels: labels,
        datasets: [
            {
                label: '현재 저축액',
                data: chartCurrent,
                backgroundColor: Color[0],
            },
            {
                label: '누적 투자액',
                data: chartSavings,
                backgroundColor: Color[1],
            },
            {
                label: '누적 이자',
                data: chartInterest,
                backgroundColor: Color[2],
            },
        ]
    }
    
    const config = {
        type: 'bar',
        data: data,
        options: {
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        boxWidth: 12,
                        boxHeight: 12,
                    }
                },
                title: {
                    display: false,
                    text: 'chchchchchch'
                },
            },
            maintainAspectRatio: false,
            responsive: true,
            scales: {
                x: {
                    stacked: true,
                },
                y: {
                    beginAtZero: true,
                    stacked: true,
                }
            }
        }
    }
    const myChart = new Chart(ctx, config);
    $('#outputtablearea').css('display', 'none');
}

function timetoachievegoal() {
    $('#outputarea').css('display', 'block');
    $('#outputtablearea').css('display', 'none');
    $('#outputchart').remove();
    $('#outputtable').remove();
    $('#outputchartarea').append('<canvas id="outputchart"></canvas>');
    tableHtml = `
    <table id="outputtable" class="container table"">
    <thead>
    <tr class="text-center">
    <th>경과 개월</th>
    <th>누적 투자액</th>
    <th>누적 이자</th>
    <th>누적 총저축액</th>
    </tr>
    </thead>
    <tbody></tbody>
    </table>
    `
    $('#outputtablearea').append(tableHtml);
    $('#outputview').append('<canvas id="outputchart"></canvas>');
    
    $('#savingsgoal-output').css('display', 'none');
    $('#savingsestimator-output').css('display', 'none');
    $('#timetoachievegoal-output').css('display', 'block');
    
    // var compounding = Number(document.getElementById('timetoachievegoal-compounding').value);
    var compounding = 1;
    var current = Number(uncomma(document.getElementById('timetoachievegoal-current').value));
    var goal = Number(uncomma(document.getElementById('timetoachievegoal-goal').value));
    var investment = Number(uncomma(document.getElementById('timetoachievegoal-investment').value));
    var annualInterest = Number(document.getElementById('timetoachievegoal-annualinterest').value) / 1200 * compounding;
    
    var numberOfYear = 0;
    var sum = 0;
    while (sum < goal) {
        sum = current * (1 + annualInterest) ** numberOfYear
        sum += investment * ((1 + annualInterest) ** numberOfYear - 1) / annualInterest;
        numberOfYear++;
    }
    numberOfYear -= 1;
    
    var result0 = parseInt(numberOfYear / 12) + '년 ' + parseInt(numberOfYear % 12) + '개월'
    var result1 = current + investment * numberOfYear;
    var result2 = current * (1 + annualInterest) ** (numberOfYear);
    var result3 = result2 + investment * ((1 + annualInterest) ** numberOfYear - 1) / annualInterest;
    
    document.getElementById('timetoachievegoal-outputvalue0').textContent = result0;
    document.getElementById('timetoachievegoal-outputvalue1').textContent = comma(Math.round(result3 - result1));
    document.getElementById('timetoachievegoal-outputvalue2').textContent = comma(Math.round(result1));
        
    let sumInvestment = [0]
    let sumInterest = [0]
    let sumSavings = [current]
    
    let chartCurrent = []
    let chartInterest = []
    let chartSavings = []
    
    const ctx = document.getElementById('outputchart');
    
    const labels = [];
    for (let i = 1; i <= numberOfYear; i++) {
        sumInvestment.push(Number(Math.round(sumInvestment.slice(-1)) + investment))
        currentInterest = (Number(sumSavings.slice(-1)) * annualInterest)
        sumInterest.push(Math.round(Number(sumInterest.slice(-1)) + currentInterest))
        sumSavings.push(Math.round(Number(sumSavings.slice(-1)) + investment + currentInterest))
        if (i % 12 == 0 || i == numberOfYear) {
            labels.push(Math.ceil(i / 12) + '년')
            chartCurrent.push(current)
            chartInterest.push(sumInterest[sumInterest.length - 1])
            chartSavings.push(sumSavings[sumSavings.length - 1] - sumInterest[sumInterest.length - 1] - current)
        }
    }
    
    for (let i = 1; i < sumSavings.length; i++) {
        var row = `
        <tr class="text-center">
        <td>${i}</td>
        <td>${comma(sumInvestment[i] + current)}</td>
        <td>${comma(sumInterest[i])}</td>
        <td>${comma(sumSavings[i])}</td>
        </tr>
        `
        $('#outputtable > tbody:last').append(row)
    }
    
    const data = {
        labels: labels,
        datasets: [
            {
                label: '현재 저축액',
                data: chartCurrent,
                backgroundColor: Color[0],
            },
            {
                label: '누적 투자액',
                data: chartSavings,
                backgroundColor: Color[1],
            },
            {
                label: '누적 이자',
                data: chartInterest,
                backgroundColor: Color[2],
            },
        ]
    }
    
    const config = {
        type: 'bar',
        data: data,
        options: {
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        boxWidth: 12,
                        boxHeight: 12,
                    }
                },
                title: {
                    display: false,
                    text: 'chchchchchch'
                },
            },
            maintainAspectRatio: false,
            responsive: true,
            scales: {
                x: {
                    stacked: true,
                },
                y: {
                    beginAtZero: true,
                    stacked: true,
                }
            }
        }
    }
    const myChart = new Chart(ctx, config);
    $('#outputtablearea').css('display', 'none');
}


function chartToggle() {
    $('#outputchartarea').css('display', 'inline-block')
    $('#outputtablearea').css('display', 'none')
}

function tableToggle() {
    $('#outputchartarea').css('display', 'none')
    $('#outputtablearea').css('display', 'inline-block')
}