import './style.css'

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <div class="flex flex-col items-center justify-center min-h-dvh bg-gray-50 text-gray-800 p-8">
    <div class="text-center mb-8">
      <h1 class="text-4xl font-bold mb-2">Greeting App</h1>
      <p class="text-gray-500">Enter your name and click the button!</p>
    </div>
    <div class="flex gap-3 items-center mb-6">
      <input
        id="name-input"
        type="text"
        placeholder="Enter your name"
        class="border border-gray-300 rounded-lg px-4 py-2 text-lg focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-transparent"
      />
      <button
        id="hello-btn"
        type="button"
        class="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-lg py-2 px-6 rounded-lg transition-colors"
      >
        Hello!
      </button>
    </div>
    <div id="greeting" class="text-2xl font-semibold text-indigo-600 min-h-9"></div>
  </div>
`

const nameInput = document.querySelector<HTMLInputElement>('#name-input')!
const helloBtn = document.querySelector<HTMLButtonElement>('#hello-btn')!
const greetingEl = document.querySelector<HTMLDivElement>('#greeting')!

helloBtn.addEventListener('click', () => {
  const name = nameInput.value.trim()
  if (name) {
    greetingEl.textContent = `Hello ${name}`
  } else {
    greetingEl.textContent = 'Please enter a name!'
  }
})

// Allow pressing Enter to trigger the greeting
nameInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    helloBtn.click()
  }
})
