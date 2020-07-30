class MusicPlayer extends Audio {
  constructor(url) {
    super(url);
    this.startEvents();

    if (url) {
      console.log("URL", url);
      this.song = url;
    }
    this.INTERVAL;
  }

  get _song_list() {
    // collect all songs url from DOM
    return $(".song_urls").map(function () {
      return this.value;
    });
  }

  _parseName(track) {
    name = track.match(/\/.*\/(.*\w*).mp3/i)[1];
    return name.replace("_", " ");
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

  load(path) {
    // load audio track
    // If path is a number then get the url from songs_list.
    let url;
    try {
      url = isNaN(path) ? path : this._song_list[parseInt(path)];
    } catch (e) {
      console.error(`${path} is out of tracks range  `, e.message);
      return false;
    }

    this.src = url;
    this.song = url;
    this.url = url;
    return true;
  }

  setDomName() {
    // update the DOM with current track name
    name = this._song;
    if (this.state["ready"] === true) {
      $("#current_track").text(name);
    }
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
    if (this.INTERVAL) {
      clearInterval(this.INTERVAL);
      console.log("INTERVAL CLEARED");
    }
  }

  get state() {
    // return info about the current audio player
    return {
      ready: this.readyState === 4,
      playing: !this.paused,
      paused: this.paused,
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
  }
}
