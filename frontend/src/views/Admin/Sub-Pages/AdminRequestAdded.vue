<template>
    <div class="request-list-container">
        <h2 class="mb-4">Added Book Requests</h2>
        <div v-if="requests.length > 0" class="request-table-wrapper">
            <table class="request-table">
                <thead>
                    <tr>
                        <th>Cover</th>
                        <th>Title</th>
                        <th>Status</th>
                        <th>Requested At</th>
                        <th>Status Updated</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(book, index) in requests" :key="book.id" class="fade-in-row"
                        :style="{ animationDelay: `${index * 80}ms` }">
                        <td><img :src="book.cover_image || defaultCover" class="book-cover" /></td>
                        <td class="truncate-title">
                            <router-link :to="`/admin/requests/${book.id}`" class="book-link" :title="book.title">
                                {{ book.title }}
                            </router-link>
                        </td>
                        <td>
                            <span class="status-label status-green">
                                {{ book.status }}
                            </span>
                        </td>
                        <td>{{ formatDateWithoutTime(book.requested_at) }}</td>
                        <td>{{ formatDateWithoutTime(book.status_updated_at) }}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div v-else class="no-requests">No added requests found.</div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import defaultCover from '@/assets/images/default-cover.png'
import api from '@/api/axios'
import { useToast } from 'vue-toastification'
import { formatDateWithoutTime } from '@/utils/date'

const toast = useToast()
const requests = ref([])

const fetchAddedRequests = async () => {
    try {
        const { data } = await api.get('/admin/requested-books/added')
        requests.value = data.requests
    } catch (err) {
        toast.error('Failed to fetch added requests')
    }
}

onMounted(fetchAddedRequests)
</script>

<style scoped>
.request-list-container {
    padding: 24px;
    position: relative;
}

.request-table-wrapper {
    overflow-x: auto;
    margin-top: 16px;
}

.request-table {
    width: 100%;
    border-collapse: collapse;
}

.request-table th,
.request-table td {
    padding: 10px;
    border-bottom: 1px solid #eee;
    text-align: left;
    vertical-align: middle;
}

.book-cover {
    width: 50px;
    height: 70px;
    object-fit: cover;
    border-radius: 4px;
}

.truncate-title {
    max-width: 200px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.status-label {
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 500;
}

.status-green {
    background-color: #e0f8e0;
    color: #27ae60;
}

.book-link {
    display: inline-block;
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    color: #2980b9;
    text-decoration: none;
    font-weight: 500;
    vertical-align: middle;
}

.book-link:hover {
    text-decoration: underline;
}

.no-requests {
    text-align: center;
    margin-top: 40px;
    font-style: italic;
}

.fade-in-row {
    animation: fadeUp 0.4s ease-out both;
}

@keyframes fadeUp {
    0% {
        opacity: 0;
        transform: translateY(15px);
    }

    100% {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>