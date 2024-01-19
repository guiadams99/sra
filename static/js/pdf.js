const btnGenerate = document.querySelector("#generate-pdf");

btnGenerate.addEventListener("click", () => {

  const pdf = document.querySelector("#pdf")

  const options = {
    margin: [0, 0, 0, 0],
    filename: "registros.pdf",
    html2canvas:{scale: 2},
    jsPDF: {unit: "mm", format: "a4", orientation: "landscape"}
  }

  html2pdf().set(options).from(pdf).save();

})