import Vue from "vue";
import VueRouter from "vue-router";
import LoginView from "../components/LoginView.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../components/AboutView.vue"),
  },
  {
    path: "/",
    name: "Login",
    component: LoginView,
    // import(/* webpackChunkName: "Login" */ "../views/LoginView"),
  },
  {
    path: "/CreateAccount",
    name: "CreateAccount",
    component: () =>
      import(/* webpackChunkName: "CreateAccount" */ "../components/CreateAccount"),
  },
  {
    path: "/dashboard",
    component: () =>
      import(/* webpackChunkName: "Dashboard" */ "../views/DashboardView"),
    children: [
      {
        path: "",
        name: "MainPage",
        component: () =>
          import(/* webpackChunkName: "MainPage" */ "../components/MainPage"),
      },
      {
        path: "/editTracker/:id",
        name: "EditTracker",
        component: () =>
          import(/* webpackChunkName: "EditTracker" */ "../components/EditTracker"),
      },
      {
        path: "/addTracker",
        name: "AddTracker",
        component: () =>
          import(/* webpackChunkName: "AddTracker" */ "../components/AddTracker"),
      },
      {
        path: "/logTable/:id",
        name: "LogTable",
        component: () =>
          import(/* webpackChunkName: "LogTable" */ "../components/LogTable"),
      },
      {
        path: "/addLog/:id",
        name: "AddLog",
        component: () =>
          import(/* webpackChunkName: "AddLog" */ "../components/AddLog"),
      },
      {
        path: "/editLog/:tk_id/:id",
        name: "EditLog",
        component: () =>
          import(/* webpackChunkName: "EditLog" */ "../components/EditLog"),
      },
      {
        path: "/charts/:id",
        name: "Charts",
        component: () =>
          import(/* webpackChunkName: "Charts" */ "../components/ChartsView"),
      },
    ],
  },
  {
    path: "/reset",
    name: "ResetPassword",
    component: () =>
      import(/* webpackChunkName: "ResetPassword" */ "../components/ResetPassword"),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
