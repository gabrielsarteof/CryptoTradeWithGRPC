document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-cliente');
    const listaClientes = document.getElementById('lista-clientes');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const id = document.getElementById('id').value;
        const nomeCompleto = document.getElementById('nome-completo').value;
        const dataNascimento = document.getElementById('data-nascimento').value;
        const cpf = document.getElementById('cpf').value;
        const numeroTelefone = document.getElementById('numero-telefone').value;
        const email = document.getElementById('email').value;

        try {
            const response = await axios.post('http://localhost:8000/clientes', {
                id: parseInt(id),  
                nome_completo: nomeCompleto,
                data_nascimento: dataNascimento,
                cpf: cpf,
                numero_telefone: numeroTelefone,
                email: email
            });

            carregarClientes();
            alert('Cliente cadastrado com sucesso.');

        } catch (error) {
            console.error('Erro ao cadastrar cliente:', error);
            alert('Erro ao cadastrar cliente. Verifique os dados e tente novamente.');
        }
    });

    async function carregarClientes() {
        try {
            const response = await axios.get('http://localhost:8000/clientes');
            const clientes = response.data;

            listaClientes.innerHTML = '';

            clientes.forEach(cliente => {
                const li = document.createElement('li');
                li.textContent = `ID: ${cliente.id}, Nome Completo: ${cliente.nome_completo}, Data de Nascimento: ${cliente.data_nascimento}, CPF: ${cliente.cpf}, Número de Telefone: ${cliente.numero_telefone}, Email: ${cliente.email}`;
                
                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Deletar';
                deleteButton.addEventListener('click', async () => {
                    try {
                        await axios.delete(`http://localhost:8000/clientes/${cliente.id}`);
                        carregarClientes();
                        alert('Cliente deletado com sucesso.');
                    } catch (error) {
                        console.error('Erro ao deletar cliente:', error);
                        alert('Erro ao deletar cliente. Tente novamente mais tarde.');
                    }
                });

                li.appendChild(deleteButton);
                listaClientes.appendChild(li);
            });

        } catch (error) {
            console.error('Erro ao carregar clientes:', error);
            alert('Erro ao carregar clientes. Tente novamente mais tarde.');
        }
    }

    carregarClientes();
});