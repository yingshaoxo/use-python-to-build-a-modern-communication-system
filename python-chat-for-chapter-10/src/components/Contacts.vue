<template>
  <div>
    <md-list>
      <md-list-item 
        v-bind:key="index" 
        v-for="(name, index) in contact_list"
      >
        <md-avatar>
          <!--img src="https://placeimg.com/40/40/people/5" alt="People"-->
          <md-icon class="md-size-2x md-balck">person</md-icon>
        </md-avatar>

        <span class="md-list-item-text">{{ name }}</span>

        <md-button class="md-icon-button md-list-action" v-on:click="chat_with(name)">
          <md-icon class="md-primary">chat_bubble</md-icon>
        </md-button>
      </md-list-item>

    </md-list>
  </div>
</template>

<script>
export default {
  name: 'Contacts',
  computed: {
    contact_list: {
      get() {
        return this.$store.state.contact_list
      },
      set() {
        //this.$store.commit('change_user_login_state', value)
      }
    },
  },
  beforeCreate: function whatever() {
      this.$store.dispatch('get_contact_list')
  },
  methods: {
    chat_with(name) {
      //console.log(`chat with ${name}`)

      this.$store.commit("set_target", name)
      this.$store.commit("set_conversation", {})

      this.$store.dispatch("get_conversation", {
        "target": name
      }).then((result) => {
        //console.log(result)
        if (result == true) {
          this.$store.dispatch('go_chat')
        } else if (result == undefined) {
          this.$store.dispatch('go_chat')
        }
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
