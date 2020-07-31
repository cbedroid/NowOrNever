import { MusicPlayer } from "./musicplayer.js";

var test;
$(document).ready(() => {
  const Audio = new MusicPlayer();
  /**********************************
   *****  MUSIC PLAYER **********
   ***********************************/

  // music play button
  $("#mp_play").on("click", function () {
    if (Audio.init && $(this).hasClass("fa-pause")) {
      //then the audio is playing then stop it
      console.log("init ipaused ");
      Audio.pause();
    }

    if (Audio.init === false) {
      // user did not slect track.. Play first track
      console.log("Loading Track first time");
      const loaded = Audio.load(0);
      if (loaded === true) Audio.play();
    }
  });

  test = Audio;
}); // READY
