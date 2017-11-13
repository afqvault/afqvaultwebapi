<template>
  <div id="tables">
  </div>
</template>

<style>
</style>

<script>
export default {
  name: 'Tables',
  data() {
    return {

    };
  },
  created() {
    this.fetchData();
  },
  watch: {
    $route: 'fetchData',
  },
  methods: {
    fetchData() {
      console.log(this.$route.params.id)
    },
  },
};
</script>
