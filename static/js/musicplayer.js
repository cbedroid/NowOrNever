export class MusicPlayer extends Audio {
  constructor(url) {
    super(url);
    this.init = false;
    this._status = false;
    this.loaded = false;
    this._song = "";
    this._songs_length;
    this._next_track = 0;
    this.startEvents();
    // Set audio progress width  according to musicplayer container width
    let pw = $('#main_musicplayer').innerWidth();
    this._PROGRESS_WIDTH = parseInt(pw / 3);
    console.log('PW', this._PROGRESS_WIDTH);
    $('#mp_progress').width(this._PROGRESS_WIDTH)
    //this.PROGRESS_WIDTH = 200; // width of HTML progress bar


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

    this._songs_length = sl.length;
    return sl;
  }

  _parseName(track) {
    try {
      //name = track.match(/\/.*\/(.*\w*).mp3/i)[1];
      //name = track.match(/\-\s*(.*.mp3)/i)[1];
      name = track.match(/audio\/*(.*.mp3)/i)[1];
      return name.replace("/s/gi", "_");
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
  get next_track() {
    return this._next_track !== undefined ? parseInt(this._next_track) : 0;
  }

  set next_track(set_it) {
    /* Set next available track for future reference 
      *  This is  set incase user is lazy and jst hit the play button again
          We will select next track for them.
      */

    //NOTE: need to rename the dataset "next_track" to something else  for clarity purpose

    /* Step 1:  On every success track load ,--> see load(),  "setter" will set the current track.*/
    /* Step 2: Following that, the logic below will decide what the next available track */

    // Step 1  Getting current track index for next step
    if (set_it !== undefined || set_it !== "undefined" || !isNaN(set_it)) {
      //then set CURRENT TRACK
      $("#ctr_next_track").data("next_track", set_it);
    }

    // Step 2 Add current track by 1 to get next track.
    try {
      const ct = parseInt($("#ctr_next_track").data("next_track"));

      // if track out of range then reset to 0
      const next_track = ct + 1 <= this._songs_length - 1 ? ct + 1 : 0;

      // update the DOM with new  next trac
      $("#ctr_next_track").data("next_track", next_track);

      console.log("NEXT TRACK", next_track);
    } catch (e) {
      // on failure , just next track to  reset it to 0
      consol.log("Next track failed", e.message);
      $("#ctr_next_track").data("next_track", 0);
    }

    // Save next track for internal usage
    this._next_track = $("#ctr_next_track").data("next_track");
  }

  load(index) {
    this.loaded = false;
    // load audio track
    // If path is a number then get the url from songs_list.
    let url;

    // if "index" argument is not pass, then
    // just load next track

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

    try {
      url = this._song_list[parseInt(index)];
    } catch (e) {
      console.error(`Track ${index} is out of tracks range  `, e.message);
      this._status = true;
      return false;
    }
    this.src = encodeURI(url);
    this.song = url;
    this.url = url;
    this.init = true;
    this.loaded = true;
    this.next_track = index;
    return true;
  }

  setDomName(name) {
    // update the DOM with current track name
    const name_of_track = name || this._song;
    $("#current_track").text(name_of_track);
    console.log("Current Song", name_of_track);
  }


  _clockTime(time) {
    // format time to clock representation

    const min = parseInt(time / 60);
    // 0 blah blah slice  add 0 to number less than 10
    const sec = ("0" + Math.floor(time % 60)).slice(-2);
    return `${min}:${sec}`;
  }

  pause() {
    super.pause();
    $("#mp_play").removeClass("fa-pause").addClass("fa-play");
    if (this.INTERVAL) {
      clearInterval(this.INTERVAL);
    }
  }

  play() {
    $("#mp_play").removeClass("fa-play").addClass("fa-pause");
    return super.play();
  }

  updateTrackTime() {
    /* Updates the Dom with current track time.
       Updates DOM progress meter.
    */
    const AUDIO = this;
    const playing =
      this.paused === false && this.ended === false && this.readyState === 4;

    if (playing === true) {
      const position = $("#track_position");
      const duration = $("#track_duration");
      const progress_val = $("#progress_meter").val();

      const wps = this._PROGRESS_WIDTH / this.duration; // width per second
      //let progress = (wps * this.currentTime).toFixed(2)
      let progress = (wps * this.currentTime);

      // set DOM track time
      $(position).text(this._clockTime(this.currentTime));
      $(duration).text(this._clockTime(this.duration));

      // set progression bar
      $("#progress_meter").val(progress);
      //console.log('Progress',progress);

      // set pressball drag event
      $("#progress_meter").on("mousedown", function () {AUDIO.pause()});
      $('#progress_meter').on("mouseup",()=>{
        const pg_val = $("#progress_meter").val();
        //console.log("dragging", pg_val * wps );
        this.currentTime =  pg_val * wps;
        $(this).val(`${Math.floor(pg_val * wps)}`);
          AUDIO.play();
      });


    }
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
      this.setDomName(this._song);
    });

    // Update DOM with track duration and currentTime
    $(audio).on("timeupdate", () => {
      this.updateTrackTime();
    });

    $(audio).on("ended", () => {
      // unloaded track
      this.loaded = false;
      // change pause button to play
      $("#mp_play").removeClass("fa-pause").addClass("fa-play");

      //TODO: add render next track
      this.load(this.next_track);
    });

    //TODO: Add on error
  }
}
