<template>
  <div>
    <section class="section main-banner" id="top" data-section="section1">
      <video autoplay muted loop id="bg-video">
        <source src="/assets/images/course-video.mp4" type="video/mp4" />
      </video>
      <div class="video-overlay header-text">
        <div class="container">
          <div class="row">
            <div class="col-lg-12">
              <div class="caption">
                <h6>Hello Students</h6>
                <h2>Welcome to Education</h2>
                <p>
                  This is an edu meeting HTML CSS template provided by
                  <a href="https://templatemo.com/page/1" target="_blank">TemplateMo website</a>.
                </p>
                <div class="main-button-red">
                  <a href="#contact">Join Us Now!</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <section class="services">
      <div class="container">
        <div class="row">
          <div class="col-lg-12">
            <div class="owl-service-item owl-carousel">
              <div v-for="(service, index) in services" :key="index" class="item">
                <div class="icon">
                  <img :src="service.image" :alt="service.title" />
                </div>
                <div class="down-content">
                  <h4>{{ service.title }}</h4>
                  <p>{{ service.description }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { onMounted } from "vue";

export default {
  setup() {
    const services = [
      {
        image: "@/assets/images/service-icon-01.png",
        title: "Best Education",
        description: "Suspendisse tempor mauris a sem elementum bibendum.",
      },
      {
        image: "@/assets/images/service-icon-02.png",
        title: "Best Teachers",
        description: "Praesent facilisis massa non vestibulum.",
      },
      {
        image: "@/assets/images/service-icon-03.png",
        title: "Best Students",
        description: "Praesent facilisis massa non vestibulum.",
      },
    ];

    onMounted(() => {
      const scriptPaths = [
        "/vendor/jquery/jquery.min.js",
        "/assets/js/isotope.min.js",
        "/assets/js/owl-carousel.js",
        "/assets/js/lightbox.js",
        "/assets/js/video.js",
       // "/assets/js/custom.js",
      ];

      scriptPaths.forEach((src) => {
        const script = document.createElement("script");
        script.src = src;
        script.async = true;
        document.body.appendChild(script);
      });
    });

    return { services };
  },
};
</script>

<style scoped>
@import "@/assets/css/fontawesome.css";
@import "@/assets/css/templatemo-edu-meeting.css";
@import "@/assets/css/owl.css";
@import "@/assets/css/lightbox.css";
</style>