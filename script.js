const quizData = {
  general: [
    { question: "Capital of India?", options: ["Delhi", "Mumbai", "Kolkata", "Chennai"], answer: "Delhi" },
    { question: "Largest ocean?", options: ["Atlantic", "Indian", "Pacific", "Arctic"], answer: "Pacific" },
    { question: "Red Planet?", options: ["Mars", "Earth", "Venus", "Jupiter"], answer: "Mars" },
    { question: "Currency of Japan?", options: ["Yen", "Dollar", "Euro", "Rupee"], answer: "Yen" },
    { question: "Tallest mountain?", options: ["Everest", "K2", "Kangchenjunga", "Lhotse"], answer: "Everest" },
  ],
  science: [
    { question: "H2O is?", options: ["Oxygen", "Hydrogen", "Water", "Salt"], answer: "Water" },
    { question: "Earth revolves around?", options: ["Moon", "Sun", "Mars", "Venus"], answer: "Sun" },
    { question: "Gold symbol?", options: ["Au", "Ag", "Gd", "Go"], answer: "Au" },
    { question: "Organ pumps blood?", options: ["Lungs", "Heart", "Kidney", "Liver"], answer: "Heart" },
    { question: "DNA is found in?", options: ["Nucleus", "Cytoplasm", "Mitochondria", "Ribosome"], answer: "Nucleus" },
  ],
  math: [
    { question: "5 + 3 =", options: ["7", "8", "9", "10"], answer: "8" },
    { question: "12 ÷ 4 =", options: ["2", "3", "4", "6"], answer: "3" },
    { question: "Square root of 49?", options: ["6", "7", "8", "9"], answer: "7" },
    { question: "10 × 2 =", options: ["20", "15", "25", "10"], answer: "20" },
    { question: "15 - 9 =", options: ["5", "7", "6", "9"], answer: "6" },
  ]
};

let currentQuiz = [];
let currentQuestion = 0;
let score = 0;
let timer;
let timeLeft = 15;

const categorySelect = document.getElementById("category");
const startBtn = document.getElementById("start-btn");
const quiz = document.getElementById("quiz");
const questionEl = document.getElementById("question");
const optionsEl = document.getElementById("options");
const nextBtn = document.getElementById("next-btn");
const resultEl = document.getElementById("result");
const scoreEl = document.getElementById("score");
const totalEl = document.getElementById("total");
const timeEl = document.getElementById("time");
const progressBar = document.getElementById("progress-bar");
const restartBtn = document.getElementById("restart-btn");

startBtn.addEventListener("click", startQuiz);
nextBtn.addEventListener("click", nextQuestion);
restartBtn.addEventListener("click", () => location.reload());

function startQuiz() {
  const category = categorySelect.value;
  currentQuiz = quizData[category];
  totalEl.textContent = currentQuiz.length;
  document.getElementById("category-container").style.display = "none";
  quiz.style.display = "block";
  loadQuestion();
}

function loadQuestion() {
  clearInterval(timer);
  resetState();

  const current = currentQuiz[currentQuestion];
  questionEl.textContent = `${currentQuestion + 1}. ${current.question}`;
  current.options.forEach((option) => {
    const button = document.createElement("button");
    button.textContent = option;
    button.addEventListener("click", () => selectAnswer(button, current.answer));
    optionsEl.appendChild(button);
  });

  timeLeft = 15;
  timeEl.textContent = timeLeft;
  timer = setInterval(updateTimer, 1000);
  updateProgress();
}

function resetState() {
  nextBtn.disabled = true;
  optionsEl.innerHTML = "";
  resultEl.textContent = "";
}

function selectAnswer(button, correctAnswer) {
  clearInterval(timer);
  const isCorrect = button.textContent === correctAnswer;
  if (isCorrect) {
    score++;
    button.style.backgroundColor = "#4CAF50";
  } else {
    button.style.backgroundColor = "#f44336";
  }
  scoreEl.textContent = score;

  Array.from(optionsEl.children).forEach((btn) => btn.disabled = true);
  resultEl.textContent = `Your Score: ${score}/${currentQuestion + 1}`;
  nextBtn.disabled = false;
}

function updateTimer() {
  timeLeft--;
  timeEl.textContent = timeLeft;
  if (timeLeft <= 0) {
    clearInterval(timer);
    resultEl.textContent = "Time’s up!";
    Array.from(optionsEl.children).forEach((btn) => btn.disabled = true);
    nextBtn.disabled = false;
  }
}

function nextQuestion() {
  currentQuestion++;
  if (currentQuestion < currentQuiz.length) {
    loadQuestion();
  } else {
    showFinalScore();
  }
}

function updateProgress() {
  const progress = ((currentQuestion + 1) / currentQuiz.length) * 100;
  progressBar.style.width = `${progress}%`;
}

function showFinalScore() {
  quiz.innerHTML = `
    <h2>Quiz Completed 🎉</h2>
    <p>Your final score: ${score} / ${currentQuiz.length}</p>
    <button onclick="location.reload()">Play Again</button>
  `;
}
