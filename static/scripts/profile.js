const editbtn = document.getElementById("edit-btn");
const savebtn = document.getElementById("save-btn");
const fields = document.getElementsByClassName("info-fields");

function editprofile() {
  console.log("Working");
  editbtn.disabled = true;
  savebtn.disabled = false;

  for (let i = 0; i < 3; i += 1) {
    fields[i].disabled = false;
  }
}

async function savechanges() {
  console.log("Working");
  editbtn.disabled = false;
  savebtn.disabled = true;

  for (let i = 0; i < 3; i += 1) {
    fields[i].disabled = true;
  }

  let username = window.location.href.split("/");
  username = username[username.length - 1];

  const payload = {
    username: username,
    fname: document.getElementById("fname").value,
    lname: document.getElementById("lname").value,
  };
  //   console.log(payload);
  const savereq = await fetch(
    `http://127.0.0.1:5000/updateprofile/${username}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }
  );
  if (!savereq.ok) {
    alert("RESULT NOT OK!");
    return;
  }

  alert("Changes Saved!");
}
