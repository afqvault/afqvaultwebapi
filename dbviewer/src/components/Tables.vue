<template>
  <div id="tables">
    <h1> {{title}} </h1>

    <!--<div v-for="d in data">
      <span v-for="(item, key, index) in schema">
        {{key}} : {{d[key]}}
      </span>
    </div>-->
    <div class="container">
      <div class="row">
        <b-table striped hover :items="data" :fields="get_fields"></b-table>
        <b-pagination
        size="md"
        :total-rows="meta.total"
        v-model="meta.page"
        :per-page="meta.max_results"
        v-on:change="fetchData">
        </b-pagination>
      </div>
    </div>
  </div>
</template>

<style>
</style>

<script>
import axios from 'axios';
import config from '../lib/config';

const urljoin = require('url-join');

export default {
  name: 'Tables',
  data() {
    return {
      data: null,
      meta: {total:1, page:1, max_results:1},
      links: null,
      schema: null,
      title: null,
      currentPage: null,
    };
  },
  computed: {
    get_fields() {
      let fields = [];
      for (const key in this.schema){
        if (this.schema[key].type == "string"){
          const entry = {key: key, sortable: true}
          fields.push(entry);
        }
      }
      return fields;
    },
  },
  created() {
    this.fetchData();
  },
  watch: {
    $route: 'fetchData',
  },
  methods: {
    fetchData(page) {
      const tableName = this.$route.params.id;
      const self = this;
      let url = urljoin(config.url, tableName);
      url = page ? url+'?page='+page : url;
      console.log('url is', url)
      axios.get(url).then((data) => {
        self.data = data.data._items;
        self.meta = data.data._meta;
        self.links = data.data._links;
        self.schema = config[tableName];
        console.log("data is", data.data)
        self.title = this.$route.params.id;
      });
    },
  },
};
</script>
