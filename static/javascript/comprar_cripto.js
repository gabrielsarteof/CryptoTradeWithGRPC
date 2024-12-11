document.addEventListener("DOMContentLoaded", function () {
    const criptomoedaSelect = document.getElementById("criptomoeda");
    const quantidadeInput = document.getElementById("quantidade");
    const precoInput = document.getElementById("preco");

    function atualizarPreco() {
        const opcaoSelecionada = criptomoedaSelect.options[criptomoedaSelect.selectedIndex];
        const precoPorUnidade = parseFloat(opcaoSelecionada.getAttribute("data-preco")) || 0;
        const quantidade = parseFloat(quantidadeInput.value) || 0;
        const precoTotal = precoPorUnidade * quantidade;

        precoInput.value = `R$ ${precoTotal.toFixed(2)}`;
    }

    // Adicionar eventos
    criptomoedaSelect.addEventListener("change", atualizarPreco);
    quantidadeInput.addEventListener("input", atualizarPreco);
});
