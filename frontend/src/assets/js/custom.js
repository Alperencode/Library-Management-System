
(function ($) {
  "use strict";

  function visible(el, partial) {
    if (!el) return false;

    const $el = $(el);
    if (!$el.length || typeof $el.offset !== 'function') return false;

    const offset = $el.offset();
    if (!offset || typeof offset.top !== 'number') return false;

    const $w = $(window),
      viewTop = $w.scrollTop(),
      viewBottom = viewTop + $w.height(),
      _top = offset.top,
      _bottom = _top + $el.height(),
      compareTop = partial ? _bottom : _top,
      compareBottom = partial ? _top : _bottom;

    return compareBottom <= viewBottom && compareTop >= viewTop;
  }

  $(window).scroll(function () {
    const $digits = $('.count-digit');

    $digits.each(function () {
      const $this = $(this);
      if (visible($this)) {
        if ($this.hasClass('counter-loaded')) return;

        $this.addClass('counter-loaded');
        jQuery({ Counter: 0 }).animate(
          { Counter: $this.text() },
          {
            duration: 3000,
            easing: 'swing',
            step: function () {
              $this.text(Math.ceil(this.Counter));
            },
          }
        );
      }
    });
  });

})(window.jQuery);
