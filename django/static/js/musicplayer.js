var test;
$(document).ready(function () {
  const isMobile = () => {
    if (
      /android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(
        navigator.userAgent
      ) ||
      /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|kllon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(
        navigator.userAgent.substr(0, 4)
      )
    )
      return true;
    return false;
  };

  const Mplayer = function () {
    this._interval;
    this.click = isMobile ? "click" : "touchstart";
    this.tracks = $("#track_list .track");
    this.current_track = $(this.tracks).first();
    this.current_artist = $("#current_artist");
    this.current_title = $("#current_title");
    this.album_viewcount = $("#album_viewcount");
    this.audio = new Audio($(this.current_track).data("song"));
    this.play_btn = $("#play_btn");
    this.play = () => this.audio.play();
    this.stop = () => this.audio.pause();
    this.ffwd = () => (this.audio.currentTime += 5);
    this.rwd = () => (this.audio.currentTime -= 5);
    this.formatTime = (time) => {
      const min = parseInt(time / 60);
      let sec = parseInt(time % 60);
      sec = sec < 10 ? `0${sec}` : sec;
      return `${min}:` + sec;
    };

    /** Create Social Share Button */
    this.createSocialShareLink = () => {
      const facebook = $(".sharelink__facebook");
      const twitter = $(".sharelink__twitter");
      const google = $(".sharelink__goggle");
      //console.log({ facebook, twitter, google });

      // get data from track
      const group = $(this.current_track).data("group");
      const title = $(this.current_track).data("title");
      const song = $(this.current_track).data("song");
      const image = $(this.current_track).data("image");
      if (!group || !image) {
        console.log("Opps..Something went wrong while sharing this song");
        return;
      }
      const postUrl = encodeURI(document.location.href);
      const postOrigin = encodeURI(document.location.origin);
      const postSong = encodeURI(`${postOrigin}${song}`);
      const postTitle = encodeURI(
        `Hi everyone, Check out ${group} new song!\n${group} - ${title}`
      );
      const postImg = encodeURI(`${postOrigin}${image}`);
      //console.log({ postUrl, postSong, postTitle, postImg });

      $(facebook).attr({
        href: `https://facebook.com/sharer.php?quote=${postTitle}&picture=${postImg}&u=${postSong}&display=popup`,
      });
      $(twitter).attr({
        href: `https://twitter.com/share?url=${postUrl}&text=${postTitle}`,
      });
    };

    this.audio.onloadeddata = () => {
      // set title and artist
      const song_artist = $(this.current_track)
        .find(".track__artist-name")
        .text();
      $(this.current_artist).text(song_artist || "");
      $(this.current_title).text($(this.current_track).data("title") || "");

      /* Set Download Button
        const download_btn = $("#btn_plus");
        $(download_btn).attr({
          href: this.audio.src,
          download: artist.trim() + " - " + title.trim(),
        });
      */

      /* Update song views count */
      $("#song_view_form")
        .one("submit", (e) => {
          e.preventDefault();
          const song_view_url = $(this.current_track).data("songref");
          if (!song_view_url) {
            console.log("invalid song playcount", song_view_url);
            return;
          }
          const csrftoken = $('[name="csrfmiddlewaretoken"]').val();
          $.ajax({
            type: "POST",
            url: song_view_url,
            data: {
              csrfmiddlewaretoken: csrftoken,
            },
            success: (resp) => {
              null;
            },
            dataType: "JSON",
          })
            .done((data) => {
              $(this.album_viewcount).text(`${data.data.total_views} views`);
            })
            .fail((e) => {
              console.log("Song view count error", e);
            });
        })
        .submit();
      this.createSocialShareLink();
    };

    this.loadandPlay = ({ currentTarget }) => {
      // load play song
      const track = currentTarget;
      $(this.tracks).removeClass("active");
      const song = $(track).data("song") || undefined;
      $(track).addClass("active");
      if (song === undefined) {
        console.log("Song cant play", song);
        return null;
      }
      this.current_track = track;
      this.audio.src = song;
      this.play();
    };

    this.audio.addEventListener("durationchange", (e) => {
      const duration = this.audio.duration;

      $("#track_end").text(this.formatTime(duration));
      // constantly update progression

      this._interval = setInterval(() => {
        const progress = document.getElementById("progression_bar");
        const progress_width = $(".progression_wrapper")[0].clientWidth;

        const pos = progress_width / this.audio.duration;
        const pos_now = parseInt(this.audio.currentTime * pos);
        progress.style.width = `${pos_now}px`;

        // // updated current track time
        // $("#track_start").text(this.formatTime(this.audio.currentTime));

        // wavesurfer.setCurrentTime(this.audio.currentTime);

        // set the waveform position
      }, 100);
    });

    this.audio.onpause = () => {
      $(this.play_btn)
        .removeClass("far fa-pause-cirle")
        .addClass("far fa-play-circle");
    };
    this.audio.onplaying = () => {
      $(this.play_btn)
        .removeClass("far fa-play-circle")
        .addClass("far fa-pause-circle");
    };
    // this.audio.onloadstart = () => {
    //   setTimeout(() => {
    //     const cover = $("#album_artwork")[0];
    //     const player_bg = is_mobile
    //       ? $("#mobile__toggle-wrapper") // mobile apply to toggler-
    //       : $("#music_player");
    //     matchColor(cover, $(player_bg));
    //   }, 100);
    // };
    this.audioPauseOrPlay = () => {
      if (this.audio.paused === true) {
        this.play();
      } else {
        this.audio.pause();
      }
    };

    this.tracks.bind("click", this.loadandPlay);
    this.play_btn.bind("click", this.audioPauseOrPlay);
  };

  const mplayer = new Mplayer();
  test = mplayer;
}); //ready
