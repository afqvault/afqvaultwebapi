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
        <b-pagination
        size="md"
        :total-rows="meta.total"
        v-model="meta.page"
        :per-page="meta.max_results"
        v-on:change="fetchData"
        align="end">
        </b-pagination>
        <b-table striped hover :items="data" :fields="get_fields" responsive="lg">
          <template slot="show_details" scope="row">
            <b-form-checkbox v-model="row.item._showDetails"></b-form-checkbox>
          </template>
          <template slot="delete" scope="row">
            <b-button variant="danger" :disabled="!userInfo.isAdmin" @click="do_delete(row.item)">x</b-button>
          </template>
          <template slot="url" scope="row">
            <a :href="row.item.url">{{row.item.url}}</a>
          </template>
          <template slot="row-details" scope="row">
            <b-card>
              <b-row class="mb-2" v-for="field in get_dict_fields">
                <b-col sm="3" class="text-sm-right"><b>{{field.key}}</b></b-col>
                <b-col>{{ row.item[field.key] }}</b-col>
              </b-row>
            </b-card>
          </template>
        </b-table>
      </div>
    </div>
  </div>
</template>

<style>
</style>

<script>
/* eslint no-underscore-dangle: ["error", { "allow": ["_items", "_meta", "_id",
                                                "_links", "_showDetails"] }] */

import axios from 'axios';
import config from '../config';

const urljoin = require('url-join');

export default {
  name: 'Tables',
  data() {
    return {
      data: null,
      meta: { total: 1, page: 1, max_results: 1 },
      links: null,
      schema: {},
      title: null,
      currentPage: null,
    };
  },
  props: ['userInfo', 'isAuthenticated'],
  computed: {
    get_fields() {
      const fields = [];
      const keys = Object.keys(this.schema);
      for (let i = 0; i < keys.length; i += 1) {
        const key = keys[i];
        if ((this.schema[key].type === 'string') || (this.schema[key].type === 'button')) {
          const entry = { key, sortable: true };
          fields.push(entry);
        }
      }
      fields.push({ key: 'show_details' });
      return fields;
    },
    get_dict_fields() {
      const fields = [];
      const keys = Object.keys(this.schema);
      for (let i = 0; i < keys.length; i += 1) {
        const key = keys[i];
        if (this.schema[key].type === 'dict') {
          const entry = { key, sortable: true };
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

      url = page ? `${url}/?page=${page}` : url;
      axios.get(url, { _: Math.random() }).then((data) => {
        data.data._items.forEach((val, idx, arr) => {
          const a = arr;
          a[idx]._showDetails = false;
        });
        self.data = data.data._items;
        self.meta = data.data._meta;
        self.links = data.data._links;
        self.schema = config[tableName];
        self.title = this.$route.params.id;
      });
    },
    do_delete(item) {
      console.log('item to delete is', item);
      axios.get(`${config.delete_url}${item._id}`, { _: Math.random() }).then((resp) => {
        console.log(resp);
        this.fetchData();
      }).catch((e) => {
        console.log('error is', e);
      });
    },
  },
};
</script>
