<template>
  <div id="app">
<!--    <nav>-->
<!--  &lt;!&ndash;      <router-link v-if="!$store.getters.getstatus" :to="{ name: 'Home' }">&ndash;&gt;-->
<!--  &lt;!&ndash;        Home |&ndash;&gt;-->
<!--  &lt;!&ndash;      </router-link>&ndash;&gt;-->
<!--      <router-link :to="{ name: 'About' }">About |</router-link>-->
<!--      <router-link v-if="!$store.getters.getstatus" :to="{ name: 'Login' }">-->
<!--        Login |-->
<!--      </router-link>-->
<!--      <router-link-->
<!--        v-if="!$store.getters.getstatus"-->
<!--        :to="{ name: 'CreateAccount' }"-->
<!--      >-->
<!--        Sign Up |-->
<!--      </router-link>-->
<!--      <router-link v-if="$store.getters.getstatus" :to="{ name: 'Dashboard' }">-->
<!--        Dashboard |-->
<!--      </router-link>-->
<!--      <a v-if="$store.getters.getstatus" href="" @click="logOut"> Log Out | </a>-->
<!--      <router-link :to="{ name: 'Test' }">Test |</router-link>-->
<!--      <router-link :to="{ name: 'Security' }">Security </router-link>-->
<!--    </nav>-->
    <router-view />
  </div>
</template>

<script>
export default {
  name: "MainApp",
  methods: {
    // logOut: async function () {
    //   // let trackers_index = this.$store.getters.getChangedTrackers;
    //   // let trackers = this.$store.getters.getTrackers;
    //   // let token_id = this.$store.getters.getToken;
    //   // for (let index = 0; index < trackers_index.length; index++) {
    //   //   let tracker_index = trackers_index[index];
    //   //   await this.makeUpdate(trackers[tracker_index], token_id);
    //   // }
    //   // Separate
    //   await this.$router.push({ name: "Login" });
    //   await this.$store.dispatch("logout_user");
    //   sessionStorage.removeItem("token");
    //   sessionStorage.removeItem("user");
    // },
  },
  mounted() {
    if (sessionStorage.getItem("token")) {
      this.$store.dispatch("store_token", {
        token: sessionStorage.getItem("token"),
      });
    }
    if (sessionStorage.getItem("user")) {
      this.$store.dispatch("store_user", {
        user: JSON.parse(sessionStorage.getItem("user")),
      });
    }
  },
};
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
