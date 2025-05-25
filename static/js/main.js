
let questions = [];

window.onload = async () => {
  const res = await fetch('/api/questions');
  questions = await res.json();
  loadQuiz();
};

function loadQuiz() {
  const quizDiv = document.getElementById('quiz');
  quizDiv.innerHTML = '';
  questions.forEach((q, idx) => {
    const qDiv = document.createElement('div');
    qDiv.innerHTML = `<p>${idx + 1}. ${q.question}</p>`;
    q.options.forEach(opt => {
      qDiv.innerHTML += `
        <label>
          <input type="radio" name="q${q.id}" value="${opt}"> ${opt}
        </label><br>`;
    });
    quizDiv.appendChild(qDiv);
  });
}

async function submitQuiz() {
  const answers = {};
  questions.forEach(q => {
    const selected = document.querySelector(`input[name="q${q.id}"]:checked`);
    if (selected) {
      answers[q.id] = selected.value;
    }
  });

  const res = await fetch('/api/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ answers })
  });

  const result = await res.json();
  document.getElementById('result').innerText =
    `You scored ${result.score} out of ${result.total}`;
}
