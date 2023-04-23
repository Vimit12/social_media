<template>
  <v-card>
    <v-layout>
      <v-navigation-drawer expand-on-hover rail>
        <v-list>
          <v-list-item
              prepend-avatar="https://randomuser.me/api/portraits/women/85.jpg"
              title="Vimit"
              subtitle="vimit@gmailcom"
          ></v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list density="compact" nav>
          <v-list-item prepend-icon="mdi-folder" title="My Files" value="myfiles"></v-list-item>
          <v-list-item prepend-icon="mdi-account-multiple" title="Shared with me" value="shared"></v-list-item>
          <v-list-item prepend-icon="mdi-star" title="Starred" value="starred"></v-list-item>
        </v-list>
      </v-navigation-drawer>

      <v-main style="height: 100%">
        <v-navigation-drawer expand-on-hover rail>
          <v-list>
            <v-list-item
                prepend-avatar="https://randomuser.me/api/portraits/women/85.jpg"
                title="Vimit"
                subtitle="vimit@gmailcom"
            ></v-list-item>
          </v-list>

          <v-divider></v-divider>

          <v-list density="compact" nav>
            <v-list-item prepend-icon="mdi-folder" title="My Files" value="myfiles"></v-list-item>
            <v-list-item prepend-icon="mdi-account-multiple" title="Shared with me" value="shared"></v-list-item>
            <v-list-item prepend-icon="mdi-star" title="Starred" value="starred"></v-list-item>
          </v-list>
        </v-navigation-drawer>
      </v-main>
    </v-layout>
  </v-card>
  <Footer />

</template>
<script>
import Footer from '@/components/FooterView.vue'
export default {
  name: 'AboutView',
  components: {
    Footer
  },
  data() {
    return {
      inactivityTimeout: null,
      showWarning: false
    }
  },
  mounted() {
    this.resetInactivityTimeout();
    window.addEventListener('mousemove', this.resetInactivityTimeout);
    window.addEventListener('keydown', this.resetInactivityTimeout);
  },
  beforeUnmount() {
    window.removeEventListener('mousemove', this.resetInactivityTimeout);
    window.removeEventListener('keydown', this.resetInactivityTimeout);
  },
  methods: {
    resetInactivityTimeout() {
      clearTimeout(this.inactivityTimeout);
      this.inactivityTimeout = setTimeout(() => {
        this.showWarning = true;
      }, 5000); // 5 seconds of inactivity to show warning
    }
  }
}

</script>

<style>



</style>
