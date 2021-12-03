function cagr() {
    var bv = document.getElementById('bv').value
    var ev = document.getElementById('ev').value
    var n = document.getElementById('n').value
    var result = ((ev / bv) ** (1 / n) - 1) * 100

    document.getElementById('result').textContent = result.toFixed(2) + ' %'
}