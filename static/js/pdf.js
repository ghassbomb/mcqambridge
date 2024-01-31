var userAnswers = [];
var questionNumber = 0;
const incorrectFeedback = document.getElementById("incorrect-answer");
const correctFeedback = document.getElementById("correct-answer");
const title = document.getElementById("title");
const numOfQuestions = correctAnswers.length;

// Recording and checking answers
function answer(option) {
  if (questionNumber === numOfQuestions) {
    toPdfScore();
    return false;
  }
  userAnswers[questionNumber] = option;
  if (option === correctAnswers[questionNumber]) {
    incorrectFeedback.style.display = "none";
    correctFeedback.style.display = "block";
  } else if (option !== correctAnswers[questionNumber]) {
    correctFeedback.style.display = "none";
    incorrectFeedback.style.display = "block";
  }
  questionNumber = questionNumber + 1;
  title.textContent = `Question ${questionNumber}`;
}

function toPdfScore() {
  var form = document.getElementById("form");
  var correctAnswersInput = document.getElementById('correct-answers');
  var userAnswersInput = document.getElementById('user-answers');
  var paperNameInput = document.getElementById('paper-name');

  correctAnswersInput.setAttribute("value", correctAnswers);
  userAnswersInput.setAttribute("value", userAnswers);
  paperNameInput.setAttribute("value", document.querySelector('title').textContent);

  form.submit();
}
var qpName = document.querySelector('title').textContent.replace('ms', 'qp')
var url = `https://pastpapers.papacambridge.com/directories/CAIE/CAIE-pastpapers/upload/${qpName}.pdf`;

document.getElementById('canvas').src = url;


// PDF Rendering (disabled because of download restrictions)
/*
const workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.0.379/pdf.worker.min.mjs';
var pdfScale = 1;
var { pdfjsLib } = globalThis;

pdfjsLib.GlobalWorkerOptions.workerSrc = workerSrc;


var pdfDoc = null,
  pageNum = 1,
  pageRendering = false,
  pageNumPending = null,
  canvas = document.getElementById("the-canvas"),
  ctx = canvas.getContext("2d");

function renderPage(num) {
  pageRendering = true;
  // Using promise to fetch the page
  pdfDoc.getPage(num).then(function (page) {
    var viewport = page.getViewport({ scale: pdfScale });
    canvas.height = viewport.height;
    canvas.width = viewport.width;
    // Render PDF page into canvas context
    var renderContext = {
      canvasContext: ctx,
      viewport: viewport,
    };
    var renderTask = page.render(renderContext);

    // Wait for rendering to finish
    renderTask.promise.then(function () {
      pageRendering = false;
      if (pageNumPending !== null) {
        // New page rendering is pending
        renderPage(pageNumPending);
        pageNumPending = null;
      }
    });
  });

  document.getElementById("page_num").textContent = num;
}

function queueRenderPage(num) {
  if (pageRendering) {
    pageNumPending = num;
  } else {
    renderPage(num);
  }
}

function onPrevPage() {
  if (pageNum <= 1) {
    return;
  }
  pageNum--;
  queueRenderPage(pageNum);
}
document.getElementById("prev").addEventListener("click", onPrevPage);

function onNextPage() {
  if (pageNum >= pdfDoc.numPages) {
    return;
  }
  pageNum++;
  queueRenderPage(pageNum);
}
document.getElementById("next").addEventListener("click", onNextPage);
var zoominbutton = document.getElementById("zoominbutton");
zoominbutton.onclick = function () {
  pdfScale = pdfScale + 0.25;
  queueRenderPage(pageNum);
};

var zoomoutbutton = document.getElementById("zoomoutbutton");
zoomoutbutton.onclick = function () {
  if (pdfScale <= 0.25) {
    return;
  }
  pdfScale = pdfScale - 0.25;
  queueRenderPage(pageNum);
};

pdfjsLib.getDocument(url).promise.then(function (pdfDoc_) {
  pdfDoc = pdfDoc_;

  renderPage(pageNum);
}); */