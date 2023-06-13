<template>
  <div class="bg-gradient-primary">
    <div class="container">
      <!-- Outer Row -->
      <div class="row justify-content-center">
        <div class="col-xl-10 col-lg-12 col-md-9">
          <div class="card o-hidden border-0 shadow-lg my-5">
            <div class="card-body p-0">
              <!-- Nested Row within Card Body -->
              <div class="row text-center">
                <div class="col-lg-6 d-none d-lg-block text-center">
                  <img
                    src="../assets/login_pic.jpg"
                    alt="Login Pic"
                    width="450"
                    height="550"
                    style="background-size: cover; background-position: center"
                  />
                </div>
                <div class="col-lg-6">
                  <div class="p-5">
                    <div class="text-center">
                      <h2 class="h4 text-gray-900 mb-4">Welcome Back!</h2>
                    </div>
                    <form class="user" @submit="validate" novalidate>
                      <div v-if="errors.length" class="col-md-12">
                        <br />
                        <ul
                          v-for="error in errors"
                          :key="error"
                          class="list-group list-group-flush"
                        >
                          <li class="list-group-item list-group-item-danger">
                            <span style="font-weight: bold; color: red">
                              {{ error }}
                            </span>
                          </li>
                        </ul>
                        <hr />
                      </div>
                      <div class="form-group">
                        <input
                          type="text"
                          class="form-control form-control-user"
                          v-model="email"
                          id="inputEmail"
                          aria-describedby="EmailHelp"
                          placeholder="Enter Email"
                        />
                      </div>
                      <div class="form-group">
                        <input
                          :type="seen ? 'text' : 'password'"
                          v-model="password"
                          class="form-control form-control-user"
                          id="inputPassword"
                          placeholder="Password"
                        />
                        <small id="EmailHelp" class="form-text text-muted"
                          >We'll never share your data with anyone else.</small
                        >
                      </div>
                      <div class="form-group">
                        <div
                          class="form-check col-md-6"
                          @click="toggleSeen"
                          style="padding-left: 30px"
                        >
                          <input
                            type="checkbox"
                            class="form-check-input"
                            id="Seen"
                          />
                          <label id="check" class="form-check-label" for="Seen"
                            >Show Password</label
                          >
                        </div>
                      </div>
                      <button
                        type="submit"
                        class="btn btn-primary btn-user btn-block"
                      >
                        Login
                      </button>
                      <hr />
                    </form>
                    <div class="text-center" style="font-size: large">
                      <router-link class="small" :to="{ name: 'ResetPassword' }"
                        >Forgot Password?</router-link
                      >
                    </div>
                    <div class="text-center" style="font-size: large">
                      <router-link class="small" :to="{ name: 'CreateAccount' }"
                        >Create an Account!</router-link
                      >
                    </div>
                  </div>
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
export default {
  name: "LoginView",
  data() {
    return {
      email: "",
      password: "",
      pass: true,
      errors: [],
      seen: false,
    };
  },
  methods: {
    toggleSeen: function () {
      this.seen = !this.seen;
    },
    validate: function (e) {
      this.errors = [];
      if (!this.email.trim()) {
        this.errors.push("Please Enter Email");
      }
      if (!this.password.trim()) {
        this.errors.push("Please Enter Password");
      } else if (this.password.trim().length < 8) {
        this.errors.push("Password Should be at least 8 characters");
      }
      if (!this.errors.length) {
        this.loginMethod();
      }
      e.preventDefault();
    },
    loginMethod: function () {
      this.pass = true;
      let user = { email: this.email, password: this.password };
      fetch("http://127.0.0.1:8000/login", {
        method: "post",
        omit: "cors",
        credentials: "omit",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(user),
      })
        .then((response) => {
          if (response.status !== 200) {
            this.pass = false;
          }
          for (const pair of response.headers.entries()) {
            if (pair[0] === "authorization-token") {
              sessionStorage.setItem("token", pair[1]);
              this.$store.dispatch("store_token", { token: pair[1] });
            }
          }
          return response.json();
        })
        .then((data) => {
          if (this.pass) {
            this.$store.dispatch("store_user", { user: data });
            sessionStorage.setItem("user", JSON.stringify(data));
            this.$router.push({ name: "MainPage" });
          } else {
            console.log(data);
            this.errors = [];
            this.errors.push(data["message"]);
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>
<style scoped>
h1 {
  font-weight: bolder;
  font-size: xxx-large;
}
a {
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
</style>
