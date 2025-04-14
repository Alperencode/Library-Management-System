<template>
    <div class="dashboard-container">
      <h2>Dashboard</h2>
      <div class="grid">
        <div class="chart-card">
          <h3>Book Borrow Count</h3>
          <Doughnut :data="borrowData" :options="chartOptions" />
          <ul>
            <li v-for="(item, index) in borrowRecents" :key="index">• {{ item }}</li>
          </ul>
        </div>

        <div class="chart-card">
          <h3>Penalty Book Count</h3>
          <Bar :data="penaltyBookData" :options="chartOptions" />
          <ul>
            <li v-for="(item, index) in penaltyBooks" :key="index">• {{ item }}</li>
          </ul>
        </div>

        <div class="chart-card">
          <h3>Book Requests</h3>
          <Line :data="requestData" :options="chartOptions" />
          <ul>
            <li v-for="(item, index) in requests" :key="index">• {{ item }}</li>
          </ul>
        </div>
  
        <div class="chart-card">
          <h3>Penalty User Count</h3>
          <Pie :data="penaltyUserData" :options="chartOptions" />
          <ul>
            <li v-for="(item, index) in penaltyUsers" :key="index">• {{ item }}</li>
          </ul>
        </div>
  
        <div class="chart-card">
          <h3>Current Book Count</h3>
          <Bar :data="currentBookData" :options="chartOptions" />
          <ul>
            <li v-for="(item, index) in currentBooks" :key="index">• {{ item }}</li>
          </ul>
        </div>
  
        <div class="chart-card">
          <h3>Add New Book</h3>
          <button class="add-btn" @click="$router.push('/admin/add-book')">Add New Book</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { Doughnut, Bar, Line, Pie } from 'vue-chartjs'
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    BarElement,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement
  } from 'chart.js'
  
  ChartJS.register(Title, Tooltip, Legend, ArcElement, BarElement, LineElement, CategoryScale, LinearScale, PointElement)
  
  const borrowData = {
    labels: ['Roman', 'Bilim', 'Tarih'],
    datasets: [{ data: [8, 6, 4], backgroundColor: ['#c76c0c', '#f0ad4e', '#ffeeba'] }]
  }
  const borrowRecents = ['Suç ve Ceza – Elif', 'Kürk Mantolu Madonna – Murat', 'Sinekli Bakkal – Merve', 'Bilinmeyen Mektup – Gökhan', 'Tutunamayanlar – Cem']
  
  const penaltyBookData = {
    labels: ['Hasar', 'Geç Teslim'],
    datasets: [{ label: 'Adet', data: [7, 5], backgroundColor: '#c76c0c' }]
  }
  const penaltyBooks = ['Aşım: Göç Destanı', 'Hasarlı: Fahrenheit 451']
  
  const requestData = {
    labels: ['Pzt', 'Salı', 'Çrş', 'Per'],
    datasets: [{ label: 'İstek', data: [3, 5, 2, 6], borderColor: '#c76c0c', fill: false }]
  }
  const requests = ['“1984” – Ahmet', '“Sefiller” – Zeynep']
  
  const penaltyUserData = {
    labels: ['Mehmet K.', 'Ayşe N.'],
    datasets: [{ data: [6, 3], backgroundColor: ['#a73535', '#7e57c2'] }]
  }
  const penaltyUsers = ['Mehmet K.', 'Ayşe N.']
  
  const currentBookData = {
    labels: ['Roman', 'Bilim', 'Tarih'],
    datasets: [{ label: 'Toplam Kitap', data: [300, 180, 150], backgroundColor: '#42a5f5' }]
  }
  const currentBooks = ['Roman: 300', 'Bilim: 180', 'Tarih: 150']
  
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { position: 'top' } }
  }
  </script>
  
  <style scoped>
  
  .dashboard-container {
    padding: 24px;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 24px;
    align-items: stretch;
  }

  .chart-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 420px;
  }

  .chart-card h3 {
    font-size: 18px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .chart-card canvas {
    width: 100% !important;
    height: 200px !important;
  }

  .chart-card ul {
    margin-top: 12px;
    padding-left: 20px;
    font-size: 14px;
    line-height: 1.6;
  }

  .add-btn {
    margin-top: 20px;
    background-color: #d4881a;
    color: white;
    border: none;
    padding: 10px 18px;
    font-size: 14px;
    border-radius: 6px;
    cursor: pointer;
  }

  </style>
  