$(document).ready(() => {
  // Sticky nav to fixed for desktop
  const nav_container = $("#main_nav_container");
  const height = $("#main_nav_container").height();
  console.log("Height", height);
  const bs_nav = $("#main_nav"); //bootstrap navv
  let fired = false;

  /* MODAL */
  // const md_upcoming = $("#modal_upcoming");
  // $(md_upcoming).modal("show");

  // $(window).on("scroll", function () {
  //   console.log("Scroller running");
  //   console.log("SCROLLER", $(this).scrollTop());
  //   if (!fired) {
  //     if ($(this).scrollTop() > height) {
  //       fired = true;
  //       console.log("changed");
  //       $(bs_nav)
  //         .removeClass("sticky-top")
  //         .addClass("override-nav-fixed fixed");
  //       fired = true;
  //     } else {
  //       console.log("changed back ");

  //       $(bs_nav).removeClass("override-nav-fixed").addClass("sticky_top");
  //     }
  //   }
  //   window.setTimeout(() => {
  //     fired = false;
  //   }, 200);
  // });
});
