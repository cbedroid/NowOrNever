var test = [];
$(document).ready(() => {

  function showComingSoon () {
    // show modal base on datetime of user last visit

    const cs_modal = $('#modal_upcoming');
    const data = {};
    const vph = 1000 * 60 * 60;
    //* 60; // visit per hour
    const today = new Date().getTime();
    let last_shown = localStorage.getItem('last_shown');
    let time_shown;
    test.push(today, last_shown, vph);
    let show = false;

    if (!last_shown)
    {
      localStorage.setItem('last_shown', today);
      last_shown = today;
    } else
    {
      time_shown = today - parseInt(last_shown);
      time_shown >= vph ? show = true : show = false
    }

    if (show === true)
    {
      // set timeout 5 seconds then show modal
      setTimeout(() => {
        $(cs_modal).modal('show');
        localStorage.setItem('last_shown', today);
      }, 5000);
      console.log('showing coming soon');
    }
    else
    {
      console.log('not yet time', time_shown, vph);
      const nt = new Date(parseInt(last_shown) + vph)
      console.log('next_time', nt);
    }


  }

  showComingSoon();
})