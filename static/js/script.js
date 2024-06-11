const init = async () => {
  sentiment = await (await fetch('/api/v1.0/stock_sentiment_score')).json()
  stock_hist = await (await fetch('/api/v1.0/stock_history')).json()

  console.log(stock_hist);

  tickers = sentiment.map(obj=>obj.Ticker);
  y_values = sentiment.map(obj=>obj['Sentiment Score'])

  document.getElementById('stocks').innerHTML = '';
  tickers.forEach(stock => {
    document.getElementById('stocks').innerHTML += `<h3>${stock}</h3>`
  })

  // Sentiment
  var trace1 = {
    x: tickers,
    y: y_values,
    type: 'bar',
    text: y_values.map(x => Math.round(x * 100) / 100),
    textposition: 'auto',
    hoverinfo: 'none',
    marker: {
      color: 'rgb(158,202,225)',
      opacity: 0.6,
      line: {
        color: 'rgb(8,48,107)',
        width: 1.5
      }
    }
  };

  var data1 = [trace1];

  var layout = {
    title: '<b>Average Sentiment Report</b>',
    barmode: 'stack'
  };

  Plotly.newPlot('chart01', data1, layout);

  // History
  
  data2 = tickers.map(x => (
    {
      x: stock_hist.filter(obj=>obj.Ticker==x).map(obj=>obj.Date),
      y: stock_hist.filter(obj=>obj.Ticker==x).map(obj=>obj.Close),
      name:x,
      type: 'scatter'
    }
  ))

  Plotly.newPlot('chart02', data2);

  console.log('Data2: ',data2);
};

init();

async function stockSel() {
  let selections = document.getElementById('selections');
  let start = document.getElementById('start');
  let end = document.getElementById('end');

  if (!selections.value || !start.value || !end.value) { return alert('Please fill all fields') };

  let stocks = JSON.stringify(document.getElementById('selections').value.split(','));

  await fetch(`/api/v1.0/load_data/${stocks}/${start.value}/${end.value}`);
  window.location.reload();
};

init();

