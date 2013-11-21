/*===========================
 *实现全屏阅读
 ============================*/
$(function () {

  //元素窗口滚动组件
  $.extend({
    scroll_opt: {
      // unit s
      speed: function() {
        // speed default is 30px/s 
        return parseInt( parseInt( $('body').css('height') ) / 30 * 1000 );
      },
      direction: 'scrollTop',
      destination: function() {
        // destination default is the end of page
        return parseInt( $('body').css('height') );
      }
    }
  });

  $.fn.extend({
    // speed and destination must be a number.
    // direction must be string 'scrollTop' or 'scrollTop'.
    start_scroll: function(direction, speed, destination) {
      var $selected = this;
      var animate_opt = {};

      speed = speed || $.scroll_opt.speed();
      direction = direction || $.scroll_opt.direction;
      destination = destination || $.scroll_opt.destination();
      animate_opt[direction] = destination;

      $selected.each(function() {
        $(this).stop().animate(animate_opt, speed, 'quartic');
      });
    },
    stop_scroll: function() {
      var $selected = this;
      $selected.each(function() {
        this.stop();
      });
    }
  });

  function goto_full_screen() {
  }

  function set_theme(theme_name) {
  }

  var $body = $('body');
  var $book_con = $('.book-con');

  //if data-target exist, it must be a selector of jquery
  //if data-target not exist, it default to be 'body' 
  var $scroll_speed_setter = $('[data-action="scroll"]');
  $scroll_speed_setter.change(function(){
    var $this = $(this);
    var target_selector = $this.attr('data-target') || 'body';
    var $scroll_elem = $(target_selector)
    $scroll_elem.start_scroll();
    return false;
  });

  var $full_screen_trigger = $('[data-action="full-screen"]');
  $full_screen_trigger.click(function () {
    var $this = $(this);
    if ( $body.hasClass('full-screen') ) {
      $this.html('全屏模式');
      $body.removeClass('full-screen');
    } else {
      $this.html('正常模式');
      $body.addClass('full-screen');
    }
  });

  var $theme_setter = $('[data-action="theme"]');
  $theme_setter.change(function () {
    var $this = $(this);
    var theme = $this.val();
    if (theme === 'default') {
      $book_con.removeClass().addClass('book-con');
    } else {
      $book_con.addClass(theme);
    }
  });

  var $fontSizeSetter = $('[data-action="fontSize"]');
  $fontSizeSetter.change(function () {
    var $this = $(this);
    $book_con.find('.main-text').css('font-size', $this.val());
  });
});
