<template>
  <section class="container">
    <div class="row">
      <div class="col-sm-9 col-md-7 col-lg-5 mx-auto">
        <div class="card card-signin my-5">
          <div class="card-body">
            <h5 class="card-title text-center">Sign In</h5>
            <form action="/" class="form" method="post">

              <div v-if="errors.non_field_errors" class="alert alert-danger"><span v-html="errors.non_field_errors"></span></div>

              <input type="hidden" name="csrfmiddlewaretoken" :value="loginform.csrftoken">


              <div class="form-label-group">
                <label for="inputEmail">Email address</label>
                <input autocomplete="on" type="email" class="form-control" placeholder="Email address" required autofocus v-model="loginform.email">
              </div>
              <div v-if="errors.email" class="field-errors alert alert-danger"><span>{{ errors.email }}</span></div>

              <br><br>


              <div class="form-label-group">
                <label for="inputPassword">Password </label>
                <input autocomplete="on" type="password" class="form-control" placeholder="Password" required v-model="loginform.password">
              </div>
              <div v-if="errors.password" class="field-errors alert alert-danger"><span>{{ errors.password }}</span></div>
              <br><br>

              <button class="btn btn-lg btn-primary btn-block text-uppercase submit-btn" @keyup.enter.prevent="Submit" @click.prevent="Submit">Sign in</button>
              <br>
              <h6>Or <a href="/sign_up/">click here</a> to register a new account</h6>

              <hr class="my-4">

            </form>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
  import Vue from 'vue'
  import axios from 'axios'
  import VueAxios from 'vue-axios'
  import qs from 'qs'

  Vue.use(VueAxios, axios);

  export default {
    name: "LoginForm",
    data: function () {
      return {
        loginform: {
          email: '',
          password: '',
          csrftoken: ''
        },
        errors: {
          non_field_errors: '',
          email: '',
          password: ''
        }
      }
    },
    methods: {
      Submit: function () {
        this.loginform.csrftoken = window.__data.csrf_token;
        let login_url = window.__data.login_url,
          data = {
            "email": this.loginform.email,
            "password": this.loginform.password
          },
          headers = {
            "X-CSRFToken": this.loginform.csrftoken,
            "Content-type": "application/x-www-form-urlencoded"
          };
        this.errors.non_field_errors = '';
        axios.post(login_url, qs.stringify(data), {headers: headers})
          .then(response => {
            if (response.data.hasOwnProperty('form_errors')) {
              let form_errors = response.data.form_errors;
              if (form_errors.hasOwnProperty('email')) {
                this.errors.email = form_errors.email[0];
              }
              if (form_errors.hasOwnProperty('password')) {
                this.errors.password = form_errors.password[0];
              }
              if (form_errors.hasOwnProperty('non_field_error')) {
                this.errors.non_field_errors = form_errors.non_field_error[0];
              }
            }
            if (response.data.hasOwnProperty('redirect_to')){
              window.location.href = response.data.redirect_to;
            }
          })
          .catch(errors => {
            this.errors.non_field_errors = 'Something went wrong please try again.';
          })
      }
    }
  }
</script>

<style scoped>
  .container {
    margin-top: 15%;
  }
  .submit-btn {
    background-color: #f6f4ff;
    color: red;
  }
  .submit-btn:hover {
    background-color: #ffe4e8;
  }
  .field-errors{
    margin-top: 1%;
    text-align: center;
  }
  .card {
    background-color: transparent;
    border: none;
  }
</style>
