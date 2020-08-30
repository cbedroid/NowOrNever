var test = [];
$(document).ready(() => {
  const is_mobile = /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(
    navigator.userAgent.toLowerCase()
  );

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

  showComingSoon();
});
