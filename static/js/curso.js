const curso = document.querySelector('#curso')
const form_curso = document.querySelector('#form-curso')
curso.addEventListener("blur", () => {
    form_curso.submit()
});