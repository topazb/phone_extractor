function showInfoPopup() {
      const infoPopup = document.getElementById('infoPopup');
      infoPopup.style.display = 'block';
      const infoButton = document.querySelector('.info-button');
      infoButton.classList.add('clicked');
    }

    function hideInfoPopup() {
      const infoPopup = document.getElementById('infoPopup');
      infoPopup.style.display = 'none';
      const infoButton = document.querySelector('.info-button');
      infoButton.classList.remove('clicked');
    }

function displayLoadingAnimation() {
  document.getElementById("loadingDiv").style.display = "block";
  document.getElementById("result").style.display = "none";
}

function hideLoadingAnimation() {
  document.getElementById("loadingDiv").style.display = "none";
  document.getElementById("result").style.display = "block";
}


function processText() {
  // Show loading animation
  displayLoadingAnimation();

  const text1 = document.getElementById("text1").value;
  if (!text1) {
     // Hide loading animation
    hideLoadingAnimation();

    alert("אנא הזן את קבוצת הוואטסאפ המלאה");
    return;
  }

  const text2 = document.getElementById("text2").value;
  const numLists = document.getElementById("numLists").value;
  const excludeNumbers = numbers; // Retrieve the numbers from the 'numbers' array

  const data = { text1, text2, num_lists: parseInt(numLists), exclude_numbers: excludeNumbers };

  fetch("https://p01--phone-extractor--rzfktjl4by88.code.run//process_text", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
  .then(response => {
    if (!response.ok) {
      throw new Error("שגיאה בעיבוד הטקסט. אנא נסה שוב.");
    }
    return response.json();
  })
  .then(result => {
    // Hide loading animation
    hideLoadingAnimation();
    displayResult(result);
  })
  .catch(error => {
    // Hide loading animation
    hideLoadingAnimation();
    displayError(error.message);
  });
}


function displayResult(result) {
  const textareaDiv = document.getElementById("textareaDiv");
  textareaDiv.innerHTML = ""; // Clear the textareaDiv

  const outputDiv = document.getElementById("outputDiv");
  outputDiv.innerHTML = ""; // Clear the outputDiv

  const numPhones = result.num_phones;
  const phoneLists = result.phone_lists;
  const list2Length = result.list2_length;
  const list2 = result.text2_items;
  const countSubtracted = result.count_subtracted; // Count Subtracted
  const countAttendees = result.count_attendees; // Corrected: Count of Attendees

  const listsTextarea = document.createElement("textarea");
  listsTextarea.classList.add("ltr-text");
  listsTextarea.style.height = "150px"; // Adjust the height as needed (e.g., set it to "150px")
  // If list2 is empty or undefined, create default group names: "group 1", "group 2", ...
  const groupNames = list2 && list2.length > 0 ? list2 : Array.from({ length: list2Length }, (_, i) => `group ${i + 1}`);
  const formattedLists = phoneLists.map((list, index) => `*${groupNames[index] || `group ${index + 1}`}:*\n${list.join("\n")}`).join("\n\n");

  listsTextarea.value = formattedLists.trim(); // Remove leading/trailing empty lines
  textareaDiv.appendChild(listsTextarea);

  // Create the copy button inside the textareaDiv
  const copyButtonContainer = document.createElement("div");
  copyButtonContainer.classList.add("copy-button-container");
  textareaDiv.appendChild(copyButtonContainer);

  const copyButton = document.createElement("button");
  copyButton.classList.add("button", "copy-button");
  copyButton.textContent = "העתק";
  copyButton.addEventListener("click", copyLists);
  copyButtonContainer.appendChild(copyButton);

  const numPhonesMsg = `סה"כ בקבוצה: ${numPhones}`;
  const numPhonesNode = document.createElement("p");
  numPhonesNode.textContent = numPhonesMsg;
  outputDiv.appendChild(numPhonesNode);

  const countAttendeesMsg = `סה״כ מודרכים: ${countAttendees}`; // Display count of attendees
  const countAttendeesNode = document.createElement("p");
  countAttendeesNode.textContent = countAttendeesMsg;
  outputDiv.appendChild(countAttendeesNode);

  const list2LengthMsg = `סה״כ מדריכים: ${list2Length}`;
  const list2LengthNode = document.createElement("p");
  list2LengthNode.textContent = list2LengthMsg;
  outputDiv.appendChild(list2LengthNode);

  const dateTimeNode = document.createElement("p");
  const currentDateTime = new Date();
  const formattedDateTime = currentDateTime.toLocaleString("he-IL");
  dateTimeNode.textContent = formattedDateTime;
  outputDiv.appendChild(dateTimeNode);
}


function copyLists() {
  const listsTextarea = document.querySelector("#result textarea");
  listsTextarea.select();

  // Copy the content to the clipboard using the Clipboard API
  navigator.clipboard.writeText(listsTextarea.value)
    .then(() => {
      console.log("Content copied to clipboard");
    })
    .catch((error) => {
      console.error("Failed to copy content to clipboard:", error);
    });
}

let numbers = [];

function displayNumbers() {
  const numberListElement = document.getElementById('numberList');
  numberListElement.innerHTML = '';

  for (const number of numbers) {
    const listItem = document.createElement('li');

    const numberText = document.createTextNode(number);
    listItem.appendChild(numberText);

    listItem.appendChild(document.createTextNode(' ')); // Add a space

const removeButton = document.createElement('button');
removeButton.textContent = '-';
removeButton.id = 'removeButton'; // Add the ID attribute to the button
removeButton.addEventListener('click', () => removeNumber(number));
listItem.appendChild(removeButton);

    numberListElement.appendChild(listItem);
  }

  // Update the section visibility based on the list length
  const excludeNumbersSection = document.getElementById('excludeNumbersSection');
  excludeNumbersSection.style.display = 'block';
}

function addNumber() {
  const newNumberInput = document.getElementById('newNumber');
  const newNumber = newNumberInput.value.trim();

  // Check if the input is a valid 10-digit number
  const numberRegex = /^\d{10}$/;
  if (!numberRegex.test(newNumber)) {
    alert('מספר לא תקין. אנא הכנס/י מספר בעל 10 ספרות.');
    return;
  }

  // Add the number to the list
  numbers.push(newNumber);
  displayNumbers();

  // Clear the input field
  newNumberInput.value = '';
}

// Listen for keydown event on the input field
const newNumberInput = document.getElementById('newNumber');
newNumberInput.addEventListener('keydown', function (event) {
  if (event.key === 'Enter') {
    addNumber();
  }
});

    function removeNumber(number) {
      const index = numbers.indexOf(number);
      if (index > -1) {
        numbers.splice(index, 1);
        displayNumbers();
      }
    }

function toggleDivVisibility() {
  var div = document.getElementById('hiddenDiv');
  if (div.style.display === 'none') {
    div.style.display = 'block';
  } else {
    div.style.display = 'none';
  }
}

// Get the info popup element
const infoPopup = document.getElementById("infoPopup");

let offsetX, offsetY, isDragging = false;

// Function to handle the start of dragging
function startDragging(event) {
  isDragging = true;
  offsetX = event.clientX - infoPopup.offsetLeft;
  offsetY = event.clientY - infoPopup.offsetTop;
}

// Function to handle the end of dragging
function stopDragging() {
  isDragging = false;
}

// Function to handle the dragging movement
function drag(event) {
  if (isDragging) {
    const x = event.clientX - offsetX;
    const y = event.clientY - offsetY;
    infoPopup.style.left = `${x}px`;
    infoPopup.style.top = `${y}px`;
  }
}

// Add event listeners for dragging
infoPopup.addEventListener("mousedown", startDragging);
window.addEventListener("mouseup", stopDragging);
window.addEventListener("mousemove", drag);

