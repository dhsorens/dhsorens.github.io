/**
 * Title slide group: Reveal `center` + class `title-slide` for my_theme.css.
 * With `vertical := true`, the first slide is an outer <section> wrapping nested
 * <section> sub-slides — `center` must go on those inners, not only the wrapper.
 */
(function () {
  var orig = Reveal.initialize;
  Reveal.initialize = function (opts) {
    var ret = orig.apply(this, arguments);
    function markTitleSlide() {
      var first = document.querySelector(".reveal .slides > section");
      if (!first) return;
      first.classList.add("title-slide");
      var inners = first.querySelectorAll(":scope > section");
      if (inners.length > 0) {
        inners.forEach(function (s) {
          s.classList.add("center");
        });
      } else {
        first.classList.add("center");
      }
      if (typeof Reveal.layout === "function") {
        Reveal.layout();
      }
    }
    if (ret != null && typeof ret.then === "function") {
      ret.then(markTitleSlide);
    } else {
      markTitleSlide();
    }
    return ret;
  };
})();
