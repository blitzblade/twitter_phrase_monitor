function renderChart(data_set, labels = [], myChart_data) {
  myChart_data.data.datasets = data_set;
  myChart_data.data.labels = labels;
  myChart_data.update();
}
