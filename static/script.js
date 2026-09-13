document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("resume_file");
  const fileBadge = document.getElementById("fileBadge");
  const fileNameDisplay = document.getElementById("fileNameDisplay");
  const removeFileBtn = document.getElementById("removeFileBtn");

  const tabText = document.getElementById("tabText");
  const tabUrl = document.getElementById("tabUrl");
  const textInputContainer = document.getElementById("textInputContainer");
  const urlInputContainer = document.getElementById("urlInputContainer");
  const jdTypeInput = document.getElementById("jd_type");

  const analyzeForm = document.getElementById("analyzeForm");
  const analyzeBtn = document.getElementById("analyzeBtn");
  const errorAlert = document.getElementById("errorAlert");
  const errorMessage = document.getElementById("errorMessage");

  const loadingOverlay = document.getElementById("loadingOverlay");
  const stepText = document.getElementById("stepText");

  const resultsSection = document.getElementById("resultsSection");
  const finalScoreNum = document.getElementById("finalScoreNum");
  const scoreCircle = document.getElementById("scoreCircle");
  const fitVerdictBadge = document.getElementById("fitVerdictBadge");

  const atsScoreVal = document.getElementById("atsScoreVal");
  const atsProgressBar = document.getElementById("atsProgressBar");
  const semanticScoreVal = document.getElementById("semanticScoreVal");
  const semanticProgressBar = document.getElementById("semanticProgressBar");
  const skillScoreVal = document.getElementById("skillScoreVal");
  const skillProgressBar = document.getElementById("skillProgressBar");

  const missingKeywordsContainer = document.getElementById("missingKeywordsContainer");
  const matchedKeywordsContainer = document.getElementById("matchedKeywordsContainer");
  const feedbackContent = document.getElementById("feedbackContent");

  let selectedFile = null;

  // File Dropzone Handling
  dropzone.addEventListener("click", () => fileInput.click());

  fileInput.addEventListener("change", (e) => {
    if (e.target.files.length > 0) {
      handleFileSelected(e.target.files[0]);
    }
  });

  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("dragover");
  });

  dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("dragover");
  });

  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
    if (e.dataTransfer.files.length > 0) {
      handleFileSelected(e.dataTransfer.files[0]);
    }
  });

  function handleFileSelected(file) {
    selectedFile = file;
    fileNameDisplay.textContent = file.name;
    fileBadge.style.display = "inline-flex";
    dropzone.style.display = "none";
    hideError();
  }

  removeFileBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    selectedFile = null;
    fileInput.value = "";
    fileBadge.style.display = "none";
    dropzone.style.display = "block";
  });

  // Tab Toggle Handling
  tabText.addEventListener("click", () => {
    tabText.classList.add("active");
    tabUrl.classList.remove("active");
    textInputContainer.style.display = "block";
    urlInputContainer.style.display = "none";
    jdTypeInput.value = "text";
  });

  tabUrl.addEventListener("click", () => {
    tabUrl.classList.add("active");
    tabText.classList.remove("active");
    urlInputContainer.style.display = "block";
    textInputContainer.style.display = "none";
    jdTypeInput.value = "url";
  });

  // Form Submission
  analyzeForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    hideError();

    if (!selectedFile) {
      showError("Please upload a resume file (PDF or Image).");
      return;
    }

    const jdType = jdTypeInput.value;
    const jdText = document.getElementById("jd_text").value.trim();
    const jdUrl = document.getElementById("jd_url").value.trim();

    if (jdType === "text" && !jdText) {
      showError("Please paste the Job Description text.");
      return;
    }

    if (jdType === "url" && !jdUrl) {
      showError("Please enter a valid Job Description URL.");
      return;
    }

    const formData = new FormData();
    formData.append("resume_file", selectedFile);
    formData.append("jd_type", jdType);
    if (jdType === "text") formData.append("jd_text", jdText);
    if (jdType === "url") formData.append("jd_url", jdUrl);

    // Show Loading
    showLoading();

    try {
      const response = await fetch("/analyze", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "An error occurred during resume analysis.");
      }

      // Display Results
      displayResults(data);
    } catch (err) {
      showError(err.message || "Failed to complete analysis. Please try again.");
    } finally {
      hideLoading();
    }
  });

  // UI Helpers
  function showError(msg) {
    errorMessage.textContent = msg;
    errorAlert.classList.remove("hidden");
    errorAlert.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  function hideError() {
    errorAlert.classList.add("hidden");
    errorMessage.textContent = "";
  }

  function showLoading() {
    loadingOverlay.classList.add("active");
  }

  function hideLoading() {
    loadingOverlay.classList.remove("active");
  }

  function displayResults(data) {
    const finalScore = data.final_score || 0;
    const atsScore = data.ats_score || 0;
    const semanticScore = data.semantic_score || 0;
    const skillScore = data.skill_match_score || 0;

    // Set Final Score
    finalScoreNum.textContent = finalScore;
    scoreCircle.style.setProperty("--score-pct", finalScore);

    // Set Verdict
    fitVerdictBadge.className = "fit-verdict-badge ";
    if (finalScore >= 80) {
      fitVerdictBadge.textContent = "Strong Match";
      fitVerdictBadge.classList.add("verdict-excellent");
    } else if (finalScore >= 65) {
      fitVerdictBadge.textContent = "Good Match";
      fitVerdictBadge.classList.add("verdict-good");
    } else if (finalScore >= 50) {
      fitVerdictBadge.textContent = "Moderate Match";
      fitVerdictBadge.classList.add("verdict-moderate");
    } else {
      fitVerdictBadge.textContent = "Needs Improvement";
      fitVerdictBadge.classList.add("verdict-poor");
    }

    // Set Breakdown Scores & Bars
    atsScoreVal.textContent = atsScore + "%";
    atsProgressBar.style.width = atsScore + "%";

    semanticScoreVal.textContent = semanticScore + "%";
    semanticProgressBar.style.width = semanticScore + "%";

    skillScoreVal.textContent = skillScore + "%";
    skillProgressBar.style.width = skillScore + "%";

    // Missing Keywords
    missingKeywordsContainer.innerHTML = "";
    if (data.missing_keywords && data.missing_keywords.length > 0) {
      data.missing_keywords.forEach((kw) => {
        const tag = document.createElement("span");
        tag.className = "keyword-tag";
        tag.textContent = kw;
        missingKeywordsContainer.appendChild(tag);
      });
    } else {
      missingKeywordsContainer.innerHTML = '<span style="color: var(--text-muted); font-size: 0.9rem;">None! Great keyword alignment.</span>';
    }

    // Matched Keywords
    matchedKeywordsContainer.innerHTML = "";
    if (data.matched_keywords && data.matched_keywords.length > 0) {
      data.matched_keywords.forEach((kw) => {
        const tag = document.createElement("span");
        tag.className = "matched-tag";
        tag.textContent = kw;
        matchedKeywordsContainer.appendChild(tag);
      });
    }

    // Format Feedback Text (Markdown parser or simple line breaks)
    if (window.marked) {
      feedbackContent.innerHTML = marked.parse(data.feedback || "");
    } else {
      feedbackContent.innerText = data.feedback || "";
    }

    resultsSection.classList.remove("hidden");
    resultsSection.scrollIntoView({ behavior: "smooth" });
  }
});
