<template>
  <div id="app">
    <b-navbar toggleable="md" type="dark" variant="info">

      <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

      <b-navbar-brand href="#">NavBar</b-navbar-brand>

      <b-collapse is-nav id="nav_collapse">

        <b-navbar-nav>
          <b-nav-item :to="'/'" exact>Home</b-nav-item>
          <span v-for="table in tables">
            <b-nav-item :to="'/tables/'+table">
              {{table}}
            </b-nav-item>
          </span>

        </b-navbar-nav>


      </b-collapse>
    </b-navbar>

    <router-view/>
  </div>
</template>

<script>
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

import config from './lib/config';


Vue.use(BootstrapVue);

export default {
  name: 'app',
  data() {
    return {
      tables: config.tables,
    };
  },
};
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
