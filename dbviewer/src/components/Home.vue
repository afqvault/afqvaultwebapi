<template>
  <div class="home">
    <div v-for="table in tables">
      <h1>{{table}}</h1>
    </div>
  </div>
</template>

<script>

import axios from 'axios';
import config from '../lib/config';

export default {
  name: 'Home',
  data() {
    return {
      msg: 'Welcome to Your Vue.js App',
      tables: config.tables,
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
