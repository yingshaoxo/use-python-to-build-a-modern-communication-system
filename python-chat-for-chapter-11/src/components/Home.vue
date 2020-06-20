<template>
  <div class="my-center no-scrollbar">
    <md-card class="md-layout-item">
      <md-card-header>
        <div class="md-title">{{ $t('home.hi') }}</div>
      </md-card-header>

      <md-card-content>
        <md-field md-clearable>
          <label>{{ $t('home.username') }}</label>
          <md-input v-model="username"></md-input>
        </md-field>

        <md-field>
          <label>{{ $t('home.password') }}</label>
          <md-input v-model="password" type="password"></md-input>
        </md-field>
      </md-card-content>

      <md-card-actions>
        <md-button type="submit" class="md-primary" v-on:click="signup">{{ $t('home.signup') }}</md-button>
        <md-button type="submit" class="md-primary" v-on:click="login">{{ $t('home.login') }}</md-button>
      </md-card-actions>
    </md-card>
  </div>
</template>

<script>
export default {
  name: "Home",
  data: () => ({
    username: null,
    password: null
  }),
  methods: {
    signup() {
      this.$store.dispatch("user_sign_up", {
        username: this.username,
        password: this.password
      });
    },
    login() {
      this.$store.dispatch("user_log_in", {
        username: this.username,
        password: this.password
      });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.resize {
  height: 100vh;
}
.my-center {
  margin-top: 26vh;
}
.no-scrollbar {
  overflow: hidden;
}
</style>
