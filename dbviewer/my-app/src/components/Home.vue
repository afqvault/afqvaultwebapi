<template>
  <div class="home">

  <div class="container-fluid">
    <div class="jumbotron">
      <div class="container">
        <h1 class="jumbotron-heading">AFQ Vault</h1>
        <p class="lead text-muted text-center"> A vault for AFQ-Browser results
          <br><br>
          <b-button variant="primary" style="color:white;" to="/tables/projects"> View Projects </b-button>
        </p>

      </div>
    </div>



  </div>


  </div>


</template>

<script>


export default {
  name: 'Home',
  data() {
    return {
      msg: 'Welcome to your Vue app boilerplate',
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
.home {
  text-align: left;
}

.home h1,h2,h3,h4{
  text-align: center;
}

.home h4 {
  color: gray;
}

.jumbotron {
    padding-top: 6rem;
    padding-bottom: 6rem;
    margin-bottom: 0;
    background-color: #fff;
}

.text-center {
    text-align: center!important;
}

.jumbotron-heading{
    margin-bottom: 20px;
    padding-bottom: 9px;
    border-bottom-style: solid;
    border-bottom: 1px solid #eee;
}

</style>
