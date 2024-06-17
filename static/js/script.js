document.getElementById('startButton').addEventListener('click', function() {
    var tickers = document.getElementById('tickers').value;
    var startDate = document.getElementById('start_date').value;
    var endDate = document.getElementById('end_date').value;

    fetch('http://127.0.0.1:5000/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tickers: tickers, start_date: startDate, end_date: endDate }),
    })
    .then(response => response.json())
    .then(data => {
        var results = 'Selected Tickers: ' + tickers + '<br>';
        for (var ticker in data) {
            results += `<p>${ticker}: Current Price - ${data[ticker].current_price}, Predicted Price - ${data[ticker].predicted_price}</p>`;
        }
        document.getElementById('selectedTickers').innerHTML = results;

        var modelsText = "We use multiple models to predict stock prices, including linear regression, ARIMA, and LSTM neural networks. These models analyze historical data to forecast future values.";
        document.getElementById('modelsText').innerText = modelsText;
    });
});