---
layout: default
title: BWV 1006
---

# J.S. Bach – BWV 1006 (Rendered with Verovio)

<div id="notation"></div>

<script src="https://www.verovio.org/javascript/app/verovio-app.js"></script>
<script>
  document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("notation");
    const app = new verovio.app(container, {
      defaultView: 'responsive',
      defaultZoom: 3
    });
    app.loadFile("bwv1006_simple.xml");
  });
</script>
