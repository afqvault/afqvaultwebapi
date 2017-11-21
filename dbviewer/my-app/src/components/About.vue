<template>
  <div id="about">
    <h1> About </h1>

    <p class="lead text-muted">AFQ-Browser is developed by:</p>

    <ul class="nolist">
      <li> Jason </li>
      <li> Adam </li>
      <li> Josh </li>
      <li> Anisha </li>
      <li> Ariel </li>
    </ul>


  </div>

</template>

<style>
.nolist{
  list-style: none;
  padding:0;
}

</style>

<script>
export default {
  name: 'about',
  data() {
    return {
      count: 1,
    };
  },
};
</script>
