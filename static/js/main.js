var test = [];
$(document).ready(() => {
  const is_mobile = /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(
    navigator.userAgent.toLowerCase()
  );

  // FOR MOBILE DEVICE
  // Reference: https://gomakethings.com/how-to-simulate-a-click-event-with-javascript/
  // var simulateClick = function (elem) {
  //   // Create our event (with options)
  //   var evt = new MouseEvent("click", {
  //     bubbles: true,
  //     cancelable: true,
  //     view: window,
  //   });
  //   // If cancelled, don't dispatch our event
  //   var canceled = !elem.dispatchEvent(evt);
  // };

  /* TOGGLE ACTIVE CLASS FOR NAVIGATION ON PAGE REFRESH */
  function activeNavLink() {
    const mainlinks = $("#main_nav_list li");

    $(mainlinks).map(function () {
      const link_location = $(this).find("a").attr("href");
      if (link_location == "/") {
        // for home page link
        $(mainlinks).removeClass("active");
        $(mainlinks).first().addClass("active");
      } else if (window.location.href.includes(link_location)) {
        $(mainlinks).removeClass("active");
        $(this).addClass("active");
      }
    });
  }
  activeNavLink();

  /*HEADER BOX SHADOW ON SCROLL */
  $(window).scroll(function () {
    var scroll = $(window).scrollTop();
    if (scroll > 0) {
      $("#main_header_nav").addClass("active");
    } else {
      $("#main_header_nav").removeClass("active");
    }
  });

  /* APPLY STYLE ON MOBILE DEVICE */
  if (is_mobile) {
    // For mobile, hide "mobile-hidden" class on page load
    $(".mobile-hidden").hide();

    $("i a button li .fa").css({ cursor: "pointer" });

    // add mobile class to corresponding element
    // that is using a mobile device
    $("section div ul").each(function (i, e) {
      if ($(e).data("mobile")) {
        $(e).removeClass("desktop").addClass("mobile");
        return e;
      }
    });
  } else {
    // HIDE STYLE FOR DESKTOP
    $(".desktop-hidden").hide();
  }

  /* MOBILE HIDE MAIN NAVIGATION ON TOUCH */
  $("body").on("click", () => {
    $(".navbar-collapse").collapse("hide");
  });

  //Fixed bootstrap 4 collaspe not working on mobile
  let is_open = false;
  $(".navbar-toggler").on("click", function (e) {
    e.preventDefault();
    e.stopPropagation();
    const nb = $(".navbar-collapse");
    const display = { false: "block", true: "none" }[is_open];
    $(nb).css("display", display);
    $(this).attr("aria-expanded", is_open == false ? true : false);
    is_open = !is_open;
  });

  // Bootstrap alert fade out
  setTimeout(function () {
    $("#alert_message").alert("close");
  }, 2500);

  /* MOBILE PROFILE FORMS TOGGLE */
  $(".pf-toggler").on("click", function (e) {
    e.preventDefault();
    $(".form-wrapper").hide(200);
    const pform = $(this).data("toggle");
    $(pform).show(1000);
  });

  function showComingSoon() {
    // show modal base on datetime of user last visit

    const cs_modal = $("#modal_upcoming");
    const data = {};
    const vph = 1000 * 60 * 60; //show modal  every hour
    //* 60; // visit per hour
    const today = new Date().getTime();
    let last_shown = localStorage.getItem("last_shown");
    let time_shown;
    test.push(today, last_shown, vph);
    let show = false;

    if (!last_shown) {
      localStorage.setItem("last_shown", today);
      last_shown = today;
    } else {
      time_shown = today - parseInt(last_shown);
      time_shown >= vph ? (show = true) : (show = false);
    }

    if (show === true) {
      // set timeout 5 seconds then show modal
      setTimeout(() => {
        $(cs_modal).modal("show");
        localStorage.setItem("last_shown", today);
      }, 5000);
    } else {
      const nt = new Date(parseInt(last_shown) + vph);
    }
  }

  $(".featured .thumb-container").on("click", function () {
    $(this).hide();
    $("#ft_video").find("iframe", "video")[0].src += "?autoplay=1";
    if (is_mobile) {
      // send press event to youtube play button
      // work around for youtube blocking autoplay
      const ytb = $(".html5-video-player");
      //simulateClick(ytb);
    }
  });
  // video thumbnail from carousel video hide on click
  $(".vc-vid").on("click", function (e) {
    e.preventDefault();
    $(".vc-vid").removeClass("active");
    $(this).toggleClass("active");

    // make sure all carousel thumb ae still showing
    $(".vc-thumb").css({ visibility: "visible" });
    // grab the src from the clicked video
    const src = $(this).find("iframe", "video")[0].src;

    // play video on featured main video spot
    // remove thumbcover from featured video
    const vc_title = $(this).find(".m-title").text();
    const lg_description = $(this).find(".vc-lg-description").text();
    $("#featured_title").text(vc_title);
    $("#featured_thumbcover").hide();
    $("#featured_vid")[0].src = src + "?autoplay=1";
    $("#featured_long_decription").text(lg_description);
  });
  showComingSoon();
});
