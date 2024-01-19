document.getElementById("planilha").addEventListener("click", function () {
    // Obter a tabela
    var tabela = document.querySelector(".table-bordered");

    // Obter o valor do campo "Total Horas"
    var totalHoras = document.getElementById("total-horas").textContent;

    // Criar um objeto do tipo Workbook
    var wb = XLSX.utils.book_new();

    // Criar uma Worksheet e adicionar a tabela
    var ws = XLSX.utils.table_to_sheet(tabela);

    // Obter o índice da última coluna na Worksheet
    var ultimaColuna = XLSX.utils.decode_range(ws["!ref"]).e.c;

    // Obter o índice da última linha na Worksheet
    var ultimaLinha = XLSX.utils.decode_range(ws["!ref"]).e.r;

    // Obter o índice da última célula na coluna "Total Horas"
    var totalHorasCellIndex = XLSX.utils.encode_cell({ c: ultimaColuna, r: 0 });

    // Definir o valor "Total Horas: valor" na última célula da coluna
    ws[totalHorasCellIndex] = { v: "Soma das Horas: " + totalHoras };

    // Limpar as células nas linhas subsequentes da coluna "Total Horas"
    for (var r = 1; r <= ultimaLinha; r++) {
        var cell = XLSX.utils.encode_cell({ c: ultimaColuna, r: r });
        delete ws[cell];
    }

    // Salvar o arquivo
    XLSX.utils.book_append_sheet(wb, ws, "Dados");
    XLSX.writeFile(wb, "dados.xlsx");
});
