<template>
  <md-content class="resize no-scrollbar">
    <div class="md-layout md-alignment-center title">
      <span class="md-title">{{ target }}</span>
    </div>

    <md-divider></md-divider>

    <md-list>
      <md-list-item v-bind:key="index" v-for="(item, index) in conversation.history">
        <div class="md-list-item-text" v-bind:class="[item.from == $store.state.username ? 'right' : 'left']">
          <span>{{ item.text }}</span>
        </div>
      </md-list-item>
    </md-list>

    <md-divider></md-divider>

    <md-field class="input">
      <label>{{ $t('chat.type_your_message_here') }}</label>
      <md-textarea v-model="text" md-autogrow></md-textarea>
      <span v-on:click="send_message">
        <md-icon>send</md-icon>
      </span>
    </md-field>

    <!--md-dialog-confirm
      :md-active.sync="audio_recording"
      md-title="Recording..."
      md-content=""
      md-confirm-text="Send"
      md-cancel-text="Cancel"
      @md-cancel="voice_input_cancel"
      @md-confirm="voice_input_stop" />

    <div class="outer">
      <div class="inner">
        <span @click="audio_recording = true">
          <md-icon>keyboard_voice</md-icon>
        </span>
      </div>
    </div-->

  </md-content>
</template>

<script>
export default {
  name: "Chat",
  data: () => ({
    text: null,
    audio_recording: false,
    audio_recorder: null,
  }),
  computed: {
    conversation: {
      get() {
        return this.$store.state.conversation;
      }
    },
    target: {
      get() {
        return this.$store.state.target;
      }
    },
  },
  watch: {
    audio_recording: function(val) {
      if (val == true) {
        this.voice_input_start()
      }
    }
  },
  methods: {
    send_message() {
      //console.log(this.text)
      //console.log(this.$store.state.target)
      this.$store.dispatch('send_text', {
        "to": this.$store.state.target,
        "text": this.text
      }).then((result) => {
        if (result == true) {
          // refersh chat history
          this.text = ""
          this.$store.dispatch("get_conversation", {
            "target": this.$store.state.target
          })
        }
      })
    },
    async record_audio() {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      const audioChunks = [];

      mediaRecorder.addEventListener("dataavailable", event => {
        audioChunks.push(event.data);
      });

      const start = () => mediaRecorder.start();

      const stop = () =>
        new Promise(resolve => {
          mediaRecorder.addEventListener("stop", () => {
            const audioBlob = new Blob(audioChunks);
            const audioUrl = URL.createObjectURL(audioBlob);
            const audio = new Audio(audioUrl);
            const play = () => audio.play();
            resolve({ audioBlob, audioUrl, play });
          });

          mediaRecorder.stop();
        });

      return { start, stop };
    },
    async voice_input_start() {
      console.log("voice recording started")
      this.audio_recorder = await this.record_audio()
      this.audio_recorder.start()
    },
    async voice_input_stop() {
      console.log("voice recording stopped")
      const audio = await this.audio_recorder.stop()
      audio.play()

      const reader = new FileReader();
      reader.readAsDataURL(audio.audioBlob);
      reader.onload = () => {
        //console.log("audio onload")
        const base64AudioMessage = reader.result.split(',')[1];
        console.log(base64AudioMessage)
      }
    },
    async voice_input_cancel() {
      console.log("voice recording canceld")
      await this.audio_recorder.stop()
      //audio.play()
    }, 
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.resize {
  height: 100vh;
}
.title {
  margin: 1.8%;
}
.white {
  background-color: rgb(255, 255, 255);
}
.no-scrollbar {
  overflow: hidden;
}
.input {
  margin: 1px;
}
.right {
  text-align: right;
}
.left {
  text-align: left;
}

.outer
{
    width:100%;
    text-align: center;
    margin-block: 2%;
}
.inner
{
    display: inline-block;
    margin-inline: 5%;
}
</style>
