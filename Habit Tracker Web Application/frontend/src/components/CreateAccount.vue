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
                <div class="col-lg-5 d-none d-lg-block">
                  <img
                    src="../assets/create_account.jpg"
                    alt="Register Pic"
                    width="400"
                    height="650"
                    style="background-size: cover; background-position: center"
                  />
                </div>
                <div class="col-lg-7">
                  <div class="p-5">
                    <div class="text-center">
                      <h2 class="h4 text-gray-900 mb-4">Create an Account!</h2>
                    </div>
                    <!--- Success Message --->
                    <div class="row g-1">
                      <div
                        v-if="msg"
                        class="col-md-12 alert alert-success"
                        role="alert"
                      >
                        <br />
                        <h5 class="alert-heading">🎉 {{ msg }} 🎉</h5>
                      </div>
                    </div>
                    <!--- Form --->
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
                      <div class="form-group row">
                        <div class="col-sm-6 mb-3 mb-sm-0">
                          <input
                            type="text"
                            class="form-control form-control-user"
                            id="inputName"
                            v-model="name"
                            placeholder="Full Name"
                          />
                        </div>
                        <div class="col-sm-6">
                          <input
                            type="text"
                            class="form-control form-control-user"
                            id="inputEmail"
                            v-model="email"
                            placeholder="Email"
                          />
                        </div>
                      </div>
                      <div class="form-group row">
                        <div class="col-sm-6 mb-3 mb-sm-0">
                          <input
                            :type="seen ? 'text' : 'password'"
                            class="form-control form-control-user"
                            id="inputPassword"
                            v-model="password"
                            placeholder="Password"
                          />
                        </div>
                        <div class="col-sm-6">
                          <input
                            :type="seen ? 'text' : 'password'"
                            class="form-control form-control-user"
                            id="inputPassword2"
                            v-model="password2"
                            placeholder="Re-enter Password"
                          />
                        </div>
                        <small id="PasswordHelp" class="form-text text-muted"
                          >Password Should be at least 8 characters long</small
                        >
                      </div>
                      <div class="form-group row">
                        <div class="col-sm-6 mb-3 mb-sm-0">
                          <label for="inputAge" class="form-label text-gray-800"
                            >Age</label
                          >
                          <input
                            type="number"
                            min="0"
                            max="130"
                            class="form-control form-control-user"
                            id="inputAge"
                            v-model="age"
                          />
                        </div>
                        <div class="col-sm-6">
                          <label for="inputGender" class="form-label"
                            >Gender</label
                          >
                          <select
                            id="inputGender"
                            class="form-select h-50 w-100"
                            v-model="gender"
                          >
                            <option disabled>Choose Your Gender</option>
                            <option value="M">Male</option>
                            <option value="F">Female</option>
                          </select>
                        </div>
                      </div>
                      <div class="form-group">
                        <input
                          type="text"
                          v-model="backup"
                          class="form-control form-control-user"
                          id="inputBackup"
                          placeholder="Backup Code"
                        />
                        <small id="backupHelp" class="form-text text-muted"
                          >This will be used for resetting password in
                          future</small
                        >
                      </div>
                      <div class="form-group">
                        <div
                          class="form-check col-md-6 text-start"
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
                        Register Account
                      </button>
                      <hr />
                    </form>
                    <div class="text-center" style="font-size: large">
                      <router-link class="small" :to="{ name: 'Login' }"
                        >Already Have an Account? Login</router-link
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
  name: "CreateAccountView",
  data() {
    return {
      email: "",
      password: "",
      password2: "",
      name: "",
      age: 0,
      backup: "",
      gender: "",
      pass: true,
      errors: [],
      seen: false,
      msg: "",
    };
  },
  methods: {
    validate: function (e) {
      this.errors = [];
      if (!this.name.trim()) {
        this.errors.push("Please Enter Your Name");
      }
      if (!this.email.trim()) {
        this.errors.push("Please Enter Email");
      }
      if (!this.password.trim()) {
        this.errors.push("Please Enter Password");
      } else if (this.password.trim().length < 8) {
        this.errors.push("Password Should Be 8 Characters Long");
      }
      if (!this.password2.trim()) {
        this.errors.push("Please Confirm Your Password");
      }
      if (this.password !== this.password2) {
        this.errors.push("Password and confirm password do not match");
      }
      if (!this.age) {
        this.errors.push("Please Enter Age");
      } else if (this.age === 0) {
        this.errors.push("Please Enter Age");
      } else if (this.age > 130) {
        this.errors.push("Please Enter Valid Age");
      }
      if (!this.gender) {
        this.errors.push("Please Select Gender");
      }
      if (!this.backup.trim()) {
        this.errors.push("Please Enter Backup Code");
      } else if (this.backup.trim().length < 6) {
        this.errors.push("Backup Code Should Be At Least 6 characters");
      }
      if (!this.errors.length) {
        this.signUpMethod();
      }
      e.preventDefault();
    },
    toggleSeen: function () {
      this.seen = !this.seen;
    },
    signUpMethod: function () {
      this.pass = true;
      let user = {
        email: this.email,
        password: this.password,
        name: this.name,
        age: this.age,
        backup: this.backup,
        gender: this.gender,
      };
      fetch("http://127.0.0.1:8000/api/user", {
        method: "post",
        omit: "no-cors",
        credentials: "omit",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(user),
      })
        .then((response) => {
          if (response.status !== 201) {
            this.pass = false;
          }
          return response.json();
        })
        .then((data) => {
          if (this.pass) {
            this.msg = data["message"];
            setTimeout(this.divert, 3000);
          } else {
            this.errors = [];
            if (data["message"]) {
              this.errors.push(`'${this.email}' ${data["message"]}`);
            }
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    divert: function () {
      this.$router.push({ name: "Login" });
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
