import Vue from 'vue'
import LoginForm from './LoginForm'


import '../../base/scss/body.scss'


var loginForm = new Vue({
    render: h => h(LoginForm)
})

loginForm.$mount('#login-form');
