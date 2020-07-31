export class MusicPlayer extends Audio {
  constructor(url) {
    super(url);
    this.init = false;
    this._status = false;
    this.loaded = false;
    this._song = "";
    this._songs_length;
    this.startEvents();

    if (url) {
      console.log("URL", url);
      this.song = url;
    }
    this.INTERVAL;
  }

  get _song_list() {
    // collect all songs url from DOM
    const sl = $(".song_urls").map(function () {
      return this.value;
    });

    console.log(sl);
    this._songs_length = sl.length;
    return sl;
  }

  _parseName(track) {
    try {
      name = track.match(/\/.*\/(.*\w*).mp3/i)[1];
      return name.replace("_", " ");
    } catch {
      return "";
    }
  }

  set song(name) {
    // set track name for DOM
    this.url = name;
    this._song = this._parseName(name);
  }

  get song() {
    // get track name for DOM (NOT FROM DOM)
    return this._song;
  }

  _next_track(set_it) {
    /* Set next available track for future reference 
      *  This is  set incase user is lazy and jst hit the play button again
          We will select next track for them.
      */

    //NOTE: need to rename the dataset "next_track" to something else  for clarity purpose

    /* Step 1:  On every success track load ,--> see load(),  "setter" will set the current track.*/
    /* Step 2: Following that, the logic below will decide what the next available track */

    // Step 1
    if (set_it !== undefined || set_it !== "undefined") {
      //then set CURRENT TRACK
      $("#ctr_next_track").data("next_track", set_it);
    }

    // Step 2
    try {
      const ct = parseInt($("#ctr_next_track").data("next_track"));
      const next_track = ct + 1 < this._songs_length - 1 ? ct + 1 : 0;
      $("#ctr_next_track").data("next_track", next_track);
      console.log("NEXT TRACK", next_track);
    } catch {
      $("#ctr_next_track").data("next_track", 0);
    }
  }

  load(index) {
    this.loaded = false;
    // load audio track
    // If path is a number then get the url from songs_list.
    let url;

    // check if songs are available
    if (this._songs_length === 0) {
      this.setDomName("No Tracks Available");
      this._status = true;
      return false;
    } else if (index > this._songs_length - 1) {
      this.setDomName("Sorry, This Tracks Unavailable");
      this._status = true;
      return false;
    }

    console.log("THIS._SONG_LIST", this._song_list, "\nIndex", index);
    try {
      url = this._song_list[parseInt(index)];
    } catch (e) {
      console.error(`Track ${index} is out of tracks range  `, e.message);
      this._status = true;
      return false;
    }
    console.log("load url", url);
    this.src = url;
    this.song = url;
    this.url = url;
    this.init = true;
    this.loaded = true;
    this._next_track(index);
    return true;
  }

  setDomName(name) {
    // update the DOM with current track name
    $("#current_track").text(name || this._song);
  }

  _clockTime(time) {
    // format time to clock representation

    const min = parseInt(time / 60);
    // 0 blah blah slice  add 0 to number less than 10
    const sec = ("0" + Math.floor(time % 60)).slice(-2);
    return `${min}:${sec}`;
  }

  updateTrackTime() {
    /* Updates the Dom with current track time.
       Updates DOM progress meter.
    */
    const playing =
      this.paused === false && this.ended === false && this.readyState === 4;

    if (playing === true) {
      const MAX_WIDTH = 200; // width of HTML progress bar
      const position = $("#track_position");
      const duration = $("#track_duration");
      const progress_ball = $("#progress_ball");

      const wps = MAX_WIDTH / this.duration; // width per second
      let progress = (wps * this.currentTime).toFixed(2);

      // set DOM track time
      $(position).text(this._clockTime(this.currentTime));
      $(duration).text(this._clockTime(this.duration));

      // set progression bar
      $("#progress_meter").css("width", progress);
      $(progress_ball).css("left", `${Math.floor(progress)}px`);
    }
  }

  pause() {
    super.pause();
    $("#mp_play").removeClass("fa-pause").addClass("fa-play");
    if (this.INTERVAL) {
      clearInterval(this.INTERVAL);
      console.log("INTERVAL CLEARED");
    }
  }

  play() {
    super.play();
    $("#mp_play").removeClass("fa-play").addClass("fa-pause");
    console.log("playing");
  }

  get state() {
    // return info about the current audio player
    return {
      ready: this.readyState === 4,
      playing: !this.paused,
      paused: this.paused,
      loaded: this.loaded,
      song: this.song,
      url: this.url,
    };
  }

  startEvents() {
    const audio = this;
    //play event
    $(audio).on("play", () => {
      this.setDomName();
    });

    // Update DOM with track duration and currentTime
    $(audio).on("timeupdate", () => {
      this.updateTrackTime();
    });

    $(audio).on("ended", () => {
      // change pause button to play
      $("#mp_play").removeClass("fa-pause").addClass("fa-play");

      //TODO: add render next track
    });

    //TODO: Add on error
  }
}