function flip() {
  // Toggle visibility of the buttons
  const card = document.getElementById("flipCard");
  const buttonContainer = document.getElementById("buttonContainer");

  card.classList.toggle("is-flipped");
  buttonContainer.classList.toggle("show-buttons");
}

document.addEventListener("DOMContentLoaded", getWords);

var words = [];
var username = "";
var score = 0;
var scores = [];
var userlevel = 1;

//GET WORDS AND USER LEVEL AND SCORE
async function getWords() {
  username = window.location.href.split("/");
  username = username[username.length - 1];

  //GET WORDS REQUEST
  let wordreq = await fetch(`http://127.0.0.1:5000/getwords/${username}`);
  if (!wordreq.ok) {
    console.log("RESULT NOT OK");
    return;
  }
  words = await wordreq.json();
  console.log("Words", words);

  //GET SCORES REQUEST
  let scoresreq = await fetch(`http://127.0.0.1:5000/getscores/${username}`);
  if (!scoresreq.ok) {
    console.log("RESULT NOT OK");
    return;
  }
  scores = await scoresreq.json();
  console.log("Initial Scores: ", scores);

  //GET USERLEVEL REQUEST
  let userlevelreq = await fetch(
    `http://127.0.0.1:5000/getuserlevel/${username}`
  );
  if (!userlevelreq.ok) {
    console.log("RESULT NOT OK");
    return;
  }
  userlevel = await userlevelreq.json();
  console.log("Initial fetch: ", userlevel);

  displayNextWord();
}

let wordIndex = 0;
function displayNextWord() {
  let word = document.getElementById("word");
  let meaning = document.getElementById("meaning");

  word.innerText = words[wordIndex].word;
  meaning.innerText = words[wordIndex].meaning;
}

async function handleAnswer(answer) {
  if (answer === 1) {
    words[wordIndex].correct_answers += 1;

    if (words[wordIndex].box_level < 5) {
      words[wordIndex].box_level += 1;
    }

    score += 100;
    console.log("I KNOW", score);
  } else {
    words[wordIndex].incorrect_answers += 1;

    if (words[wordIndex].box_level > 1) {
      words[wordIndex].box_level -= 1;
    }

    score -= 50;
    console.log("I DON'T KNOW", score);
  }

  //When all words are done
  if (wordIndex === 4) {
    console.log(words);
    alert(`YOUR SCORE IS ${score}`);

    //Decision for adjusting userlevel
    if (score > 300 && userlevel.userlevel < 4) {
      userlevel.userlevel += 1;
    } else if (score < 0 && userlevel.userlevel > 1) {
      userlevel.userlevel -= 1;
    }

    //Update Userlevel
    console.log("Final userlevel: ", userlevel);
    const updateUserlevelReq = await fetch(
      `http://127.0.0.1:5000/updateuserlevel/${username}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userlevel),
      }
    );

    if (!updateUserlevelReq.ok) {
      alert("RESULT NOT OK!");
      return;
    }

    //Update Scores
    scores.score1 = scores.score2;
    scores.score2 = scores.score3;
    scores.score3 = scores.score4;
    scores.score4 = scores.score5;
    scores.score5 = score;
    if (score < 0) {
      scores.score5 = 0;
    }
    console.log("Final scores: ", scores);
    const updateScores = await fetch(
      `http://127.0.0.1:5000/updatescores/${username}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(scores),
      }
    );

    if (!updateScores.ok) {
      alert("RESULT NOT OK!");
      return;
    }

    //Update Words Data
    const updateReq = await fetch(
      `http://127.0.0.1:5000/updatewords/${username}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(words),
      }
    );

    if (!updateReq.ok) {
      alert("RESULT NOT OK!");
      return;
    }

    //Update Streak
    checkStreak();

    window.location.href = `http://127.0.0.1:5000/homepage/${username}`;
    return;
  }

  wordIndex += 1;
  flip();
  await new Promise((r) => setTimeout(r, 500));
  displayNextWord();
}

async function checkStreak() {
  let streakreq = await fetch(`http://127.0.0.1:5000/getstreak/${username}`);
  if (!streakreq.ok) {
    alert("RESULT NOT OK!");
    return;
  }
  let streakdata = await streakreq.json();

  if (!streakdata.laststreak) {
    streakdata.laststreak = new Date();
    streakdata.streak_count = 1;
  } else {
    let laststreak = new Date(streakdata.laststreak).getTime();
    let now = new Date().getTime();
    if (now - laststreak > 2 * 86400000) {
      streakdata.laststreak = new Date();
      streakdata.streak_count = 1;
    } else if (now - laststreak > 86400000) {
      streakdata.laststreak = new Date();
      streakdata.streak_count += 1;
    }
  }

  console.log("Final Streak: ", streakdata);

  let updatestreak = await fetch(
    `http://127.0.0.1:5000/updatestreak/${username}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(streakdata),
    }
  );

  if (!updatestreak.ok) {
    alert("RESULT NT OK!");
    return;
  }
}
