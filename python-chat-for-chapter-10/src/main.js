import Vue from 'vue'
import Vuex from 'vuex'
import App from './App.vue'
import VueRouter from 'vue-router'
import VueI18n from 'vue-i18n'
import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css'
import sha256 from 'crypto-js/sha256'
const axios = require('axios').default

const host = location.protocol + '//' + document.domain + ':' + "8888" //location.protocol + '//' + document.domain + ':' + location.port
const url_for_usermanagement = host + "/api/v1/usermanagement"
const url_for_verify = host + "/api/v1/verify"
const url_for_getting_contact_list = host + "/api/v1/contactlist"
const url_for_receive = host + "/api/v1/receive"
const url_for_send = host + "/api/v1/send"

Vue.config.productionTip = false
Vue.use(Vuex)
Vue.use(VueRouter)
Vue.use(VueI18n)
Vue.use(VueMaterial)

// Ready translated locale messages
const messages = {
    en: {
        home: {
            hi: 'Hi There !',
            username: "Username",
            password: "Password",
            signup: "Sign up",
            login: "Log in",
        },
        chat: {
            type_your_message_here: "Type your message here",
        }
    },
    cn: {
        home: {
            hi: '你好啊！',
            username: "用户名",
            password: "密码",
            signup: "注册",
            login: "登陆",
        },
        chat: {
            type_your_message_here: "请在此输入你的消息",
        }
    },
}

const i18n = new VueI18n({
    locale: 'en', // set locale
    messages, // set locale messages
})

const Home = resolve => require(['./components/Home.vue'], resolve)
const Contacts = resolve => require(['./components/Contacts.vue'], resolve)
const Chat = resolve => require(['./components/Chat.vue'], resolve)

const routes = [
    { path: '/home', component: Home },
    { path: '/contacts', component: Contacts },
    { path: '/chat', component: Chat }
]

const router = new VueRouter({
    mode: 'history',
    routes: routes
})

const store = new Vuex.Store({
    state: {
        username: "",
        temp_token: "",
        contact_list: [],
        target: "",
        conversation: {},
    },
    mutations: {
        set_username(_, username) {
            this.state.username = username
        },
        set_temp_token(_, temp_token) {
            this.state.temp_token = temp_token
        },
        set_contact_list(_, contact_list) {
            this.state.contact_list = contact_list
        },
        set_target(_, name) {
            this.state.target = name
        },
        set_conversation(_, conversation) {
            this.state.conversation = conversation
        }
    },
    actions: {
        async initialization(store) {
            store.dispatch("go_home")

            // get state from storage
            if (localStorage.getItem('store')) {
                // Replace the state object with the stored item
                this.replaceState(
                    Object.assign(store.state, JSON.parse(localStorage.getItem('store')))
                );
            }

            if ((store.state.username != "") && (store.state.temp_token != "")) {
                //console.log(store.state)
                store.dispatch("verify", {
                    "username": store.state.username,
                    "temp_token": store.state.temp_token,
                }).then((yes_or_no) => {
                    if (yes_or_no == true) {
                        store.dispatch("go_contacts")
                    }
                })
            }

            setInterval(() => {
                if (store.state.target) {
                    store.dispatch("get_conversation", {
                        "target": store.state.target
                    })
                }
            }, 1000)
        },
        async go_home() {
            router.push("home")
        },
        async go_contacts() {
            router.push("contacts")
        },
        async go_chat() {
            router.push("chat")
        },
        async user_sign_up(_, obj) {
            let username = obj.username
            let password = obj.password

            let salt = username.slice(Math.floor(username.length / 2))
            let sha256_password = sha256(password + salt).toString()

            let body = {
                "username": username,
                "sha256_password": sha256_password,
            }
            let data = {
                "action": "signup",
                "body": body,
            }

            //console.log(sha256_password)
            axios.post(url_for_usermanagement, data).then(function (response) {
                alert(response.data.status)
            }).catch(function (error) {
                console.log(error);
            });
        },
        async user_log_in(_, obj) {
            let username = obj.username
            let password = obj.password

            let salt = username.slice(Math.floor(username.length / 2))
            let sha256_password = sha256(password + salt).toString()

            let body = {
                "username": username,
                "sha256_password": sha256_password,
            }
            let data = {
                "action": "login",
                "body": body,
            }

            //console.log(sha256_password)
            axios.post(url_for_usermanagement, data).then(function (response) {
                alert(response.data.status)
                if ("temp_token" in response.data.result) {
                    let temp_token = response.data.result.temp_token
                    store.commit("set_temp_token", temp_token)
                    store.commit("set_username", username)
                    store.dispatch("go_contacts")
                }
            }).catch(function (error) {
                console.log(error);
            });
        },
        async verify(_, obj) {
            let username = obj.username
            let temp_token = obj.temp_token

            let data = {
                "username": username,
                "temp_token": temp_token,
            }

            return axios.post(url_for_verify, data).then(function (response) {
                if (response.data.status.includes("ok")) {
                    return true
                } else {
                    return false
                }
            }).catch(function (error) {
                console.log(error);
                return false
            });
        },
        async get_contact_list() {
            let username = store.state.username
            let temp_token = store.state.temp_token

            let data = {
                "username": username,
                "temp_token": temp_token,
            }

            await axios.post(url_for_getting_contact_list, data).then(function (response) {
                if (response.data) {
                    if ("status" in response.data) {
                        if (response.data.status == "ok") {
                            if (response.data.result) {
                                if ("name_list" in response.data.result) {
                                    store.commit("set_contact_list", response.data.result.name_list)
                                }
                            }
                        }
                    }
                }
            }).catch(function (error) {
                console.log(error);
            });
        },
        async get_conversation(_, obj) {
            let username = store.state.username
            let temp_token = store.state.temp_token

            let body = {
                "target": obj.target
            }
            let data = {
                "username": username,
                "temp_token": temp_token,
                "body": body,
            }

            return axios.post(url_for_receive, data).then(function (response) {
                if (response.data) {
                    //console.log(response.data)
                    if ("status" in response.data) {
                        if (response.data.status == "ok") {
                            if (response.data.result) {
                                if ("history" in response.data.result[0]) {
                                    store.commit("set_conversation", response.data.result[0])
                                    return true
                                }
                            }
                        }
                    }
                }
            }).catch(function (error) {
                console.log(error);
            });
        },
        async send_text(_, obj) {
            let username = store.state.username
            let temp_token = store.state.temp_token

            let body = {
                "to": obj.to,
                "text": obj.text
            }
            let data = {
                "username": username,
                "temp_token": temp_token,
                "body": body,
            }

            //console.log(body)

            return axios.post(url_for_send, data).then(function (response) {
                if (response.data) {
                    //console.log(response.data)
                    if ("status" in response.data) {
                        if (response.data.status == "ok") {
                            return true
                        }
                    }
                }
            }).catch(function (error) {
                console.log(error);
            });
        },
    },
})

// Subscribe to store updates, save changed state to storage
store.subscribe((mutation, state) => {
    // Store the state object as a JSON string
    localStorage.setItem('store', JSON.stringify(state))
});

new Vue({
    router: router,
    store: store,
    i18n: i18n,
    beforeCreate: () => {
        store.dispatch("initialization")
    },
    render: h => h(App),
}).$mount('#app')
