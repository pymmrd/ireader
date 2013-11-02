$(function() {
    var $body = $('body');
    
    $body.on('click.collapse', '[data-toggle="collapse"]', function() {
        var $this = $(this);
        var speed = 'normal';
        var $tar = $($this.attr('data-target'));
        $tar.toggle();
        //if ($tar.css('display') === 'none') {
        //    $tar.slideDown('normal');
        //} else {
        //    $tar.slideUp('normal');
        //}
    });
    
});
