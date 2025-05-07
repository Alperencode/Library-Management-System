<template>
    <div class="admin-add-book-container">
        <h2 class="mb-4">Edit Book</h2>
        <form class="book-form" @submit.prevent="submitForm">
            <div class="form-group">
                <label>Title</label>
                <input v-model="form.title" type="text" required />
            </div>

            <div class="form-group">
                <label>Authors (comma separated)</label>
                <input v-model="authorInput" type="text" @blur="addAuthors" />
                <div class="tag-list">
                    <span class="tag" v-for="(author, idx) in form.authors" :key="idx">
                        {{ author }}
                        <button type="button" @click="form.authors.splice(idx, 1)">×</button>
                    </span>
                </div>
            </div>

            <div class="form-group">
                <label>Categories (use `/` to separate subcategories)</label>
                <input v-model="categoryInput" type="text" @blur="addCategories" />
                <div class="tag-list">
                    <span class="tag" v-for="(cat, idx) in form.categories" :key="idx">
                        {{ cat.subcategory ? `${cat.category}/${cat.subcategory}` : cat.category }}
                        <button type="button" @click="form.categories.splice(idx, 1)">×</button>
                    </span>
                </div>
            </div>

            <div class="form-group">
                <label>Language</label>
                <select class="styled-select" v-model="form.language">
                    <option disabled value="">Select a language</option>
                    <option v-for="lang in languages" :key="lang.code" :value="lang.code">
                        {{ lang.name }} ({{ lang.code }})
                    </option>
                </select>
            </div>

            <div class="form-group">
                <label>Page Count</label>
                <input v-model.number="form.page_count" type="number" min="0" />
            </div>

            <div class="form-group">
                <label>ISBN</label>
                <input v-model="form.isbn" type="text" />
            </div>

            <div class="form-group">
                <label>Publisher</label>
                <input v-model="form.publisher" type="text" />
            </div>

            <div class="form-group">
                <label>Cover Image URL</label>
                <input v-model="form.cover_image" type="text" />
            </div>

            <div class="form-group">
                <label>Description</label>
                <textarea v-model="form.description"></textarea>
            </div>

            <button class="submit-btn" type="submit">Update Book</button>
        </form>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import api from '@/api/axios'
import ISO6391 from 'iso-639-1'

const route = useRoute()
const router = useRouter()
const toast = useToast()

const languages = ref([])
onMounted(() => {
    languages.value = ISO6391.getAllCodes()
        .map(code => ({ code, name: ISO6391.getNativeName(code) || ISO6391.getName(code) }))
})

const form = ref({
    title: '',
    authors: [],
    categories: [],
    language: '',
    page_count: null,
    isbn: '',
    publisher: '',
    cover_image: '',
    description: ''
})

const authorInput = ref('')
const categoryInput = ref('')

const fetchBook = async () => {
    try {
        const { id } = route.params
        const { data } = await api.get(`/admin/book/${id}`)
        const b = data.book

        form.value = {
            title: b.title || '',
            authors: b.authors || [],
            categories: (b.categories || []).map(cat =>
                typeof cat === 'string'
                    ? { category: cat, subcategory: null }
                    : cat
            ),
            language: b.language || '',
            page_count: b.page_count || null,
            isbn: b.isbn || '',
            publisher: b.publisher || '',
            cover_image: b.cover_image || '',
            description: b.description || ''
        }
    } catch (err) {
        toast.error("Failed to fetch book data.")
    }
}

onMounted(fetchBook)

const addAuthors = () => {
    if (authorInput.value.trim()) {
        const newAuthors = authorInput.value.split(',').map(a => a.trim()).filter(Boolean)
        form.value.authors.push(...newAuthors)
        authorInput.value = ''
    }
}

const addCategories = () => {
    if (categoryInput.value.trim()) {
        const rawCategories = categoryInput.value.split(',').map(c => c.trim()).filter(Boolean)
        const structured = rawCategories.map(raw => {
            const parts = raw.split('/')
            return { category: parts[0], subcategory: parts[1] || null }
        })
        form.value.categories.push(...structured)
        categoryInput.value = ''
    }
}

const submitForm = async () => {
    if (!form.value.title.trim()) {
        toast.error("Title is required")
        return
    }

    if (form.value.authors.length === 0) {
        toast.error("At least one author is required")
        return
    }

    if (
        form.value.categories.length === 0 ||
        !form.value.categories.some(cat => cat.category && cat.category.trim())
    ) {
        toast.error("At least one valid category is required")
        return
    }

    if (!form.value.isbn.trim()) {
        toast.error("ISBN is required")
        return
    }

    try {
        const { id } = route.params
        const { data } = await api.patch(`/admin/book/${id}`, form.value)
        if (data.code === 'Success') {
            toast.success(data.message)
            router.push('/admin/books')
        }
    } catch (err) {
        const msg = err?.response?.data?.message || 'Failed to update book.'
        toast.error(msg)
    }
}
</script>


<style scoped>
.admin-add-book-container {
    max-width: 700px;
    margin: auto;
    padding: 24px;
}

.book-form {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.form-group {
    display: flex;
    flex-direction: column;
}

.form-group label {
    font-weight: 600;
    margin-bottom: 6px;
}

.form-group input,
.form-group textarea {
    padding: 10px;
    border-radius: 6px;
    border: 1px solid #ccc;
    font-size: 14px;
}

textarea {
    resize: vertical;
}

.submit-btn {
    padding: 10px 20px;
    background-color: #2c3e50;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 16px;
    cursor: pointer;
    align-self: flex-start;
}

.tag-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 8px;
}

.tag {
    background-color: #d9edf7;
    color: #31708f;
    padding: 4px 10px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
}

.tag button {
    background: transparent;
    border: none;
    font-size: 16px;
    cursor: pointer;
    color: #31708f;
}

.styled-select {
    padding: 10px;
    border-radius: 6px;
    border: 1px solid #ccc;
    font-size: 14px;
    background-color: #fff;
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
}
</style>