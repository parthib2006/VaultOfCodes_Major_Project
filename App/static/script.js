    const functionSelect = document.getElementById("function");
    const templateSelect = document.getElementById("template");
    const userInput = document.getElementById("user_input");
    const submitBtn = document.getElementById("submit");
    const responseArea = document.getElementById("response_area");
    const responseText = document.getElementById("response_text");
    const status = document.getElementById("status");
    const extrasDiv = document.getElementById("extras");
    let lastLogId = null;

    function renderExtras() {
      const f = functionSelect.value;
      extrasDiv.innerHTML = "";
      if (f === "create") {
        extrasDiv.innerHTML = `
          <label>Style: <input id="extra_style" placeholder="story / poem" /></label>
          <label>Tone: <input id="extra_tone" placeholder="melancholic / hopeful" /></label>
        `;
      } else if (f === "summarize") {
        extrasDiv.innerHTML = `<label>Audience: <input id="extra_audience" placeholder="researcher / manager / student" /></label>`;
      } else {
        extrasDiv.innerHTML = ``;
      }
    }

    functionSelect.addEventListener("change", renderExtras);
    renderExtras();

    submitBtn.addEventListener("click", async () => {
      status.innerText = "Calling assistant...";
      responseArea.classList.add("hidden");
      const payload = {
        function: functionSelect.value,
        template_id: templateSelect.value,
        user_input: userInput.value,
        extra: {}
      };
      // feed extras
      if (document.getElementById("extra_style")) payload.extra.STYLE = document.getElementById("extra_style").value;
      if (document.getElementById("extra_tone")) payload.extra.TONE = document.getElementById("extra_tone").value;
      if (document.getElementById("extra_audience")) payload.extra.AUDIENCE = document.getElementById("extra_audience").value;

      try {
        const r = await fetch("/api/assistant", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify(payload)
        });
        const j = await r.json();
        if (j.ok) {
          responseText.innerText = j.response;
          lastLogId = j.log_id;
          responseArea.classList.remove("hidden");
          status.innerText = "Response received.";
        } else {
          status.innerText = "Error: " + (j.error || "unknown");
        }
      } catch (e) {
        status.innerText = "Request failed: " + e.toString();
      }
    });

    document.getElementById("fb_yes").addEventListener("click", () => sendFeedback(true));
    document.getElementById("fb_no").addEventListener("click", () => sendFeedback(false));

    async function sendFeedback(helpful) {
      if (!lastLogId) {
        alert("No response to give feedback for.");
        return;
      }
      const comment = document.getElementById("fb_comment").value || "";
      try {
        await fetch("/api/feedback", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({log_id: lastLogId, helpful: helpful, comment: comment})
        });
        alert("Thanks for the feedback!");
      } catch (e) {
        alert("Feedback failed: " + e.toString());
      }
    }