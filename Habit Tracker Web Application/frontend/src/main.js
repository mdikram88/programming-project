import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import "../theme-css/sb-admin-2.min.css";
import "chart.js/dist/chart";
//import "@fortawesome/fontawesome-free/js/all.js";

Vue.config.productionTip = false;

Vue.filter("toTitleCase", function (value) {
  return value.replace(/\w\S*/g, function (txt) {
    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
  });
});

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
