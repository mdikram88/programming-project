<template>
  <div>
    <div id="wrapper">
      <!-- Main Content -->
      <div id="content">
        <!-- Begin Page Content -->
        <div class="container-fluid text-start">
          <!-- Page Heading -->
          <h1 class="h3 mb-2 text-dark-800" v-if="tracker['tracker_name']">
            {{ tracker["tracker_name"] | toTitleCase }} Log Table
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
                <a
                  :href="getLogsCsv"
                  class="d-none d-sm-inline-block btn btn-primary shadow-sm"
                  id="AllTrackers"
                  download="Logs.csv"
                  @click="sendAlert"
                >
                  <i class="fas fa-download fa-sm text-white-50"></i>
                  Generate Logs Csv</a
                >
              </div>
            </div>
          </div>


          <div class="row text-center" v-if="tracker['logs'] === []">
            <div class="row g-5"></div>
            <h2 style="color: red">No Logs Found to show Table</h2>
          </div>
          <!-- DataTales Example -->
          <div class="card shadow mb-4" v-else>
            <div class="card-header py-3 text-start">
              <h5 class="m-0 font-weight-bold text-primary">Log Table</h5>
            </div>
            <div class="card-body">
              <table class="table">
                <tbody>
                  <tr>
                    <td style="width: 5%" class="text-start">
                      <b>Show Entries :</b>
                      <select class="form-select" v-model="entries">
                        <option value="10" selected>10</option>
                        <option value="25">25</option>
                        <option value="50">50</option>
                        <option value="100">100</option>
                      </select>
                    </td>
                    <td style="width: 20%"></td>
                    <td style="width: 10%" class="text-end">
                      <form
                        class="d-none d-sm-inline-block form-inline mr-auto ml-md-3 my-2 my-md-0 mw-100 navbar-search"
                      >
                        <div class="input-group">
                          <input
                            type="date"
                            class="form-control bg-light border-2 small"
                            placeholder="Search By Record Time"
                            aria-label="Search"
                            v-model="search"
                            aria-describedby="basic-addon2"
                          />
                          <div class="input-group-append">
                            <button class="btn btn-primary" type="button">
                              <i class="bi bi-search"></i>
                            </button>
                          </div>
                        </div>
                      </form>
                    </td>
                  </tr>
                </tbody>
              </table>
              <div class="row gap-2">
                <div class="table-responsive">
                  <table class="table table-bordered table-hover">
                    <thead class="text-dark">
                      <tr>
                        <th>S.no</th>
                        <th>Record Time</th>
                        <th>Value</th>
                        <th>Note</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tfoot class="text-dark">
                      <tr>
                        <th>S.no</th>
                        <th>Record Time</th>
                        <th>Value</th>
                        <th>Note</th>
                        <th>Actions</th>
                      </tr>
                    </tfoot>
                    <tbody>
                      <tr v-for="(log, index) in filteredLogs" :key="index">
                        <td style="width: 5%">{{ index + 1 }}</td>
                        <td>{{ log["time"] }}</td>
                        <td style="width: 20%">{{ log["value"] }}</td>
                        <td style="width: 40%">{{ log["note"] }}</td>
                        <td style="width: 15%" class="text-center">
                          <router-link
                            :to="{
                              name: 'EditLog',
                              params: {
                                tk_id: `${tracker['tracker_id']}`,
                                id: `${log['log_id']}`,
                              },
                            }"
                            class="btn btn-warning btn-circle"
                          >
                            <i class="bi bi-pencil-square"></i>
                          </router-link>
                          &nbsp;&nbsp;
                          <button
                            class="btn btn-danger btn-circle"
                            @click="deleteLog(log)"
                          >
                            <i class="bi bi-trash-fill"></i>
                          </button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <table class="table">
                  <tbody>
                    <tr>
                      <td>
                        Showing {{ start + 1 }} to
                        {{ Math.min(logs.length, start + step) }} out of
                        {{ logs.length }}
                      </td>
                      <td class="text-end">
                        <button @click="prevList" class="btn btn-primary">
                          Previous
                        </button>
                        &nbsp;
                        <button @click="nextList" class="btn btn-primary">
                          Next
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "LogTable",
  data() {
    return {
      id: "",
      pass: true,
      tracker: "",
      search: "",
      logs: [],
      step: 10,
      start: 0,
      entries: "10",
    };
  },
  methods: {
    sendAlert: function () {
      alert("Log File Ready to Download");
    },
    nextList: function () {
      if (this.start + this.step - 1 < this.logs.length) {
        this.start = this.start + this.step;
      }
    },
    prevList: function () {
      if (this.start >= 9) {
        this.start = this.start - this.step;
      }
    },
    deleteLog: function (obj) {
      var resp = prompt(
        "Do You want to delete Log? 'Yes' or 'No'\n" +
          "Data will be lost permanently",
        "No"
      );

      if (resp && resp.toLowerCase() === "yes") {
        let token_id = this.$store.getters.getToken;
        fetch(`http://127.0.0.1:8000/api/log/${obj["log_id"]}`, {
          method: "delete",
          omit: "cors",
          credentials: "omit",
          headers: {
            "Content-Type": "application/json",
            "Authorization-Token": token_id,
          },
        })
          .then((response) => {
            if (response.status === 200) {
              this.$store.dispatch("deleteLog", { log_obj: obj });
              let ind = this.logs.findIndex((object) => {
                return object.log_id === obj.log_id;
              });
              this.logs.splice(ind, 1);
              alert("Log Deleted Successfully");
            } else {
              throw new Error("Http Error : " + response.status);
            }
            response.json();
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        console.log("Denied");
      }
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
  },
  computed: {
    getLogsCsv: function () {
      let logs = this.tracker["logs"];
      let headers = ["S.no", "Record Time", "Value", "Note"];
      let csv_Array = [];
      csv_Array.push(headers.join(","));
      if (logs) {
        let data = logs.map((lg, index) => ({
          "S.no": index + 1,
          "Record Time": lg["time"],
          Value: lg["value"],
          Note: lg["note"],
        }));
        for (let index = 0; index < data.length; index++) {
          csv_Array.push(Object.values(data[index]).join(","));
        }
      }
      let csv = new Blob([csv_Array.join("\n")], { type: "text/csv" });
      return window.URL.createObjectURL(csv);
    },
    filteredLogs: function () {
      let arr = this.logs.filter((tk) => {
        return tk["time"].toLowerCase().match(this.search.toLowerCase());
      });
      return arr.slice(this.start, this.start + parseInt(this.entries));
    },
  },
  watch: {
    entries(nw) {
      this.step = parseInt(nw);
    },
  },
};
</script>
<style scoped>
h1 {
  font-weight: bold;
  font-size: xx-large;
}
</style>
