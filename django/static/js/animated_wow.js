$(document).ready(() => {
  String.prototype.format = function () {
    var i = 0,
      args = arguments;
    return this.replace(/{}/g, function () {
      return typeof args[i] != "undefined" ? args[i++] : "";
    });
  };

  new WOW({
    boxClass: "wow", // default
    animateClass: "animated", // default
    offset: 0, // default
    mobile: true,
    live: true, // default
  }).init();
});
