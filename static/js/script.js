const formatarMoeda = (valor) => {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(valor);
};

let categoriaAtual = "eletronicos";

function mudarCategoria(novaCategoria) {
  voltarParaProdutos(); // Garante que estamos na tela de produtos

  categoriaAtual = novaCategoria;
  document.getElementById("categoria_atual").value = novaCategoria;

  // Atualiza visual do menu
  document.getElementById("btn-eletronicos").classList.remove("active");
  document.getElementById("btn-roupas").classList.remove("active");
  document.getElementById(`btn-${novaCategoria}`).classList.add("active");

  // Lógica Específica
  if (novaCategoria === "roupas") {
    document.getElementById("titulo-secao").innerText =
      "👕 Gerenciador de Roupas";
    document.getElementById("grupo-tamanho").style.display = "block"; // Mostra Tamanho
  } else {
    document.getElementById("titulo-secao").innerText =
      "🖥️ Gerenciador de Periféricos";
    document.getElementById("grupo-tamanho").style.display = "none"; // Esconde Tamanho
  }

  limparFormulario();
  carregarProdutos(); // Recarrega a tabela filtrada
}

async function carregarProdutos() {
  // Passamos a categoria na URL para o Python filtrar
  const response = await fetch(`/api/produtos?categoria=${categoriaAtual}`);
  const produtos = await response.json();

  const tabela = document.getElementById("tabela-corpo");
  tabela.innerHTML = "";

  produtos.forEach((prod) => {
    // [id, codigo, nome, quantidade, preco, categoria, tamanho]
    const id = prod[0];
    const codigo = prod[1];
    const nome = prod[2];
    const quantidade = prod[3];
    const preco = prod[4];
    const categoria = prod[5];
    const tamanho = prod[6];

    const total = quantidade * preco;

    // Se for roupa, mostra o tamanho. Se for eletrônico, deixa vazio ou traço
    let detalhe = "-";

    if (
      categoria === "roupas" &&
      tamanho &&
      tamanho !== "null" &&
      tamanho !== ""
    ) {
      detalhe = `Tam: <strong>${tamanho}</strong>`;
    }

    let classeLinha = quantidade < 5 ? "alerta-estoque" : "";

    const row = `<tr class="${classeLinha}">
            <td class="cod-col">${codigo}</td>
            <td>${nome}</td>
            <td>${detalhe}</td> <td>${quantidade}</td>
            <td>${formatarMoeda(total)}</td>
            <td>
                <button onclick="editar(${id}, '${codigo}', '${nome}', ${quantidade}, ${preco}, '${tamanho}')" class="btn-edit">✏️</button>
                <button onclick="deletar(${id})" class="btn-delete">🗑️</button>
            </td>
        </tr>`;
    tabela.innerHTML += row;
  });
}

async function salvarProduto() {
  // ... (pega os campos id, codigo, nome, qtd, preco iguais) ...
  const id = document.getElementById("id_produto").value;
  const codigo = document.getElementById("codigo").value;
  const nome = document.getElementById("nome").value;
  const quantidade = document.getElementById("quantidade").value;
  const preco = document.getElementById("preco").value;

  // Pega o Tamanho e a Categoria
  const tamanho = document.getElementById("tamanho").value;
  const categoria = categoriaAtual;

  // Validação adaptada
  if (!id) {
    if (!codigo || !nome || !quantidade || !preco) {
      alert("Preencha os campos obrigatórios!");
      return;
    }
    // Se for roupa, obriga tamanho
    if (categoria === "roupas" && !tamanho) {
      alert("Para roupas, o tamanho é obrigatório!");
      return;
    }
  }

  const dados = { codigo, nome, quantidade, preco, categoria, tamanho };

  // ... (Resto da função de fetch/post/put é IDÊNTICA à anterior) ...
  let url = "/api/adicionar";
  let method = "POST";
  if (id) {
    url = `/api/atualizar/${id}`;
    method = "PUT";
  }

  const response = await fetch(url, {
    method: method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dados),
  });

  if (response.ok) {
    limparFormulario();
    carregarProdutos();
    carregarHistorico();
    if (!id) alert("Cadastrado com sucesso!");
  } else {
    const erro = await response.json();
    alert(erro.message);
  }
}

function editar(id, codigo, nome, quantidade, preco, tamanho) {
  document.getElementById("id_produto").value = id;
  document.getElementById("codigo").value = codigo;
  document.getElementById("nome").value = nome;
  document.getElementById("quantidade").value = quantidade;
  document.getElementById("preco").value = preco;

  // Preenche o tamanho (mesmo se for 'undefined' vira vazio)
  document.getElementById("tamanho").value =
    tamanho && tamanho !== "null" ? tamanho : "";

  const btn = document.getElementById("btn-salvar");
  btn.innerText = "Atualizar";
  btn.style.backgroundColor = "#ffc107";
  btn.style.color = "black";
  document.getElementById("btn-cancelar").style.display = "block";
}

// No limparFormulario, adicione:
// document.getElementById("tamanho").value = "";
// Mostra botão cancelar
//document.getElementById("btn-cancelar").style.display = "block";

async function deletar(id) {
  if (confirm("Tem certeza que deseja excluir este produto?")) {
    await fetch(`/api/deletar/${id}`, { method: "DELETE" });
    carregarProdutos();
    carregarHistorico();
  }
}

function limparFormulario() {
  // ... Limpe os outros campos ...
  document.getElementById("preco").value = "";
  document.getElementById("id_produto").value = "";
  document.getElementById("codigo").value = "";
  document.getElementById("nome").value = "";
  document.getElementById("quantidade").value = "";

  const btn = document.getElementById("btn-salvar");
  btn.innerText = "Adicionar ao Estoque";
  btn.style.backgroundColor = "#28a745";
  btn.style.color = "white";
  document.getElementById("btn-cancelar").style.display = "none";
}

// Função de Filtro (Busca)
function filtrarTabela() {
  const termo = document.getElementById("input-busca").value.toLowerCase();
  const linhas = document.querySelectorAll("#tabela-corpo tr");

  linhas.forEach((linha) => {
    const textoDaLinha = linha.innerText.toLowerCase();
    if (textoDaLinha.includes(termo)) {
      linha.style.display = ""; // Mostra
    } else {
      linha.style.display = "none"; // Esconde
    }
  });
}

// Nova função para carregar histórico
async function carregarHistorico() {
  const response = await fetch("/api/historico");
  const logs = await response.json();

  const lista = document.getElementById("lista-historico");
  lista.innerHTML = "";

  if (logs.length === 0) {
    lista.innerHTML = "<li>Sem histórico disponível.</li>";
    return;
  }

  logs.forEach((log) => {
    // log = [id, mensagem, data_hora]
    const item = `<li style="border-bottom: 1px solid #ddd; padding: 10px 0; display: flex; justify-content: space-between;">
            <span>${log[1]}</span>
            <small style="color: #666; font-weight: bold;">${log[2]}</small>
        </li>`;
    lista.innerHTML += item;
  });
}

function mostrarTelaHistorico() {
  // 1. Esconde a tela de produtos
  document.getElementById("view-produtos").style.display = "none";

  // 2. Mostra a tela de histórico
  document.getElementById("view-historico").style.display = "block";

  // 3. Atualiza os botões laterais (Visual)
  document.getElementById("btn-eletronicos").classList.remove("active");
  document.getElementById("btn-roupas").classList.remove("active");
  document.getElementById("btn-historico").classList.add("active"); // Vamos criar estilo para este active depois se quiser

  // 4. Carrega os dados
  carregarHistorico();
}

function voltarParaProdutos() {
  document.getElementById("view-historico").style.display = "none";
  document.getElementById("view-produtos").style.display = "block";
  // Remove o destaque do botão histórico
  document.getElementById("btn-historico").classList.remove("active");
}

// Inicializa
document.addEventListener("DOMContentLoaded", () => {
  carregarProdutos();
  carregarHistorico();
});
