<template>
  <div class="search-bar">
    <input class="input-line full-width" type="text" :value="props.modelValue"
      @keyup.enter="emit('update:modelValue', $event.target.value)"
      placeholder="Search by Author, Title, Publisher, ISBN..." />
    <button class="barcode-button" @click="router.push('/scan-book')" title="Scan a book">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
        <path
          d="M2 4h1v16H2V4zm2 0h2v16H4V4zm4 0h1v16H8V4zm2 0h2v16h-2V4zm4 0h1v16h-1V4zm2 0h2v16h-2V4zm4 0h1v16h-1V4z" />
      </svg>
    </button>
    <div class="order-menu-wrapper">
      <button class="order-button" @click="toggleOrderMenu" title="Sort books">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
          <path d="M3 18h6v-2H3v2zm0-5h12v-2H3v2zm0-7v2h18V6H3z" />
        </svg>
      </button>
      <transition name="fade">
        <ul v-if="orderMenuOpen" class="order-menu">
          <li @click="emitOrder('most')">Most Borrowed</li>
          <li @click="emitOrder('recent')">Recently Added</li>
          <li @click="emitOrder('az')">A - Z</li>
          <li @click="emitOrder('za')">Z - A</li>
        </ul>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'
import { useRouter } from 'vue-router'


const props = defineProps({
  modelValue: String
})

const emit = defineEmits(['update:modelValue', 'order'])

const router = useRouter()
const orderMenuOpen = ref(false)

const toggleOrderMenu = () => {
  orderMenuOpen.value = !orderMenuOpen.value
}

const emitOrder = (type) => {
  emit('order', type)
  orderMenuOpen.value = false
}

</script>

<style scoped>
.search-bar {
  margin: 40px 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.input-line {
  background: none;
  margin-bottom: 0;
  padding: 6px 10px;
  line-height: 2.4em;
  color: #fff;
  font-family: roboto;
  font-weight: 300;
  font-size: 1.2rem;
  border: none;
  border-bottom: 1px solid rgba(255, 255, 255, 0.65);
  transition: all 0.2s ease;
  width: 100%;
}

.input-line:focus {
  outline: none;
}

.full-width {
  width: 100%;
}

::placeholder {
  color: rgba(255, 255, 255, 0.65);
}

.barcode-button,
.order-button {
  background: #f5f5f5;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 8px 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.barcode-button:hover,
.order-button:hover {
  background: #e0e0e0;
}

.order-menu-wrapper {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.order-menu {
  position: absolute;
  left: calc(100% + 8px);
  top: 100%;
  margin-top: 8px;
  background: white;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  list-style: none;
  padding: 0;
  margin: 0;
  z-index: 10;
  overflow: hidden;
}

.order-menu li {
  padding: 10px 15px;
  cursor: pointer;
  transition: background 0.2s;
  white-space: nowrap;
}

.order-menu li:hover {
  background: #f5a425;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>