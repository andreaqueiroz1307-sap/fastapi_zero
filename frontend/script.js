const API = 'http://127.0.0.1:8000';

let userAtual = null;
let tarefaEditando = null;

async function api(url, method = 'GET', body = null) {
  const res = await fetch(API + url, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : null
  });

  let data = null;
  try {
    data = await res.json();
  } catch {
    data = null;
  }

  if (!res.ok) {
    throw new Error(data?.detail || 'Erro na requisição');
  }

  return data;
}

function limparMensagens() {
  document.getElementById('loginErro').innerText = '';
  document.getElementById('cadastroErro').innerText = '';
  document.getElementById('tarefaErro').innerText = '';
  document.getElementById('erroEdicao').innerText = '';
  document.getElementById('alterarSenhaErro').innerText = '';
  document.getElementById('alterarSenhaSucesso').innerText = '';
  document.getElementById('esqueciSenhaErro').innerText = '';
  document.getElementById('esqueciSenhaSucesso').innerText = '';
}

function limparCamposCriacao() {
  document.getElementById('titulo').value = '';
  document.getElementById('descricao').value = '';
  document.getElementById('prioridade').value = 'baixa';
  document.getElementById('dataLimite').value = '';
}

function limparCamposEdicao() {
  document.getElementById('editTitulo').value = '';
  document.getElementById('editDescricao').value = '';
  document.getElementById('editPrioridade').value = 'baixa';
  document.getElementById('editDataLimite').value = '';
}

function limparCamposSenha() {
  document.getElementById('senhaAtual').value = '';
  document.getElementById('novaSenha').value = '';
  document.getElementById('confirmarNovaSenha').value = '';
}

function limparCamposEsqueciSenha() {
  document.getElementById('esqueciEmail').value = '';
  document.getElementById('esqueciNovaSenha').value = '';
  document.getElementById('esqueciConfirmarSenha').value = '';
}

function esconderMenuUsuario() {
  document.getElementById('userMenu').classList.add('hidden');
}

function alternarMenuUsuario() {
  document.getElementById('userMenu').classList.toggle('hidden');
}

async function login() {
  limparMensagens();

  try {
    const email = document.getElementById('loginEmail').value.trim();
    const senha = document.getElementById('loginSenha').value.trim();

    if (!email || !senha) {
      document.getElementById('loginErro').innerText =
        'Preencha email e senha.';
      return;
    }

    const user = await api('/login', 'POST', { email, senha });
    userAtual = user;

    document.getElementById('userMenuTrigger').innerText = user.nome;

    document.getElementById('loginEmail').value = '';
    document.getElementById('loginSenha').value = '';

    toggle('login', 'home');
    await listarTarefas();
  } catch (e) {
    document.getElementById('loginErro').innerText = e.message;
  }
}

async function cadastrar() {
  limparMensagens();

  try {
    const nome = document.getElementById('cadNome').value.trim();
    const email = document.getElementById('cadEmail').value.trim();
    const senha = document.getElementById('cadSenha').value.trim();

    if (!nome || !email || !senha) {
      document.getElementById('cadastroErro').innerText =
        'Preencha todos os campos.';
      return;
    }

    await api('/users', 'POST', { nome, email, senha });

    alert('Usuário criado!');
    mostrarLogin();
  } catch (e) {
    document.getElementById('cadastroErro').innerText = e.message;
  }
}

async function redefinirSenha() {
  limparMensagens();

  try {
    const email = document.getElementById('esqueciEmail').value.trim();
    const novaSenha = document.getElementById('esqueciNovaSenha').value.trim();
    const confirmarSenha = document
      .getElementById('esqueciConfirmarSenha')
      .value.trim();

    if (!email || !novaSenha || !confirmarSenha) {
      document.getElementById('esqueciSenhaErro').innerText =
        'Preencha todos os campos.';
      return;
    }

    if (novaSenha !== confirmarSenha) {
      document.getElementById('esqueciSenhaErro').innerText =
        'A confirmação da nova senha não confere.';
      return;
    }

    const resposta = await api('/users/redefinir-senha', 'PUT', {
      email: email,
      nova_senha: novaSenha
    });

    document.getElementById('esqueciSenhaSucesso').innerText =
      resposta.message || 'Senha redefinida com sucesso.';

    limparCamposEsqueciSenha();
  } catch (e) {
    document.getElementById('esqueciSenhaErro').innerText = e.message;
  }
}

async function listarTarefas() {
  try {
    const tarefas = await api('/tarefas');
    const tarefasDiv = document.getElementById('tarefas');
    tarefasDiv.innerHTML = '';

    const tarefasDoUsuario = tarefas.filter((t) => {
      const donoId = t.user_id ?? t.usuario?.id;
      return Number(donoId) === Number(userAtual.id);
    });

    if (tarefasDoUsuario.length === 0) {
      tarefasDiv.innerHTML = `
        <div class="empty-state">Nenhuma tarefa encontrada.</div>
      `;
      return;
    }

    tarefasDoUsuario.forEach((t) => {
      const div = document.createElement('div');
      div.className = 'task';

      div.innerHTML = `
        <h3>${t.titulo}</h3>
        <p>${t.descricao}</p>
        <span class="prioridade">Prioridade: ${t.prioridade}</span>
        <p><strong>Prazo:</strong> ${t.data_limite || '---'}</p>
      `;

      div.addEventListener('click', () => abrirEdicao(t));
      tarefasDiv.appendChild(div);
    });
  } catch (e) {
    alert(e.message);
  }
}

function abrirEdicao(t) {
  limparMensagens();
  esconderMenuUsuario();

  tarefaEditando = t;

  document.getElementById('editTitulo').value = t.titulo || '';
  document.getElementById('editDescricao').value = t.descricao || '';
  document.getElementById('editPrioridade').value = t.prioridade || 'baixa';
  document.getElementById('editDataLimite').value = t.data_limite || '';

  toggle('home', 'editarTarefa');
}

async function salvarEdicaoTarefa() {
  limparMensagens();

  try {
    await api(`/tarefas/${tarefaEditando.id}`, 'PUT', {
      titulo: document.getElementById('editTitulo').value.trim(),
      descricao: document.getElementById('editDescricao').value.trim(),
      prioridade: document.getElementById('editPrioridade').value,
      data_limite: document.getElementById('editDataLimite').value || null
    });

    voltarHomeDeEditar();
  } catch (e) {
    document.getElementById('erroEdicao').innerText = e.message;
  }
}

async function criarTarefa() {
  limparMensagens();

  try {
    await api('/tarefas', 'POST', {
      titulo: document.getElementById('titulo').value.trim(),
      descricao: document.getElementById('descricao').value.trim(),
      prioridade: document.getElementById('prioridade').value,
      data_limite: document.getElementById('dataLimite').value || null,
      user_id: userAtual.id
    });

    limparCamposCriacao();
    voltarHome();
  } catch (e) {
    document.getElementById('tarefaErro').innerText = e.message;
  }
}

async function salvarNovaSenha() {
  limparMensagens();

  try {
    const senhaAtual = document.getElementById('senhaAtual').value.trim();
    const novaSenha = document.getElementById('novaSenha').value.trim();
    const confirmarNovaSenha =
      document.getElementById('confirmarNovaSenha').value.trim();

    if (!senhaAtual || !novaSenha || !confirmarNovaSenha) {
      document.getElementById('alterarSenhaErro').innerText =
        'Preencha todos os campos.';
      return;
    }

    if (novaSenha !== confirmarNovaSenha) {
      document.getElementById('alterarSenhaErro').innerText =
        'A confirmação da nova senha não confere.';
      return;
    }

    const resposta = await api(
      `/users/${userAtual.id}/alterar-senha`,
      'PUT',
      {
        senha_atual: senhaAtual,
        nova_senha: novaSenha
      }
    );

    document.getElementById('alterarSenhaSucesso').innerText =
      resposta.message;

    limparCamposSenha();
  } catch (e) {
    document.getElementById('alterarSenhaErro').innerText = e.message;
  }
}

function mostrarCadastro() {
  limparMensagens();
  esconderMenuUsuario();
  toggle('login', 'cadastro');
}

function mostrarEsqueciSenha() {
  limparMensagens();
  esconderMenuUsuario();
  limparCamposEsqueciSenha();

  document.getElementById('login').classList.add('hidden');
  document.getElementById('cadastro').classList.add('hidden');
  document.getElementById('home').classList.add('hidden');
  document.getElementById('criarTarefa').classList.add('hidden');
  document.getElementById('editarTarefa').classList.add('hidden');
  document.getElementById('alterarSenha').classList.add('hidden');
  document.getElementById('esqueciSenha').classList.remove('hidden');
}

function mostrarLogin() {
  limparMensagens();
  esconderMenuUsuario();

  document.getElementById('cadastro').classList.add('hidden');
  document.getElementById('home').classList.add('hidden');
  document.getElementById('criarTarefa').classList.add('hidden');
  document.getElementById('editarTarefa').classList.add('hidden');
  document.getElementById('alterarSenha').classList.add('hidden');
  document.getElementById('esqueciSenha').classList.add('hidden');
  document.getElementById('login').classList.remove('hidden');
}

function mostrarCriarTarefa() {
  limparMensagens();
  esconderMenuUsuario();
  toggle('home', 'criarTarefa');
}

function voltarHome() {
  limparMensagens();
  esconderMenuUsuario();
  toggle('criarTarefa', 'home');
  listarTarefas();
}

function voltarHomeDeEditar() {
  limparMensagens();
  limparCamposEdicao();
  esconderMenuUsuario();
  tarefaEditando = null;

  toggle('editarTarefa', 'home');
  listarTarefas();
}

function mostrarTelaAlterarSenha() {
  limparMensagens();
  limparCamposSenha();
  esconderMenuUsuario();
  toggle('home', 'alterarSenha');
}

function voltarHomeDeAlterarSenha() {
  limparMensagens();
  limparCamposSenha();
  esconderMenuUsuario();
  toggle('alterarSenha', 'home');
}

function logout() {
  userAtual = null;
  tarefaEditando = null;

  document.getElementById('userMenuTrigger').innerText = '';
  document.getElementById('tarefas').innerHTML = '';

  limparCamposCriacao();
  limparCamposEdicao();
  limparCamposSenha();
  limparCamposEsqueciSenha();
  esconderMenuUsuario();
  mostrarLogin();
}

function toggle(hide, show) {
  document.getElementById(hide).classList.add('hidden');
  document.getElementById(show).classList.remove('hidden');
}

document.addEventListener('click', (event) => {
  const menu = document.getElementById('userMenu');
  const trigger = document.getElementById('userMenuTrigger');

  if (!menu || !trigger) return;

  const clicouDentro =
    menu.contains(event.target) || trigger.contains(event.target);

  if (!clicouDentro) {
    esconderMenuUsuario();
  }
});

document
  .getElementById('userMenuTrigger')
  .addEventListener('click', (event) => {
    event.stopPropagation();
    alternarMenuUsuario();
  });

document.addEventListener('keydown', (event) => {
  if (event.key !== 'Enter') return;

  const loginVisivel = !document.getElementById('login').classList.contains('hidden');
  const cadastroVisivel = !document.getElementById('cadastro').classList.contains('hidden');
  const alterarSenhaVisivel = !document.getElementById('alterarSenha').classList.contains('hidden');
  const esqueciSenhaVisivel = !document.getElementById('esqueciSenha').classList.contains('hidden');

  if (loginVisivel) {
    login();
    return;
  }

  if (cadastroVisivel) {
    const nome = document.getElementById('cadNome').value.trim();
    const email = document.getElementById('cadEmail').value.trim();
    const senha = document.getElementById('cadSenha').value.trim();

    if (nome && email && senha) {
      cadastrar();
    }
    return;
  }

  if (alterarSenhaVisivel) {
    const senhaAtual = document.getElementById('senhaAtual').value.trim();
    const novaSenha = document.getElementById('novaSenha').value.trim();
    const confirmar = document.getElementById('confirmarNovaSenha').value.trim();

    if (senhaAtual && novaSenha && confirmar) {
      salvarNovaSenha();
    }
    return;
  }

  if (esqueciSenhaVisivel) {
    const email = document.getElementById('esqueciEmail').value.trim();
    const novaSenha = document.getElementById('esqueciNovaSenha').value.trim();
    const confirmar = document.getElementById('esqueciConfirmarSenha').value.trim();

    if (email && novaSenha && confirmar) {
      redefinirSenha();
    }
  }
});