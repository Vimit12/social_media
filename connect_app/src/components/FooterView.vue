<script>

</script>

<template>
  <footer class="footer">

    <div class="icons">

      <a href="#"><i class="fab fa-facebook"></i></a>
      <a href="#"><i class="fab fa-linkedin"></i></a>
      <a href="#"><i class="fab fa-instagram"></i></a>
      <a href="#"><i class="fab fa-twitter"></i></a>
      <p class="company-name">
        Vimit &copy; 2023, ALL Rights Reserved
      </p>

    </div>
  </footer>
</template>

<style scoped>
.footer{
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  /* height: 10%; */
  background: #f5f3f6;
  text-align: center;
  color: #f4f4f4;
}

.icons{
  padding-top: 1rem;
}

/* .icons a{
    text-decoration: none;
    font-size: 2rem;
    margin: 0.5rem;
    color: #f4f4f4;
} */

.company-name{
  color: rgb(39, 35, 35);
  font-size: 1 rem;
  /* margin-top: 0.1rem; */
}

@media (max-width: 500px){
  html{
    font-size: 50%;
  }
}

@media(min-width: 501px) and (max-width: 768px){
  html{
    font-size: 50%;
  }
}
</style>
