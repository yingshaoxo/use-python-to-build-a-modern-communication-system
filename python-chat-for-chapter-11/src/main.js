import Vue from 'vue'
import Vuex from 'vuex'
import App from './App.vue'
import VueRouter from 'vue-router'
import VueI18n from 'vue-i18n'
import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css'
import sha256 from 'crypto-js/sha256'
import md5 from 'crypto-js/md5'
const axios = require('axios').default
import VueChatScroll from 'vue-chat-scroll'

const host = location.protocol + '//' + document.domain + ':' + "8888" //location.protocol + '//' + document.domain + ':' + location.port
const url_for_usermanagement = host + "/api/v1/usermanagement"
const url_for_verify = host + "/api/v1/verify"
const url_for_getting_contact_list = host + "/api/v1/contactlist"
const url_for_receive = host + "/api/v1/receive"
const url_for_send = host + "/api/v1/send"
const url_for_file = host + "/api/v1/file"

Vue.config.productionTip = false
Vue.use(Vuex)
Vue.use(VueRouter)
Vue.use(VueI18n)
Vue.use(VueMaterial)
Vue.use(VueChatScroll)

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
        files: {},
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
            if (JSON.stringify(conversation) != JSON.stringify(this.state.conversation)) {
                //console.log("conversation updated")
                this.state.conversation = conversation
            }
        },
        set_file(_, obj) {
            if (!(obj.file_id in this.state.files)) {
                //console.log(obj)
                this.state.files[obj.file_id] = obj.file_dict
                //console.log("files", this.state.files)
            }
        }
    },
    actions: {
        async initialization(store) {
            await store.dispatch("go_home")

            // get state from storage
            if (localStorage.getItem('store')) {
                // Replace the state object with the stored item
                this.replaceState(
                    Object.assign(store.state, JSON.parse(localStorage.getItem('store')))
                );
            }

            if ((store.state.username != "") && (store.state.temp_token != "")) {
                //console.log(store.state)
                await store.dispatch("verify", {
                    "username": store.state.username,
                    "temp_token": store.state.temp_token,
                }).then(async (yes_or_no) => {
                    if (yes_or_no == true) {
                        await store.dispatch("go_contacts")
                    }
                })
            }

            setInterval(async () => {
                if (store.state.target) {
                    await store.dispatch("get_conversation", {
                        "target": store.state.target
                    })
                }
            }, 1000)
            /*
            if (store.state.target) {
                store.dispatch("get_conversation", {
                    "target": store.state.target
                })
            }
            */
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
            axios.post(url_for_usermanagement, data).then(async function (response) {
                alert(response.data.status)
                if ("temp_token" in response.data.result) {
                    let temp_token = response.data.result.temp_token
                    store.commit("set_temp_token", temp_token)
                    store.commit("set_username", username)
                    await store.dispatch("go_contacts")
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

            return axios.post(url_for_receive, data).then(async function (response) {
                if (response.data) {
                    //console.log(response.data)
                    if ("status" in response.data) {
                        if (response.data.status == "ok") {
                            if (response.data.result) {
                                if ("history" in response.data.result[0]) {
                                    //console.log(response.data.result[0].history)
                                    let conversation = response.data.result[0]

                                    for (let item of conversation.history) {
                                        await store.dispatch("update_files", {
                                            "type": item.content.type,
                                            "file_id": item.content.file_id,
                                        })
                                    }

                                    store.commit("set_conversation", conversation)

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
        async send(_, obj) {
            let username = store.state.username
            let temp_token = store.state.temp_token

            let content = {
                "type": obj.type,
                "name": md5(obj.file).toString(),
                "file": obj.file,
            }
            let body = {
                "to": obj.to,
                "content": content
            }
            let data = {
                "username": username,
                "temp_token": temp_token,
                "body": body,
            }

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
        async get_file(_, obj) {
            let username = store.state.username
            let temp_token = store.state.temp_token

            //console.log(obj)
            let body = {
                "file_id": obj.file_id
            }
            let data = {
                "username": username,
                "temp_token": temp_token,
                "body": body,
            }

            return axios.post(url_for_file, data).then(function (response) {
                if (response.data) {
                    //console.log(response.data)
                    if ("status" in response.data) {
                        if (response.data.status == "ok") {
                            if (response.data.result) {
                                //console.log(response.data.result)
                                return response.data.result
                            }
                        }
                    }
                }
            }).catch(function (error) {
                console.log(error);
            });
        },
        async update_files(_, obj) {
            let file_id = obj.file_id
            let type = obj.type
            if (!(file_id in this.state.files)) {
                let new_file = await store.dispatch("get_file", {"file_id": file_id})
                //console.log("new_file", new_file)
                store.commit("set_file", {
                    'file_id': file_id,
                    'file_dict': {
                        "type": type,
                        "file": new_file,
                    }
                })
            }
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
    beforeCreate: async () => {
        await store.dispatch("initialization")
    },
    render: h => h(App),
}).$mount('#app')
