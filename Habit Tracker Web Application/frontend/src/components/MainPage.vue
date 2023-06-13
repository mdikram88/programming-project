<template>
  <div>
    <div class="row g-3">
      <div class="col-md-12">
        <div class="d-sm-flex align-items-center justify-content-between mb-4">
          <h1 class="h1 mb-0 text-gray-800">Dashboard</h1>
          <a
            :href="getTrackersCsv"
            class="d-none d-sm-inline-block btn btn-primary shadow-sm"
            id="AllTrackers"
            @click="sendAlert"
            download="All_Trackers.csv"
          >
            <i class="fas fa-download fa-sm text-white-50"></i>
            Generate Trackers Csv</a
          >
        </div>
      </div>
    </div>
    <div class="row g-3">
      <div class="col-md-12 text-start">
        <h5>Welcome {{ this.$store.getters.getUserName | toTitleCase }}</h5>
      </div>
      <br />
      <div class="col-md-3">
        <router-link
          :to="{ name: 'AddTracker' }"
          class="form-control btn btn-primary"
        >
          Add New Tracker
        </router-link>
      </div>
      <div class="col-md-4"></div>
      <div class="col-md-5 text-end">
        <form
          class="d-none d-sm-inline-block form-inline mr-auto ml-md-3 my-2 my-md-0 mw-100 navbar-search"
        >
          <div class="input-group">
            <input
              type="text"
              class="form-control bg-light border-2 small"
              placeholder="Search Tracker.."
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
      </div>
    </div>
    <div class="row g-3" v-if="!this.$store.getters.getTrackers.length">
      <br />&nbsp; <br />&nbsp; <br />&nbsp; <br />&nbsp;
      <h2>No Tracker Found</h2>
      <h3>Please Create New Trackers</h3>
    </div>
    <div class="row g-3" v-else>
      <div
        class="col-md-12"
        v-for="(tracker, index) in filteredTrackers"
        :key="index"
      >
        <br />

        <div class="card text-center border-success">
          <div class="card-header border-success">
            <b>Tracker Type:</b> {{ tracker["tracker_type"] }}
          </div>
          <div class="card-body border-success">
            <h4 class="card-title">
              {{ tracker["tracker_name"] | toTitleCase }}
            </h4>
            <p class="card-text">
              {{ tracker["description"] | toTitleCase }}
            </p>
            <router-link
              :to="{
                name: 'Charts',
                params: { id: tracker['tracker_id'] },
              }"
              class="btn btn-info"
              data-bs-toggle="tooltip"
              title="Show Charts"
            >
              <i class="bi bi-graph-up"></i>
              &nbsp;
              <span>Charts</span>
            </router-link>
            &nbsp;
            <router-link
              :to="{
                name: 'LogTable',
                params: { id: `${tracker['tracker_id']}` },
              }"
              class="btn btn-success"
              data-bs-toggle="tooltip"
              title="Show Log Table"
            >
              <i class="bi bi-table"></i>
              &nbsp;
              <span>Logs Table</span>
            </router-link>
            <br />
            <br />
            <div class="row gap-5">
              <div class="col-md-12 text-center">
                <router-link
                  :to="{
                    name: 'EditTracker',
                    params: { id: `${tracker['tracker_id']}` },
                  }"
                  class="btn btn-warning btn-circle"
                  data-bs-toggle="tooltip"
                  title="Edit Tracker"
                >
                  <i class="bi bi-pencil-square"></i>
                </router-link>
                &nbsp;
                <router-link
                  :to="{
                    name: 'AddLog',
                    params: { id: `${tracker['tracker_id']}` },
                  }"
                  class="btn btn-success btn-circle"
                  data-bs-toggle="tooltip"
                  title="Add New Log Entry"
                >
                  <i class="bi bi-plus-square"></i>
                </router-link>
                &nbsp;
                <button
                  class="btn btn-danger btn-circle"
                  @click="deleteTracker(tracker['tracker_id'])"
                  data-bs-toggle="tooltip"
                  title="Delete Tracker"
                >
                  <i class="bi bi-trash-fill"></i>
                </button>
              </div>
            </div>
          </div>
          <div class="card-footer text-muted border-success">
            <b>Last Visited:</b>
            {{ tracker["last_time"] | lastVisited }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MainPage.vue",
  data() {
    return {
      search: "",
    };
  },
  methods: {
    sendAlert: function () {
      alert("Tracker file ready to Download");
    },
    makeUpdate: function (tracker, token_id) {
      let pass = true;
      fetch(`http://127.0.0.1:8000/api/tracker/${tracker["tracker_id"]}`, {
        method: "put",
        omit: "cors",
        credentials: "omit",
        headers: {
          "Content-Type": "application/json",
          "Authorization-Token": token_id,
        },
        body: JSON.stringify(tracker),
      })
        .then((response) => {
          if (response.status !== 200) {
            pass = false;
          }
          return response.json();
        })
        .then((data) => {
          if (!pass) {
            console.log("Update Failed");
            console.log(data);
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    // eslint-disable-next-line no-unused-vars
    deleteTracker: function (t_id) {
      var resp = prompt(
        "Do You want to delete Tracker? 'Yes' or 'No'\n" +
          "Data will be lost permanently",
        "No"
      );

      if (resp && resp.toLowerCase() === "yes") {
        let token_id = this.$store.getters.getToken;
        fetch(`http://127.0.0.1:8000/api/tracker/${t_id}`, {
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
              this.$store.dispatch("deleteTracker", { id: t_id });
              alert("Tracker Deleted Successfully");
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
  computed: {
    getTrackersCsv: function () {
      let trackers = [];
      let headers = [
        "S.no",
        "Tracker Name",
        "Description",
        "Tracker Type",
        "Options",
        "Last Visited",
      ];
      let csv_Array = [];
      csv_Array.push(headers.join(","));
      trackers = this.$store.getters.getTrackers;
      if (trackers.length !== 0) {
        let data = trackers.map((tk, index) => ({
          "S.no": index + 1,
          "Tracker Name": tk["tracker_name"],
          Description: tk["description"],
          "Tracker Type": tk["tracker_type"],
          Setting: tk["setting"],
          "Last Visited": tk["last_time"],
        }));
        for (let index = 0; index < data.length; index++) {
          csv_Array.push(Object.values(data[index]).join(","));
        }
      }
      let csv = new Blob([csv_Array.join("\n")], { type: "text/csv" });
      return window.URL.createObjectURL(csv);
    },
    filteredTrackers: function () {
      return this.$store.getters.getTrackers.filter((tk) => {
        return tk["tracker_name"]
          .toLowerCase()
          .match(this.search.toLowerCase());
      });
    },
  },
  filters: {
    lastVisited: function (value) {
      let arr = [1000, 60, 60, 24, 7, 30, 365];
      let unit = ["second", "minute", "hour", "day", "week", "month"];
      let ind = 0;
      let current_time = new Date();
      let last_time = new Date(value);
      var time_diff = current_time - last_time;
      while (Math.floor(time_diff / arr[ind]) >= 1) {
        time_diff = Math.floor(time_diff / arr[ind]);
        ind++;
      }
      let lt = "";
      if (time_diff > 1) {
        lt = time_diff + " " + unit[ind - 1] + "s" + " ago";
      } else {
        lt = time_diff + " " + unit[ind - 1] + " ago";
      }
      return lt;
    },
  },
  mounted() {
    let trackers_index = this.$store.getters.getChangedTrackers;
    let trackers = this.$store.getters.getTrackers;
    let token_id = this.$store.getters.getToken;
    for (let index = 0; index < trackers_index.length; index++) {
      let tracker_index = trackers_index[index];
      this.makeUpdate(trackers[tracker_index], token_id);
    }
    this.$store.dispatch("resetChangedTracker");
  },
};
</script>

<style scoped></style>
