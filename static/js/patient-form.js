document.addEventListener("DOMContentLoaded", function () {
    let currentIndex = $("#formset_container .form-group").length;
    const emptyFormHtml = $("#empty_form").html();

    function addForm(index) {
        let $newForm = emptyFormHtml.replace(/__prefix__/g, index);
        // $newForm.find(':input, label').addClass('form-group');
        $("#formset_container").append($newForm);
    }

    function deleteForm(index) {
        $("#formset_container").children().last().remove();
    }

    $('#generate_forms').click(function () {
        addForm(currentIndex);

        currentIndex += 1;
        $("#id_patientForm-TOTAL_FORMS").val(currentIndex);
    });
    $('#delete_forms').click(function () {
        deleteForm(currentIndex);

        currentIndex -= 1;
        $("#id_patientForm-TOTAL_FORMS").val(currentIndex);
    });
});