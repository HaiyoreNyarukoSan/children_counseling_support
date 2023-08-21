$(function () {
    $("#generate_forms").on("click", function (e) {
        e.preventDefault();
        const numForms = parseInt($("#num_forms").val());
        const totalForms = parseInt($("#id_patientForm-TOTAL_FORMS").val());
        const emptyFormHtml = $("#empty_form").html();

        if (numForms > totalForms) {
            for (let i = totalForms; i < numForms; i++) {
                const newForm = $(emptyFormHtml).clone();
                newForm.find(':input').each(function () {
                    $(this).attr('id', $(this).attr('id').replace('__prefix__', i));
                    $(this).attr('name', $(this).attr('name').replace('__prefix__', i));
                });
                const new_div = $('<div>');
                new_div.append(newForm)
                console.log(newForm);
                const formTitle = `<strong class="form-control">${i + 1}번째 자식분</strong>`;
                $("#formset_container").append(formTitle);
                $("#formset_container").append(new_div);
            }
        } else {
            for (let i = totalForms - 1; i >= numForms; i--) {
                $("#formset_container").children().last().remove(); // Remove the form
                $("#formset_container").children().last().remove(); // Remove the <strong>
            }
        }

        $("#id_patientForm-TOTAL_FORMS").val(numForms);
    })
})