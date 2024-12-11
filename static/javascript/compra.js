document.addEventListener('DOMContentLoaded', function() {
    const selectCripto = document.getElementById('criptomoeda');
    const inputQuantidade = document.getElementById('quantidade');
    const precoTotal = document.getElementById('preco');

    const precosCriptos = {
        btc: 200000,  // Exemplo de preço do Bitcoin
        eth: 14000,   // Exemplo de preço do Ethereum
        ltc: 500,     // Exemplo de preço do Litecoin
    };

    function atualizarPreco() {
        const criptoSelecionada = selectCripto.value;
        const quantidade = parseFloat(inputQuantidade.value);

        if (!isNaN(quantidade) && quantidade > 0) {
            const preco = precosCriptos[criptoSelecionada];
            const precoFinal = preco * quantidade;
            precoTotal.value = R$ ${precoFinal.toFixed(2)};
        } else {
            precoTotal.value = 'R$ 0,00';
        }
    }

    // Atualiza o preço quando a criptomoeda ou quantidade mudar
    selectCripto.addEventListener('change', atualizarPreco);
    inputQuantidade.addEventListener('input', atualizarPreco);
});