<template>
  <div>
    <div class="container" v-if="!this.$store.getters.getstatus">
      <div class="row g-3">
        <div class="col-lg-12">
          <br />
          <h1 id="forbidden">Forbidden Zone</h1>
          <h2>Please Login</h2>
        </div>
      </div>
    </div>
    <!-------- Else ------------>
    <div id="wrapper" v-else>
      <!-- Sidebar -->
      <ul
        class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion"
        id="accordionSidebar"
      >
        <!-- Sidebar - Brand -->
        <a
          class="sidebar-brand d-flex align-items-center justify-content-center"
        >
          <div class="sidebar-brand-icon rotate-n-15">
            <i class="bi bi-alarm"></i>
          </div>
          <div class="sidebar-brand-text mx-3">Quantified Self</div>
        </a>

        <!-- Divider -->
        <hr class="sidebar-divider my-0" />

        <!-- Nav Item - Dashboard -->
        <li class="nav-item active">
          <router-link :to="{ name: 'MainPage' }"
            ><a class="nav-link">
              <i class="fas fa-fw fa-tachometer-alt"></i>
              <span>Dashboard</span></a
            ></router-link
          >
        </li>

        <!-- Divider -->
        <hr class="sidebar-divider" />

        <!-- Heading -->
        <div class="sidebar-heading">Interface</div>

        <!-- Nav Item - Pages Collapse Menu -->
        <li class="nav-item">
          <a class="nav-link collapsed" href="" @click="logOut">
            <i class="bi bi-box-arrow-left"></i>&nbsp;
            <span>Log Out</span>
          </a>
        </li>

        <!-- Divider -->
        <hr class="sidebar-divider" />
      </ul>
      <!-- Main Content -->
      <div id="content">
        <!---Top Bar--->
        <nav
          class="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow bg-gradient-primary"
        ></nav>
        <!-- End of Top bar -->

        <div class="container-fluid">
          <!-- Page Heading -->
          <router-view />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    logOut: async function () {
      // let trackers_index = this.$store.getters.getChangedTrackers;
      // let trackers = this.$store.getters.getTrackers;
      // let token_id = this.$store.getters.getToken;
      // for (let index = 0; index < trackers_index.length; index++) {
      //   let tracker_index = trackers_index[index];
      //   await this.makeUpdate(trackers[tracker_index], token_id);
      // }
      // Separate
      await this.$router.push({ name: "Login"});
      await this.$store.dispatch("logout_user");
      sessionStorage.removeItem("token");
      sessionStorage.removeItem("user");
    },
  },
};
</script>
<style scoped>
#forbidden {
  color: red;
}
h1 {
  font-weight: bolder;
  font-size: xxx-large;
}
</style>
