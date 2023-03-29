dataElement = document.getElementsByTagName('span')[document.getElementsByTagName('span').length - 1]
let serverDate = new Date(dataElement.textContent)
let userDate = new Date()
deltaTime = Math.abs(serverDate - userDate)

if (deltaTime > 1000 * 60 * 60 * 24) {
  dataElement.innerHTML = serverDate.getFullYear()
} else {
  dataElement.innerHTML = userDate.getFullYear()
}
