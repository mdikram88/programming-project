<template>
  <div>
    <div class="container">
      <div class="row g-3">
        <div class="col-md-12">
          <div
            class="d-sm-flex align-items-center justify-content-between mb-4"
          >
            <h1 class="h1 mb-0 text-gray-800">Add Log</h1>
          </div>
        </div>
      </div>
      <div class="row g-3">
        <div class="col-12">
          <h4 class="text-muted">For {{ tracker["tracker_name"] }}</h4>
          <br />
        </div>
      </div>
      <div class="row g-1">
        <div class="col-md-2"></div>
        <div v-if="msg" class="col-md-8 alert alert-success" role="alert">
          <br />
          <h3 class="alert-heading">🎉 {{ msg }} 🎉</h3>
        </div>
        <div class="col-md-2"></div>
      </div>
      <div class="row g-2">
        <div class="col-md-4"></div>
        <div class="col-md-4">
          <form class="row gy-3 text-start" @submit="validate" novalidate>
            <div v-if="errors.length" class="col-md-12">
              <br />
              <ul
                v-for="error in errors"
                :key="error"
                class="list-group list-group-flush"
              >
                <li class="list-group-item list-group-item-danger">
                  <span style="font-weight: bold; color: red">{{ error }}</span>
                </li>
              </ul>
            </div>
            <div class="col-md-12">
              <label for="RecordTime" class="form-label">
                <b>Record Time</b>
              </label>
              <input
                type="datetime-local"
                class="form-control"
                id="RecordTime"
                v-model="time"
                placeholder="Enter Date time"
              />
            </div>
            <div class="col-md-12" v-if="tk_type !== ''">
              <label for="Value" class="form-label">
                <b>Value</b>
              </label>
              <input
                :type="tk_type ? 'number' : 'time'"
                class="form-control"
                id="RecordTime"
                v-model="value"
                :placeholder="
                  tk_type ? 'Enter A Numerical Value' : 'Select Time Duration'
                "
              />
            </div>
            <div
              class="col-md-12"
              v-else-if="tracker['tracker_type'] === 'Multiple Choice'"
            >
              <label for="inputValue" class="form-label"><b>Value</b></label>
              <select
                id="inputValue"
                class="form-select h-50 w-100"
                v-model="value"
                aria-label="Default select example"
              >
                <option disabled>Choose An Option</option>
                <option
                  v-for="(opt, index) in tracker['setting'].split('-')"
                  :key="index"
                >
                  {{ opt }}
                </option>
              </select>
              <small class="text-muted">Select an Option</small>
            </div>
            <div class="col-md-12" v-else>
              <label for="inputValue" class="form-label"><b>Value</b></label>
              <select
                id="inputValue"
                class="form-select h-50 w-100"
                v-model="value"
              >
                <option disabled>Choose An Option</option>
                <option>Yes</option>
                <option>No</option>
              </select>
              <small class="text-muted">Select an Option</small>
            </div>
            <div class="col-md-12">
              <label for="inputNote" class="form-label"><b>Note</b></label>
              <input
                type="text"
                class="form-control"
                id="inputNote"
                v-model="note"
              />
            </div>
            <div class="col-md-12 text-center">
              <div class="col-md-6 btn-group">
                <button type="submit" class="btn btn-success">Add</button>
              </div>
              <div class="col-md-6 btn-group">
                <a class="btn btn-danger" @click="returnBack">Cancel</a>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      pass: true,
      msg: "",
      errors: [],
      id: "",
      time: "",
      tk_type: "",
      value: "",
      note: "",
      tracker: "",
    };
  },
  methods: {
    validate: function (e) {
      this.errors = [];
      if (!this.value) {
        this.errors.push("Please Enter Value");
      }
      if (!this.errors.length) {
        this.addLog();
      }
      e.preventDefault();
    },
    returnBack: function () {
      this.$router.push({ name: "MainPage" });
    },
    addLog: function () {
      let new_log = {
        time: this.time,
        value: this.value,
        note: this.note,
        tracker_id: this.id,
      };
      let token_id = this.$store.getters.getToken;
      fetch("http://127.0.0.1:8000/api/log", {
        method: "post",
        omit: "cors",
        credentials: "omit",
        headers: {
          "Content-Type": "application/json",
          "Authorization-Token": token_id,
        },
        body: JSON.stringify(new_log),
      })
        .then((response) => {
          if (response.status !== 201) {
            this.pass = false;
          }
          return response.json();
        })
        .then((data) => {
          if (this.pass) {
            this.msg = "Log Created Successfully";
            new_log = data;
            this.$store.dispatch("addLog", { nlog: new_log });
            setTimeout(this.divert, 3000);
          } else {
            this.errors = [];
            if (data["message"]) {
              this.errors.push(data["message"]);
            }
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    divert: function () {
      this.$router.push({ name: "MainPage" });
    },
  },
  mounted: function () {
    this.id = parseInt(this.$route.params.id);
    this.tracker = this.$store.getters.getTrackerById(this.id);
    let ct = new Date();
    this.time =
      ct.getFullYear() +
      "-" +
      (ct.getMonth() + 1).toLocaleString("en-US", {
        minimumIntegerDigits: 2,
        useGrouping: false,
      }) +
      "-" +
      ct.getDate().toLocaleString("en-US", {
        minimumIntegerDigits: 2,
        useGrouping: false,
      }) +
      "T" +
      ct.getHours().toLocaleString("en-US", {
        minimumIntegerDigits: 2,
        useGrouping: false,
      }) +
      ":" +
      ct.getMinutes().toLocaleString("en-US", {
        minimumIntegerDigits: 2,
        useGrouping: false,
      });
    if (this.tracker["tracker_type"] === "Numerical") {
      this.tk_type = true;
    } else if (this.tracker["tracker_type"] === "Time Duration") {
      this.tk_type = false;
      this.value = "00:00";
    }
  },
};
</script>
<style scoped>
h1 {
  font-weight: bold;
  font-size: xxx-large;
}
</style>
