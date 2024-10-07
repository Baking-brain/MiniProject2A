var quizData = [];

let currentQuestion = 0;
let wrongWords = "";
let correctWords = "";

const questionEl = document.getElementById("question");
const optionsContainer = document.getElementById("options-container");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const endBtn = document.getElementById("endBtn");

document.addEventListener("DOMContentLoaded", getMasteredWords);

var username = window.location.href.split("/");
username = username[username.length - 1];

function loadQuestion() {
  const currentQuizData = quizData[currentQuestion];

  // Set question text
  questionEl.textContent = currentQuizData.question;

  // Clear previous options
  optionsContainer.innerHTML = "";

  // Set new options
  currentQuizData.options.forEach((option, index) => {
    const optionEl = document.createElement("div");
    optionEl.classList.add("option");
    optionEl.innerHTML = `
            <label>
                <input type="radio" name="option" value="${currentQuizData.correct}">
                ${option}
            </label>
        `;
    optionsContainer.appendChild(optionEl);
  });

  // Handle button visibility
  if (currentQuestion === 0) {
    prevBtn.style.display = "none";
  } else {
    prevBtn.style.display = "inline-block";
  }

  if (currentQuestion === quizData.length - 1) {
    nextBtn.style.display = "none";
    endBtn.style.display = "inline-block";
  } else {
    nextBtn.style.display = "inline-block";
    endBtn.style.display = "none";
  }
}

function nextQuestion() {
  //Get current Options
  const options = document.getElementsByName("option");
  // console.log("Options: ", options);
  // console.log("Option value: ", options[0].value);

  //Find selected option
  let selectedoption = "";
  for (let iter = 0; iter < 4; iter += 1) {
    if (options[iter].checked) {
      selectedoption = iter;
    }
  }
  // console.log("Selected option: ", selectedoption);

  //Detemine if answer is correct
  if (selectedoption === "") {
    alert("Please selct a option");
    return;
  } else if (selectedoption === Number(options[0].value)) {
    alert("CORRECT ANSWER");
    correctWords += quizData[currentQuestion].question + " ";
  } else {
    alert("INCORRECT ANSWER");
    wrongWords += quizData[currentQuestion].question + " ";
  }

  if (currentQuestion < quizData.length - 1) {
    currentQuestion++;
    loadQuestion();
  } else {
    endTest();
  }
}

function prevQuestion() {
  if (currentQuestion > 0) {
    currentQuestion--;
    loadQuestion();
  }
}

function endTest() {
  alert(
    "Test completed! Thank you for participating. Your got the answer wrong for following words: \n" +
      wrongWords +
      "\n\nAnd Answered correctly for following words: \n" +
      correctWords
  );
  // You can add any additional functionality here, like submitting answers.
  window.location.href = `http://127.0.0.1:5000/homepage/${username}`;
}

async function getMasteredWords() {
  const wordreq = await fetch(
    `http://127.0.0.1:5000/getmasteredwords/${username}`
  );
  if (!wordreq.ok) {
    alert("RESULT NOT OK!");
    return;
  }
  let words = await wordreq.json();
  console.log("MASTERED WORDS: ", words);

  if (words.error) {
    alert(words.error);
    window.location.href = `http://127.0.0.1:5000/homepage/${username}`;
    return;
  }

  for (let iter = 0; iter < 5; iter += 1) {
    let tempoptions = [
      words[(iter + 1) % 5].meaning,
      words[(iter + 2) % 5].meaning,
      words[(iter + 3) % 5].meaning,
    ];
    let rand = Math.floor(Math.random() * 4);
    tempoptions.splice(rand, 0, words[iter].meaning);

    let tempword = {
      question: words[iter].word,
      options: tempoptions,
      correct: rand,
    };

    quizData.push(tempword);
  }

  console.log("Quiz Data: ", quizData);
  loadQuestion();
}
