<template>
  <div>
    <div class="container">
      <div class="row g-3">
        <div class="col-md-12">
          <div
            class="d-sm-flex align-items-center justify-content-between mb-4"
          >
            <h1 class="h1 mb-0 text-gray-800">Edit Tracker</h1>
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
                  <span style="font-weight: bold; color: red">{{ error }}</span>
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
                v-model="tracker['tracker_name']"
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
                v-model="tracker['description']"
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
                v-model="tracker['tracker_type']"
              >
                <option disabled>Numerical</option>
                <option disabled>Multiple Choice</option>
                <option disabled>Boolean</option>
                <option disabled>Time Duration</option>
              </select>
            </div>
            <div class="col-md-12" v-if="tracker['setting']">
              <label for="Settings" class="form-label">
                <b>Options</b>
              </label>
              <input
                type="text"
                class="form-control"
                id="Settings"
                v-model="tracker['setting']"
                placeholder="Enter Options Seperated By Comma"
                disabled
              />
            </div>
            <div class="col-md-12 text-center">
              <div class="col-md-6 btn-group">
                <button type="submit" class="btn btn-success">Update</button>
              </div>
              <div class="col-md-6 btn-group">
                <a class="btn btn-danger" @click="returnBack">Cancel</a>
              </div>
            </div>
          </form>
        </div>
        <div class="col-md-4"></div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      msg: "",
      tracker: "",
      id: "",
      pass: true,
      errors: [],
    };
  },
  methods: {
    returnBack: function () {
      this.$router.push({ name: "MainPage" });
    },
    validate: function (e) {
      this.errors = [];
      if (!this.tracker["tracker_name"].trim()) {
        this.errors.push("Tracker Name cannot be Empty");
      }
      if (!this.tracker["description"].trim()) {
        this.errors.push("Description cannot be Empty");
      }
      if (!this.errors.length) {
        this.UpdateTracker();
      }
      e.preventDefault();
    },
    UpdateTracker: function () {
      this.errors = [];
      this.pass = true;
      let token_id = this.$store.getters.getToken;
      fetch(`http://127.0.0.1:8000/api/tracker/${this.tracker["tracker_id"]}`, {
        method: "put",
        omit: "cors",
        credentials: "omit",
        headers: {
          "Content-Type": "application/json",
          "Authorization-Token": token_id,
        },
        body: JSON.stringify(this.tracker),
      })
        .then((response) => {
          if (response.status !== 200) {
            this.pass = false;
          }
          return response.json();
        })
        .then((data) => {
          if (this.pass) {
            this.msg = data["message"];
            // console.log(this.tracker);
            this.$store.dispatch("updateTracker", {
              tracker_obj: this.tracker,
            });
            setTimeout(this.divert, 3000);
          } else {
            if (data["message"]) {
              this.errors.push(data["message"]);
            }
            console.log(data);
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
  },
};
</script>
<style scoped>
h1 {
  font-weight: bold;
  font-size: xxx-large;
}
</style>
