const button = document.getElementById("askButton");
const question = document.getElementById("question");
const statusText = document.getElementById("status");
const result = document.getElementById("result");

button.addEventListener("click", async () => {
  const value = question.value.trim();
  if (value.length < 5) {
    statusText.textContent = "Please enter a research question of at least 5 characters.";
    return;
  }
  button.disabled = true;
  statusText.textContent = "The agents are analyzing, researching, and reviewing...";
  result.classList.add("hidden");
  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: value })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Request failed");
    document.getElementById("answer").textContent = data.answer;
    const list = document.getElementById("sources");
    list.replaceChildren();
    (data.sources || []).forEach(source => {
      const li = document.createElement("li");
      li.textContent = source;
      list.appendChild(li);
    });
    document.getElementById("disclaimer").textContent = data.disclaimer;
    result.classList.remove("hidden");
    statusText.textContent = "Research response ready.";
  } catch (error) {
    statusText.textContent = `Error: ${error.message}`;
  } finally {
    button.disabled = false;
  }
});
