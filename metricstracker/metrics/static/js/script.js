// Инициализация air-datepicker
$(function() {
    var startDate = new Date();
    var endDate = startDate.getDate();
    startDate.setDate(endDate - 6);
    endDate = new Date();
    $('.date-range').datepicker({
        language: 'en',
		range : true,
		todayButton: new Date(),
		clearButton: true,
		toggleSelected: true,
        maxDate : new Date(),
		multipleDates: true,
		multipleDatesSeparator: " - ",
        autoClose: true
    });

    $('.date-range').data('datepicker').selectDate([new Date(startDate), new Date(endDate)]);

    if (document.getElementById('ctrChart')) {
        updateCTR();
    } else if (document.getElementById('evpmChart')) {
        updateEvPM();
    } else {
        updateAggregation();
    }

});



function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// получение CSRF-токена
const csrfToken = getCookie('csrftoken');

let ctrChart = null;
let evpmChart = null;

function updateCTR() {
  const dateRange = $('.date-range').val();

  const [startDate, endDate] = dateRange.split(' - ');

  if (!startDate || !endDate) {
    alert("Выберите диапазон дат");
    return;
  }

  fetch('/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    },
    body: JSON.stringify({ startDate, endDate })
  })
  .then(response => response.json())
  .then(data => {
    buildChartCTR(data);
  })
  .catch(error => {
    console.error('Data update error:', error);
  });

}

function updateEvPM() {
  const dateRange = $('.date-range').val();

  const [startDate, endDate] = dateRange.split(' - ');

  if (!startDate || !endDate) {
    alert("Выберите диапазон дат");
    return;
  }

  const tag = $('#events-list').val();

  fetch('/evpm', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    },
    body: JSON.stringify({ startDate, endDate, tag })
  })
  .then(response => response.json())
  .then(data => {
        buildChartEvPM(data);
  })
  .catch(error => {
    console.error('Data update error:', error);
  });

}


function updateAggregation() {
  const dateRange = $('.date-range').val();

  const [startDate, endDate] = dateRange.split(' - ');

  if (!startDate || !endDate) {
    alert("Выберите диапазон дат");
    return;
  }

  const tag = $('#events-list').val();
  const aggregationType = $('#aggregation-list').val();

  fetch('/aggregation-tables', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    },
    body: JSON.stringify({ startDate, endDate, tag, aggregationType })
  })
  .then(response => response.json())
  .then(data => {
        buildTable(data);
  })
  .catch(error => {
    console.error('Data update error:', error);
  });

}


function displayResult(data) {
    // Вывод данных на страницу
    const resultContainer = document.getElementById('result-container');
    resultContainer.innerHTML = '<h2>Результаты:</h2>';
    console.log(data);
    // Пример вывода данных в виде списка
    const list = document.createElement('ul');
    for (const day in data) {
        const listItem = document.createElement('li');
        listItem.textContent = `${day}: ${data[day]}`;
        list.appendChild(listItem);
    }

    resultContainer.appendChild(list);
}


function buildChartCTR(data) {

    if (!ctrChart) {
        const ctx = document.getElementById('ctrChart');
        ctrChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: Object.keys(data),
          datasets: [{
            data: Object.values(data),
            lineTension: 0,
            backgroundColor: 'transparent',
            borderColor: '#007bff',
            borderWidth: 4,
            pointBackgroundColor: '#007bff'
          }]
        },
        options: {
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              boxPadding: 3
            }
          }
        }
      });
    } else {
      // Если график уже существует, обновляем его данные и отрисовываем
        ctrChart.data.labels = Object.keys(data);
        ctrChart.data.datasets[0].data = Object.values(data);
        ctrChart.update();  // Явное обновление графика
    }
}


function buildChartEvPM(data) {

    if (!evpmChart) {
        const ctx = document.getElementById('evpmChart');
        evpmChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: Object.keys(data),
          datasets: [{
            data: Object.values(data),
            lineTension: 0,
            backgroundColor: 'transparent',
            borderColor: '#007bff',
            borderWidth: 4,
            pointBackgroundColor: '#007bff'
          }]
        },
        options: {
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              boxPadding: 3
            }
          }
        }
      });
    } else {
      // Если график уже существует, обновляем его данные и отрисовываем
        evpmChart.data.labels = Object.keys(data);
        evpmChart.data.datasets[0].data = Object.values(data);
        evpmChart.update();  // Явное обновление графика
    }
}


function buildTable(data) {

    var titleContainer = document.getElementById('title-container');
    var headersRow = document.getElementById('table-headers');
    var tableBody = document.getElementById('table-body');
    titleContainer.innerHTML = '';
    headersRow.innerHTML = '';
    tableBody.innerHTML = '';

    if (!data || data.length === 0) {
        var title = document.createElement('h3');
        title.textContent = 'No data';
        titleContainer.appendChild(title);
    } else {
        var headers = Object.keys(data[0]);

   // Создаем заголовки таблицы
    headers.forEach(function (header) {
    var th = document.createElement('th');
        th.textContent = header;
        headersRow.appendChild(th);
    });

    // Создаем строки таблицы
    data.forEach(function (rowData) {
        var row = document.createElement('tr');
        headers.forEach(function (header) {
            var td = document.createElement('td');
            td.textContent = rowData[header];
            row.appendChild(td);
        });
        tableBody.appendChild(row);
    });
    }
}