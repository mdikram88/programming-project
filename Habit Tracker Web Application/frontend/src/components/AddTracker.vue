<template>
  <div>
    <div>
      <div class="container">
        <div class="row g-3">
          <div class="col-md-12">
            <div
              class="d-sm-flex align-items-center justify-content-between mb-4"
            >
              <h1 class="h1 mb-0 text-gray-800">Create Tracker</h1>
            </div>
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
                    <span style="font-weight: bold; color: red">{{
                      error
                    }}</span>
                  </li>
                </ul>
              </div>
              <div class="col-md-12">
                <label for="TrackerName" class="form-label">
                  <b>Tracker Name</b>
                </label>
                <input
                  type="text"
                  class="form-control"
                  id="TrackerName"
                  v-model="tracker_name"
                  placeholder="Enter Tracker Name"
                />
              </div>
              <div class="col-md-12">
                <label for="Description" class="form-label">
                  <b>Description</b>
                </label>
                <input
                  type="text"
                  class="form-control text-dark"
                  id="Description"
                  v-model="description"
                  placeholder="Description"
                />
              </div>
              <div class="col-md-12">
                <label for="TrackerType" class="form-label">
                  <b>Tracker Type</b>
                </label>
                <select
                  id="TrackerType"
                  class="form-select h-50 w-100"
                  v-model="tracker_type"
                >
                  <option>Numerical</option>
                  <option>Multiple Choice</option>
                  <option>Boolean</option>
                  <option>Time Duration</option>
                </select>
              </div>
              <div class="col-md-12" v-if="tracker_type === 'Multiple Choice'">
                <label for="Settings" class="form-label">
                  <b>Options</b>
                </label>
                <input
                  type="text"
                  class="form-control"
                  id="Settings"
                  v-model="setting"
                  placeholder="Enter Options Seperated By Hyphen '-'"
                /><small id="Settings" class="form-text text-muted"
                  >Options Should be hyphen '-' separate</small
                >
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
  </div>
</template>

<script>
export default {
  data() {
    return {
      tracker_name: "",
      description: "",
      tracker_type: "",
      setting: "",
      user_id: "",
      last_time: "",
      pass: false,
      errors: [],
      msg: "",
    };
  },
  methods: {
    validate: function (e) {
      this.errors = [];
      if (!this.tracker_name.trim()) {
        this.errors.push("Please fill Tracker Name");
      }
      if (!this.description.trim()) {
        this.errors.push("Please fill Description");
      }
      if (!this.tracker_type.trim()) {
        this.errors.push("Please Select Tracker Type");
      }
      if (this.tracker_type === "Multiple Choice") {
        if (this.setting.split("-").length < 2) {
          this.errors.push("At least give two hyphen separated options");
        } else {
          let index = 0;
          let array = this.setting.split("-");
          while (index < array.length) {
            if (array[index].trim() === "") {
              this.errors.push("There is Empty option in Options");
              break;
            }
            index++;
          }
        }
      }

      if (!this.errors.length) {
        this.addTracker();
      }

      e.preventDefault();
    },
    returnBack: function () {
      this.$router.push({ name: "MainPage" });
    },
    addTracker: function () {
      this.pass = true;
      let token_id = this.$store.getters.getToken;
      let new_tracker = {
        tracker_name: this.tracker_name,
        description: this.description,
        tracker_type: this.tracker_type,
        setting: this.setting,
        user_id: this.$store.getters.getuser["user_id"],
        last_time: new Date(),
      };
      if (new_tracker["tracker_type"] === "Boolean") {
        new_tracker["setting"] = "Yes-No";
      }
      fetch("http://127.0.0.1:8000/api/tracker", {
        method: "post",
        omit: "cors",
        credentials: "omit",
        headers: {
          "Content-Type": "application/json",
          "Authorization-Token": token_id,
        },
        body: JSON.stringify(new_tracker),
      })
        .then((response) => {
          if (response.status !== 201) {
            this.pass = false;
          }
          return response.json();
        })
        .then((data) => {
          if (this.pass) {
            this.msg = "Tracker Created Successfully";
            new_tracker = data;
            new_tracker["logs"] = [];
            this.$store.dispatch("addTracker", { tracker: new_tracker });
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
};
</script>
<style scoped>
h1 {
  font-weight: bold;
  font-size: xxx-large;
}
</style>
