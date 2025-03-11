<template>
  <header class="header-area header-sticky">
    <div class="container">
      <div class="row">
        <div class="col-12">
          <nav class="main-nav">
            <RouterLink to="/" class="logo">Edu Meeting</RouterLink>
            <ul class="nav">
              <li class="scroll-to-section"><RouterLink to="/" class="active">Home</RouterLink></li>
              <li><RouterLink to="/meetings">Meetings</RouterLink></li>
              <li class="scroll-to-section"><a href="#apply">Apply Now</a></li>
              <li class="has-sub">
                <a href="javascript:void(0)">Pages</a>
                <ul class="sub-menu">
                  <li><RouterLink to="/meetings">Upcoming Meetings</RouterLink></li>
                  <li><RouterLink to="/meeting-details">Meeting Details</RouterLink></li>
                </ul>
              </li>
              <li class="scroll-to-section"><a href="#courses">Courses</a></li>
              <li class="scroll-to-section"><a href="#contact">Contact Us</a></li>
              <li><RouterLink to="/login">Sign In</RouterLink></li>
              <li><RouterLink to="/register">Sign Up</RouterLink></li>
            </ul>
            <a class="menu-trigger"><span>Menu</span></a>
          </nav>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: "MainHeader",
  mounted() {
    this.loadCustomScript();
  },
  methods: {
    loadCustomScript() {
      const script = document.createElement("script");
      script.src = "/assets/js/custom.js";
      script.async = true;
      document.body.appendChild(script);
    },
  },
};
</script>