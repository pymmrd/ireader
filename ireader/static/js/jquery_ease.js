(function($) {
/*!
 * Animation type extension
 * By Steven Yan at 2013-5-9
 */
  $.extend( $.easing, {
    sin: function ( p ) {
      return Math.sin( p*Math.PI/2 );
    },

    triple: function ( p ) {
      return Math.pow( p, 3 );;
    },
    
    quartic: function ( p ) {
      return Math.pow( p, 4 );;
    },
    
    circle: function ( p ) {
      return Math.sqrt(2*p - p*p);
    },
    
    //vibration type
    vibra: function ( p ) {
      var t = 0.5, k = 0.15;
      return p < t ? 
        Math.pow( p/t, 2 ) :
        ( 1 - p )/2 * Math.sin( (p - t)/k*Math.PI ) + 1;
    },
    
    rebound: function ( p ) {
      var t = 0.7, k = 1 - t;
      return p < t ? 
        Math.pow( p/t, 2 ) :
        0.05 * Math.sin( (p - t)/k*Math.PI ) + 1;
    },
    
    //acceleration type
    accel: function ( p ) {
      return Math.pow( p, 2 );
    }
  });
})(jQuery);
