import { MusicPlayer } from "./musicplayer.js";
var was_playing = [];
$(document).ready(function () {
  const audio_tracks = $(".mp_audio");
  const track_list = $(".track-list");
  let CURRENT_TRACK;

  // AUDIO PLAYER
  function stopAll(audio) {
    $(audio).each(function () {
      try {
        this.pause();
      } catch (e) {
        console.log("E", e.message);
      }
    });
  }

  function musicProgress(track) {
    const meter = $("#progress_meter");
    const ball = $("#progress_ball");
    const max_width = 200; // width of progress bar

    const playing = track.paused === false && track.ended === false;
    const wps = max_width / track.duration; // width per second

    if (playing) {
      // update the progress bar
      let progress = (wps * track.currentTime).toFixed(2);
      console.log("PROGRESS", progress);
      const track_total = track.duration;
      $(meter).css("width", progress);
      $(ball).css("left", `${progress}px`);

      // update track time
      const cp = (track.currentTime / 60).toFixed(2);
      const tt = (track.duration / 60).toFixed(2);
      $("#track_duration").text(tt);
      $("#track_position").text(cp);
    }
    //update DOM with track duration
  }

  /* MUSIC CONTROLS */
  function musicControls(player) {
    // change play button to pause
    const play_btn = $("#mp_play");

    $(play_btn).toggleClass("fa-pause");

    /**** PLAY PAUSE STOP *****/

    $(play_btn).click(function () {
      const was_playing = player.paused === false && player.ended === false;

      // change the play to stop .. vice versa
      if (was_playing) {
        $(this).removeClass("fa-pause").addClass("fa-play");
        player.pause();
      } else {
        // resume current track
        player.play();
        $(this).removeClass("fa-play").addClass("fa-pause");
      }
    });
  }

  function audioPlay(track) {
    // kill all tracks on startup
    stopAll(audio_tracks);
    // Reset play button
    $("#mp_play").removeClass("fa-stop");
    // Play song
    was_playing.push(track);
    track.play().then(function () {
      musicControls(track);
      CURRENT_TRACK = track;
    });
    test = track;
  }

  $(track_list).click(function () {
    // list-items
    const current_track = $(this).find("audio")[0];
    console.log("Track", current_track);

    // Toggle tracks's equalizer class  active
    $(track_list).each(function () {
      $(this).find("i.active").removeClass("active");
    });

    $(this).find("i").toggleClass("active");
    audioPlay(current_track);
  });

  setInterval(() => {
    if (CURRENT_TRACK !== undefined) {
      musicProgress(CURRENT_TRACK);
    }
  }, 500);
}); // READY
