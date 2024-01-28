const YEAR_MIN = 18;
const YEAR_MAX = 23;
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const flag = `${urlParams.get('flag')}`

function reportError(message) {
  document.getElementById("error-message").textContent = message;
  document.getElementById("error-message").hidden = false;
}

if (flag === 'False') {
  reportError('This PDF does not exist!');
}

function handleSubjectChange() {
  subjectElement = document.getElementById("subject");
  asLevel = document.getElementById("as-level");
  a2Level = document.getElementById("a2-level");
  extended = document.getElementById("extended");

  extended.disabled = ![
    "0625",
    "0620",
    "0610",
    "0653",
    "5090",
    "5070",
    "5054",
    "5129",
  ].includes(subjectElement.value);

  isAsAlevel = false;

  if (subjectElement.value === "9708") {
    isAsAlevel = true;
  }
  asLevel.disabled = !isAsAlevel;
  a2Level.disabled = !isAsAlevel;

  if (!isAsAlevel) {
    asLevel.checked = true;
  }
}

function handleMonthChange() {
  monthElement = document.querySelector("input[name=month]:checked");
  alevelElement = document.querySelector("input[name=alevel]:checked");
  subjectElement = document.getElementById("subject");
  yearElement = document.getElementById("year");
  subjectGroup = subjectElement.selectedOptions[0].parentElement.label;

  disableOptions = (one, two, three) => {
    document.getElementById("one").disabled = one;
    document.getElementById("two").disabled = two;
    document.getElementById("three").disabled = three;
  };

  disableOptions(false, false, false);

  if (monthElement.value === "m" && subjectGroup === "IGCSE") {
    disableOptions(true, false, true);
  } else if (monthElement.value === "m" && subjectGroup === "O Levels") {
    disableOptions(true, true, true);
  } else if (monthElement.value === "s" && subjectGroup === "O Levels") {
    disableOptions(false, false, true);
  } else if (
    ["5090", "5070", "5054", "5129"].includes(subjectElement.value) &&
    monthElement.value === "w"
  ) {
    disableOptions(false, false, true);
  } else if (subjectElement.value === "2281" && monthElement.value === "w") {
    disableOptions(false, false, false);
  } else if (
    subjectGroup === "AS and A Levels" &&
    alevelElement.value == "as-level" &&
    monthElement.value === "m"
  ) {
    disableOptions(true, false, true);
  } else if (alevelElement.value == "a2-level" && monthElement.value === "m") {
    disableOptions(true, false, true);
  }
}

document.getElementById("main-form").addEventListener("submit", (e) => {
  subjectValue = document.getElementById("subject").value;
  yearValue = document.getElementById("year").value;
  monthValue = document.querySelector("input[name=month]:checked").value;

  if (
    subjectValue === "please-select" ||
    yearValue === "" ||
    monthValue === ""
  ) {
    e.preventDefault(); // Prevent the form submission
    reportError("Please fill in all required fields!");
  }
});

document.getElementById("subject").addEventListener("change", () => {
  handleSubjectChange();
  handleMonthChange();
});

document.querySelectorAll("input[name=month]").forEach((monthInput) => {
  monthInput.addEventListener("change", () => {
    handleMonthChange();
  });
});
