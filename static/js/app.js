import { MusicPlayer } from "./musicplayer.js";

$(document).ready(() => {
  const Audio = new MusicPlayer();
  let seekInterval;
  /**********************************
   *****  MUSIC PLAYER **********
   ***********************************/
  const is_mobile = /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(
    navigator.userAgent.toLowerCase()
  );


  /* APPLY STYLE ON MOBILE */
  if (is_mobile)
  {
    $('i a button li .fa').css({ 'cursor': 'pointer' });

    // add mobile class to corresponding element
    // thats using a mobile device
    $('section div ul').each(function (i, e) {
      if ($(e).data('mobile'))
      {
        $(e).removeClass('desktop').addClass('mobile');
        return e;
      }
    });
  }

  // BIND REWIND AND FFWD
  bindSeekEvent("#mp_rewind", -1);
  bindSeekEvent("#mp_fast_forward", 1);
  volumeControl();

  // music play button
  $("#mp_play").on("click", function () {
    if (Audio.init && $(this).hasClass("fa-pause"))
    {
      //then the audio is playing then stop it
      console.log("init paused ");
      Audio.pause();
    } else if (Audio.state["loaded"])
    {
      Audio.play();
    }

    // method: for user pressing play button without selecting track
    if (Audio.init === false || Audio.ended === true)
    {
      // If user did not slect track.. Play first track
      console.log(`Loading Track: ${Audio.src}`);
      const nt = Audio.next_track;
      const auto_selected = nt;
      const loaded = Audio.load(auto_selected);
      if (loaded === true)
      {
        $(".mp-equalizer").removeClass("active");
        const equalizer = $(".mp-equalizer")[nt];

        $(equalizer).addClass("active");
        Audio.play();
      }
    }
  });

  // Set track when track is click
  $(".track-item").on("click", function () {
    $(".mp-equalizer").removeClass("active");
    $(this).find(".mp-equalizer").addClass("active");

    const track = $(this).data("tracknumber");
    if (track !== undefined)
    {
      Audio.load(parseInt(track) - 1);
      Audio.play();
    }
  });

  function setAudioTime (time) {
    // Set Audio Player track time
    Audio.currentTime = time;
  }

  // Rewind track button
  function bindSeekEvent (element, direction) {
    // Bind both rewind and fast forward to mouse click event
    let ct = Audio.currentTime;
    $(element).on("click", () => {
      ct = Audio.currentTime;
      console.log('FIRST CT', ct);
      if (Audio.state["loaded"])
      {
        const SEEK = 5;
        // hint: Direction -1 == rewind  and 1 == fast forward

        /* NOTE: no need to worry setting Audio currentTime over range negative or positive
           The built in audio module will handle this correctly */

        // Bind long-press rewind and fast-forward button for desktop and mobile
        $(element).on("mousedown", () => {
          seekInterval = setInterval(() => {
            if (direction < 0)
            {
              ct = Audio.currentTime - 5;
            } else
            {
              ct = Audio.currentTime + 5
            }

            // TODO: fixed both seek btn when pressed for the first time
            if (ct > 0) setAudioTime(ct.toFixed(2));
          }, 100);
        }); // mousedown
      } // if statement
    }); //clicked

    $(element).on("mouseup", () => {
      /* Remove interval and release Audio.currentTime */
      console.log('SEEK TIME', ct.toFixed(2))
      clearInterval(seekInterval);
      $(element).off("mousedown");
    }); // mouseup
  } // end function bindSeekEvent

  // Bind Volume button
  function volumeControl () {
    $("#volume_btn").on("click", function () {
      const vol_wrap = $("#volume_slider_wrapper");
      $(vol_wrap).css("visibility", "visible");

      $("#volume_slider").on("change", function () {
        Audio.volume = $(this).val();
        console.log(Audio.volume);
      });
      // hide the volume control
      $(vol_wrap).on("mouseleave", () => {
        setTimeout(() => {
          $(vol_wrap).css("visibility", "hidden");
        }, 1000);
      });
    });
  }
}); // READY
