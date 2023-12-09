<!-- Home page which is the default view -->
<template>
  <div class="container">
    <div class="home">
      <div class="title">
        <h1>Suicide Predictor</h1>
      </div>
      <div class="content">
        <p>Our website tries to predict suicide rate on a country to country basis.</p>
        <p>User needs to upload an excel file with various feature values in the input page.</p>
        <p>This project aims to help health agencies across countries to predict suicide rates in order to bring new policies which can help in reducing suicides.</p>
      </div>
    </div>
    <div class="bottom-image-container">
        <img src="/images/hug.jpg" alt="Bottom Image">
      </div>
  </div>
</template>

<script>
</script>

<style scoped>


.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.home {
  text-align: center;
  flex-grow: 1;
  padding: 20px;
}

h1{
  font-size: 2.5rem;
}

.content p{
    font-size: 1.3rem;
}
.bottom-image-container {
  text-align: center;
  margin-top: 10px ;
}

.bottom-image-container img {
  width: 90%;
}

@media screen and (min-width: 1200px) {
  .home {
    max-width: 800px;
    margin: 0 auto;
  }

  .bottom-image-container img {
    max-width: 700px;
    margin: 0 auto;
  }
}

</style>
