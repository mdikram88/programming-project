<template>
  <div>
    <div id="wrapper">
      <!-- Main Content -->
      <div id="content">
        <!-- Begin Page Content -->
        <div class="container-fluid text-start">
          <!-- Page Heading -->
          <h1 class="h3 mb-2 text-dark-800" v-if="tracker['tracker_name']">
            {{ tracker["tracker_name"] | toTitleCase }} Charts
            <br />
          </h1>
          <p class="mb-2" v-if="tracker['tracker_type']">
            <b>Tracker Type :</b> {{ tracker["tracker_type"] }}
          </p>
          <div class="row g-3">
            <div class="col-md-12">
              <div
                class="d-sm-flex align-items-center justify-content-between mb-4"
              >
                <p class="mb-0">
                  <b>Description : </b> {{ tracker["description"] }}
                </p>
              </div>
            </div>
          </div>
          <div class="row text-center" v-if="tracker['logs'] === []">
            <div class="row g-5"></div>
            <h2 style="color: red">No Logs Found to show Charts</h2>
          </div>
          <!-- Content Row -->
          <div class="row" v-else>
            <!-- Bar Chart -->
            <div :class="num ? '' : 'col-xl-8 col-lg-7'">
              <div class="card shadow mb-4">
                <div class="card-header py-3">
                  <h6 class="m-0 font-weight-bold text-primary">Bar Chart</h6>
                </div>
                <div class="card-body">
                  <div class="chart-bar">
                    <canvas id="myBarChart"></canvas>
                  </div>
                  <hr />
                </div>
                <div class="card-footer">
                  <a id="download2" class="btn btn-primary">Download</a>
                </div>
              </div>
            </div>
            <!-- Donut Chart -->
            <div class="col-xl-4 col-lg-5" :style="'display :' + prop">
              <div class="card shadow mb-4">
                <!-- Card Header - Dropdown -->
                <div class="card-header py-3">
                  <h6 class="m-0 font-weight-bold text-primary">Donut Chart</h6>
                </div>
                <!-- Card Body -->
                <div class="card-body">
                  <div class="chart-pie pt-4">
                    <canvas id="myPieChart"></canvas>
                  </div>
                  <hr />
                </div>
                <!---Card Footer-->
                <div class="card-footer">
                  <a id="download1" class="btn btn-primary">Download</a>
                </div>
              </div>
            </div>
            <!-- Area Chart -->
            <div>
              <div class="card shadow mb-4" v-if="num === true">
                <div class="card-header py-3">
                  <h6 class="m-0 font-weight-bold text-primary">Area Chart</h6>
                </div>
                <div class="card-body">
                  <div class="chart-area">
                    <canvas id="myAreaChart"></canvas>
                  </div>
                  <hr />
                </div>
                <div class="card-footer">
                  <a id="download3" class="btn btn-primary">Download</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Chart from "chart.js/auto";

export default {
  name: "ChartsPage",
  data() {
    return {
      id: "",
      tracker: "",
      num: true,
      prop: "inline",
      logs: [],
    };
  },
  methods: {
    barChart: function () {
      var ctx = document.getElementById("myBarChart");
      let data = [];
      let tick_size = 15;
      let x_title = "Dates";
      let label = "Tracker Values";
      let y_title = "Value";
      if (
        this.tracker["tracker_type"] === "Multiple Choice" ||
        this.tracker["tracker_type"] === "Boolean"
      ) {
        data = this.getDataset1();
        tick_size = 20;
        x_title = "Options";
        y_title = "Total Count";
        label = "Option Count";
      } else {
        data = this.getDataset2();
      }
      var myBarChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: Object.keys(data),
          datasets: [
            {
              data: Object.values(data),
              barPercentage: 0.4,
              label: `${label}`,
              backgroundColor: [
                "rgb(20,200,138)",
                "rgb(51,94,190)",
                "rgb(215,17,17)",
                "rgb(233,192,9)",
                "rgba(255, 99, 132)",
                "rgba(54, 162, 235)",
                "rgba(255, 206, 86)",
                "rgba(75, 192, 192)",
                "rgba(153, 102, 255)",
                "rgba(255, 159, 64)",
              ],
              borderColor: "#4e73df",
            },
          ],
        },
        options: {
          animation: {
            onComplete: function () {
              let a = document.getElementById("download2");
              a.href = myBarChart.toBase64Image();
              a.download = "Bar Chart";
            },
          },
          maintainAspectRatio: false,
          layout: {
            padding: {
              left: 10,
              right: 25,
              top: 25,
              bottom: 0,
            },
          },
          scales: {
            x: {
              drawBorder: false,
              barPercentage: 0.4,
              title: {
                display: true,
                text: `${x_title}`,
                font: {
                  size: 20,
                  weight: "bold",
                },
              },
              ticks: {
                font: {
                  size: `${tick_size}`,
                  weight: "bold",
                },
              },
            },
            y: {
              title: {
                display: true,
                text: `${y_title}`,
                font: {
                  size: 20,
                  weight: "bold",
                },
              },
              ticks: {
                font: {
                  size: 13,
                  weight: "bold",
                },
                min: 0,
                max: 10,
                maxTicksLimit: 5,
                padding: 10,
                drawBorder: false,
              },
              gridLines: {
                color: "rgb(234, 236, 244)",
                zeroLineColor: "rgb(234, 236, 244)",
                drawBorder: false,
                borderDash: [2],
                zeroLineBorderDash: [2],
                display: false,
              },
            },
          },
          legend: {
            display: false,
          },
          tooltips: {
            titleMarginBottom: 10,
            titleFontColor: "#6e707e",
            titleFontSize: 14,
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            borderColor: "#dddfeb",
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            caretPadding: 10,
          },
        },
        plugins: [
          {
            id: "custom_canvas_background_color",
            beforeDraw: (chart) => {
              const ctx = chart.canvas.getContext("2d");
              ctx.save();
              ctx.globalCompositeOperation = "destination-over";
              ctx.fillStyle = "white";
              ctx.fillRect(0, 0, chart.canvas.width, chart.canvas.height);
              ctx.restore();
            },
          },
        ],
      });
      myBarChart;
    },
    pieChart: function () {
      var ctx = document.getElementById("myPieChart");
      ctx.style.backgroundColor = "rgba(255,255,255)";
      let data = this.getDataset1();
      var myPieChart = new Chart(ctx, {
        type: "doughnut",
        data: {
          labels: Object.keys(data),
          datasets: [
            {
              data: Object.values(data),
              backgroundColor: [
                "#4e73df",
                "#1cc88a",
                "#36b9cc",
                "rgba(255, 99, 132)",
                "rgba(54, 162, 235)",
                "rgba(255, 206, 86)",
                "rgba(75, 192, 192)",
                "rgba(153, 102, 255)",
                "rgba(255, 159, 64)",
              ],
              hoverBackgroundColor: ["#2e59d9", "#17a673", "#2c9faf"],
              hoverBorderColor: "rgba(234, 236, 244, 1)",
            },
          ],
        },
        options: {
          animation: {
            onComplete: function () {
              let a = document.getElementById("download1");
              a.href = myPieChart.toBase64Image();
              a.download = "DoughNut Chart";
            },
          },
          maintainAspectRatio: false,
          tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            borderColor: "#dddfeb",
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            caretPadding: 10,
          },
          legend: {
            display: true,
          },
          cutout: 85,
        },
        plugins: [
          {
            id: "custom_canvas_background_color",
            beforeDraw: (chart) => {
              const ctx = chart.canvas.getContext("2d");
              ctx.save();
              ctx.globalCompositeOperation = "destination-over";
              ctx.fillStyle = "white";
              ctx.fillRect(0, 0, chart.canvas.width, chart.canvas.height);
              ctx.restore();
            },
          },
        ],
      });
      myPieChart;
    },
    areaChart: function () {
      var ctx = document.getElementById("myAreaChart");
      let data = [];
      data = this.getDataset2();
      // Creating Charts
      var myLineChart = new Chart(ctx, {
        type: "line",
        data: {
          labels: Object.keys(data),
          datasets: [
            {
              label: "Tracker Value",
              lineTension: 0.3,
              backgroundColor: "rgba(78, 115, 223, 0.05)",
              borderColor: "rgba(78, 115, 223, 1)",
              pointRadius: 3,
              pointBackgroundColor: "rgba(78, 115, 223, 1)",
              pointBorderColor: "rgba(78, 115, 223, 1)",
              pointHoverRadius: 3,
              pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
              pointHoverBorderColor: "rgba(78, 115, 223, 1)",
              pointHitRadius: 10,
              pointBorderWidth: 2,
              data: Object.values(data),
            },
          ],
        },
        options: {
          animation: {
            onComplete: function () {
              let a = document.getElementById("download3");
              a.href = myLineChart.toBase64Image();
              a.download = "Line Chart";
            },
          },
          maintainAspectRatio: false,
          layout: {
            padding: {
              left: 10,
              right: 25,
              top: 25,
              bottom: 0,
            },
          },
          scales: {
            x: {
              title: {
                display: true,
                text: "Dates",
                font: {
                  size: 20,
                  weight: "bold",
                },
              },
              time: {
                unit: "date",
              },
              gridLines: {
                display: false,
                drawBorder: false,
              },
              ticks: {
                maxTicksLimit: 7,
                font: {
                  size: 15,
                },
              },
            },
            y: {
              title: {
                display: true,
                text: "Values",
                font: {
                  size: 20,
                  weight: "bold",
                },
              },
              beginAtZero: true,
              ticks: {
                maxTicksLimit: 5,
                padding: 10,
              },
              gridLines: {
                color: "rgb(234, 236, 244)",
                zeroLineColor: "rgb(234, 236, 244)",
                drawBorder: false,
                borderDash: [2],
                zeroLineBorderDash: [2],
              },
            },
          },
          legend: {
            display: false,
          },
          tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            titleMarginBottom: 10,
            titleFontColor: "#6e707e",
            titleFontSize: 14,
            borderColor: "#dddfeb",
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            intersect: false,
            mode: "index",
            caretPadding: 10,
          },
        },
        plugins: [
          {
            id: "custom_canvas_background_color",
            beforeDraw: (chart) => {
              const ctx = chart.canvas.getContext("2d");
              ctx.save();
              ctx.globalCompositeOperation = "destination-over";
              ctx.fillStyle = "white";
              ctx.fillRect(0, 0, chart.canvas.width, chart.canvas.height);
              ctx.restore();
            },
          },
        ],
      });
      myLineChart;
    },
    getDataset1: function () {
      let options = {};
      if (this.tracker["tracker_type"] === "Multiple Choice") {
        for (const opt of this.tracker["setting"].split("-")) {
          options[opt.trim()] = 0;
        }
      } else {
        options["Yes"] = 0;
        options["No"] = 0;
      }
      for (const log of this.logs.slice(-30)) {
        options[log["value"]]++;
      }
      return options;
    },
    getDataset2: function () {
      let data = {};
      let date = "";
      for (const log of this.logs.slice(-30)) {
        date = log["time"].slice(5, 10);
        data[date] = 0;
      }
      if (this.tracker["tracker_type"] === "Numerical") {
        for (const log of this.logs.slice(-30)) {
          date = log["time"].slice(5, 10);
          data[date] += parseInt(log["value"]);
        }
      } else {
        for (const log of this.logs.slice(-30)) {
          date = log["time"].slice(5, 10);
          let values = log["value"].split(":");
          data[date] += parseInt(values[0]) * 60 + parseInt(values[1]);
        }
      }
      return data;
    },
  },
  mounted: function () {
    this.id = parseInt(this.$route.params.id);
    this.tracker = this.$store.getters.getTrackerById(this.id);
    this.logs = this.tracker["logs"];
    if (this.logs.length === 0) {
      this.start = -1;
    }
    // SEPARATE Updating tracker last visit time
    this.tracker["last_time"] = new Date();
    this.$store.dispatch("updateTracker", {
      tracker_obj: this.tracker,
    });
    // Adding tracker index to later update it on logout
    if (!this.$store.getters.getChangedTrackers.includes(this.id)) {
      this.$store.dispatch("appendChangedTracker", { id: this.id });
    }
    if (
      this.tracker["tracker_type"] === "Multiple Choice" ||
      this.tracker["tracker_type"] === "Boolean"
    ) {
      this.num = false;
      this.pieChart();
    } else {
      this.prop = "none";
      this.areaChart();
    }
    this.barChart();
  },
};
</script>
<style scoped>
h1 {
  font-weight: bold;
  font-size: xx-large;
}
</style>
