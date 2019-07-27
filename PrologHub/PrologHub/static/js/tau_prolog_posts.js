function pl_query(query_value, code_value, query_id) {
    const engine = pl.create();

    const answers_id = `${ query_id }_answers`;
    const answers = document.getElementById(answers_id);
    answers.innerHTML = "";
    const give_answer = pl_answer(answers)

    const parsed = engine.consult(code_value);
    if (parsed !== true) {
        give_answer(parsed)
        }

    const queried = engine.query(query_value);
    if (queried !== true) {
        give_answer(queried)
        }

    engine.answers(give_answer);
}

function pl_answer(answers) {
    return function (answer) {
        if(answer) {
            answers.innerHTML = answers.innerHTML + `<li class="list-group-item list-group-item-success">${pl.format_answer(answer)}</li>`
        } else {
            answers.innerHTML = answers.innerHTML + `<li class="list-group-item list-group-item-warning">${pl.format_answer(answer)}</li>`
        }
    }
}
