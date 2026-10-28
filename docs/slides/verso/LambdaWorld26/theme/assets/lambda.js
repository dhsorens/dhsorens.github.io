/**
 * Lambda World theme helpers.
 *
 * 1. On a vertical group, VersoSlides puts the `%%%` metadata (and so
 *    `data-state`) on the group's wrapper, and reveal.js applies a wrapper's
 *    state to every sub-slide. Our lw-* layouts are meant for the opener only,
 *    so move lw-* states from the wrapper onto its first slide.
 * 2. Vertically center lw-title / lw-section / lw-statement slides (the deck
 *    uses `center := false`): reveal.js centers any slide with class `center`.
 *
 * Loaded after Reveal.initialize, so wait for `ready` if needed.
 */
(function () {
  var LAYOUTS = ["lw-title", "lw-section", "lw-statement"];

  function moveGroupLayouts() {
    document.querySelectorAll(".reveal .slides > section[data-state]").forEach(function (stack) {
      var first = stack.querySelector(":scope > section");
      if (!first) return;
      var states = stack.getAttribute("data-state").split(/\s+/);
      var moved = states.filter(function (s) { return LAYOUTS.indexOf(s) >= 0; });
      if (moved.length === 0) return;
      var kept = states.filter(function (s) { return s && moved.indexOf(s) < 0; });
      if (kept.length) stack.setAttribute("data-state", kept.join(" "));
      else stack.removeAttribute("data-state");
      var own = (first.getAttribute("data-state") || "").split(/\s+/).filter(Boolean);
      first.setAttribute("data-state", own.concat(moved).join(" "));
    });
  }

  function centerLayoutSlides() {
    var sel = LAYOUTS.map(function (s) { return '[data-state~="' + s + '"]'; }).join(", ");
    document.querySelectorAll(".reveal .slides section").forEach(function (s) {
      if (s.matches(sel) && !s.querySelector(":scope > section")) s.classList.add("center");
    });
  }

  // reveal.js computed the viewport's state classes before the move above, so
  // keep the lw-* ones in sync with the current slide ourselves (this runs
  // after reveal.js's own update on every slide change).
  function syncViewport() {
    var viewport = Reveal.getViewportElement();
    var current = Reveal.getCurrentSlide();
    LAYOUTS.forEach(function (s) {
      viewport.classList.toggle(s, !!current && current.matches('[data-state~="' + s + '"]'));
    });
  }

  function apply() {
    moveGroupLayouts();
    centerLayoutSlides();
    syncViewport();
    Reveal.on("slidechanged", syncViewport);
    Reveal.layout();
  }

  moveGroupLayouts();
  if (Reveal.isReady()) apply();
  else Reveal.on("ready", apply);
})();
