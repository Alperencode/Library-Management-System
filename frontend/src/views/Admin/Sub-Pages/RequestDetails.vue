<template>
    <div v-if="request" class="request-details-container">
        <div class="book-card">
            <img v-if="request.cover_image" :src="request.cover_image" class="cover" alt="Cover" />
            <img v-else :src="defaultCover" class="cover" alt="Default Cover" />

            <div class="info">
                <h2>{{ request.title }}</h2>
                <p><strong>Authors:</strong> {{ request.authors.join(', ') }}</p>
                <p><strong>Publisher:</strong> {{ request.publisher }}</p>
                <p><strong>ISBN:</strong> {{ request.isbn }}</p>
                <p><strong>Requested At:</strong> {{ formatDate(request.requested_at) }}</p>
                <p><strong>Status Updated:</strong> {{ formatDate(request.status_updated_at) }}</p>
                <p>
                    <strong>Status:</strong>
                    <span :class="['status', statusColor(request.status)]">{{ request.status }}</span>
                </p>
                <p><strong>Requested by:</strong> {{ requesterCount }} user(s)</p>

                <div class="actions">
                    <button class="add" @click="addBook">+ Add Book</button>

                    <div class="status-update-group">
                        <select v-model="selectedStatus" class="status-select">
                            <option disabled value="">Change Status</option>
                            <option value="Request Sent">Request Sent</option>
                            <option value="On Hold">On Hold</option>
                        </select>
                        <button class="change-status-btn" :disabled="!selectedStatus"
                            @click="updateStatus(selectedStatus)">
                            Change Status
                        </button>
                    </div>

                    <button class="decline" @click="declineRequest">✕ Decline</button>
                </div>
            </div>
        </div>

        <div class="requesters-section" v-if="requesters.length">
            <h3>Requesters</h3>
            <ul>
                <li v-for="r in requesters" :key="r.id">
                    <span class="user-icon">👤</span> {{ r.username }} ({{ r.email }})
                </li>
            </ul>
        </div>
    </div>

    <div v-else class="loading-state">
        <p>Loading request details...</p>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'
import { useToast } from 'vue-toastification'
import defaultCover from '@/assets/images/default-cover.png'

const route = useRoute()
const router = useRouter()
const toast = useToast()

const id = route.params.id
const request = ref(null)
const requesters = ref([])
const requesterCount = ref(0)
const selectedStatus = ref('')

onMounted(async () => {
    try {
        const { data } = await api.get(`/admin/requested-books/info/${id}`)
        request.value = data.request
        requesters.value = data.requesters
        requesterCount.value = data.requester_count
    } catch (err) {
        toast.error('Failed to load request info')
    }
})

async function addBook() {
    try {
        await api.post('/admin/add-book', { request_id: id })
        toast.success('Book successfully added to catalog')
        router.push('/admin/requests')
    } catch (err) {
        toast.error('Failed to add book')
    }
}

async function updateStatus(newStatus) {
    try {
        await api.patch(`/admin/requested-books/${id}`, { status: newStatus })
        toast.success(`Status updated to "${newStatus}"`)
        router.push('/admin/requests')
    } catch (err) {
        toast.error(`Failed to update status to "${newStatus}"`)
    }
}

async function declineRequest() {
    try {
        const statusValue = 'Denied'
        await api.patch(`/admin/requested-books/${id}`, { status: statusValue })
        toast.success('Request declined')
        router.push('/admin/requests')
    } catch (err) {
        console.error(err)
        toast.error('Failed to decline request')
    }
}

function statusColor(status) {
    switch (status) {
        case 'ADDED': return 'green'
        case 'DENIED': return 'red'
        case 'Request Sent': return 'gray'
        case 'On Hold': return 'orange'
        default: return 'blue'
    }
}

function formatDate(isoString) {
    return new Date(isoString).toLocaleString()
}
</script>


<style scoped>
.request-details-container {
    min-height: calc(100vh - 60px);
    max-width: 900px;
    margin: 40px auto;
    padding: 20px;
    background: #f5f7fa;
    border-radius: 12px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.07);
}

.book-card {
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.cover {
    width: 160px;
    height: 230px;
    object-fit: cover;
    border-radius: 10px;
    background: #ddd;
    border: 1px solid #ccc;
}

.info {
    flex: 1;
    min-width: 250px;
    font-size: 15px;
    color: #333;
}

.info h2 {
    margin-top: 0;
    font-size: 22px;
    color: #222;
}

.status {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: bold;
    margin-top: 4px;
    margin-left: 6px;
}

.status.green {
    background: #e9f9ec;
    color: #2ecc71;
}

.status.red {
    background: #ffe4e4;
    color: #e74c3c;
}

.status.gray {
    background: #e0e0e0;
    color: #555;
}

.status.orange {
    background: #fff0db;
    color: #e67e22;
}

.actions {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 18px;
}

.actions button {
    padding: 10px 20px;
    font-size: 15px;
    border: none;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    transition: 0.2s ease;
}

.actions .add {
    background-color: #3498db;
    color: white;
}

.actions .add:hover {
    background-color: #2c80b4;
}

.actions .decline {
    background-color: #e74c3c;
    color: white;
}

.actions .decline:hover {
    background-color: #c0392b;
}

.status-update-group {
    display: flex;
    gap: 10px;
    align-items: center;
    flex-wrap: wrap;
}

.status-select {
    padding: 8px 12px;
    border-radius: 6px;
    border: 1px solid #ccc;
    background-color: #f9f9f9;
    font-size: 14px;
}

.change-status-btn {
    padding: 8px 14px;
    background-color: #f39c12;
    color: white;
    border: none;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
}

.change-status-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.requesters-section {
    margin-top: 24px;
    background: #fff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 1px 6px rgba(0, 0, 0, 0.05);
}

.requesters-section h3 {
    margin-bottom: 12px;
    font-size: 18px;
    color: #333;
}

.requesters-section ul {
    list-style: none;
    padding: 0;
}

.requesters-section li {
    font-size: 15px;
    margin-bottom: 8px;
    color: #444;
}

.user-icon {
    margin-right: 6px;
    color: #888;
}

.loading-state {
    text-align: center;
    padding: 60px 0;
    font-size: 18px;
    color: #aaa;
}
</style>