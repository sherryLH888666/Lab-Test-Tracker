<template>
  <div class="app">
    <header>
      <h1>Lab Test Record Tracker</h1>
      <p class="sub">
        Demo full-stack project aligned with UL Solutions &mdash; Laboratory Operations Digitization
      </p>
    </header>

    <section class="stats">
      <span>Total records: <b>{{ total }}</b></span>
      <button class="ghost" @click="doSeed" :disabled="seeding">
        {{ seeding ? 'Seeding…' : 'Seed 5,000 rows' }}
      </button>
    </section>

    <section class="filters">
      <input v-model="keyword" placeholder="Search sample id / test name" @input="onFilter" />
      <select v-model="statusFilter" @change="load">
        <option value="">All status</option>
        <option value="pass">PASS</option>
        <option value="fail">FAIL</option>
        <option value="pending">PENDING</option>
      </select>
    </section>

    <section class="form">
      <h3>Add record</h3>
      <div class="row">
        <input v-model="form.sample_id" placeholder="sample id *" />
        <input v-model="form.test_name" placeholder="test name *" />
        <input v-model="form.operator" placeholder="operator" />
        <input v-model.number="form.result_value" type="number" placeholder="value" />
        <input v-model="form.unit" placeholder="unit" />
        <select v-model="form.status">
          <option value="pending">pending</option>
          <option value="pass">pass</option>
          <option value="fail">fail</option>
        </select>
        <button @click="add">Add</button>
      </div>
    </section>

    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Sample</th>
          <th>Test</th>
          <th>Operator</th>
          <th>Value</th>
          <th>Status</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in rows" :key="r.id">
          <td>{{ r.id }}</td>
          <td>{{ r.sample_id }}</td>
          <td>{{ r.test_name }}</td>
          <td>{{ r.operator }}</td>
          <td>{{ r.result_value }} {{ r.unit }}</td>
          <td><span :class="'badge ' + (r.status || '')">{{ r.status }}</span></td>
          <td><button class="danger" @click="remove(r.id)">del</button></td>
        </tr>
      </tbody>
    </table>

    <footer>
      <button @click="prev" :disabled="skip === 0">Prev</button>
      <span>page {{ page }}</span>
      <button @click="next">Next</button>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as api from './api'

const rows = ref<api.TestRecord[]>([])
const total = ref(0)
const keyword = ref('')
const statusFilter = ref('')
const skip = ref(0)
const limit = 20
const page = ref(1)
const seeding = ref(false)
const form = ref({
  sample_id: '',
  test_name: '',
  operator: '',
  result_value: null as number | null,
  unit: '',
  status: 'pending'
})

async function load() {
  const params: any = { skip: skip.value, limit }
  if (statusFilter.value) params.status = statusFilter.value
  if (keyword.value) params.keyword = keyword.value
  rows.value = await api.listRecords(params)
  total.value = (await api.countRecords(params)).total
}

function onFilter() {
  skip.value = 0
  page.value = 1
  load()
}

function next() {
  skip.value += limit
  page.value += 1
  load()
}

function prev() {
  if (skip.value > 0) {
    skip.value -= limit
    page.value -= 1
    load()
  }
}

async function add() {
  if (!form.value.sample_id || !form.value.test_name) return
  await api.createRecord({ ...form.value })
  form.value = {
    sample_id: '',
    test_name: '',
    operator: '',
    result_value: null,
    unit: '',
    status: 'pending'
  }
  await load()
}

async function remove(id: number) {
  await api.deleteRecord(id)
  await load()
}

async function doSeed() {
  seeding.value = true
  await api.seedRecords(5000)
  seeding.value = false
  await load()
}

onMounted(load)
</script>

<style scoped>
.app {
  max-width: 960px;
  margin: 0 auto;
  padding: 24px;
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  color: #1f2933;
}
header h1 {
  margin: 0 0 4px;
  font-size: 22px;
}
.sub {
  margin: 0 0 16px;
  color: #616e7c;
  font-size: 13px;
}
.stats,
.filters,
.form {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 14px;
  flex-wrap: wrap;
}
.stats b {
  color: #0b69ff;
}
input,
select {
  padding: 8px 10px;
  border: 1px solid #cbd2d9;
  border-radius: 6px;
  font-size: 13px;
}
button {
  padding: 8px 14px;
  border: none;
  border-radius: 6px;
  background: #0b69ff;
  color: #fff;
  cursor: pointer;
  font-size: 13px;
}
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
button.ghost {
  background: #e4e7eb;
  color: #1f2933;
}
button.danger {
  background: #e12d39;
  padding: 4px 10px;
}
.form .row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 8px;
  font-size: 13px;
}
th,
td {
  text-align: left;
  padding: 8px 10px;
  border-bottom: 1px solid #e4e7eb;
}
th {
  background: #f5f7fa;
}
.badge {
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
}
.badge.pass {
  background: #e3f9e5;
  color: #0b6b2f;
}
.badge.fail {
  background: #ffe3e3;
  color: #b42318;
}
.badge.pending {
  background: #fff4e6;
  color: #b25e09;
}
footer {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-top: 14px;
}
</style>
