import './style.css'

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <div class="flex flex-col items-center justify-center min-h-dvh bg-gray-50 text-gray-800 p-8">
    <div class="text-center mb-8">
      <h1 class="text-4xl font-bold mb-2">Greeting App</h1>
      <p class="text-gray-500">Enter names (one per line) and click the button!</p>
    </div>
    <div class="flex flex-col gap-3 items-center mb-6">
      <textarea
        id="name-input"
        placeholder="Enter names, one per line"
        rows="4"
        class="border border-gray-300 rounded-lg px-4 py-2 text-lg w-full max-w-md focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-transparent resize-y"
      ></textarea>
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

const nameInput = document.querySelector<HTMLTextAreaElement>('#name-input')!
const helloBtn = document.querySelector<HTMLButtonElement>('#hello-btn')!
const greetingEl = document.querySelector<HTMLDivElement>('#greeting')!

helloBtn.addEventListener('click', () => {
  const names = nameInput.value
    .split('\n')
    .map(name => name.trim())
    .filter(name => name.length > 0)

  if (names.length === 0) {
    greetingEl.textContent = 'Please enter at least one name!'
  } else if (names.length === 1) {
    greetingEl.textContent = `Hello ${names[0]}`
  } else {
    const last = names.pop()!
    greetingEl.textContent = `Hello ${names.join(', ')} and ${last}`
  }
})

// Allow pressing Ctrl+Enter (or Cmd+Enter on Mac) to trigger the greeting
nameInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
    helloBtn.click()
  }
})
