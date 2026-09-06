"use strict";
/* THE ROUTER — five screens, and the Back button that walks them.
 *
 *   pages    the three scrolling pages: the statement, the philosophy, the machine
 *   machine  inside the Macintosh, looking at the folder
 *   doc      one of the seven files, open in the window
 *
 * WHAT IS ADDRESSABLE, AND WHAT IS NOT.
 *
 * Six documents carry a hash, so a link to one opens it. FINAL DOES NOT. Oran ruled that the
 * ending has no address — "המטרה שהוא יחפור במסמך על מנת לגלות אותם" — because it is meant to
 * be reached by working through the file, not by being handed a link to the contact details.
 *
 * So opening READ ME pushes a history entry with no change of URL. Back still walks out of it,
 * because history is a stack of states and only some of them happen to have addresses. This is
 * why build check 4 was rewritten one-way: every URL must resolve to a state, but a state is
 * not required to have a URL. The old two-way check would have refused to build this.
 *
 * ONE STATE OBJECT, ONE APPLY. Every path in and out goes through go() and render(), so there
 * is no second place where the shell can be turned on. The bug that costs a day in a router is
 * two code paths that both half-know how to open something.
 */
(function () {
  var DOCS = (window.KIT && window.KIT.order) ? window.KIT.order.slice() : [];
  var SILENT = "final";                     /* the one file with no address */
  var html = document.documentElement;

  var state = { screen: "pages", id: null };
  var applying = false;

  function hashFor(s) {
    if (s.screen === "machine") { return "#machine"; }
    if (s.screen === "doc" && s.id && s.id !== SILENT) { return "#" + s.id; }
    return "";                              /* pages, and the ending, carry no hash */
  }

  function stateFromHash() {
    var h = (location.hash || "").replace(/^#/, "");
    if (h === "machine") { return { screen: "machine", id: null }; }
    if (h && DOCS.indexOf(h) >= 0 && h !== SILENT) { return { screen: "doc", id: h }; }
    return { screen: "pages", id: null };
  }

  /* ---------------------------------------------------------------- rendering a state */
  function enterShell() {
    if (html.classList.contains("mw-on")) { return; }
    html.classList.add("mw-on");
    if (typeof window.__shellInit === "function") { window.__shellInit(); }
  }

  function leaveShell() {
    if (!html.classList.contains("mw-on")) { return; }
    if (typeof shut === "function") { shut(); }
    html.classList.remove("mw-on");
  }

  function render(s) {
    applying = true;
    try {
      if (s.screen === "pages") {
        leaveShell();
      } else {
        enterShell();
        if (s.screen === "doc" && s.id) {
          if (typeof show === "function") { show(s.id); }
        } else if (typeof shut === "function") {
          shut();
        }
      }
    } finally { applying = false; }
  }

  /* ---------------------------------------------------------------- moving between them */
  function go(screen, id, replace) {
    var next = { screen: screen, id: id || null };
    if (next.screen === state.screen && next.id === state.id) { return; }
    state = next;
    var url = location.pathname + location.search + hashFor(next);
    try {
      if (replace) { history.replaceState(next, "", url); }
      else { history.pushState(next, "", url); }
    } catch (e) { /* file:// and other opaque origins refuse pushState; the shell still works */ }
    render(next);
  }

  window.addEventListener("popstate", function (e) {
    var s = (e.state && e.state.screen) ? e.state : stateFromHash();
    state = { screen: s.screen, id: s.id || null };
    render(state);
  });

  /* ---------------------------------------------------------------- the doors */

  /* into the machine — page 3 calls this when the reader clicks the screen */
  window.__enterMachine = function () { go("machine", null); };

  /* out of it — the folder's own close box */
  window.__mwExit = function () { go("pages", null); };

  /* a file opens. The folder calls show() directly, so this is how the router hears about it
     rather than being the thing that did it: one state object, updated from wherever the open
     actually happened. */
  window.__mwOpened = function (id) {
    if (applying) { return; }
    go("doc", id);
  };

  /* and closes, back to the folder rather than out of the machine — Oran: "חוזר לתיקייה
     כאשר לוחצים על BACK", and the X replaced BACK. */
  window.__mwClosed = function () {
    if (applying) { return; }
    if (state.screen === "doc") { go("machine", null); }
  };

  /* ---------------------------------------------------------------- arriving with a hash */
  var first = stateFromHash();
  if (first.screen !== "pages") {
    /* replace, not push: the address the reader arrived at is where they are, and Back should
       leave the site rather than walk into a state they never visited. */
    window.addEventListener("load", function () {
      setTimeout(function () { go(first.screen, first.id, true); }, 60);
    });
  } else {
    try { history.replaceState(state, "", location.pathname + location.search); } catch (e) { }
  }
})();
