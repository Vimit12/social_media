<template>
  <VueSidebarMenuAkahon  menuTitle="connectMe"  profileImg='@/assets/img/connected_img.png' />
</template>

<script>
// import RightSideBar from "../components/RightSideBar.vue";
// import SideBar from "../components/SideBar";
import VueSidebarMenuAkahon from "vue-sidebar-menu-akahon";
export default {
  name: "HomeView",
  data: () => ({
    // menuLogo:"@/assets/image/connected_img.png"
  }),
  props:{
    menuLogo: {
      type: String,
      default: '@/assets/image/connected_img.png',
    }
  },
  components: {
    // SideBar,
    // RightSideBar,
    VueSidebarMenuAkahon
  },
  methods: {},
};
</script>
<style scoped>

</style>