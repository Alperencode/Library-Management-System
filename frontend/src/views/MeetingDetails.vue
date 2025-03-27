<template>
  <div>
    <!-- Sub Header -->
    <div class="sub-header">
      <div class="container">
        <div class="row">
          <div class="col-lg-8 col-sm-8">
            <div class="left-content">
              <p>This is an educational <em>HTML CSS</em> template by TemplateMo website.</p>
            </div>
          </div>
          <div class="col-lg-4 col-sm-4">
            <div class="right-icons">
              <ul>
                <li><a href="#"><i class="fa fa-facebook"></i></a></li>
                <li><a href="#"><i class="fa fa-twitter"></i></a></li>
                <li><a href="#"><i class="fa fa-behance"></i></a></li>
                <li><a href="#"><i class="fa fa-linkedin"></i></a></li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Page Heading -->
    <section class="heading-page header-text" id="top">
      <div class="container">
        <div class="row">
          <div class="col-lg-12">
            <h6>Get all details</h6>
            <h2>Online Teaching and Learning Tools</h2>
          </div>
        </div>
      </div>
    </section>

    <!-- Meeting Details -->
    <section class="meetings-page" id="meetings">
      <div class="container">
        <div class="row">
          <div class="col-lg-12">
            <div class="meeting-single-item">
              <div class="thumb">
                <div class="price"><span>$14.00</span></div>
                <div class="date"><h6>Nov <span>12</span></h6></div>
                <a href="#"><img src="@/assets/images/single-meeting.jpg" alt="Meeting" /></a>
              </div>
              <div class="down-content">
                <a href="#"><h4>Online Teaching and Learning Tools</h4></a>
                <p>Recreio dos Bandeirantes, Rio de Janeiro - RJ, 22795-008, Brazil</p>
                <p class="description">
                  This is an edu meeting HTML CSS template provided by
                  <a href="https://templatemo.com/" target="_blank" rel="nofollow">TemplateMo website</a>. This is a Bootstrap v5.1.3 layout...
                  <br /><br />
                  You are allowed to use this edu meeting CSS template for your school or university or business. You can feel free to modify or edit this layout.
                </p>
                <div class="row">
                  <div class="col-lg-4">
                    <div class="hours">
                      <h5>Hours</h5>
                      <p>Monday - Friday: 07:00 AM - 13:00 PM<br />Saturday - Sunday: 09:00 AM - 15:00 PM</p>
                    </div>
                  </div>
                  <div class="col-lg-4">
                    <div class="location">
                      <h5>Location</h5>
                      <p>Recreio dos Bandeirantes,<br />Rio de Janeiro - RJ, 22795-008, Brazil</p>
                    </div>
                  </div>
                  <div class="col-lg-4">
                    <div class="book-now">
                      <h5>Book Now</h5>
                      <p>010-020-0340<br />090-080-0760</p>
                    </div>
                  </div>
                  <div class="col-lg-12">
                    <div class="share">
                      <h5>Share:</h5>
                      <ul>
                        <li><a href="#">Facebook</a>,</li>
                        <li><a href="#">Twitter</a>,</li>
                        <li><a href="#">LinkedIn</a>,</li>
                        <li><a href="#">Behance</a></li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
              <div class="main-button-red mt-4">
                <a href="/meetings">Back To Meetings List</a>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="footer">
        <p>
          Copyright © 2022 Edu Meeting Co., Ltd.
          <br />
          Design: <a href="https://templatemo.com" target="_blank">TemplateMo</a>
        </p>
      </div>
    </section>
  </div>
</template>

<script>
import { onMounted } from "vue";

export default {
  name: "MeetingDetailPage",
  setup() {
    onMounted(() => {
      const scripts = [
        "/vendor/jquery/jquery.min.js",
        "/assets/js/isotope.min.js",
        "/assets/js/owl-carousel.js",
        "/assets/js/lightbox.js",
        "/assets/js/tabs.js",
        "/assets/js/video.js",
        "/assets/js/slick-slider.js",
        "/assets/js/custom.js",
      ];
      scripts.forEach((src) => {
        const s = document.createElement("script");
        s.src = src;
        s.async = true;
        document.body.appendChild(s);
      });
    });

    return {};
  },
};
</script>

<style scoped>
@import "@/assets/css/fontawesome.css";
@import "@/assets/css/templatemo-edu-meeting.css";
@import "@/assets/css/owl.css";
@import "@/assets/css/lightbox.css";
</style>