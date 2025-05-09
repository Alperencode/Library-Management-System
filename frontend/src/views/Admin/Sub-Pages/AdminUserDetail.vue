<template>
    <div class="user-detail-page" v-if="user">
        <button @click="goBack" class="back-button">← Back to Users</button>
        <h2>User Detail</h2>

        <div class="user-detail-card">
            <p><strong>Username:</strong> {{ user.username }}</p>
            <p><strong>Email:</strong> {{ user.email }}</p>
            <p><strong>Role:</strong> {{ user.role }}</p>
            <p><strong>Status:</strong> {{ user.banned ? 'Banned' : 'Active' }}</p>
        </div>

        <div class="user-summary-cards">
            <div class="summary-card clickable" @click="isBorrowedOpen = !isBorrowedOpen">
                <p>Borrowed Books</p>
                <h3>{{ user.borrowed_books?.length || 0 }}</h3>
                <span>{{ isBorrowedOpen ? '↑' : '↓' }}</span>
            </div>

            <div class="summary-card clickable" @click="isOverdueOpen = !isOverdueOpen">
                <p>Overdue Books</p>
                <h3>{{ user.overdue_books?.length || 0 }}</h3>
                <span>{{ isOverdueOpen ? '↑' : '↓' }}</span>
            </div>

            <div class="summary-card clickable" @click="isRequestedOpen = !isRequestedOpen">
                <p>Requested Books</p>
                <h3>{{ user.requested_books?.length || 0 }}</h3>
                <span>{{ isRequestedOpen ? '↑' : '↓' }}</span>
            </div>

            <div class="summary-card clickable" @click="isNotifyOpen = !isNotifyOpen">
                <p>Notify Me List</p>
                <h3>{{ user.notify_me_list?.length || 0 }}</h3>
                <span>{{ isNotifyOpen ? '↑' : '↓' }}</span>
            </div>

            <div class="summary-card clickable" @click="isPenaltiesOpen = !isPenaltiesOpen">
                <p>Penalties</p>
                <h3>{{ user.penalties?.length || 0 }}</h3>
                <span>{{ isPenaltiesOpen ? '↑' : '↓' }}</span>
            </div>
        </div>

        <transition name="fade-slide">
            <div v-if="isBorrowedOpen" class="borrowed-books-section">
                <h3>Borrowed Books</h3>
                <div v-if="loadingBorrowed">Loading borrowed books...</div>
                <table v-else-if="borrowedBooksDetails.length > 0" class="borrowed-books-table">
                    <thead>
                        <tr>
                            <th></th>
                            <th>Book Name</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(book, index) in borrowedBooksDetails" :key="book.id">
                            <td>{{ index + 1 }}</td>
                            <td>
                                <router-link :to="`/admin/books/${book.id}`" class="book-link book-title">
                                    {{ book.title || book.name }}
                                </router-link>

                            </td>
                        </tr>
                    </tbody>
                </table>
                <p v-else>No borrowed books.</p>
            </div>
        </transition>

        <transition name="fade-slide">
            <div v-if="isOverdueOpen" class="borrowed-books-section">
                <h3>Overdue Books</h3>
                <div v-if="loadingOverdue">Loading overdue books...</div>
                <table v-else-if="overdueBooksDetails.length > 0" class="borrowed-books-table">
                    <thead>
                        <tr>
                            <th></th>
                            <th>Book Name</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(book, index) in overdueBooksDetails" :key="book.id">
                            <td>{{ index + 1 }}</td>
                            <td>
                                <router-link :to="`/admin/books/${book.id}`" class="book-link book-title">
                                    {{ book.title || book.name }}
                                </router-link>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <p v-else>No overdue books.</p>
            </div>
        </transition>

        <transition name="fade-slide">
            <div v-if="isRequestedOpen" class="borrowed-books-section">
                <h3>Requested Books</h3>
                <div v-if="loadingRequested">Loading requested books...</div>
                <table v-else-if="requestedBooksDetails.length > 0" class="borrowed-books-table">
                    <thead>
                        <tr>
                            <th></th>
                            <th>Book Name</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(book, index) in requestedBooksDetails" :key="book.id">
                            <td>{{ index + 1 }}</td>
                            <td>
                                <router-link :to="`/admin/requests/${book.id}`" class="book-link book-title">
                                    {{ book.title || book.name }}
                                </router-link>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <p v-else>No requested books.</p>
            </div>
        </transition>

        <transition name="fade-slide">
            <div v-if="isNotifyOpen" class="borrowed-books-section">
                <h3>Notify Me List</h3>
                <div v-if="loadingNotify">Loading notify me list...</div>
                <table v-else-if="notifyMeListDetails.length > 0" class="borrowed-books-table">
                    <thead>
                        <tr>
                            <th></th>
                            <th>Book Name</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(book, index) in notifyMeListDetails" :key="book.id">
                            <td>{{ index + 1 }}</td>
                            <td>
                                <router-link :to="`/admin/books/${book.id}`" class="book-link book-title">
                                    {{ book.title || book.name }}
                                </router-link>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <p v-else>No notify me list items.</p>
            </div>
        </transition>

        <transition name="fade-slide">
            <div v-if="isPenaltiesOpen" class="borrowed-books-section">
                <h3>Penalties</h3>
                <div v-if="loadingPenalties">Loading penalties...</div>
                <table v-else-if="penaltiesDetails.length > 0" class="borrowed-books-table">
                    <thead>
                        <tr>
                            <th></th>
                            <th>Book Name</th>
                            <th>Amount</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(penalty, index) in penaltiesDetails" :key="penalty.book.id">
                            <td>{{ index + 1 }}</td>
                            <td>
                                <router-link :to="`/admin/books/${penalty.book.id}`" class="book-link book-title">
                                    {{ penalty.book.title || penalty.book.name }}
                                </router-link>
                            </td>
                            <td>₺{{ penalty.amount }}</td>
                        </tr>
                    </tbody>
                    <tfoot>
                        <tr>
                            <td colspan="2" style="text-align: right; font-weight: bold;">Total:</td>
                            <td style="font-weight: bold;">₺{{ totalPenaltyAmount }}</td>
                        </tr>
                    </tfoot>
                </table>
                <p v-else>No penalties.</p>
            </div>
        </transition>
    </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/api/axios';

const route = useRoute();
const router = useRouter();

const user = ref(null);

const borrowedBooksDetails = ref([]);
const overdueBooksDetails = ref([]);
const requestedBooksDetails = ref([]);
const notifyMeListDetails = ref([]);
const penaltiesDetails = ref([]);

const isBorrowedOpen = ref(false);
const isOverdueOpen = ref(false);
const isRequestedOpen = ref(false);
const isNotifyOpen = ref(false);
const isPenaltiesOpen = ref(false);

const loadingBorrowed = ref(false);
const loadingOverdue = ref(false);
const loadingRequested = ref(false);
const loadingNotify = ref(false);
const loadingPenalties = ref(false);

const hasFetched = {
    borrowed: ref(false),
    overdue: ref(false),
    requested: ref(false),
    notify: ref(false),
    penalties: ref(false),
};

const fetchBookDetails = async (bookIds, type = 'normal') => {
    try {
        const promises = bookIds.map(id => {
            if (type === 'requested') {
                return api.get(`/admin/requested-books/info/${id}`);
            }
            return api.get(`/books/${id}`);
        });
        const results = await Promise.all(promises);
        return results.map((res, index) => {
            if (type === 'requested') {
                return {
                    ...res.data.request,
                    id: bookIds[index]
                };
            }
            return {
                ...res.data.book,
                id: bookIds[index]
            };
        });
    } catch (error) {
        console.error('Failed to fetch book details:', error);
        return [];
    }
};

const fetchUserDetail = async () => {
    try {
        const userId = route.params.id;
        const response = await api.get(`/admin/users/${userId}`);
        user.value = response.data.user;
    } catch (error) {
        console.error('Failed to fetch user detail:', error);
    }
};

const goBack = () => {
    router.push('/admin/users');
};

const totalPenaltyAmount = computed(() => {
    return penaltiesDetails.value.reduce((sum, penalty) => sum + penalty.amount, 0);
});

watch(isBorrowedOpen, async (newVal) => {
    if (newVal && !hasFetched.borrowed.value && user.value?.borrowed_books?.length > 0) {
        loadingBorrowed.value = true;
        try {
            borrowedBooksDetails.value = await fetchBookDetails(user.value.borrowed_books);
            hasFetched.borrowed.value = true;
        } catch (error) {
            console.error('Failed to fetch borrowed books:', error);
        } finally {
            loadingBorrowed.value = false;
        }
    }
});

watch(isOverdueOpen, async (newVal) => {
    if (newVal && !hasFetched.overdue.value && user.value?.overdue_books?.length > 0) {
        loadingOverdue.value = true;
        try {
            overdueBooksDetails.value = await fetchBookDetails(user.value.overdue_books);
            hasFetched.overdue.value = true;
        } catch (error) {
            console.error('Failed to fetch overdue books:', error);
        } finally {
            loadingOverdue.value = false;
        }
    }
});

watch(isRequestedOpen, async (newVal) => {
    if (newVal && !hasFetched.requested.value && user.value?.requested_books?.length > 0) {
        loadingRequested.value = true;
        try {
            requestedBooksDetails.value = await fetchBookDetails(
                user.value.requested_books.map(b => b.id),
                'requested'
            );
            hasFetched.requested.value = true;
        } catch (error) {
            console.error('Failed to fetch requested books:', error);
        } finally {
            loadingRequested.value = false;
        }
    }
});

watch(isNotifyOpen, async (newVal) => {
    if (newVal && !hasFetched.notify.value && user.value?.notify_me_list?.length > 0) {
        loadingNotify.value = true;
        try {
            notifyMeListDetails.value = await fetchBookDetails(user.value.notify_me_list);
            hasFetched.notify.value = true;
        } catch (error) {
            console.error('Failed to fetch notify me list:', error);
        } finally {
            loadingNotify.value = false;
        }
    }
});

watch(isPenaltiesOpen, async (newVal) => {
    if (newVal && !hasFetched.penalties.value && user.value?.penalties?.length > 0) {
        loadingPenalties.value = true;
        try {
            const bookIds = user.value.penalties.map(p => p.book_id);
            const books = await fetchBookDetails(bookIds);
            penaltiesDetails.value = user.value.penalties.map((penalty, index) => ({
                book: books[index],
                amount: penalty.amount
            }));
            hasFetched.penalties.value = true;
        } catch (error) {
            console.error('Failed to fetch penalties:', error);
        } finally {
            loadingPenalties.value = false;
        }
    }
});

onMounted(() => {
    fetchUserDetail();
});
</script>

<style scoped>
.user-detail-page {
    padding: 40px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.user-detail-card {
    background: #fff;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    width: 360px;
    margin-bottom: 20px;
}

.user-detail-card p {
    margin: 12px 0;
    font-size: 16px;
}

.user-summary-cards {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin-top: 20px;
    justify-content: center;
}

.summary-card {
    background: #ffffff;
    padding: 16px 24px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    width: 160px;
    text-align: center;
}

.summary-card p {
    margin: 0;
    font-size: 14px;
    color: #666;
}

.summary-card h3 {
    margin-top: 8px;
    font-size: 22px;
    color: #4caf50;
}

.back-button {
    position: fixed;
    top: 20px;
    left: 300px;
    background-color: #4caf50;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    cursor: pointer;
    z-index: 999;
}

.back-button:hover {
    background-color: #388e3c;
}

.borrowed-books-section {
    margin-top: 40px;
    width: 100%;
    max-width: 600px;
}

.borrowed-books-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 12px;
}

.borrowed-books-table th,
.borrowed-books-table td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: center;
}

.borrowed-books-table th {
    background-color: #f5f5f5;
    font-weight: bold;
}

.summary-card.clickable {
    cursor: pointer;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.summary-card.clickable:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.borrowed-books-table tbody tr:hover {
    background-color: #f1f8e9;
    transition: background-color 0.3s ease;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
    transition: all 0.4s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
    opacity: 0;
    transform: scale(0.95);
}

.user-detail-page h2:hover {
    color: #4caf50;
    transition: color 0.3s;
}

.borrowed-books-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    margin-top: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    overflow: hidden;
}

.borrowed-books-table th {
    background-color: #f0f4f8;
    color: #333;
    font-weight: 600;
    font-size: 16px;
    padding: 14px;
    text-align: left;
    border-bottom: 2px solid #e0e0e0;
}

.borrowed-books-table td {
    background-color: #ffffff;
    padding: 14px;
    font-size: 15px;
    color: #555;
    border-bottom: 1px solid #f0f0f0;
}

.borrowed-books-table tbody tr:hover {
    background-color: #f9fbe7;
    transition: background-color 0.3s ease;
}

.borrowed-books-table thead tr:first-child th:first-child {
    border-top-left-radius: 8px;
}

.borrowed-books-table thead tr:first-child th:last-child {
    border-top-right-radius: 8px;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
    transition: all 0.4s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
    opacity: 0;
    transform: scale(0.95);
}

.book-link {
    color: #3498db;
    text-decoration: none;
    font-weight: 500;
}

.book-link:hover {
    text-decoration: underline;
}
</style>