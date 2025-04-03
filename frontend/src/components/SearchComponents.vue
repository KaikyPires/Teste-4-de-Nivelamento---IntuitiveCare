<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import axios from 'axios'

interface SearchResult {
  Nome_Fantasia: string;
  Razao_Social: string;
  Registro_ANS: number;
  Telefone: string;
  Endereco_eletronico: string;
  Logradouro: string;
  Numero: string;
  Bairro: string;
  Cidade: string;
  UF: string;
}

const searchQuery = ref('')
const searchResults = ref<SearchResult[]>([])
const isLoading = ref(false)
const currentPage = ref(1)
const itemsPerPage = ref(10)
const totalPages = ref(1)
const isDarkMode = ref(false)

const fetchResults = async () => {
  if (searchQuery.value.length < 3) {
    searchResults.value = [];
    totalPages.value = 1;
    return;
  }

  isLoading.value = true;

  try {
    const response = await axios.get(`http://127.0.0.1:5000/buscar?q=${encodeURIComponent(searchQuery.value)}`);
    const data = response.data;
    if (Array.isArray(data)) {
      searchResults.value = data;
      totalPages.value = Math.ceil(searchResults.value.length / itemsPerPage.value);
    } else {
      console.error('A resposta da API não é um array. Tipo recebido:', typeof data);
      searchResults.value = [];
    }
  } catch (error) {
    console.error('Erro ao buscar os dados:', error);
    searchResults.value = [];
  } finally {
    isLoading.value = false;
  }
};

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  document.documentElement.setAttribute('data-theme', isDarkMode.value ? 'dark' : 'light')
}

onMounted(() => {
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  isDarkMode.value = prefersDark
  document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light')
})

watch(searchQuery, () => {
  fetchResults();
});
</script>

<template>
  <div class="search-container">
    <button class="theme-toggle" @click="toggleDarkMode">
      {{ isDarkMode ? '🌞' : '🌙' }}
    </button>
    <div class="logo">
      <img src="@/assets/image.png" alt="Logo Personalizado" class="custom-logo"/>
    </div>
    
    <div class="search-box">
      <input v-model="searchQuery" type="text" placeholder="Pesquisar Operadora" class="search-input" />
    </div>

    <div v-if="isLoading" class="loading">Carregando...</div>
    
    <div v-if="searchResults.length > 0" class="results-container">
      <table class="results-table">
        <thead>
          <tr>
            <th>Nome Fantasia</th>
            <th>Razão Social</th>
            <th>Registro ANS</th>
            <th>Contato</th>
            <th>Endereço</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(result, index) in searchResults.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage)" :key="index">
            <td>{{ result.Nome_Fantasia || 'Não informado' }}</td>
            <td>{{ result.Razao_Social || 'Não informado' }}</td>
            <td>{{ result.Registro_ANS || 'Não informado' }}</td>
            <td>
              {{ result.Telefone || 'Não informado' }}<br>
              {{ result.Endereco_eletronico || 'Não informado' }}
            </td>
            <td>
              {{ result.Logradouro || '' }} {{ result.Numero || '' }},
              {{ result.Bairro || '' }} - {{ result.Cidade || '' }}/{{ result.UF || '' }}
            </td>
          </tr>
        </tbody>
      </table>
      
      <div class="pagination">
        <button @click="currentPage--" :disabled="currentPage === 1">Anterior</button>
        <span>Página {{ currentPage }} de {{ totalPages }}</span>
        <button @click="currentPage++" :disabled="currentPage === totalPages">Próximo</button>
      </div>
    </div>
  </div>
</template>


<style scoped>
:root {
  --bg-color: white;
  --text-color: black;
  --border-color: #ddd;
  --hover-bg: #f0f0f0;
}

[data-theme='dark'] {
  --bg-color: #121212;
  --text-color: white;
  --border-color: #333;
  --hover-bg: #333;
}

body {
  background-color: var(--bg-color);
  color: var(--text-color);
}

.search-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 10vh;
}

.theme-toggle {
  position: absolute;
  top: 20px;
  right: 20px;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

.logo {
  margin-bottom: 20px;
}

.custom-logo {
  width: 300px;
  height: auto;
}

.search-box {
  display: flex;
  align-items: center;
  border: 1px solid var(--border-color);
  border-radius: 24px;
  padding: 0 16px;
  width: 600px;
  background: var(--bg-color);
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  padding: 10px;
  background: transparent;
  font-size: 16px;
  color: var(--text-color);
}

.results-container {
  margin-top: 20px;
  width: 80%;
  max-width: 1000px;
}

.results-table {
  width: 100%;
  border-collapse: collapse;
  background-color: var(--bg-color);
}

.results-table th, .results-table td {
  padding: 12px;
  border-bottom: 1px solid var(--border-color);
  text-align: left;
}

.results-table th {
  background-color: var(--hover-bg);
  cursor: pointer;
}

.results-table tr:hover {
  background-color: var(--hover-bg);
}

.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}

.loading {
  margin-top: 20px;
  font-size: 18px;
}

</style>
