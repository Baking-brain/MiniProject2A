function logout() {
  let action = confirm("Are You Sure?");
  if (action) {
    togglemenu();
    window.location.href = "http://127.0.0.1:5000/";
  }
}

let submenu = document.getElementById("submenu");
var username = "";

function togglemenu() {
  submenu.classList.toggle("open-menu");
}

document.addEventListener("DOMContentLoaded", getstreak);

async function getstreak() {
  username = window.location.href;
  username = username.split("/");
  username = username[username.length - 1];

  let streakreq = await fetch(`http://127.0.0.1:5000/getstreak/${username}`);
  if (!streakreq.ok) {
    alert("RESULT NOT OK!");
    return;
  }

  let streak = await streakreq.json();
  document.getElementById("streakdays").innerText = streak.streak_count;
}

function openLearn() {
  // console.log(username);
  window.location.href = `http://127.0.0.1:5000/learn/${username}`;
}

function openReview() {
  // console.log(username);
  window.location.href = `http://127.0.0.1:5000/review/${username}`;
}

function openStats() {
  // console.log(username);
  window.location.href = `http://127.0.0.1:5000/stats/${username}`;
}

function openProfile() {
  // console.log(username);
  togglemenu();
  window.location.href = `http://127.0.0.1:5000/profile/${username}`;
}
