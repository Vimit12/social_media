<template>
  <div class="home">
<!--    <img alt="Vue logo" src="../assets/logo.png">-->
    <Login />
    <Footer />
  </div>
</template>

<script>
// @ is an alias to /src
import Login from '@/components/LoginView.vue'
import Footer from '@/components/FooterView.vue'
export default {
  name: 'LoginView',
  components: {
    Login,
    Footer
  }
}
</script>

<style>

body {

  background: rgb(225,232,118);
  background: radial-gradient(circle, rgba(225,232,118,1) 0%, rgba(255,213,186,1) 100%);
}

</style>