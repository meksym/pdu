'user strict'


function main() {
    var Delta = Quill.import('delta')
    let formRow = document.createElement('div')
    let editorContainer = document.createElement('div')
    editorContainer.spellcheck = false
    let fieldset = document.querySelector('fieldset')
    let submitInputs = document.querySelector('.submit-row').children
    formRow.classList.add('form-row')
    formRow.append(editorContainer)
    fieldset.append(formRow)
    function paste(node, delta) {
        if (delta && delta.ops && delta.ops.length)
        return new Delta().insert(delta.ops[0].insert)
        else return new Delta()
    }
    let editor = new Quill(editorContainer, {
            bounds: document.body,
            debug: 'warn',
            modules: {
                toolbar: [
                    ['bold', 'italic', 'strike'],
                    [{'header': [2, 3, false]}],
                    [{'align': []}],
                    [{'list': 'ordered'}, {'list': 'bullet'}],
                    ['image', 'video', 'link'],
                    ['clean'],
                ],
                clipboard: {
                    matchers: [
                        ['h1', paste],
                        ['code', paste],
                        ['h2', paste],
                        ['h3', paste],
                        ['h4', paste],
                        ['h5', paste],
                        ['h6', paste],
                        ['p', paste],
                        ['em', paste],
                        ['strong', paste],
                        ['span', paste],
                        ['a', paste],
                        ['li', paste],
                    ]
                }
            },
            theme: 'snow',
    })
    if (id_json_text.value != 'null')
        editor.setContents(JSON.parse(id_json_text.value))
    for (let input of submitInputs) input.addEventListener('click', event => {
        id_json_text.value = JSON.stringify(editor.getContents())
        id_html_text.value = editor.root.innerHTML
    })
}

document.addEventListener("DOMContentLoaded", main)
