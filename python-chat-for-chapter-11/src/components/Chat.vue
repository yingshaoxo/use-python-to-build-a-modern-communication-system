<template>
  <md-content class="resize no-scrollbar">
    <div class="md-layout md-alignment-center title">
      <span class="md-title">{{ target }}</span>
    </div>

    <md-divider></md-divider>

    <md-list class="message-list" v-chat-scroll="{always: false, smooth: true}">
      <md-list-item v-bind:key="index" v-for="(item, index) in conversation.history" class="message-list-item">
        <div class="md-list-item-text" v-bind:class="[item.from == $store.state.username ? 'right' : 'left']">
          <div v-if="item.content.type == 'text'" class="multiline-text have-height">
            {{ display_a_file(item.content.file_id) }}
          </div>
          <div v-if="item.content.type == 'audio'">
            <audio v-bind:src="display_a_file(item.content.file_id)" controls mediaGroup="yingshaox_o" class="have-height">
              Your browser does not support the
              <code>audio</code> element.
            </audio>
          </div>
        </div>
      </md-list-item>
    </md-list>

    <md-divider style="margin-top: 1vh;"></md-divider>

    <md-field class="input">
      <label>{{ $t('chat.type_your_message_here') }}</label>
      <md-textarea v-model="text" md-autogrow></md-textarea>
      <span v-on:click="send_message">
        <md-icon>send</md-icon>
      </span>
    </md-field>

    <md-dialog-confirm
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
    </div>

  </md-content>
</template>

<script>
//import { mapActions } from 'vuex'
import { mapState } from 'vuex'

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
    ...mapState(['files']), // map `this.files` to `this.$store.state.files`
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
      this.$store.dispatch('send', {
        "to": this.$store.state.target,
        "type": "text",
        "file": this.text,
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
        const base64AudioMessage = reader.result//.split(',')[1];
        //console.log(base64AudioMessage)

        this.$store.dispatch('send', {
          "to": this.$store.state.target,
          "type": "audio",
          "file": base64AudioMessage,
        }).then((result) => {
          if (result == true) {
            //console.log("after message sent: ", result)

            // refersh chat history
            this.$store.dispatch("get_conversation", {
              "target": this.$store.state.target
            })
          }
        })

      }
    },
    async voice_input_cancel() {
      console.log("voice recording canceld")
      await this.audio_recorder.stop()
      //audio.play()
    }, 
    dataURLtoBlob(dataurl) {
      var parts = dataurl.split(','), mime = parts[0].match(/:(.*?);/)[1]
      if(parts[0].indexOf('base64') !== -1) {
          var bstr = atob(parts[1]), n = bstr.length, u8arr = new Uint8Array(n)
          while(n--){
              u8arr[n] = bstr.charCodeAt(n)
          }

          return new Blob([u8arr], {type:mime})
      } else {
          var raw = decodeURIComponent(parts[1])
          return new Blob([raw], {type: mime})
      }
    },
    display_a_file(file_id) {
      //console.log("files at component", this.files)
      if (file_id in this.files) {
        let file_dict = this.files[file_id]
        let type = file_dict.type
        let file = file_dict.file
        //console.log("display a file: ", file_dict)
        if (type == "text") {
          return file
        } else if (type == "audio") {
          let audio_blob = this.dataURLtoBlob(file)
          let audio_url = URL.createObjectURL(audio_blob);
          return audio_url
        }
      } else {
        return undefined
      }
    },
    //...mapActions(['get_file']), // map `this.get_file()` to `this.$store.dispatch('get_file')`
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
  height: 5vh;
}
.white {
  background-color: rgb(255, 255, 255);
}
.no-scrollbar {
  overflow: hidden;
}

.message-list {
  overflow-y: scroll;
  max-height: 80vh;
}
.message-list-item {
  margin-top: 1vh;
}
.multiline-text {
  white-space: pre-line; 
  word-break: break-all;
  overflow-wrap: break-word;
  /*text-align: left;*/
}
.have-height {
  min-height: 5vh;
}
.right {
  position: absolute;
  text-align: right;
  width: 35%;
  right: 4vw;
}
.left {
  position: absolute;
  text-align: left;
  width: 35%;
  left: 4vw;
}


.input {
  margin: 0.5vw;
  width: 99.2vw;
  height: 6vh;
}
.outer
{
    width:100%;
    text-align: center;
    margin-top: 2%;
}
.inner
{
    display: inline-block;
    margin-inline: 0px;
}
</style>