document.addEventListener("DOMContentLoaded", () => {
  // Handle Django messages
  const container = document.getElementById("django-messages");
  if (container) {
    try {
      const messages = JSON.parse(container.dataset.messages);
      messages.forEach(({ text, tag }) => {
        if (tag === "info") {
          alertify.message(text);
        } else if (typeof alertify[tag] === "function") {
          alertify[tag](text);
        } else {
          console.warn(`Unknown alertify tag: ${tag}`);
        }
      });
    } catch (err) {
      console.error("Error parsing Django messages:", err);
    }
  }

  // Handle subscribe button
  const btn = document.getElementById("subscribe");
  if (btn) {
    btn.addEventListener("click", function (e) {
      if (btn.hasAttribute("data-disabled")) {
        e.preventDefault();
        alertify.message("You have already subscribed");
      }
    });
  }
});
