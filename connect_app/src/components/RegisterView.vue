<template>
  <v-sheet width="450" class="mx-auto" style="padding: 2em;margin-top: 3em;margin-bottom: 3em;" border>
    <v-card text="Register"  color="black" style="margin-bottom: 1em;"></v-card>
    <v-form ref="form" >
      <v-text-field v-model="username" label="username" required></v-text-field>
      <v-text-field v-model="name" label="Full name" required></v-text-field>
      <v-text-field v-model="email" label="Email" :rules="[emailRule]" required></v-text-field>
      <v-text-field v-model="mobile" label="Mobile" required></v-text-field>
      <v-text-field v-model="pass" label="Password" :rules="[passwordRule]"  :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                    :type="showPassword ? 'text' : 'password'"
                    @click:append="showPassword = !showPassword" required></v-text-field>
      <v-text-field v-model="alt_pass" label="Re-Type Password" :rules="[passwordRule]" :append-icon="altshowPassword ? 'mdi-eye' : 'mdi-eye-off'"
                    :type="altshowPassword ? 'text' : 'password'"
                    @click:append="altshowPassword = !altshowPassword" required></v-text-field>
      <p style="color: crimson;font-size: 12px; " class="errMsg"></p>
      <div class="d-flex flex-column">
        <v-row>
          <v-col>
            <v-btn color="green" class="mt-4" block @click="createForm">Success</v-btn>
          </v-col>
          <v-col>
            <v-btn color="red" class="mt-4" block @click="resetForm">Reset</v-btn>
          </v-col>

        </v-row>
      </div>
    </v-form>
  </v-sheet>
  <Footer />
</template>

<script>
/* eslint-disable */
import { createToast } from 'mosha-vue-toastify';
import 'mosha-vue-toastify/dist/style.css'
import Footer from '@/components/FooterView.vue'
import axios from 'axios';
export default {
  name: 'RegisterView',
  props: {
    // msg: String
  },
  components: {
    Footer
  },
  data() {
    return {
      username:"",
      name: "",
      email: "",
      mobile: "",
      pass: "",
      alt_pass: "",
      userBody: {
        "username": "",
        "name": "",
        "email": "",
        "password": "",
        "profile":{
          "mobile": ""
        }
      },
      showPassword: false,
      altshowPassword: false,
      emptyKeys:[],
      emailRule: (value) => {
        if (!value || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
          return true;
        }
        return 'Please enter a valid email address';
      },
      passwordRule: (value) => {
        if (!value) return 'Password is required';
        if (value.length < 8) return 'Password must be at least 8 characters long';
        if (!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?#&])[A-Za-z\d@$!%#*?&]+$/.test(value))
          return 'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character';
        return true;
      },
    }
  },
  watch: {
    username: function (val) {
      if (!(val == "")){
        this.resetMsg();
      }
    },
    name: function (val) {
      if (!(val == "")){
        this.resetMsg();
      }
    },
    mobile: function (val) {
      if (!(val == "")){
        this.resetMsg();
      }
    },
    email: function (val) {
      if (!(val == "")){
        this.resetMsg();
      }
    },
    pass: function (val) {
      if (!(val == "")){
        this.resetMsg();
      }
    },
    alt_pass: function (val) {
      if (!(val == "")){
        this.resetMsg();
      }

    }
  },
  methods: {
    resetMsg(){
      var elements = document.getElementsByClassName("errMsg");
      var element = elements[0];
      element.textContent = "";
    },
    getEmptyKeys() {
      this.emptyKeys = [];
      for (let key in this.userBody) {
        if (!this.userBody[key] || this.userBody[key] === "") {
          this.emptyKeys.push(key);
        }
      }
      return this.emptyKeys;
    },
    resetForm() {
      this.username = "";
      this.password = "";
      this.name = "";
      this.email = "";
      this.mobile = "";
      this.pass = "";
      this.alt_pass = "";
      this.resetMsg();
    },

    createForm(){

      //password match logic
      if (this.alt_pass !== this.pass){
        var elements = document.getElementsByClassName("errMsg");
        var element = elements[0];
        element.textContent = "The passwords don't match.";
        this.alt_pass = "";
        this.pass = "";

        createToast("The passwords don't match.",
            {
              showIcon: 'true',
              hideProgressBar: 'false',
              type: 'info',
              showCloseButton: 'true',
              transition: 'slide',
              position: 'bottom-center',
            })
        return
      }
      //defining userBody schema for passing it to API
      this.userBody = {
        "username": this.username,
        "name": this.name,
        "email": this.email,
        "password": this.pass,
        "profile":{
          "mobile": this.mobile
        }
      }

      //all the API to verify whether username exists or not
      // Set request headers including authorization token
      // eslint-disable-next-line
      const headers = {
        // 'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      };

      // Set request data as an object
      // eslint-disable-next-line
      const requestData = {
        username: this.username
      };

      if (this.getEmptyKeys()){
        if (this.mobile == null || this.mobile == "") {
          this.emptyKeys.push("mobile");

        }
      }

      // // Make axios POST request with headers and data
      if (this.emptyKeys.length == 0){
            axios.post(`${process.env.BASE_API_URL}/api/username/`, requestData, { headers })
                .then(response => {
                  // Handle API response data
                  var resp = response.data;
                  if (resp.status_code == 200){
                    //register user
                      axios.post(`${process.env.BASE_API_URL}/api/sign_up/`, this.userBody, { headers })
                        .then(response => {
                        // Handle API response data
                          var resp = response.data;
                          if (resp.status_code == 200){
                            createToast(JSON.stringify(resp.message),
                                {
                                  showIcon: 'true',
                                  hideProgressBar: 'false',
                                  type: 'success',
                                  showCloseButton: 'true',
                                  transition: 'slide',
                                  position: 'bottom-center',
                                })
                            // this.$router.push(name: 'About', params: { message: 'Hello from Home' })
                            this.$router.push({ name: 'home' })
                            localStorage.setItem('loginUser', JSON.stringify({ username: this.username}));

                          } else if (resp.status_code == 400){
                            createToast(JSON.stringify(resp.error),
                                {
                                  showIcon: 'true',
                                  hideProgressBar: 'false',
                                  type: 'warning',
                                  showCloseButton: 'true',
                                  transition: 'slide',
                                  position: 'bottom-center',
                                })
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
                  }
                  else {
                    var elements = document.getElementsByClassName("errMsg");
                    var element = elements[0];
                    element.textContent = "Username is already taken";
                    createToast("Username is already taken",
                        {
                          showIcon: 'true',
                          hideProgressBar: 'false',
                          type: 'info',
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
          }
      else{
        var elements = document.getElementsByClassName("errMsg");
        var element = elements[0];
        element.textContent = JSON.stringify(this.emptyKeys) + " these fields are mandatory!!"
        createToast(JSON.stringify(this.emptyKeys) + " these fields are mandatory!!",
            {
              showIcon: 'true',
              hideProgressBar: 'false',
              type: 'info',
              showCloseButton: 'true',
              transition: 'slide',
              position: 'bottom-center',
            })
      }
    }
  },
  mounted() {
    console.log('Mounted')
  },
  computed: {

  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>


</style>
