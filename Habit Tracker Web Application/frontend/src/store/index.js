import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    user: Object,
    has_user: false,
    token: "",
    changed_trackers: [],
  },
  getters: {
    getChangedTrackers(state) {
      return state.changed_trackers;
    },
    getToken(state) {
      return state.token;
    },
    getstatus(state) {
      return state.has_user;
    },
    getuser(state) {
      return state.user;
    },
    getUserName(state) {
      let n = state.user["name"].split(" ");
      if (n.length > 1) {
        return n[0] + " " + n[1];
      }
      return n[0];
    },
    getTrackers(state) {
      return state.user["trackers"];
    },
    getTrackerIndex: (state) => (id) => {
      return state.user["trackers"].findIndex((object) => {
        return object.tracker_id === id;
      });
    },
    getTrackerById: (state, getters) => (id) => {
      const ind = getters.getTrackerIndex(id);
      return JSON.parse(JSON.stringify(state.user["trackers"][ind]));
    },
    getLogs: (state, getters) => (tk_id) => {
      const tk_index = getters.getTrackerIndex(tk_id);
      return state.user["trackers"][tk_index]["logs"];
    },
    getLogIndex: (state, getters) => (tk_id, id) => {
      const ind = getters.getTrackerIndex(tk_id);
      return state.user["trackers"][ind]["logs"].findIndex((object) => {
        return object.log_id === id;
      });
    },
    getLogById: (state, getters) => (tk_id, id) => {
      const lg_ind = getters.getLogIndex(tk_id, id);
      const tk_ind = getters.getTrackerIndex(tk_id);
      return JSON.parse(
        JSON.stringify(state.user["trackers"][tk_ind]["logs"][lg_ind])
      );
    },
  },
  mutations: {
    appendChangedTracker(state, id) {
      const index = state.user["trackers"].findIndex((object) => {
        return object.tracker_id === id;
      });
      // console.log(index);
      state.changed_trackers.push(index);
    },
    resetChangedTracker(state) {
      state.changed_trackers = [];
    },
    user_id_increment(state, n) {
      state.user["user_id"] += n;
    },
    store_user(state, obj) {
      state.user = obj;
    },
    changeStatus(state) {
      state.has_user = !state.has_user;
    },
    store_token(state, tk) {
      state.token = tk;
    },
    reset_user(state) {
      state.user = Object;
      state.has_user = false;
      state.token = "";
    },
    deleteTracker(state, id) {
      const index = state.user["trackers"].findIndex((object) => {
        return object.tracker_id === id;
      });
      state.user["trackers"].splice(index, 1);
      sessionStorage.setItem("user", JSON.stringify(state.user));
    },
    updateTracker(state, tracker_obj) {
      const index = state.user["trackers"].findIndex((object) => {
        return object.tracker_id === tracker_obj.tracker_id;
      });
      state.user["trackers"][index] = tracker_obj;
      sessionStorage.setItem("user", JSON.stringify(state.user));
    },
    addTracker(state, tracker_obj) {
      state.user["trackers"].push(tracker_obj);
      sessionStorage.setItem("user", JSON.stringify(state.user));
    },
    addLog(state, log_obj) {
      const tk_index = state.user["trackers"].findIndex((object) => {
        return object.tracker_id === log_obj.tracker_id;
      });
      state.user["trackers"][tk_index]["logs"].push(log_obj);
      sessionStorage.setItem("user", JSON.stringify(state.user));
    },
    updateLog(state, log_obj) {
      const tk_index = state.user["trackers"].findIndex((object) => {
        return object.tracker_id === log_obj.tracker_id;
      });
      const lg_index = state.user["trackers"][tk_index]["logs"].findIndex(
        (obj) => {
          return obj.log_id === log_obj.log_id;
        }
      );
      state.user["trackers"][tk_index]["logs"][lg_index] = log_obj;
    },
    deleteLog(state, log_obj) {
      const tk_index = state.user["trackers"].findIndex((object) => {
        return object.tracker_id === log_obj.tracker_id;
      });
      const lg_index = state.user["trackers"][tk_index]["logs"].findIndex(
        (obj) => {
          return obj.log_id === log_obj.log_id;
        }
      );
      state.user["trackers"][tk_index]["logs"].splice(lg_index, 1);
      sessionStorage.setItem("user", JSON.stringify(state.user));
    },
  },
  actions: {
    appendChangedTracker(context, payload) {
      context.commit("appendChangedTracker", payload.id);
    },
    user_id_increment(context, payload) {
      context.commit("user_id_increment", payload.amount);
    },
    store_user(context, payload) {
      context.commit("store_user", payload.user);
      context.commit("changeStatus");
    },
    store_token(context, payload) {
      context.commit("store_token", payload.token);
    },
    logout_user(context) {
      context.commit("reset_user");
    },
    deleteTracker(context, payload) {
      context.commit("deleteTracker", payload.id);
    },
    updateTracker(context, payload) {
      context.commit("updateTracker", payload.tracker_obj);
    },
    addTracker(context, payload) {
      context.commit("addTracker", payload.tracker);
    },
    addLog(context, payload) {
      context.commit("addLog", payload.nlog);
    },
    updateLog(context, payload) {
      context.commit("updateLog", payload.updatedLog);
    },
    deleteLog(context, payload) {
      context.commit("deleteLog", payload.log_obj);
    },
    resetChangedTracker(context) {
      context.commit("resetChangedTracker");
    },
  },
  modules: {},
});
