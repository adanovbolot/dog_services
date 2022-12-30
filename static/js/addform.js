let skillsForm = document.querySelectorAll(".skills-form")
let container = document.querySelector("#form-container")
let addButton = document.querySelector("#add-form")
let totalForms = document.querySelector("#id_profile_skills-TOTAL_FORMS")



function addForm(e) {
    e.preventDefault()
    console.log('hello')
    let newForm = skillsForm[0].cloneNode(true) //Clone the bird form
    let formRegex = RegExp(`form-(\\d){1}-`,'g') //Regex to find all instances of the form number

    formNum++ //Increment the form number
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`) //Update the new form to have the correct form number
    container.insertBefore(newForm, addButton) //Insert the new form at the end of the list of forms

    totalForms.setAttribute('value', `${formNum+1}`) //Increment the number of total forms in the management form
}