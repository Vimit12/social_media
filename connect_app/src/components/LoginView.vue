<template>
<!--  <v-card>-->
      <v-sheet width="450" class="mx-auto" style="padding: 3em;margin-top: 5em;" border>
        <v-card text="Login"  color="black" style="margin-bottom: 1em;"></v-card>
        <v-form ref="form" >
          <v-text-field v-model="username" label="username" required></v-text-field>
<!--          <v-text-field v-model="password" label="Password" type="password" :counter="10" required></v-text-field>-->
          <v-text-field
              v-model="password"
              :rules="[passwordRule]"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showPassword ? 'text' : 'password'"
              @click:append="showPassword = !showPassword"
              label="Password"
          ></v-text-field>
<!--          <v-checkbox label="Remember me?" color="success" value=true></v-checkbox>-->
          <v-checkbox label="Remember me?" color="success" v-model="checkbox"></v-checkbox>
          <div class="d-flex flex-column">
            <v-row>
              <v-col>
                <v-btn color="green" class="mt-6" block @click="loginForm" :disabled="isDisabled">Success</v-btn>
              </v-col>
              <v-col>
                <v-btn color="red" class="mt-6" block @click="resetForm">Reset</v-btn>
              </v-col>
            </v-row>
            <v-row>
              <v-col align-self="center">
                <router-link to="/register">
                  <a>Register</a>
                </router-link>

              </v-col>
              <v-col align-self="center">
                <router-link to="/about">
                  <a>Forgot Password?</a>
                </router-link>
              </v-col>
            </v-row>
          </div>
        </v-form>
      </v-sheet>

<!--  </v-card>-->
</template>

<script>
/* eslint-disable */
import axios from 'axios';
import {createToast} from "mosha-vue-toastify";
export default {
  name: 'LoginView',
  props: {
    // msg: String
  },
  components: {
    // Footer
  },
  data() {
    return {
      username: "",
      password: "",
      showPassword: false,
      isDisabled: true,
      passwordRule: (value) => {
        if (!value) return 'Password is required';
        if (value.length < 8) return 'Password must be at least 8 characters long';
        if (!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?#&])[A-Za-z\d@$!%#*?&]+$/.test(value))
          return 'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character';
        this.isDisabled = false;
        return true;
      },
      checkbox:false
    }
  },
  watch: {
    checkbox:function (val){
      if (val){
        let data = {
          username: this.username, password: this.password, checked: this.checkbox
        }
        localStorage.setItem('loginDetail', JSON.stringify(data));
        localStorage.removeItem('loginUser');
      } else{
        // localStorage.removeItem('loginDetail');
        // this.resetForm();
      }
    },
  },
  methods: {
    loginForm() {
      if ((!this.username) || (!this.password)){
        createToast(this.username ? "Please enter password." : "please enter username.",
            {
              showIcon: 'true',
              hideProgressBar: 'false',
              type: 'warning',
              showCloseButton: 'true',
              transition: 'slide',
              position: 'bottom-center',
            })
        return
      }
      //defining userBody schema for passing it to API
      this.userBody = {
        "username": this.username,
        "password": this.password
      }

      //all the API to verify whether username exists or not
      // Set request headers including authorization token
      // eslint-disable-next-line
      const headers = {
        // 'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      };
      axios.post(`${process.env.BASE_API_URL}/api/login/`, this.userBody, { headers })
          .then(response => {
            // Handle API response data

            var resp = response.data;
            if (resp.status_code == 200){


              localStorage.setItem('userData', JSON.stringify(resp.message));
              this.$router.push({ name: 'home' })

            } else {
              createToast(JSON.stringify(resp.error),
                  {
                    showIcon: 'true',
                    hideProgressBar: 'false',
                    type: 'danger',
                    showCloseButton: 'true',
                    transition: 'slide',
                    position: 'bottom-center',
                  })
            }
          })
          .catch(error => {
            // Handle API error
            console.error(error);
          });

    },
    resetForm() {
      this.username = "";
      this.password = "";
      this.checkbox = false;
      localStorage.removeItem("loginUser")
    },

  },
  mounted() {
    const data = JSON.parse(localStorage.getItem('loginDetail'));
    const myData = JSON.parse(localStorage.getItem('loginUser'));
    if (data && !myData){
      this.username = data.username;
      this.password = data.password;
      this.checkbox = data.checked;
    }else{
      if (myData) this.username =  myData.username
    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

a {
  color: blueviolet;
}


</style>
