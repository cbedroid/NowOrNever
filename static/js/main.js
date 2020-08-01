import { MusicPlayer } from "./musicplayer.js";

var test;
$(document).ready(() => {
  const Audio = new MusicPlayer();
  let seekInterval;
  test = Audio;
  /**********************************
   *****  MUSIC PLAYER **********
   ***********************************/
  // BIND REWIND AND FFWD

  bindSeekEvent("#mp_rewind", -1);
  bindSeekEvent("#mp_fast_forward", 1);
  volumeControl();

  // music play button
  $("#mp_play").on("click", function () {
    if (Audio.init && $(this).hasClass("fa-pause")) {
      //then the audio is playing then stop it
      console.log("init paused ");
      Audio.pause();
    } else if (Audio.state["loaded"]) {
      Audio.play();
    }

    // user press play button without selecting track
    if (Audio.init === false || Audio.ended === true) {
      // user did not slect track.. Play first track
      console.log(`Loading Track: ${Audio.src}`);
      const auto_selected = Audio.next_track;
      const loaded = Audio.load(auto_selected);
      if (loaded === true) Audio.play();
    }
  });

  // Set track when track is click
  $(".track-item").click(function () {
    $(".mp-equalizer").removeClass("active");
    $(this).find(".mp-equalizer").addClass("active");

    const track = $(this).data("tracknumber");
    if (track !== undefined) {
      Audio.load(parseInt(track) - 1);
      Audio.play();
    }
    console.log({ track });
  });

  function setAudioTime(time) {
    console.log("TIMER", time);
    Audio.currentTime = time;
  }

  // Rewind track button
  function bindSeekEvent(element, direction) {
    // Bind both rewind and fast forward to mouse click event

    $(element).on("click", () => {
      let ct = Audio.currentTime;
      if (Audio.state["loaded"]) {
        const SEEK = 5; // five second SEEK
        // Direction -1 == rewind  and 1 == fast forward

        const seek = direction < 0 ? -SEEK : SEEK;
        /* NOTE: no need to worry setting Audio currentTime over range negative or positive
           The built in audio module will handle this correctly */
        ct += seek;
        setAudioTime(ct);

        $(element).on("mousedown", () => {
          seekInterval = setInterval(() => {
            ct = Audio.currentTime;
            ct += seek;
            console.log("MouseDown", ct);
            setAudioTime(ct);
          }, 100);
        }); // mousedown
      } // if statement
    }); //clicked

    $(element).on("mouseup", () => {
      /* Remove interval and release Audio.currentTime */
      clearInterval(seekInterval);
      $(element).off("mousedown");
      console.log("interval cleared");
    }); // mouseup
  } // end function bindSeekEvent

  // Bind Volume button
  function volumeControl() {
    $("#volume_btn").click(function () {
      console.log("clicked");
      const vol_wrap = $("#volume_slider_wrapper");
      $(vol_wrap).show();

      $("#volume_slider").on("change", function () {
        Audio.volume = $(this).val();
        console.log($(this).val());
      });
      // hide the volume control
      $(vol_wrap).on("mouseleave", () => {
        console.log("leaving volume");
        setTimeout(() => {
          $(vol_wrap).hide(1500);
        }, 1000);
      });
    });
  }
}); // READY
